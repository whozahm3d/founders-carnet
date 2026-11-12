"""Run the backend suite and measure app/ line coverage with stdlib tracing."""

from __future__ import annotations

import dis
import sys
import threading
from collections import defaultdict
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = (REPOSITORY_ROOT / "backend").resolve()
sys.path.insert(0, str(BACKEND_ROOT))

APP_ROOT = (REPOSITORY_ROOT / "backend" / "app").resolve()
COVERED_LINES: dict[Path, set[int]] = defaultdict(set)


def trace_project_lines(frame, event, _argument):
    filename = Path(frame.f_code.co_filename).resolve()
    if APP_ROOT not in filename.parents and filename != APP_ROOT:
        return None
    if event == "line":
        COVERED_LINES[filename].add(frame.f_lineno)
    return trace_project_lines


def executable_lines(source_path: Path) -> set[int]:
    code = compile(source_path.read_text(encoding="utf-8"), str(source_path), "exec")
    return {line for _offset, line in dis.findlinestarts(code)}


def main() -> int:
    junit_path = REPOSITORY_ROOT / "docs" / "test-results" / "step9-backend-20261113.xml"
    sys.settrace(trace_project_lines)
    threading.settrace(trace_project_lines)
    result = pytest.main(["-q", f"--junitxml={junit_path}"])
    threading.settrace(None)
    sys.settrace(None)

    source_files = sorted(APP_ROOT.rglob("*.py"))
    report_path = REPOSITORY_ROOT / "docs" / "test-results" / "step9-coverage-20261113.txt"
    totals = [0, 0]
    with report_path.open("w", encoding="utf-8", newline="\n") as report:
        report.write("Python stdlib line tracing; scope: backend/app; full backend pytest suite\n")
        report.write("Coverage counts executable line starts observed during the run.\n\n")
        report.write("File | Covered | Executable | Percent\n")
        report.write("--- | ---: | ---: | ---:\n")
        for source_path in source_files:
            executable = executable_lines(source_path)
            covered = executable & COVERED_LINES.get(source_path, set())
            totals[0] += len(covered)
            totals[1] += len(executable)
            relative_path = source_path.relative_to(REPOSITORY_ROOT).as_posix()
            percentage = 100 * len(covered) / len(executable) if executable else 100.0
            report.write(f"{relative_path} | {len(covered)} | {len(executable)} | {percentage:.1f}%\n")
        overall = 100 * totals[0] / totals[1] if totals[1] else 100.0
        report.write(f"\nTotal | {totals[0]} | {totals[1]} | {overall:.1f}%\n")
    print(f"App line coverage: {totals[0]}/{totals[1]} ({overall:.1f}%); report: {report_path}")
    return int(result)


if __name__ == "__main__":
    raise SystemExit(main())
