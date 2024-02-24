import contextlib
import os
import subprocess

from .utilities import execute_command


def get_detect_secrets_version():
    """
    Obtain the version of detect-secrets
    :return: The version of detect-secrets
    """

    with contextlib.suppress(subprocess.CalledProcessError):
        version = subprocess.check_output(
            ["detect-secrets", "--version"],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

    # If version is empty, return None
    if not version:
        return None

    # If version contains
    # WARNING: You are running an outdated version of detect-secrets.
    #  Your version: 0.13.1+ibm.58.dss
    #  Latest version: 0.13.1+ibm.61.dss
    #  See upgrade guide at https://ibm.biz/detect-secrets-how-to-upgrade
    # 0.13.1+ibm.58.dss
    # obtain only '0.13.1+ibm.58.dss'
    if "WARNING: You are running an outdated version of detect-secrets" in version:
        version = version.split("\n")[5]

    return version.strip()


def does_secrets_baseline_exist(repository_path, repo):
    """
    Check if the secrets baseline file exists
    :param repository_path: The path to the repository
    :param repo: The repository to check
    :return: True if the secrets baseline file exists, False otherwise
    """

    return os.path.isfile(f'{repository_path}/{repo.name}/.secrets.baseline')


def delete_secrets_baseline(repositories_path, repo):
    """
    Delete the secrets baseline file
    :param repositories_path: The path to the where the repositories are cloned
    :param repo: The repository
    :return: The path to the secrets baseline file
    """

    secrets_baseline_path = f'{repositories_path}/{repo.name}/.secrets.baseline'

    if os.path.isfile(secrets_baseline_path):
        os.remove(secrets_baseline_path)

    return secrets_baseline_path


def get_current_exclude_files(repository_path):
    """
    Get the current exclude files
    :param repository_path: The path to the repository
    :return: The current exclude files
    """

    # use jq to get the exclude files from the .secrets.baseline file
    command = f"cd {repository_path} && cat .secrets.baseline | jq '.exclude.files'"
    output = execute_command(command)

    return output


def get_current_exclude_lines(repository_path):
    """
    Get the current exclude files
    :param repository_path: The path to the repository
    :return: The current exclude files
    """

    # use jq to get the exclude lines from the .secrets.baseline file
    command = f"cd {repository_path} && cat .secrets.baseline | jq '.exclude.lines'"
    output = execute_command(command)

    return output


def update_secrets_scan(repository_path, exclude_files_pattern=None, exclude_lines_pattern=None):
    """
    Update the .secrets.baseline file for a given repository.
    :param repository_path: The path to the repository.
    :param exclude_files_pattern: The pattern to exclude files.
    :param exclude_lines_pattern: The pattern to exclude lines.
    """

    command = f"cd {repository_path} && detect-secrets scan --update .secrets.baseline"

    if exclude_files_pattern and exclude_lines_pattern:
        command += f" --exclude-files {exclude_files_pattern} --exclude-lines {exclude_lines_pattern}"
    elif exclude_files_pattern:
        command += f" --exclude-files {exclude_files_pattern}"
    elif exclude_lines_pattern:
        command += f" --exclude-lines {exclude_lines_pattern}"

    execute_command(command)


def audit_secrets(repository_path):
    """
    Audit the .secrets.baseline file
    :param repository_path: The path to the repository
    """

    execute_command(f"cd {repository_path} && yes 'n' | detect-secrets audit .secrets.baseline")
