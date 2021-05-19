#! /usr/bin/env python
import os

import semver

from git import Git

git = Git()


def bump_version(latest):
    """
    Uses SemVer package to bump the version, defaults to patch and parses a commit message to find a trigger for a
    major or minor bump. Supported triggers are:
        - #major
        - #minor

    :param latest:
    :return:
    """
    msg = git.get_last_commit_message().lower()
    if "#major" in msg:
        print("Bumping: major")
        return semver.bump_major(latest)
    elif "#minor" in msg:
        print("Bumping: minor")
        return semver.bump_minor(latest)
    else:
        print("Bumping: patch")
        return semver.bump_patch(latest)


def main():
    """
    Main function to bump the SemVer. Designed to run in GitLab CI.
    :return:
    """
    https_url = os.environ.get("CI_REPOSITORY_URL")
    if not https_url:
        raise EnvironmentError("You need to set the repo url with the env variable 'CI_REPOSITORY_URL'")

    git.set_ssh_push_url(https_url=https_url)

    latest = git.get_newest_tag()
    if not latest:
        version = "1.0.0"
        print(f"No tag was present, using {version}")
    elif "-" not in latest:
        raise ValueError("Commit is already tagged, skipping")
    else:
        version = bump_version(latest=latest)
        print(f"Bumping to: {version}")

    git.tag(tag=version)
    git.push_tag(tag=version)


if __name__ == "__main__":
    main()
