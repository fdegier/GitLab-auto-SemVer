import re
import subprocess

from typing import Union, Any, Tuple


class Git:
    @staticmethod
    def _execute_cmd(cmd: str, output: bool = False) -> Union[bool, str]:
        """
        Executes a command  via Subprocess
        :param cmd: bash like command
        :param output: Whether the command should return an output
        :return: Status and optional output
        """
        if not output:
            try:
                a = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                print(a)
                return True
            except subprocess.CalledProcessError as E:
                print(f"Error: {E}")
                return False
        else:
            try:
                a = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode().strip()
                print(a)
                return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode().strip()
            except subprocess.CalledProcessError as E:
                print(f"Error: {E}")
                return False

    def set_ssh_push_url(self, https_url: str):
        """
        Converts the GitLab HTTPS url to a SSH url
        :param https_url: repository url
        :return:
        """
        url = re.sub(r'.+@([^/]+)/', r'git@\1:', https_url)
        print(url)
        self._execute_cmd(cmd=f"git remote set-url --push origin {url}")

    def get_push_url(self) -> str:
        """
        Get SSH push url, mostly used for testing
        :return: remote push url
        """
        return self._execute_cmd(cmd=f"git remote get-url --push origin", output=True)

    def tag(self, tag: str):
        """
        Tags a repository with a new tag
        :param tag: SemVer tag
        :return:
        """
        self._execute_cmd(cmd=f"git tag {tag}")

    def push_tag(self, tag: str):
        """
        Push a tag to Git remote
        :param tag: Git tag
        :return:
        """
        self._execute_cmd(cmd=f"git push origin {tag}")

    def get_last_commit_message(self) -> str:
        """
        Returns the last commit message so it can be used to parse for major / minor bumps
        :return: Last commit message
        """
        msg = self._execute_cmd(cmd="git show -s --format=%s", output=True)
        if not msg:
            raise ValueError("No commit messages are available")
        return msg

    def get_newest_tag(self) -> Union[bool, str]:
        """
        Gets the newest / latest tag
        :return: newest / latest tag
        """
        tag = self._execute_cmd(cmd="git describe --tags", output=True)
        if not tag:
            return False
        return tag

