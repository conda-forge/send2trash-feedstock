"""Run tests from site-packages."""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

COV_FAIL_UNDER = 37

SP_DIR = Path(os.environ["SP_DIR"])

RUN = [
    "coverage",
    "run",
    "--source=send2trash",
    "--branch",
    "-m",
    "pytest",
    "-vv",
    "--tb=long",
    "--color=yes",
]

REPORT = [
    "coverage",
    "report",
    "--show-missing",
    "--skip-covered",
    f"--fail-under={COV_FAIL_UNDER}",
]


def do(*args: Any) -> int:
    args = [*map(str, args)]
    print(">>>", *args, flush=True)
    rc = subprocess.call(args)
    print("<<<", rc, "from", *args)
    return rc


def main() -> int:
    sp_test = SP_DIR / "_sendt2trash_tests"
    rc = 1
    try:
        shutil.copytree("tests", sp_test)
        rc = do(*RUN, f"{sp_test}") or do(*REPORT)
    finally:
        shutil.rmtree(sp_test)
    return rc


if __name__ == "__main__":
    sys.exit(main())
