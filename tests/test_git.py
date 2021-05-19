from unittest import TestCase

from git import Git


class TestGit(TestCase):
    def setUp(self) -> None:
        self.git = Git()
        self.url = "https://user:[masked]@gitlab.com/gitlab-org/gitlab-foss.git"

    def test_set_push_url(self):
        self.git.set_ssh_push_url(https_url=self.url)
        ssh_url = "git@gitlab.com:gitlab-org/gitlab-foss.git"
        self.assertEqual(ssh_url, self.git.get_push_url())

    def test_get_push_url(self):
        ssh_url = "git@gitlab.com:gitlab-org/gitlab-foss.git"
        self.assertEqual(ssh_url, self.git.get_push_url())

    def test_tag(self):
        tag = "2.3.4"
        self.git.tag(tag=tag)
        self.assertEqual(tag, self.git._execute_cmd(f"git tag | grep {tag}", output=True))
