"""Render RESULTS.md using CSV files only."""

from __future__ import annotations

import csv
from datetime import date
from statistics import median
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
OUTPUT = ROOT / "RESULTS.md"


def read_csv(name: str) -> tuple[list[str], list[dict[str, str]]]:
    with (RESULTS / name).open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        return list(reader.fieldnames or []), list(reader)


def table(headers: list[str], rows: list[dict[str, str]]) -> str:
    if not headers:
        return "_CSV has no header._"
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(row.get(header, "") for header in headers) + " |" for row in rows)
    return "\n".join(lines)


def wilson(successes: int, total: int) -> str:
    if total == 0:
        return "n/a"
    z = 1.96
    proportion = successes / total
    denominator = 1 + z * z / total
    center = (proportion + z * z / (2 * total)) / denominator
    margin = z * ((proportion * (1 - proportion) / total + z * z / (4 * total * total)) ** 0.5) / denominator
    return f"{max(0.0, center - margin):.3f}–{min(1.0, center + margin):.3f}"


def e2e_summary(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    summary: list[dict[str, str]] = []
    variants = sorted({row.get("variant", "") for row in rows})
    for variant in variants:
        subset = [row for row in rows if row.get("variant") == variant]
        for metric, predicate in (
            ("citation correctness", lambda row: row.get("citation_correct", "").lower() == "true"),
            ("no unsupported claim", lambda row: float(row.get("unsupported_claim_rate") or 0) == 0),
            ("date correctness", lambda row: row.get("date_correct", "").lower() == "true"),
        ):
            successes = sum(predicate(row) for row in subset)
            summary.append({"variant": variant, "metric": metric, "n": str(len(subset)), "count": str(successes), "value": f"{successes}/{len(subset)}", "wilson_95_ci": wilson(successes, len(subset))})
        predicted = [row for row in subset if row.get("abstained", "").lower() == "true"]
        expected = [row for row in subset if row.get("should_abstain", "").lower() == "true"]
        tp = sum(row.get("should_abstain", "").lower() == "true" for row in predicted)
        fp = len(predicted) - tp
        fn = sum(row.get("abstained", "").lower() != "true" for row in expected)
        summary.append({"variant": variant, "metric": "abstention precision", "n": str(tp + fp), "count": str(tp), "value": f"{tp}/{tp + fp}" if tp + fp else "n/a", "wilson_95_ci": wilson(tp, tp + fp)})
        summary.append({"variant": variant, "metric": "abstention recall", "n": str(tp + fn), "count": str(tp), "value": f"{tp}/{tp + fn}" if tp + fn else "n/a", "wilson_95_ci": wilson(tp, tp + fn)})
        latencies = sorted(int(row["latency_ms"]) for row in subset if row.get("latency_ms", "").isdigit())
        summary.append({"variant": variant, "metric": "latency median / p95 (ms)", "n": str(len(latencies)), "count": "", "value": f"{median(latencies):.0f} / {latencies[min(len(latencies)-1, int(0.95*(len(latencies)-1)))]:.0f}" if latencies else "n/a", "wilson_95_ci": "n/a"})
    return summary


def main() -> None:
    _, metadata = read_csv("run_metadata.csv")
    _, splits = read_csv("split_sizes.csv")
    retrieval_headers, retrieval = read_csv("retrieval.csv")
    e2e_headers, e2e = read_csv("e2e.csv")
    e2e_summary_rows = e2e_summary(e2e)
    test_headers, tests = read_csv("test_cases.csv")
    failure_headers, failures = read_csv("failure_causes.csv")
    info = metadata[0] if metadata else {}
    split = splits[0] if splits else {}
    report = f"""# Compliance RAG evaluation results

Run date: {info.get('run_date') or date.today().isoformat()}

Model IDs: {info.get('model_ids') or 'not recorded'}

Run status: {info.get('status') or 'not recorded'}

Corpus hashes: {info.get('corpus_hashes') or 'not recorded'}

Split seed: {split.get('seed') or 'not recorded'}; dev: {split.get('dev_count') or '0'}; test: {split.get('test_count') or '0'}.

## Retrieval

{table(retrieval_headers, retrieval)}

## End-to-end versus no-retrieval baseline

{table(e2e_headers, e2e)}

### End-to-end counts and Wilson 95% confidence intervals

{table(["variant", "metric", "n", "count", "value", "wilson_95_ci"], e2e_summary_rows)}

## Test cases

{table(test_headers, tests)}

## Failure causes

{table(failure_headers, failures)}

## Not run / limitations

{info.get('not_run_reason') or 'No limitations recorded in run_metadata.csv.'}
"""
    OUTPUT.write_text(report, encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
