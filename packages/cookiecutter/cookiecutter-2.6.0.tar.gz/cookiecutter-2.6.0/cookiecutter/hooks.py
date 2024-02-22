"""Functions for discovering and executing various cookiecutter hooks."""

import errno
import logging
import os
import subprocess  # nosec
import sys
import tempfile
from pathlib import Path

from jinja2.exceptions import UndefinedError

from cookiecutter import utils
from cookiecutter.exceptions import FailedHookException
from cookiecutter.utils import (
    create_env_with_context,
    create_tmp_repo_dir,
    rmtree,
    work_in,
)

logger = logging.getLogger(__name__)

_HOOKS = [
    'pre_prompt',
    'pre_gen_project',
    'post_gen_project',
]
EXIT_SUCCESS = 0


def valid_hook(hook_file, hook_name):
    """Determine if a hook file is valid.

    :param hook_file: The hook file to consider for validity
    :param hook_name: The hook to find
    :return: The hook file validity
    """
    filename = os.path.basename(hook_file)
    basename = os.path.splitext(filename)[0]
    matching_hook = basename == hook_name
    supported_hook = basename in _HOOKS
    backup_file = filename.endswith('~')

    return matching_hook and supported_hook and not backup_file


def find_hook(hook_name, hooks_dir='hooks'):
    """Return a dict of all hook scripts provided.

    Must be called with the project template as the current working directory.
    Dict's key will be the hook/script's name, without extension, while values
    will be the absolute path to the script. Missing scripts will not be
    included in the returned dict.

    :param hook_name: The hook to find
    :param hooks_dir: The hook directory in the template
    :return: The absolute path to the hook script or None
    """
    logger.debug('hooks_dir is %s', os.path.abspath(hooks_dir))

    if not os.path.isdir(hooks_dir):
        logger.debug('No hooks/dir in template_dir')
        return None

    scripts = []
    for hook_file in os.listdir(hooks_dir):
        if valid_hook(hook_file, hook_name):
            scripts.append(os.path.abspath(os.path.join(hooks_dir, hook_file)))

    if len(scripts) == 0:
        return None
    return scripts


def run_script(script_path, cwd='.'):
    """Execute a script from a working directory.

    :param script_path: Absolute path to the script to run.
    :param cwd: The directory to run the script from.
    """
    run_thru_shell = sys.platform.startswith('win')
    if script_path.endswith('.py'):
        script_command = [sys.executable, script_path]
    else:
        script_command = [script_path]

    utils.make_executable(script_path)

    try:
        proc = subprocess.Popen(script_command, shell=run_thru_shell, cwd=cwd)  # nosec
        exit_status = proc.wait()
        if exit_status != EXIT_SUCCESS:
            raise FailedHookException(
                f'Hook script failed (exit status: {exit_status})'
            )
    except OSError as err:
        if err.errno == errno.ENOEXEC:
            raise FailedHookException(
                'Hook script failed, might be an empty file or missing a shebang'
            ) from err
        raise FailedHookException(f'Hook script failed (error: {err})') from err


def run_script_with_context(script_path, cwd, context):
    """Execute a script after rendering it with Jinja.

    :param script_path: Absolute path to the script to run.
    :param cwd: The directory to run the script from.
    :param context: Cookiecutter project template context.
    """
    _, extension = os.path.splitext(script_path)

    with open(script_path, encoding='utf-8') as file:
        contents = file.read()

    with tempfile.NamedTemporaryFile(delete=False, mode='wb', suffix=extension) as temp:
        env = create_env_with_context(context)
        template = env.from_string(contents)
        output = template.render(**context)
        temp.write(output.encode('utf-8'))

    run_script(temp.name, cwd)


def run_hook(hook_name, project_dir, context):
    """
    Try to find and execute a hook from the specified project directory.

    :param hook_name: The hook to execute.
    :param project_dir: The directory to execute the script from.
    :param context: Cookiecutter project context.
    """
    scripts = find_hook(hook_name)
    if not scripts:
        logger.debug('No %s hook found', hook_name)
        return
    logger.debug('Running hook %s', hook_name)
    for script in scripts:
        run_script_with_context(script, project_dir, context)


def run_hook_from_repo_dir(
    repo_dir, hook_name, project_dir, context, delete_project_on_failure
):
    """Run hook from repo directory, clean project directory if hook fails.

    :param repo_dir: Project template input directory.
    :param hook_name: The hook to execute.
    :param project_dir: The directory to execute the script from.
    :param context: Cookiecutter project context.
    :param delete_project_on_failure: Delete the project directory on hook
        failure?
    """
    with work_in(repo_dir):
        try:
            run_hook(hook_name, project_dir, context)
        except (
            FailedHookException,
            UndefinedError,
        ):
            if delete_project_on_failure:
                rmtree(project_dir)
            logger.error(
                "Stopping generation because %s hook "
                "script didn't exit successfully",
                hook_name,
            )
            raise


def run_pre_prompt_hook(repo_dir: "os.PathLike[str]") -> Path:
    """Run pre_prompt hook from repo directory.

    :param repo_dir: Project template input directory.
    """
    # Check if we have a valid pre_prompt script
    with work_in(repo_dir):
        scripts = find_hook('pre_prompt')
        if not scripts:
            return repo_dir

    # Create a temporary directory
    repo_dir = create_tmp_repo_dir(repo_dir)
    with work_in(repo_dir):
        scripts = find_hook('pre_prompt')
        for script in scripts:
            try:
                run_script(script, repo_dir)
            except FailedHookException:
                raise FailedHookException('Pre-Prompt Hook script failed')
    return repo_dir
