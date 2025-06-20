from git import Repo, InvalidGitRepositoryError
from patchwork.logger import logger
from patchwork.step import Step
import os
class CloneRepo(Step):
    required_keys = {"repo_url"}
    def __init__(self, inputs: dict):
        super().__init__(inputs)
        if not all(key in inputs.keys() for key in self.required_keys):
            raise ValueError(f'Missing required data: "{self.required_keys}"')
        self.repo_url = inputs.get("repo_url")
        self.branch = inputs.get("branch", "master")
        self.clone_dir = self.repo_url.rstrip('/').split('/')[-1].replace('.git', '')

    def run(self):
        cwd = os.path.abspath(os.getcwd())
        clone_dir = os.path.abspath(self.clone_dir)
        if is_valid_git_repo(cwd, self.repo_url):
            logger.info(f"Already inside a valid Git repo for '{self.repo_url}'. Skipping clone.")
            return
        if os.path.exists(clone_dir):
            if is_valid_git_repo(clone_dir, self.repo_url):
                logger.warning(f"Repo already exists at '{clone_dir}'. Please move into it:\n   cd {clone_dir}")
            else:
                self.set_status(f"Directory '{clone_dir}' exists but is not the correct repo. Please remove or fix it.")
            return
        logger.info(f"Cloning '{self.repo_url}' into '{clone_dir}'...")
        Repo.clone_from(self.repo_url, clone_dir, branch=self.branch)
        os.chdir(clone_dir)


def is_valid_git_repo(repo_path, expected_url):
    try:
        repo = Repo(repo_path)
        origin_url = next(repo.remote("origin").urls)
        return origin_url.rstrip("/") == expected_url.rstrip("/")
    except InvalidGitRepositoryError:
        return False
    except Exception:
        return False

