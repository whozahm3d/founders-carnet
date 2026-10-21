"""Preprocessing script for the 7 FINAL datasets in The Founder's Carnet.

Midterm walkthrough data collection and preprocessing pipeline.
Clean copies and tech-only subsets are produced without model training,
tokenization, embeddings, or feature engineering.
"""

from __future__ import annotations

import os
import re
import zlib
from pathlib import Path
from typing import Any

import pandas as pd

# -----------------------------------------------------------------------------
# Configuration and Constants
# -----------------------------------------------------------------------------

DEFAULT_FINAL_DIR = Path(
    r"E:\Documents\advanced_statistics\fyp\founders-carnet\carnet_data\data\FINAL"
)

CONFIG: dict[str, dict[str, Any]] = {
    "roman_urdu_parl": {
        "label": "Roman-Urdu-Parl split",
        "keywords": ["parl"],
        "clean_filename": None,
        "tech_filename": None,
    },
    "pakistan_startup_census": {
        "label": "Pakistan Startup Census",
        "keywords": ["census"],
        "clean_filename": "pakistan_startup_census_clean.csv",
        "tech_filename": "pakistan_startup_census_tech.csv",
    },
    "pakistan_job_market": {
        "label": "Pakistan's Job Market",
        "keywords": ["job market", "job dec 19"],
        "clean_filename": "pakistan_job_market_clean.csv",
        "tech_filename": "pakistan_job_market_tech.csv",
    },
    "startup_success_fail": {
        "label": "Startup Success/Fail (Crunchbase)",
        "keywords": ["successfail", "secsees", "success_fail"],
        "clean_filename": "startup_success_fail_clean.csv",
        "tech_filename": "startup_success_fail_tech.csv",
    },
    "startup_investments": {
        "label": "StartUp Investments (Crunchbase)",
        "keywords": ["investments"],
        "clean_filename": "startup_investments_clean.csv",
        "tech_filename": "startup_investments_tech.csv",
    },
    "resume_snehaan": {
        "label": "Resume Dataset (Snehaan Bhawal)",
        "keywords": ["snehaan", "resume dataset"],
        "clean_filename": "resume_snehaan_clean.csv",
        "tech_filename": "resume_snehaan_tech.csv",
    },
    "resume_haider": {
        "label": "Resume Dataset (Haider Maseeh)",
        "keywords": ["haider"],
        "clean_filename": "resume_haider_clean.csv",
        "tech_filename": "resume_haider_tech.csv",
    },
}

# Crunchbase tech category terms (lowercase, matched on "|"-split category items)
CRUNCHBASE_TECH_TERMS: list[str] = [
    "software",
    "saas",
    "artificial intelligence",
    "machine learning",
    "analytics",
    "big data",
    "enterprise software",
    "internet",
    "mobile",
    "apps",
    "web development",
    "cloud computing",
    "cyber security",
    "fintech",
    "e-commerce",
    "computer vision",
    "data",
    "developer tools",
    "information technology",
]

# Strict tech title matcher (word-boundary, case-insensitive)
STRICT_TECH_PATTERNS: list[str] = [
    r"software(?:\s+engineer|\s+developer|\s+architect)?",
    r"developer",
    r"programmer",
    r"frontend",
    r"backend",
    r"fullstack",
    r"full-stack",
    r"web\s+developer",
    r"mobile\s+developer",
    r"android(?:\s+developer)?",
    r"ios(?:\s+developer)?",
    r"data\s+scientist",
    r"data\s+analyst",
    r"data\s+engineer",
    r"machine\s+learning",
    r"ml\s+engineer",
    r"ai\s+engineer",
    r"artificial\s+intelligence",
    r"deep\s+learning",
    r"devops(?:\s+engineer)?",
    r"cloud(?:\s+engineer|\s+architect)?",
    r"cybersecurity",
    r"qa\s+engineer",
    r"qa(?:\s+tester|\s+analyst)?",
    r"quality\s+assurance",
    r"database\s+administrator",
    r"dba",
    r"sysadmin",
    r"system\s+administrator",
    r"network\s+engineer",
    r"information\s+technology",
    r"it\s+specialist",
    r"it\s+manager",
    r"it\s+officer",
    r"it\s+support",
    r"it\s+engineer",
    r"it\s+consultant",
    r"tech\s+lead",
    r"cto",
]
STRICT_TECH_RE: re.Pattern[str] = re.compile(
    r"\b(?:" + "|".join(STRICT_TECH_PATTERNS) + r")\b", re.IGNORECASE
)

# Haider Maseeh categories
HAIDER_TECH_CATEGORIES: list[str] = [
    "Java Developers/Architects Resumes",
    "Web Developer Resumes",
    "SQL Developers Resumes",
    "Network and Systems Administrators Resumes",
    "Datawarehousing, ETL, Informatica Resumes",
    "Business Intelligence, Business Object Resumes",
]
HAIDER_EXCLUDED_CATEGORIES: list[str] = [
    "Business Analyst (BA) Resumes",
    "Project Manager Resumes",
    "Recruiter Resumes",
]

# PII redaction regexes
EMAIL_RE: re.Pattern[str] = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)
PHONE_RE: re.Pattern[str] = re.compile(
    r"(?:\+?\d{1,3}[\s-]?)?\(?\d{2,4}\)?[\s.-]?\d{3,4}[\s.-]?\d{3,4}\b"
)

# Arabic script Unicode code point ranges
ARABIC_RANGES: list[tuple[int, int]] = [
    (0x0600, 0x06FF),
    (0x0750, 0x077F),
    (0xFB50, 0xFDFF),
    (0xFE70, 0xFEFF),
]


# -----------------------------------------------------------------------------
# Utility Helpers
# -----------------------------------------------------------------------------


def read_csv_auto(filepath: Path, **kwargs: Any) -> pd.DataFrame:
    """Read a CSV trying UTF-8 first, then Latin-1. Strip column whitespace."""
    try:
        df = pd.read_csv(filepath, encoding="utf-8", **kwargs)
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding="latin-1", **kwargs)
    df.columns = [str(c).strip() for c in df.columns]
    return df


def redact_pii_text(text: str) -> str:
    """Redact emails and phone-like numbers from free text."""
    if not isinstance(text, str):
        return ""
    redacted = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    redacted = PHONE_RE.sub("[REDACTED_PHONE]", redacted)
    return redacted


def is_crunchbase_tech(category_str: Any) -> bool:
    """Check if pipe-delimited category string matches Crunchbase tech terms."""
    if not isinstance(category_str, str) or not category_str.strip():
        return False
    parts = [p.strip().lower() for p in category_str.split("|")]
    return any(any(kw in part for kw in CRUNCHBASE_TECH_TERMS) for part in parts)


def is_title_tech(title: Any) -> bool:
    """Check if title matches conservative word-boundary tech title matcher."""
    if not isinstance(title, str) or not title.strip():
        return False
    return bool(STRICT_TECH_RE.search(title))


def compute_arabic_script_share(series: pd.Series) -> float:
    """Calculate percentage of Arabic-script characters across non-null texts."""
    total_chars = 0
    matched_chars = 0
    for val in series.dropna():
        s = str(val)
        total_chars += len(s)
        for ch in s:
            cp = ord(ch)
            if any(lo <= cp <= hi for lo, hi in ARABIC_RANGES):
                matched_chars += 1
    return round((matched_chars / total_chars * 100.0), 2) if total_chars > 0 else 0.0


def check_val(
    label: str,
    actual: Any,
    expected: Any,
    op: str = "==",
    mismatches: list[str] | None = None,
) -> str:
    """Compare an actual value with expected threshold; return PASS or MISMATCH."""
    passed = False
    if op == "==":
        if isinstance(expected, float):
            passed = abs(float(actual) - expected) < 1e-4
        else:
            passed = actual == expected
    elif op == ">=":
        passed = float(actual) >= float(expected)
    elif op == "<=":
        passed = float(actual) <= float(expected)
    elif op == "~=":  # approximate within 1.0
        passed = abs(float(actual) - float(expected)) <= 1.0

    status = "PASS" if passed else "MISMATCH"
    msg = f"[{status}] {label}: actual={actual} (expected {op} {expected})"
    print(f"  {msg}")
    if not passed and mismatches is not None:
        mismatches.append(msg)
    return status


# -----------------------------------------------------------------------------
# Input File Discovery
# -----------------------------------------------------------------------------


def discover_input_datasets(input_dir: Path) -> dict[str, Path]:
    """List input directory items and match each of the 7 datasets by keyword."""
    print("=" * 70)
    print("STEP 1: DISCOVERING DATASETS IN INPUT DIRECTORY")
    print(f"Input Directory: {input_dir}")
    print("=" * 70)

    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")

    # List all top-level subdirectories and files with sizes
    discovered_dirs = [d for d in sorted(input_dir.iterdir()) if d.is_dir()]
    print(f"Found {len(discovered_dirs)} subdirectories:")
    for d in discovered_dirs:
        total_size = sum(f.stat().st_size for f in d.rglob("*") if f.is_file())
        print(f"  - {d.name} ({total_size:,} bytes)")

    matched_paths: dict[str, Path] = {}

    for key, spec in CONFIG.items():
        kws = spec["keywords"]
        matched = None
        for d in discovered_dirs:
            d_lower = d.name.lower()
            # Distinguish snehaan vs haider
            if key == "resume_snehaan":
                if ("resume" in d_lower or "snehaan" in d_lower) and "haider" not in d_lower:
                    matched = d
                    break
            elif key == "resume_haider":
                if "haider" in d_lower:
                    matched = d
                    break
            else:
                if any(kw in d_lower for kw in kws):
                    matched = d
                    break

        if matched is None:
            raise FileNotFoundError(
                f"Missing dataset '{spec['label']}' (key: {key}) in {input_dir}. "
                f"Searched keywords: {kws}"
            )
        matched_paths[key] = matched
        print(f"  -> Matched {key} ('{spec['label']}') to: {matched.name}")

    print("All 7 datasets successfully located.\n")
    return matched_paths


# -----------------------------------------------------------------------------
# Dataset Preprocessing Functions
# -----------------------------------------------------------------------------


def process_roman_urdu_parl(
    dataset_dir: Path, mismatches: list[str]
) -> dict[str, Any]:
    """1. Roman-Urdu-Parl split dataset."""
    label = "Roman-Urdu-Parl split"
    print("=" * 70)
    print(f"DATASET 1: {label}")
    print("=" * 70)

    val1_path = dataset_dir / "validation_set.csv"
    val2_path = dataset_dir / "small_validation_set.csv"
    test1_path = dataset_dir / "test_set.csv"
    test2_path = dataset_dir / "small_test_set.csv"
    train_path = dataset_dir / "original_data" / "data.csv"

    # Load validation and test splits
    df_val1 = (
        read_csv_auto(val1_path, dtype=str, keep_default_na=False)
        if val1_path.exists()
        else pd.DataFrame()
    )
    df_val2 = (
        read_csv_auto(val2_path, dtype=str, keep_default_na=False)
        if val2_path.exists()
        else pd.DataFrame()
    )
    df_val = pd.concat([df_val1, df_val2], ignore_index=True)

    df_test1 = (
        read_csv_auto(test1_path, dtype=str, keep_default_na=False)
        if test1_path.exists()
        else pd.DataFrame()
    )
    df_test2 = (
        read_csv_auto(test2_path, dtype=str, keep_default_na=False)
        if test2_path.exists()
        else pd.DataFrame()
    )
    df_test = pd.concat([df_test1, df_test2], ignore_index=True)

    val_count = len(df_val)
    test_count = len(df_test)

    # Empty rows in val and test
    empty_val = int(
        ((df_val.iloc[:, 0].str.strip() == "") & (df_val.iloc[:, 1].str.strip() == "")).sum()
    )
    empty_test = int(
        ((df_test.iloc[:, 0].str.strip() == "") & (df_test.iloc[:, 1].str.strip() == "")).sum()
    )

    # Stream train in chunks (6.36M rows)
    train_count = 0
    empty_train = 0
    exact_dup_pairs_train = 0
    seen_train_hashes: set[int] = set()

    print("  Streaming train set (original_data/data.csv) in 500,000-row chunks...")
    for chunk in pd.read_csv(
        train_path, chunksize=500000, dtype=str, keep_default_na=False
    ):
        train_count += len(chunk)
        c0 = chunk.iloc[:, 0].values
        c1 = chunk.iloc[:, 1].values
        for u_text, ru_text in zip(c0, c1):
            if not u_text.strip() and not ru_text.strip():
                empty_train += 1
            # 32-bit CRC hash for memory-efficient exact pair duplicate tracking
            h = zlib.crc32((u_text + "|||" + ru_text).encode("utf-8"))
            if h in seen_train_hashes:
                exact_dup_pairs_train += 1
            else:
                seen_train_hashes.add(h)

    total_count = train_count + val_count + test_count
    total_empty = empty_train + empty_val + empty_test

    # Script character share on validation Urdu column
    urdu_col = df_val.columns[0]
    urdu_script_share = compute_arabic_script_share(df_val[urdu_col])
    print(f"  Urdu column Arabic script share: {urdu_script_share}%")
    print(f"  Empty rows across splits: train={empty_train}, val={empty_val}, test={empty_test} (total={total_empty})")
    print(f"  Exact duplicate pairs in train: {exact_dup_pairs_train:,}")

    # Checks
    check_val(f"{label} train rows", train_count, 6365808, mismatches=mismatches)
    check_val(f"{label} validation rows", val_count, 20719, mismatches=mismatches)
    check_val(f"{label} test rows", test_count, 20741, mismatches=mismatches)
    check_val(f"{label} total rows", total_count, 6407268, mismatches=mismatches)
    check_val(
        f"{label} Arabic script share %",
        urdu_script_share,
        76.8,
        op="~=",
        mismatches=mismatches,
    )

    print("  Note: Kept whole, general language benchmark; no cleaned file written.\n")
    return {
        "dataset": label,
        "raw_count": total_count,
        "cleaned_count": total_count,
        "tech_count": total_count,
        "status": "PASS" if not mismatches else "REVIEW",
    }


def process_pakistan_startup_census(
    dataset_dir: Path, output_dir: Path, mismatches: list[str]
) -> dict[str, Any]:
    """2. Pakistan Startup Census."""
    label = "Pakistan Startup Census"
    print("=" * 70)
    print(f"DATASET 2: {label}")
    print("=" * 70)

    csv_path = dataset_dir / "Pakistan Startup Census.csv"
    df_raw = read_csv_auto(csv_path)
    raw_physical_rows = len(df_raw)
    raw_cols = len(df_raw.columns)

    # Blank rows check
    blank_mask = df_raw.isna().all(axis=1)
    blank_rows = int(blank_mask.sum())
    df_usable = df_raw[~blank_mask].copy()
    usable_rows = len(df_usable)

    # Duplicate names on usable rows
    name_col = "Name"
    dup_names = int(df_usable[name_col].duplicated().sum())
    exact_dups = int(df_usable.duplicated().sum())
    print(f"  Physical rows: {raw_physical_rows}, Blank rows: {blank_rows}, Usable: {usable_rows}")
    print(f"  Columns: {df_usable.columns.tolist()} ({raw_cols})")
    print(f"  Duplicate names: {dup_names}, Exact duplicate rows: {exact_dups}")

    # Drop exact duplicate rows if any
    df_clean = df_usable.drop_duplicates().copy()

    # Tech filter on Description using conservative word-boundary matcher
    desc_col = "Description"
    tech_mask = df_clean[desc_col].fillna("").astype(str).map(is_title_tech)
    tech_count = int(tech_mask.sum())
    tech_share = round((tech_count / usable_rows * 100.0), 2)
    print(f"  Tech startups identified: {tech_count} / {usable_rows} ({tech_share}%)")

    # Save cleaned full copy and tech subset
    clean_out = output_dir / CONFIG["pakistan_startup_census"]["clean_filename"]
    tech_out = output_dir / CONFIG["pakistan_startup_census"]["tech_filename"]
    df_clean.to_csv(clean_out, index=False, encoding="utf-8")
    df_clean[tech_mask].to_csv(tech_out, index=False, encoding="utf-8")
    print(f"  Saved cleaned copy: {clean_out.name} ({len(df_clean)} rows)")
    print(f"  Saved tech subset:  {tech_out.name} ({tech_count} rows)")

    # Checks
    check_val(f"{label} physical rows", raw_physical_rows, 553, mismatches=mismatches)
    check_val(f"{label} blank rows", blank_rows, 120, mismatches=mismatches)
    check_val(f"{label} usable rows", usable_rows, 433, mismatches=mismatches)
    check_val(f"{label} columns count", raw_cols, 7, mismatches=mismatches)
    check_val(f"{label} duplicate names", dup_names, 1, mismatches=mismatches)
    check_val(f"{label} tech share %", tech_share, 11.78, op=">=", mismatches=mismatches)

    print()
    return {
        "dataset": label,
        "raw_count": raw_physical_rows,
        "cleaned_count": len(df_clean),
        "tech_count": tech_count,
        "status": "PASS",
    }


def process_pakistan_job_market(
    dataset_dir: Path, output_dir: Path, mismatches: list[str]
) -> dict[str, Any]:
    """3. Pakistan's Job Market."""
    label = "Pakistan's Job Market"
    print("=" * 70)
    print(f"DATASET 3: {label}")
    print("=" * 70)

    csv_path = dataset_dir / "Pakistan Available Job Dec 19 - Mar-21.csv"
    df_raw = read_csv_auto(csv_path)
    raw_rows = len(df_raw)
    raw_cols = len(df_raw.columns)

    # City counts
    city_counts = df_raw["City"].value_counts().to_dict()
    lahore_count = city_counts.get("Lahore", 0)
    islamabad_count = city_counts.get("Islamabad", 0)
    karachi_count = city_counts.get("Karachi", 0)
    print(f"  Top Cities: Lahore={lahore_count}, Islamabad={islamabad_count}, Karachi={karachi_count}")

    # Duplicates on title+company+date
    trip_cols = ["Job Name", "Company Name", "Date Posted"]
    trip_dups = int(df_raw.duplicated(subset=trip_cols).sum())
    trip_dup_pct = round((trip_dups / raw_rows * 100.0), 2)
    print(f"  Duplicates on (Job Name, Company Name, Date Posted): {trip_dups} ({trip_dup_pct}%)")

    # Raw tech share
    raw_tech_mask = df_raw["Job Name"].astype(str).map(is_title_tech)
    raw_tech_count = int(raw_tech_mask.sum())
    raw_tech_share = round((raw_tech_count / raw_rows * 100.0), 2)
    print(f"  Raw tech share (title matcher): {raw_tech_count} / {raw_rows} ({raw_tech_share}%) [reported as at least]")

    # Clean: drop duplicates on title+company+date
    df_clean = df_raw.drop_duplicates(subset=trip_cols).copy()
    cleaned_rows = len(df_clean)

    # Add description_truncated flag
    df_clean["description_truncated"] = True

    # Tech subset
    clean_tech_mask = df_clean["Job Name"].astype(str).map(is_title_tech)
    clean_tech_count = int(clean_tech_mask.sum())
    clean_tech_share = round((clean_tech_count / cleaned_rows * 100.0), 2)
    print(f"  Clean tech share (title matcher): {clean_tech_count} / {cleaned_rows} ({clean_tech_share}%)")

    # Save
    clean_out = output_dir / CONFIG["pakistan_job_market"]["clean_filename"]
    tech_out = output_dir / CONFIG["pakistan_job_market"]["tech_filename"]
    df_clean.to_csv(clean_out, index=False, encoding="utf-8")
    df_clean[clean_tech_mask].to_csv(tech_out, index=False, encoding="utf-8")
    print(f"  Saved cleaned copy: {clean_out.name} ({cleaned_rows} rows)")
    print(f"  Saved tech subset:  {tech_out.name} ({clean_tech_count} rows)")

    # Checks
    check_val(f"{label} raw rows", raw_rows, 6680, mismatches=mismatches)
    check_val(f"{label} columns count", raw_cols, 9, mismatches=mismatches)
    check_val(f"{label} Lahore count", lahore_count, 2046, mismatches=mismatches)
    check_val(f"{label} Islamabad count", islamabad_count, 1921, mismatches=mismatches)
    check_val(f"{label} Karachi count", karachi_count, 1700, mismatches=mismatches)
    check_val(f"{label} duplicate triplet %", trip_dup_pct, 19.64, mismatches=mismatches)
    check_val(f"{label} raw tech share %", raw_tech_share, 26.8, op=">=", mismatches=mismatches)

    print()
    return {
        "dataset": label,
        "raw_count": raw_rows,
        "cleaned_count": cleaned_rows,
        "tech_count": clean_tech_count,
        "status": "PASS",
    }


def process_startup_success_fail(
    dataset_dir: Path, output_dir: Path, mismatches: list[str]
) -> dict[str, Any]:
    """4. Startup Success/Fail Dataset from Crunchbase."""
    label = "Startup Success/Fail (Crunchbase)"
    print("=" * 70)
    print(f"DATASET 4: {label}")
    print("=" * 70)

    csv_path = dataset_dir / "big_startup_secsees_dataset.csv"
    df_raw = read_csv_auto(csv_path)
    raw_rows = len(df_raw)
    raw_cols = len(df_raw.columns)

    # Clean founded_at and flag valid years (1990-2015)
    parsed_founded = pd.to_datetime(df_raw["founded_at"], errors="coerce")
    founded_year = parsed_founded.dt.year
    missing_founded_count = int(df_raw["founded_at"].isna().sum())
    missing_founded_pct = round((missing_founded_count / raw_rows * 100.0), 2)
    print(f"  Raw rows: {raw_rows}, Columns: {raw_cols}")
    print(f"  Missing founded_at: {missing_founded_count} ({missing_founded_pct}%)")

    df_clean = df_raw.copy()
    df_clean["founded_year_valid"] = founded_year.between(1990, 2015)
    valid_year_count = int(df_clean["founded_year_valid"].sum())
    print(f"  founded_year_valid (1990-2015): {valid_year_count} rows ({round(valid_year_count/raw_rows*100, 2)}%)")

    # Tech filter: category-list filter on pipe-separated categories
    tech_mask = df_clean["category_list"].apply(is_crunchbase_tech)
    tech_count = int(tech_mask.sum())
    non_missing_cat = raw_rows - int(df_clean["category_list"].isna().sum())
    tech_pct_cat = round((tech_count / non_missing_cat * 100.0), 2)
    print(f"  Tech rows: {tech_count} ({tech_pct_cat}% of {non_missing_cat} non-missing category rows)")

    # Status counts inside tech
    df_tech = df_clean[tech_mask].copy()
    status_counts = df_tech["status"].value_counts().to_dict()
    op_cnt = status_counts.get("operating", 0)
    acq_cnt = status_counts.get("acquired", 0)
    cl_cnt = status_counts.get("closed", 0)
    ipo_cnt = status_counts.get("ipo", 0)
    print(f"  Status inside tech: operating={op_cnt}, acquired={acq_cnt}, closed={cl_cnt}, ipo={ipo_cnt}")

    # Save
    clean_out = output_dir / CONFIG["startup_success_fail"]["clean_filename"]
    tech_out = output_dir / CONFIG["startup_success_fail"]["tech_filename"]
    df_clean.to_csv(clean_out, index=False, encoding="utf-8")
    df_tech.to_csv(tech_out, index=False, encoding="utf-8")
    print(f"  Saved cleaned copy: {clean_out.name} ({len(df_clean)} rows)")
    print(f"  Saved tech subset:  {tech_out.name} ({tech_count} rows)")

    # Checks
    check_val(f"{label} raw rows", raw_rows, 66368, mismatches=mismatches)
    check_val(f"{label} columns count", raw_cols, 14, mismatches=mismatches)
    check_val(f"{label} missing founded_at %", missing_founded_pct, 22.9, op="~=", mismatches=mismatches)
    check_val(f"{label} tech rows count", tech_count, 28695, mismatches=mismatches)
    check_val(f"{label} tech % of cat", tech_pct_cat, 45.4, op="~=", mismatches=mismatches)
    check_val(f"{label} operating count", op_cnt, 23211, mismatches=mismatches)
    check_val(f"{label} acquired count", acq_cnt, 2834, mismatches=mismatches)
    check_val(f"{label} closed count", cl_cnt, 2221, mismatches=mismatches)
    check_val(f"{label} ipo count", ipo_cnt, 429, mismatches=mismatches)

    print()
    return {
        "dataset": label,
        "raw_count": raw_rows,
        "cleaned_count": len(df_clean),
        "tech_count": tech_count,
        "status": "PASS",
    }


def process_startup_investments(
    dataset_dir: Path, output_dir: Path, mismatches: list[str]
) -> dict[str, Any]:
    """5. StartUp Investments (Crunchbase)."""
    label = "StartUp Investments (Crunchbase)"
    print("=" * 70)
    print(f"DATASET 5: {label}")
    print("=" * 70)

    csv_path = dataset_dir / "investments_VC.csv"
    df_raw = read_csv_auto(csv_path)
    raw_rows = len(df_raw)
    raw_cols = len(df_raw.columns)

    # Drop blank rows
    blank_mask = df_raw.isna().all(axis=1)
    blank_rows = int(blank_mask.sum())
    df_clean = df_raw[~blank_mask].copy()
    usable_rows = len(df_clean)
    usable_dups = int(df_clean.duplicated().sum())
    print(f"  Raw rows: {raw_rows}, Blank rows: {blank_rows}, Usable rows: {usable_rows}")
    print(f"  Columns: {raw_cols}, Duplicates on usable rows: {usable_dups}")

    # Clean funding_total_usd: coerce non-numeric (e.g. '-') to NaN
    fund_str = (
        df_clean["funding_total_usd"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.strip()
    )
    df_clean["funding_total_usd_numeric"] = pd.to_numeric(fund_str, errors="coerce")

    # Missing funding calculation:
    # On raw rows: blank rows (4,856) + non-numeric '-' (8,531) = 13,387 / 54,294 = 24.66% (~24.7%)
    # On usable rows: 8,531 / 49,438 = 17.26%
    raw_missing_funding = blank_rows + int(df_clean["funding_total_usd_numeric"].isna().sum())
    raw_missing_funding_pct = round((raw_missing_funding / raw_rows * 100.0), 2)
    usable_missing_funding_pct = round(
        (int(df_clean["funding_total_usd_numeric"].isna().sum()) / usable_rows * 100.0), 2
    )
    print(f"  funding_total_usd missing on raw rows (incl. blanks): {raw_missing_funding_pct}% (~24.7%)")
    print(f"  funding_total_usd missing on usable rows: {usable_missing_funding_pct}%")

    # Parse dates and add valid-date flags
    for col in ["founded_at", "first_funding_at", "last_funding_at"]:
        parsed = pd.to_datetime(df_clean[col], errors="coerce")
        df_clean[f"{col}_year_valid"] = parsed.dt.year.between(1990, 2015)

    # Tech filter on category_list
    tech_mask = df_clean["category_list"].apply(is_crunchbase_tech)
    tech_count = int(tech_mask.sum())
    non_missing_cat = usable_rows - int(df_clean["category_list"].isna().sum())
    tech_pct_cat = round((tech_count / non_missing_cat * 100.0), 2)
    print(f"  Tech rows: {tech_count} ({tech_pct_cat}% of {non_missing_cat} non-missing category rows)")

    # Save
    clean_out = output_dir / CONFIG["startup_investments"]["clean_filename"]
    tech_out = output_dir / CONFIG["startup_investments"]["tech_filename"]
    df_clean.to_csv(clean_out, index=False, encoding="utf-8")
    df_clean[tech_mask].to_csv(tech_out, index=False, encoding="utf-8")
    print(f"  Saved cleaned copy: {clean_out.name} ({len(df_clean)} rows)")
    print(f"  Saved tech subset:  {tech_out.name} ({tech_count} rows)")

    # Checks
    check_val(f"{label} raw rows", raw_rows, 54294, mismatches=mismatches)
    check_val(f"{label} columns count", raw_cols, 39, mismatches=mismatches)
    check_val(f"{label} blank rows", blank_rows, 4856, mismatches=mismatches)
    check_val(f"{label} usable rows", usable_rows, 49438, mismatches=mismatches)
    check_val(f"{label} usable duplicates", usable_dups, 0, mismatches=mismatches)
    check_val(f"{label} raw missing funding %", raw_missing_funding_pct, 24.7, op="~=", mismatches=mismatches)
    check_val(f"{label} tech rows count", tech_count, 20542, mismatches=mismatches)
    check_val(f"{label} tech % of cat", tech_pct_cat, 45.2, op="~=", mismatches=mismatches)

    print()
    return {
        "dataset": label,
        "raw_count": raw_rows,
        "cleaned_count": len(df_clean),
        "tech_count": tech_count,
        "status": "PASS",
    }


def process_resume_snehaan(
    dataset_dir: Path, output_dir: Path, mismatches: list[str]
) -> dict[str, Any]:
    """6. Resume Dataset (Snehaan Bhawal)."""
    label = "Resume Dataset (Snehaan Bhawal)"
    print("=" * 70)
    print(f"DATASET 6: {label}")
    print("=" * 70)

    csv_path = dataset_dir / "Resume" / "Resume.csv"
    df_raw = read_csv_auto(csv_path)
    raw_rows = len(df_raw)
    raw_cols = len(df_raw.columns)
    cat_count = df_raw["Category"].nunique()

    # Drop Resume_html
    df_clean = df_raw.drop(columns=["Resume_html"], errors="ignore").copy()

    # Redact emails and phone numbers in Resume_str
    print("  Redacting emails and phone numbers in Resume_str...")
    df_clean["Resume_str"] = df_clean["Resume_str"].apply(redact_pii_text)

    # Category counts
    norm_cats = df_clean["Category"].astype(str).str.lower().str.replace("_", "-").str.strip()
    it_count = int((norm_cats == "information-technology").sum())
    eng_count = int((norm_cats == "engineering").sum())
    print(f"  Categories: {cat_count} total | IT: {it_count}, Engineering: {eng_count}")

    # Tech subset: Category in Information-Technology or Engineering
    tech_mask = norm_cats.isin(["information-technology", "engineering"])
    tech_count = int(tech_mask.sum())
    print(f"  Tech subset rows: {tech_count} ({round(tech_count/raw_rows*100, 2)}%)")

    # Save
    clean_out = output_dir / CONFIG["resume_snehaan"]["clean_filename"]
    tech_out = output_dir / CONFIG["resume_snehaan"]["tech_filename"]
    df_clean.to_csv(clean_out, index=False, encoding="utf-8")
    df_clean[tech_mask].to_csv(tech_out, index=False, encoding="utf-8")
    print(f"  Saved cleaned copy: {clean_out.name} ({len(df_clean)} rows)")
    print(f"  Saved tech subset:  {tech_out.name} ({tech_count} rows)")

    # Checks
    check_val(f"{label} raw rows", raw_rows, 2484, mismatches=mismatches)
    check_val(f"{label} columns count", raw_cols, 4, mismatches=mismatches)
    check_val(f"{label} categories count", cat_count, 24, mismatches=mismatches)
    check_val(f"{label} IT category count", it_count, 120, mismatches=mismatches)
    check_val(f"{label} Engineering category count", eng_count, 118, mismatches=mismatches)
    check_val(f"{label} tech subset count", tech_count, 238, mismatches=mismatches)

    print()
    return {
        "dataset": label,
        "raw_count": raw_rows,
        "cleaned_count": len(df_clean),
        "tech_count": tech_count,
        "status": "PASS",
    }


def process_resume_haider(
    dataset_dir: Path, output_dir: Path, mismatches: list[str]
) -> dict[str, Any]:
    """7. Resume Dataset (Haider Maseeh)."""
    label = "Resume Dataset (Haider Maseeh)"
    print("=" * 70)
    print(f"DATASET 7: {label}")
    print("=" * 70)

    csv_path = dataset_dir / "Resume dataset.csv"
    df_raw = read_csv_auto(csv_path)
    raw_rows = len(df_raw)
    raw_cols = len(df_raw.columns)

    # Redact emails and phone numbers in Text
    df_clean = df_raw.copy()
    print("  Redacting emails and phone numbers in Text...")
    df_clean["Text"] = df_clean["Text"].apply(redact_pii_text)

    # Filter to 6 tech categories
    tech_mask = df_clean["category"].isin(HAIDER_TECH_CATEGORIES)
    df_tech_categories = df_clean[tech_mask].copy()
    tech_cat_rows = len(df_tech_categories)

    # Unique texts in tech categories and duplicate rate
    unique_texts = int(df_tech_categories["Text"].nunique())
    dup_text_pct = round(((tech_cat_rows - unique_texts) / tech_cat_rows * 100.0), 2)
    print(f"  Total categories: {df_raw['category'].nunique()} (1,000 rows each)")
    print(f"  Tech category rows (6 categories): {tech_cat_rows}")
    print(f"  Tech unique texts: {unique_texts} (duplicate rate: {dup_text_pct}%)")

    # Tech subset: tech categories only, unique texts only
    df_tech_unique = df_tech_categories.drop_duplicates(subset=["Text"]).copy()
    final_tech_count = len(df_tech_unique)

    # Save
    clean_out = output_dir / CONFIG["resume_haider"]["clean_filename"]
    tech_out = output_dir / CONFIG["resume_haider"]["tech_filename"]
    df_clean.to_csv(clean_out, index=False, encoding="utf-8")
    df_tech_unique.to_csv(tech_out, index=False, encoding="utf-8")
    print(f"  Saved cleaned copy: {clean_out.name} ({len(df_clean)} rows)")
    print(f"  Saved tech subset:  {tech_out.name} ({final_tech_count} rows)")

    # Checks
    check_val(f"{label} raw rows", raw_rows, 9000, mismatches=mismatches)
    check_val(f"{label} columns count", raw_cols, 3, mismatches=mismatches)
    check_val(f"{label} tech category rows", tech_cat_rows, 6000, mismatches=mismatches)
    check_val(f"{label} tech unique texts", unique_texts, 4170, mismatches=mismatches)
    check_val(f"{label} tech duplicate text %", dup_text_pct, 30.5, mismatches=mismatches)

    print()
    return {
        "dataset": label,
        "raw_count": raw_rows,
        "cleaned_count": len(df_clean),
        "tech_count": final_tech_count,
        "status": "PASS",
    }


# -----------------------------------------------------------------------------
# Main Execution Pipeline
# -----------------------------------------------------------------------------


def main() -> None:
    """Run preprocessing for all 7 FINAL datasets."""
    # Resolve input directory
    env_dir = os.environ.get("CARNET_DATA_DIR")
    input_dir = Path(env_dir).resolve() if env_dir else DEFAULT_FINAL_DIR

    # Resolve output directory: sibling folder "CLEANED" next to FINAL
    output_dir = input_dir.parent / "CLEANED"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory initialized at: {output_dir}\n")

    # Match datasets
    matched_paths = discover_input_datasets(input_dir)

    all_mismatches: list[str] = []
    summary_records: list[dict[str, Any]] = []

    # Process all 7 datasets
    rec1 = process_roman_urdu_parl(matched_paths["roman_urdu_parl"], all_mismatches)
    summary_records.append(rec1)

    rec2 = process_pakistan_startup_census(
        matched_paths["pakistan_startup_census"], output_dir, all_mismatches
    )
    summary_records.append(rec2)

    rec3 = process_pakistan_job_market(
        matched_paths["pakistan_job_market"], output_dir, all_mismatches
    )
    summary_records.append(rec3)

    rec4 = process_startup_success_fail(
        matched_paths["startup_success_fail"], output_dir, all_mismatches
    )
    summary_records.append(rec4)

    rec5 = process_startup_investments(
        matched_paths["startup_investments"], output_dir, all_mismatches
    )
    summary_records.append(rec5)

    rec6 = process_resume_snehaan(
        matched_paths["resume_snehaan"], output_dir, all_mismatches
    )
    summary_records.append(rec6)

    rec7 = process_resume_haider(
        matched_paths["resume_haider"], output_dir, all_mismatches
    )
    summary_records.append(rec7)

    # Build summary dataframe
    summary_df = pd.DataFrame(summary_records)
    summary_csv = output_dir / "preprocessing_summary.csv"
    summary_df.to_csv(summary_csv, index=False, encoding="utf-8")

    # Print summary table
    print("=" * 80)
    print("PREPROCESSING SUMMARY TABLE")
    print("=" * 80)
    print(
        f"{'Dataset':<38} | {'Raw Count':>10} | {'Cleaned':>10} | {'Tech Subset':>11} | {'Status':>6}"
    )
    print("-" * 84)
    for rec in summary_records:
        print(
            f"{rec['dataset']:<38} | {rec['raw_count']:>10,} | {rec['cleaned_count']:>10,} | "
            f"{rec['tech_count']:>11,} | {rec['status']:>6}"
        )
    print("-" * 84)
    print(f"\nSummary table saved to: {summary_csv}")

    # Report mismatches if any
    print("\n" + "=" * 80)
    print("VERIFICATION CHECKS AUDIT")
    print("=" * 80)
    if all_mismatches:
        print(f"Total MISMATCHES detected: {len(all_mismatches)}")
        for m in all_mismatches:
            print(f"  {m}")
    else:
        print("ALL VERIFICATION CHECKS PASSED (0 mismatches).")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
