from pathlib import Path
import subprocess
import logging


# Removes the redundant empty lines from robocopy output.
class NoNewLineFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = record.msg.rstrip('\n')
        return True

logger = logging.getLogger(__name__)
logger.addFilter(NoNewLineFilter())


def _run_robocopy(
    source_dir: Path,
    destination_dir: Path,
    file: str, num_retries: int,
    verbose: bool,
    dry_run: bool,
    unbuffered_IO: bool,
    flags: list = [],
) -> int:
    assert num_retries >= 0
    command = [
        'robocopy', str(source_dir), str(destination_dir), file,
        '/mt:8', f'/r:{num_retries}', '/w:1'
    ]
    command.extend(flags)

    if dry_run:
        command.append('/l')
    if unbuffered_IO:
        command.append('/j')
    if verbose:
        command.append('/v')
        command.append('/x')
        logger.info(" ".join(command))
    else:
        command.append('/njh')
        command.append('/njs')

    with subprocess.Popen(command, text=True, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE) as process:
        for out in process.stdout:
            logger.info(out)

        process.wait()
        if process.returncode < 8:
            logger.info(f"robocopy succeeded with return code: {process.returncode}")
        else:
            logger.error(f"robocopy returned error code: {process.returncode}")

        return process.returncode


# Copies the file to the destination, with the same filename.
def copy_file(
    source_file: Path,
    destination_dir: Path,
    num_retries: int = 10,
    verbose: bool = False,
    dry_run: bool = False,
    unbuffered_IO: bool = False
) -> bool:
    assert source_file.is_file()

    result = _run_robocopy(
        source_dir=str(source_file.parent),
        destination_dir=str(destination_dir),
        file=str(source_file.name),
        num_retries=num_retries,
        verbose=verbose,
        dry_run=dry_run,
        unbuffered_IO=unbuffered_IO
    )
    return result < 8


# Copies the file to the destination, then deletes the source file.
def move_file(
    source_file: Path,
    destination_dir: Path,
    num_retries: int = 10,
    verbose: bool = False,
    dry_run: bool = False,
    unbuffered_IO: bool = False
) -> bool:
    assert source_file.is_file()

    result = _run_robocopy(
        source_dir=str(source_file.parent),
        destination_dir=str(destination_dir),
        file=str(source_file.name),
        num_retries=num_retries,
        verbose=verbose,
        dry_run=dry_run,
        unbuffered_IO=unbuffered_IO,
        flags=['/mov']
    )
    return result < 8


# Copies all files to the destination.
def copy_directory(
    source_dir: Path,
    destination_dir: Path,
    recursive: bool = True,
    num_retries: int = 10,
    verbose: bool = False,
    dry_run: bool = False,
    unbuffered_IO: bool = False
) -> bool:
    assert source_dir.is_dir()

    result = _run_robocopy(
        source_dir=str(source_dir),
        destination_dir=str(destination_dir),
        file='*',
        num_retries=num_retries,
        verbose=verbose,
        dry_run=dry_run,
        unbuffered_IO=unbuffered_IO,
        flags=['/e'] if recursive else []
    )
    return result < 8


# Copies all files to the destination, then deletes the sources.
def move_directory(
    source_dir: Path,
    destination_dir: Path,
    recursive: bool = True,
    num_retries: int = 10,
    verbose: bool = False,
    dry_run: bool = False,
    unbuffered_IO: bool = False
) -> bool:
    assert source_dir.is_dir()

    result = _run_robocopy(
        source_dir=str(source_dir),
        destination_dir=str(destination_dir),
        file='*',
        num_retries=num_retries,
        verbose=verbose,
        dry_run=dry_run,
        unbuffered_IO=unbuffered_IO,
        flags=['/move', '/e'] if recursive else ['/move']
    )
    return result < 8


# Copies all files to the destination, and deletes extra files.
def mirror_directory(
    source_dir: Path,
    destination_dir: Path,
    num_retries: int = 10,
    verbose: bool = False,
    dry_run: bool = False,
    unbuffered_IO: bool = False
) -> bool:
    assert source_dir.is_dir()

    result = _run_robocopy(
        source_dir=str(source_dir),
        destination_dir=str(destination_dir),
        file='*',
        num_retries=num_retries,
        verbose=verbose,
        dry_run=dry_run,
        unbuffered_IO=unbuffered_IO,
        flags=['/mir', '/im']
    )
    return result < 8
