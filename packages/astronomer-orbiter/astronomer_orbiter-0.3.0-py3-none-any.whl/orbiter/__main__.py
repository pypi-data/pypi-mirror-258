from __future__ import annotations

import logging
import os
import shlex
import sys
from pathlib import Path

import click
import sh
from loguru import logger

from orbiter.util import import_from_qualname
from orbiter.rules import TranslationRuleset


# ### LOGGING ###
def formatter(r):
    return (
        "<lvl>"
        + (
            "[{time:HH:mm:ss}|{level}] "
            if r["level"].no != logging.INFO
            else "[{time:HH:mm:ss}] "
        )
        + "{message}</>\n{exception}"  # add [time] WARN, etc. if it's not INFO  # exception
    )


logging.getLogger("sh").setLevel(logging.WARNING)
logger.remove()
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
sys.tracebacklimit = 1000 if LOG_LEVEL == "DEBUG" else 0
logger_defaults = dict(colorize=True, format=formatter)
exceptions_off = {"backtrace": False, "diagnose": False}
exceptions_on = {"backtrace": True, "diagnose": True}
logger.add(
    sys.stdout,
    level=LOG_LEVEL,
    **logger_defaults,
    **(exceptions_off if LOG_LEVEL != "DEBUG" else exceptions_on),
)
# ###############
SH_KWARGS = dict(_out=sys.stdout, _err=sys.stderr)


# noinspection PyUnresolvedReferences
def run_ruff_formatter(output_dir: Path):
    logger.info("Reformatting output...")
    try:
        sh.ruff(*shlex.split(f"check --fix {output_dir}"), **SH_KWARGS)
    except sh.ErrorReturnCode_1:
        click.echo("Ruff encountered an error!")
        raise click.Abort()
    sh.ruff(*shlex.split(f"format {output_dir}"), **SH_KWARGS)


def fetch_translation_ruleset(
    qualified_name: str,
) -> TranslationRuleset:
    sys.path.insert(0, os.getcwd())
    (_, translation_ruleset) = import_from_qualname(qualified_name)
    if not isinstance(translation_ruleset, TranslationRuleset):
        raise RuntimeError(
            f"translation_ruleset={translation_ruleset} is not a TranslationRuleset"
        )
    return translation_ruleset


@click.group(epilog="Check out https://astronomer.github.io/orbiter for more details")
def orbiter():
    """
    `orbiter` is a CLI that runs on your workstation
    and converts workflow definitions from other tools to Airflow Projects.
    """


@orbiter.command()
@click.version_option(package_name="orbiter", prog_name="orbiter")
@click.argument(
    "input-dir",
    type=click.Path(
        exists=True,
        dir_okay=True,
        file_okay=False,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
    default=Path.cwd() / "workflow",
    required=True,
)
@click.argument(
    "output-dir",
    type=click.Path(
        dir_okay=True,
        file_okay=False,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
    default=Path.cwd() / "output",
    required=True,
)
@click.option(
    "-r",
    "--ruleset",
    help="Qualified name of a TranslationRuleset",
    type=str,
    required=True,
)
@click.option(
    "--format/--no-format",
    "_format",
    help="[optional] format the output with Ruff",
    default=True,
    show_default=True,
)
def translate(
    input_dir: Path,
    output_dir: Path,
    ruleset: str | None,
    _format: bool,
):
    """
    Translate workflow artifacts in an `INPUT_DIR` folder
    to an `OUTPUT_DIR` Airflow Project folder.

    Provide a specific ruleset with the `--ruleset` flag.

    `INPUT_DIR` defaults to `$CWD/workflow`

    `OUTPUT_DIR` defaults to `$CWD/output`
    """
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    # noinspection PyProtectedMember
    fetch_translation_ruleset(qualified_name=ruleset)._translate_folder(
        input_dir=input_dir
    ).render(output_dir)
    if _format:
        run_ruff_formatter(output_dir)


if __name__ == "__main__":
    orbiter()
