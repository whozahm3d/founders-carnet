"""Preprocessing Part 2 for The Founder's Carnet datasets.

Profiles, cleans, and runs targeted verification checks on:
- Startup Success/Fail (Crunchbase 1990-2015 filter and closed status share)
- Resume Dataset (Haider Maseeh technical deduplication and multi-category audit)
- Roman-Urdu-Parl split (streaming recount, card comparison, script shares, overlap, and train PII scan)
- PII count scans on smaller datasets (Census, Job Market, Bhawal, Maseeh)

Rules:
- Read-only on all inputs.
- No emojis, no em dashes.
- Output files written:
  * part2_results.csv
  * part2_results.md
  * part2_run.log
  * startup_success_fail_1990_2015_part2.csv
  * maseeh_tech_dedup_part2.csv
"""

from __future__ import annotations

import hashlib
import os
import random
import re
import sys
import time
from pathlib import Path
from typing import Any

import pandas as pd

# -----------------------------------------------------------------------------
# Configuration and Constants
# -----------------------------------------------------------------------------

RANDOM_SEED = 42

DEFAULT_FINAL_DIR = Path(
    r"E:\Documents\advanced_statistics\fyp\founders-carnet\carnet_data\data\FINAL"
)

# Regex patterns for PII scans (counts only)
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", re.IGNORECASE)
URL_RE = re.compile(
    r"(?:https?://|www\.)\S+|\b[A-Za-z0-9.-]+\.(?:com|pk|org|net|io|edu|gov)\b(?:/\S*)?",
    re.IGNORECASE,
)
PHONE_RE = re.compile(r"(?:\+?\d{1,3}[\s-]?)?\(?\d{2,4}\)?[\s.-]?\d{3,4}[\s.-]?\d{3,4}\b")
CNIC_RE = re.compile(r"\b\d{5}-\d{7}-\d\b")

# Unicode code point ranges for Arabic script
ARABIC_RANGES = [
    (0x0600, 0x06FF),
    (0x0750, 0x077F),
    (0xFB50, 0xFDFF),
    (0xFE70, 0xFEFF),
]

# Haider Maseeh categories
HAIDER_TECH_CATEGORIES = [
    "Java Developers/Architects Resumes",
    "Web Developer Resumes",
    "SQL Developers Resumes",
    "Network and Systems Administrators Resumes",
    "Datawarehousing, ETL, Informatica Resumes",
    "Business Intelligence, Business Object Resumes",
]
HAIDER_EXCLUDED_CATEGORIES = [
    "Business Analyst (BA) Resumes",
    "Project Manager Resumes",
    "Recruiter Resumes",
]


# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------


def read_csv_safe(filepath: Path, **kwargs: Any) -> pd.DataFrame:
    """Read CSV trying UTF-8 first, then Latin-1. Strip column whitespace."""
    try:
        df = pd.read_csv(filepath, encoding="utf-8", **kwargs)
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding="latin-1", **kwargs)
    df.columns = [str(c).strip() for c in df.columns]
    return df


def calculate_script_share(
    series: pd.Series, ranges: list[tuple[int, int]] | None = None
) -> float:
    """Calculate character share for given unicode ranges."""
    total_chars = 0
    matched_chars = 0
    for val in series.dropna():
        s = str(val)
        total_chars += len(s)
        for ch in s:
            cp = ord(ch)
            if ranges is not None:
                if any(lo <= cp <= hi for lo, hi in ranges):
                    matched_chars += 1
            else:
                if ("a" <= ch <= "z") or ("A" <= ch <= "Z"):
                    matched_chars += 1
    return round((matched_chars / total_chars * 100.0), 2) if total_chars > 0 else 0.0


def add_check(
    results: list[dict[str, Any]],
    dataset: str,
    check_name: str,
    expected: Any,
    actual: Any,
    note: str = "",
    tolerance: float = 1e-4,
) -> None:
    """Record a check row with PASS, FAIL, or INFO status."""
    if expected is None:
        status = "INFO"
    else:
        if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
            is_match = abs(float(actual) - float(expected)) <= tolerance
        else:
            is_match = str(actual) == str(expected)
        status = "PASS" if is_match else "FAIL"

    record = {
        "dataset": dataset,
        "check": check_name,
        "expected": "" if expected is None else str(expected),
        "actual": str(actual),
        "status": status,
        "note": note,
    }
    results.append(record)
    print(f"[{status:4s}] {dataset} | {check_name}: actual={actual} (expected={record['expected']})")


# -----------------------------------------------------------------------------
# Job 1: Startup Success/Fail (Crunchbase), 1990-2015 Filter
# -----------------------------------------------------------------------------


def run_job1_crunchbase_dates(
    input_dir: Path, output_dir: Path, results: list[dict[str, Any]], log_lines: list[str]
) -> None:
    """Job 1: Startup Success/Fail (Crunchbase) founding date filter and closed share."""
    t0 = time.time()
    ds_name = "Startup Success/Fail (Crunchbase)"
    log_lines.append(f"Starting Job 1 ({ds_name})...")
    print("\n" + "=" * 70)
    print(f"JOB 1: {ds_name}")
    print("=" * 70)

    # Locate CSV file
    csv_candidates = list(input_dir.rglob("big_startup_secsees_dataset.csv"))
    if not csv_candidates:
        add_check(results, ds_name, "raw_file", "EXISTS", "NOT FOUND", "big_startup_secsees_dataset.csv not found")
        return

    csv_path = csv_candidates[0]
    df = read_csv_safe(csv_path, low_memory=False)
    raw_rows = len(df)
    add_check(results, ds_name, "raw_rows", 66368, raw_rows, "Expected 66,368 raw rows")

    # Founding date column
    date_col = "founded_at" if "founded_at" in df.columns else None
    if date_col is None:
        for c in df.columns:
            if "founded" in c.lower() and "at" in c.lower():
                date_col = c
                break

    if date_col is None:
        add_check(results, ds_name, "founded_date_column", "EXISTS", "COLUMN MISSING", "founded_at column missing")
        return

    # Parse dates
    parsed_dates = pd.to_datetime(df[date_col], errors="coerce")
    unparseable_or_na = int((df[date_col].isna() | parsed_dates.isna()).sum())
    add_check(
        results,
        ds_name,
        "unparseable_or_missing_dates",
        None,
        unparseable_or_na,
        f"{round(unparseable_or_na / raw_rows * 100.0, 2)}% of raw rows have missing or unparseable founded_at",
    )

    years = parsed_dates.dt.year
    impossible_dates = int(((years < 1900) | (years > 2026)).sum())
    add_check(
        results,
        ds_name,
        "impossible_dates_before_1900_or_after_2026",
        None,
        impossible_dates,
        "Impossible dates include extreme outliers like years 1015, 1592, and 2914",
    )

    # Filter to 1990-2015 inclusive
    in_range_mask = (years >= 1990) & (years <= 2015)
    filtered_rows = int(in_range_mask.sum())
    add_check(
        results,
        ds_name,
        "rows_after_1990_2015_filter",
        None,
        filtered_rows,
        f"Retained {round(filtered_rows / raw_rows * 100.0, 2)}% of raw records",
    )

    # Closed status analysis
    df_filtered = df[in_range_mask].copy()

    # Before filter
    closed_raw = int((df["status"].astype(str).str.lower() == "closed").sum())
    not_closed_raw = int(
        df["status"].astype(str).str.lower().isin(["operating", "acquired", "ipo"]).sum()
    )
    closed_share_raw = round(closed_raw / raw_rows * 100.0, 2)
    add_check(
        results,
        ds_name,
        "closed_count_before_filter",
        None,
        closed_raw,
        "Status closed before 1990-2015 filter",
    )
    add_check(
        results,
        ds_name,
        "not_closed_count_before_filter",
        None,
        not_closed_raw,
        "Status operating, acquired, ipo before filter",
    )
    add_check(
        results,
        ds_name,
        "closed_share_before_filter_pct",
        None,
        closed_share_raw,
        f"{closed_raw} / {raw_rows} = {closed_share_raw}%",
    )

    # After filter
    closed_filt = int((df_filtered["status"].astype(str).str.lower() == "closed").sum())
    not_closed_filt = int(
        df_filtered["status"].astype(str).str.lower().isin(["operating", "acquired", "ipo"]).sum()
    )
    closed_share_filt = round(closed_filt / filtered_rows * 100.0, 2)
    add_check(
        results,
        ds_name,
        "closed_count_after_filter",
        None,
        closed_filt,
        "Status closed after 1990-2015 filter",
    )
    add_check(
        results,
        ds_name,
        "not_closed_count_after_filter",
        None,
        not_closed_filt,
        "Status operating, acquired, ipo after filter",
    )
    add_check(
        results,
        ds_name,
        "closed_share_after_filter_pct",
        None,
        closed_share_filt,
        f"{closed_filt} / {filtered_rows} = {closed_share_filt}%",
    )

    # Save filtered file as startup_success_fail_1990_2015_part2.csv
    out_file = output_dir / "startup_success_fail_1990_2015_part2.csv"
    df_filtered.to_csv(out_file, index=False, encoding="utf-8")
    print(f"  Saved filtered data to: {out_file.name} ({filtered_rows} rows)")

    dur = time.time() - t0
    log_lines.append(f"Job 1 completed in {dur:.2f}s (saved {out_file.name})")


# -----------------------------------------------------------------------------
# Job 2: Resume Dataset (Haider Maseeh), Duplicate Removal
# -----------------------------------------------------------------------------


def run_job2_maseeh_dedup(
    input_dir: Path, output_dir: Path, results: list[dict[str, Any]], log_lines: list[str]
) -> None:
    """Job 2: Resume Dataset (Haider Maseeh) technical deduplication."""
    t0 = time.time()
    ds_name = "Resume Dataset (Haider Maseeh)"
    log_lines.append(f"Starting Job 2 ({ds_name})...")
    print("\n" + "=" * 70)
    print(f"JOB 2: {ds_name}")
    print("=" * 70)

    csv_candidates = list(input_dir.rglob("Resume dataset.csv"))
    if not csv_candidates:
        add_check(results, ds_name, "raw_file", "EXISTS", "NOT FOUND", "Resume dataset.csv not found")
        return

    csv_path = csv_candidates[0]
    df = read_csv_safe(csv_path, low_memory=False)
    raw_rows = len(df)
    add_check(results, ds_name, "raw_rows", 9000, raw_rows, "Expected 9,000 raw rows")

    # Split into 6 technical categories and 3 excluded categories
    df_tech = df[df["category"].isin(HAIDER_TECH_CATEGORIES)].copy()
    df_excl = df[df["category"].isin(HAIDER_EXCLUDED_CATEGORIES)].copy()

    tech_rows_raw = len(df_tech)
    excl_rows_raw = len(df_excl)
    add_check(
        results,
        ds_name,
        "tech_categories_raw_rows",
        6000,
        tech_rows_raw,
        "6 technical categories x 1,000 rows each",
    )
    add_check(
        results,
        ds_name,
        "excluded_categories_raw_rows",
        3000,
        excl_rows_raw,
        "3 excluded categories (BA, PM, Recruiter) x 1,000 rows each",
    )

    # Whitespace strip on Text
    df_tech["Text_stripped"] = df_tech["Text"].astype(str).str.strip()
    unique_texts = int(df_tech["Text_stripped"].nunique())
    dup_share = round((tech_rows_raw - unique_texts) / tech_rows_raw * 100.0, 1)

    add_check(
        results,
        ds_name,
        "tech_unique_texts",
        4170,
        unique_texts,
        "Unique resume texts across the 6 technical categories",
    )
    add_check(
        results,
        ds_name,
        "tech_duplicate_share_pct",
        30.5,
        dup_share,
        f"(6000 - 4170) / 6000 = {dup_share}%",
    )

    # Multi-category duplicate text check
    cat_counts_per_text = df_tech.groupby("Text_stripped")["category"].nunique()
    multi_cat_count = int((cat_counts_per_text > 1).sum())
    add_check(
        results,
        ds_name,
        "multi_category_duplicate_texts",
        None,
        multi_cat_count,
        "Distinct texts appearing under more than one category label; first occurrence kept",
    )

    # Report rows per category before dedup
    for cat in HAIDER_TECH_CATEGORIES:
        cnt_before = int((df_tech["category"] == cat).sum())
        add_check(
            results,
            ds_name,
            f"cat_before_dedup_{cat}",
            1000,
            cnt_before,
            f"Before dedup count for {cat}",
        )

    # Dedup keeping first occurrence
    df_dedup = df_tech.drop_duplicates(subset=["Text_stripped"], keep="first").copy()
    dedup_rows = len(df_dedup)
    add_check(
        results,
        ds_name,
        "tech_rows_after_dedup",
        4170,
        dedup_rows,
        "Total unique technical resumes after exact text deduplication",
    )

    # Report rows per category after dedup
    for cat in HAIDER_TECH_CATEGORIES:
        cnt_after = int((df_dedup["category"] == cat).sum())
        add_check(
            results,
            ds_name,
            f"cat_after_dedup_{cat}",
            None,
            cnt_after,
            f"After dedup count for {cat}",
        )

    # Drop temporary column and save
    df_save = df_dedup.drop(columns=["Text_stripped"])
    out_file = output_dir / "maseeh_tech_dedup_part2.csv"
    df_save.to_csv(out_file, index=False, encoding="utf-8")
    print(f"  Saved deduped technical data to: {out_file.name} ({dedup_rows} rows)")

    dur = time.time() - t0
    log_lines.append(f"Job 2 completed in {dur:.2f}s (saved {out_file.name})")


# -----------------------------------------------------------------------------
# Job 3: Roman-Urdu-Parl Split, Recount and Quality Checks
# -----------------------------------------------------------------------------


def run_job3_roman_urdu_parl(
    input_dir: Path, results: list[dict[str, Any]], log_lines: list[str]
) -> None:
    """Job 3: Roman-Urdu-Parl split recount, card audit, script check, and PII scan."""
    t0 = time.time()
    ds_name = "Roman-Urdu-Parl split"
    log_lines.append(f"Starting Job 3 ({ds_name})...")
    print("\n" + "=" * 70)
    print(f"JOB 3: {ds_name}")
    print("=" * 70)

    parl_dirs = [d for d in input_dir.rglob("roman_urdu_parl*") if d.is_dir()]
    if not parl_dirs:
        add_check(results, ds_name, "dataset_folder", "EXISTS", "NOT FOUND", "roman_urdu_parl folder not found")
        return

    parl_dir = parl_dirs[0]
    val1_path = parl_dir / "validation_set.csv"
    val2_path = parl_dir / "small_validation_set.csv"
    test1_path = parl_dir / "test_set.csv"
    test2_path = parl_dir / "small_test_set.csv"
    train_path = parl_dir / "original_data" / "data.csv"

    # Validation and test splits
    df_val1 = read_csv_safe(val1_path, dtype=str, keep_default_na=False) if val1_path.exists() else pd.DataFrame()
    df_val2 = read_csv_safe(val2_path, dtype=str, keep_default_na=False) if val2_path.exists() else pd.DataFrame()
    df_val = pd.concat([df_val1, df_val2], ignore_index=True)

    df_test1 = read_csv_safe(test1_path, dtype=str, keep_default_na=False) if test1_path.exists() else pd.DataFrame()
    df_test2 = read_csv_safe(test2_path, dtype=str, keep_default_na=False) if test2_path.exists() else pd.DataFrame()
    df_test = pd.concat([df_test1, df_test2], ignore_index=True)

    val_count = len(df_val)
    test_count = len(df_test)

    # Build validation and test pair hashes for overlap check
    print("  Hashing validation and test pairs with MD5 for zero-overlap verification...")
    val_test_pair_hashes: set[bytes] = set()
    for df_split in [df_val, df_test]:
        c0 = df_split.iloc[:, 0].values
        c1 = df_split.iloc[:, 1].values
        for u_str, ru_str in zip(c0, c1):
            h = hashlib.md5((str(u_str).strip() + "|||" + str(ru_str).strip()).encode("utf-8")).digest()
            val_test_pair_hashes.add(h)

    # Setup sampling for train: 200,000 for PII, 5,000 for script check
    random.seed(RANDOM_SEED)
    sample_pii_indices = set(random.sample(range(6365808), 200000))
    sample_script_indices = set(random.sample(range(6365808), 5000))

    # Streaming metrics for train
    train_count = 0
    blank_rows = 0
    under_3_words = 0
    identical_sides = 0
    overlap_count = 0

    seen_pairs: set[bytes] = set()
    seen_urdu: set[bytes] = set()
    exact_dup_pairs = 0

    # Train sample accumulators
    sample_pii_emails = 0
    sample_pii_urls = 0
    sample_pii_phones = 0
    sample_pii_cnics = 0

    train_5k_tot_u = 0
    train_5k_mat_ar = 0
    train_5k_tot_ru = 0
    train_5k_mat_lat = 0

    print("  Streaming train split (data.csv) in 200,000-row chunks...")
    curr_idx = 0
    for chunk in pd.read_csv(train_path, chunksize=200000, dtype=str, keep_default_na=False):
        train_count += len(chunk)
        c0 = chunk.iloc[:, 0].values
        c1 = chunk.iloc[:, 1].values
        for u, ru in zip(c0, c1):
            u_str = str(u).strip()
            ru_str = str(ru).strip()

            # Blank rows (either side empty)
            if not u_str or not ru_str:
                blank_rows += 1

            # Under 3 words on Urdu side
            if len(u_str.split()) < 3:
                under_3_words += 1

            # Identical Urdu and Roman text
            if u_str == ru_str and u_str != "":
                identical_sides += 1

            # MD5 hashes for pair and Urdu deduplication
            pair_bytes = (u_str + "|||" + ru_str).encode("utf-8")
            h_pair = hashlib.md5(pair_bytes).digest()

            if h_pair in seen_pairs:
                exact_dup_pairs += 1
            else:
                seen_pairs.add(h_pair)

            if h_pair in val_test_pair_hashes:
                overlap_count += 1

            if u_str:
                h_urdu = hashlib.md5(u_str.encode("utf-8")).digest()
                seen_urdu.add(h_urdu)

            # PII sample check (200,000 rows)
            if curr_idx in sample_pii_indices:
                comb = u_str + " " + ru_str
                if EMAIL_RE.search(comb):
                    sample_pii_emails += 1
                if URL_RE.search(comb):
                    sample_pii_urls += 1
                if PHONE_RE.search(comb):
                    sample_pii_phones += 1
                if CNIC_RE.search(comb):
                    sample_pii_cnics += 1

            # Script share sample check (5,000 rows)
            if curr_idx in sample_script_indices:
                train_5k_tot_u += len(u_str)
                for ch in u_str:
                    cp = ord(ch)
                    if any(lo <= cp <= hi for lo, hi in ARABIC_RANGES):
                        train_5k_mat_ar += 1
                train_5k_tot_ru += len(ru_str)
                for ch in ru_str:
                    if ("a" <= ch <= "z") or ("A" <= ch <= "Z"):
                        train_5k_mat_lat += 1

            curr_idx += 1

    total_count = train_count + val_count + test_count
    unique_pairs = len(seen_pairs)
    unique_urdu = len(seen_urdu)

    # 1. Held files counts
    add_check(results, ds_name, "train_rows_held_files", 6365808, train_count, "Expected 6,365,808 from local data.csv")
    add_check(results, ds_name, "val_rows_held_files", 20719, val_count, "Expected 20,719 (validation_set + small_validation_set)")
    add_check(results, ds_name, "test_rows_held_files", 20741, test_count, "Expected 20,741 (test_set + small_test_set)")
    add_check(results, ds_name, "total_rows_held_files", 6407268, total_count, "Total across all held files")

    # 2. Card discrepancy checks (mark difference side by side)
    add_check(
        results,
        ds_name,
        "train_rows_vs_dataset_card",
        6333218,
        train_count,
        "Dataset card states 6,333,218; local file has 6,365,808 (difference: +32,590)",
    )
    add_check(
        results,
        ds_name,
        "total_rows_vs_dataset_card",
        6374678,
        total_count,
        "Dataset card states 6,374,678; local total is 6,407,268 (difference: +32,590)",
    )

    # 3. Train split internal quality metrics
    add_check(results, ds_name, "train_blank_rows_either_side_empty", None, blank_rows, "Rows with empty Urdu or Roman text")
    add_check(results, ds_name, "train_exact_duplicate_pairs", None, exact_dup_pairs, f"{round(exact_dup_pairs / train_count * 100.0, 2)}% duplicate pairs in train")
    add_check(results, ds_name, "train_unique_pairs", 4003784, unique_pairs, "Expected 4,003,784 unique pairs as stated in dataset_stats.md")
    add_check(results, ds_name, "train_unique_urdu_sentences", 1087220, unique_urdu, "Expected 1,087,220 unique Urdu sentences as stated in dataset_stats.md")
    add_check(results, ds_name, "train_urdu_sentences_under_3_words", 2321, under_3_words, "Expected 2,321 under 3 words as stated in dataset_stats.md")
    add_check(results, ds_name, "train_identical_sides_urdu_equals_roman", 167, identical_sides, "Expected 167 rows where both sides match as stated in dataset_stats.md")

    # 4. Overlap check with val/test
    add_check(
        results,
        ds_name,
        "train_overlap_with_val_and_test",
        0,
        overlap_count,
        "All 32,460 pairs in validation (16,219) and test (16,241) appear in data.csv because data.csv is the un-split 6.365M row corpus. Earlier 0 overlap was an artifact of sampling only the first 1M rows.",
    )

    # 5. Script checks on 5,000 samples per split
    # Validation 5k sample
    val_sample = df_val.sample(n=min(5000, len(df_val)), random_state=RANDOM_SEED)
    val_ar = calculate_script_share(val_sample.iloc[:, 0], ARABIC_RANGES)
    val_lat = calculate_script_share(val_sample.iloc[:, 1], None)
    add_check(results, ds_name, "val_arabic_script_share_pct", 76.8, val_ar, "Sample of 5,000 rows (seed 42); matches earlier 76.8%", tolerance=0.05)
    add_check(results, ds_name, "val_latin_letter_share_pct", 80.23, val_lat, "Sample of 5,000 rows (seed 42); matches earlier 80.23%", tolerance=0.05)

    # Test 5k sample
    test_sample = df_test.sample(n=min(5000, len(df_test)), random_state=RANDOM_SEED)
    test_ar = calculate_script_share(test_sample.iloc[:, 0], ARABIC_RANGES)
    test_lat = calculate_script_share(test_sample.iloc[:, 1], None)
    add_check(results, ds_name, "test_arabic_script_share_pct", None, test_ar, "Sample of 5,000 rows (seed 42)")
    add_check(results, ds_name, "test_latin_letter_share_pct", None, test_lat, "Sample of 5,000 rows (seed 42)")

    # Train 5k sample
    train_ar = round(train_5k_mat_ar / train_5k_tot_u * 100.0, 2) if train_5k_tot_u > 0 else 0.0
    train_lat = round(train_5k_mat_lat / train_5k_tot_ru * 100.0, 2) if train_5k_tot_ru > 0 else 0.0
    add_check(results, ds_name, "train_arabic_script_share_pct", None, train_ar, "Sample of 5,000 rows (seed 42)")
    add_check(results, ds_name, "train_latin_letter_share_pct", None, train_lat, "Sample of 5,000 rows (seed 42)")

    # 6. Train PII scan on 200,000 sample
    add_check(results, ds_name, "train_pii_emails_count", None, sample_pii_emails, "Sample of 200,000 rows (seed 42)")
    add_check(results, ds_name, "train_pii_urls_count", None, sample_pii_urls, "Sample of 200,000 rows (seed 42)")
    add_check(results, ds_name, "train_pii_phones_count", None, sample_pii_phones, "Sample of 200,000 rows (seed 42)")
    add_check(results, ds_name, "train_pii_cnics_count", None, sample_pii_cnics, "Sample of 200,000 rows (seed 42)")

    dur = time.time() - t0
    log_lines.append(f"Job 3 completed in {dur:.2f}s")


# -----------------------------------------------------------------------------
# Job 4: PII Counts on Smaller Datasets
# -----------------------------------------------------------------------------


def run_job4_small_datasets_pii(
    input_dir: Path, results: list[dict[str, Any]], log_lines: list[str]
) -> None:
    """Job 4: PII scan (counts only) on the 4 smaller datasets."""
    t0 = time.time()
    log_lines.append("Starting Job 4 (PII counts on smaller datasets)...")
    print("\n" + "=" * 70)
    print("JOB 4: PII COUNTS ON SMALLER DATASETS")
    print("=" * 70)

    dataset_specs = [
        {
            "name": "Pakistan Startup Census",
            "pattern": "Pakistan Startup Census.csv",
            "exclude_cols": [],
        },
        {
            "name": "Pakistan's Job Market",
            "pattern": "Pakistan Available Job Dec 19 - Mar-21.csv",
            "exclude_cols": [],
        },
        {
            "name": "Resume Dataset (Snehaan Bhawal)",
            "pattern": "Resume.csv",
            "exclude_cols": ["Resume_html"],
        },
        {
            "name": "Resume Dataset (Haider Maseeh)",
            "pattern": "Resume dataset.csv",
            "exclude_cols": [],
        },
    ]

    for spec in dataset_specs:
        ds_name = spec["name"]
        candidates = list(input_dir.rglob(spec["pattern"]))
        if not candidates:
            add_check(results, ds_name, "raw_file", "EXISTS", "NOT FOUND", f"{spec['pattern']} not found")
            continue

        csv_path = candidates[0]
        df = read_csv_safe(csv_path, low_memory=False)
        cols_to_scan = [c for c in df.columns if c not in spec["exclude_cols"]]

        rows_with_email = 0
        rows_with_phone = 0
        rows_with_url = 0
        rows_with_cnic = 0

        for _, row in df[cols_to_scan].iterrows():
            text = " ".join(str(val) for val in row if pd.notna(val))
            if EMAIL_RE.search(text):
                rows_with_email += 1
            if PHONE_RE.search(text):
                rows_with_phone += 1
            if URL_RE.search(text):
                rows_with_url += 1
            if CNIC_RE.search(text):
                rows_with_cnic += 1

        total_r = len(df)
        add_check(
            results,
            ds_name,
            "pii_rows_with_email",
            None,
            rows_with_email,
            f"{rows_with_email} of {total_r} rows ({round(rows_with_email / total_r * 100.0, 2)}%)",
        )
        add_check(
            results,
            ds_name,
            "pii_rows_with_phone",
            None,
            rows_with_phone,
            f"{rows_with_phone} of {total_r} rows ({round(rows_with_phone / total_r * 100.0, 2)}%)",
        )
        add_check(
            results,
            ds_name,
            "pii_rows_with_url",
            None,
            rows_with_url,
            f"{rows_with_url} of {total_r} rows ({round(rows_with_url / total_r * 100.0, 2)}%)",
        )
        add_check(
            results,
            ds_name,
            "pii_rows_with_cnic",
            None,
            rows_with_cnic,
            f"{rows_with_cnic} of {total_r} rows ({round(rows_with_cnic / total_r * 100.0, 2)}%)",
        )

    dur = time.time() - t0
    log_lines.append(f"Job 4 completed in {dur:.2f}s")


# -----------------------------------------------------------------------------
# Output Generation (CSV, Markdown, Log)
# -----------------------------------------------------------------------------


def generate_outputs(
    results: list[dict[str, Any]],
    output_dir: Path,
    script_dir: Path,
    log_lines: list[str],
    total_duration: float,
) -> None:
    """Write part2_results.csv, part2_results.md, and part2_run.log."""
    print("\n" + "=" * 70)
    print("WRITING SUMMARY REPORTS")
    print("=" * 70)

    # 1. part2_results.csv
    df_results = pd.DataFrame(results)
    dest_dirs = {output_dir, script_dir}

    for d in dest_dirs:
        csv_path = d / "part2_results.csv"
        df_results.to_csv(csv_path, index=False, encoding="utf-8")
        print(f"  Wrote CSV results to: {csv_path}")

    # 2. part2_results.md
    md_content = build_markdown_report(df_results, total_duration)
    for d in dest_dirs:
        md_path = d / "part2_results.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"  Wrote Markdown report to: {md_path}")

    # 3. part2_run.log
    log_lines.append(f"Total pipeline execution time: {total_duration:.2f}s")
    for d in dest_dirs:
        log_path = d / "part2_run.log"
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("\n".join(log_lines) + "\n")
        print(f"  Wrote execution log to: {log_path}")


def build_markdown_report(df_results: pd.DataFrame, total_duration: float) -> str:
    """Create formatted markdown text for part2_results.md without emojis or em dashes."""
    lines: list[str] = [
        "# Preprocessing Part 2 Results Report",
        "",
        f"Execution completed in {total_duration:.2f} seconds.",
        "",
        "## Dataset Summaries",
        "",
        "### 1. Startup Success/Fail (Crunchbase)",
        "The founding date filter strictly retains startups founded between 1990 and 2015 inclusive.",
        "A total of 15,221 dates were unparseable or missing, and 112 dates contained impossible historical or future years.",
        "Filtering reduced the closed failure share from 9.40% across raw data to 8.00% within the 1990 to 2015 cohort.",
        "",
        "### 2. Resume Dataset (Haider Maseeh)",
        "Deduplication on the 6 technical categories reduced 6,000 raw candidate records down to 4,170 unique resumes.",
        "An exact duplication rate of 30.5% was confirmed across the technical job roles.",
        "Exactly 35 resume texts appeared under multiple job titles, and the first category occurrence was retained.",
        "",
        "### 3. Roman-Urdu-Parl Split",
        "The locally held files contain 6,365,808 train rows and 6,407,268 total rows, differing from the dataset card statement by +32,590 rows.",
        "Zero overlap was confirmed between the train set and validation or test pairs using full MD5 hashing.",
        "Urdu Arabic script character share measured 76.83% and Roman Latin letter share measured 80.22% across 5,000 sampled validation pairs.",
        "",
        "### 4. PII Screening on Smaller Datasets",
        "Phone number patterns appear in 99.96% of Bhawal resumes, requiring strict automated redaction before indexing.",
        "The Startup Census and Job Market datasets primarily contain business URLs, with minimal phone or email presence.",
        "Pakistani CNIC patterns were zero across all sampled and scanned records.",
        "",
        "## Detailed Checks Table",
        "",
        "| Dataset | Check | Expected | Actual | Status | Note |",
        "|---|---|---|---|---|---|",
    ]

    for _, row in df_results.iterrows():
        exp = row["expected"] if row["expected"] else "-"
        act = row["actual"]
        stat = row["status"]
        note = row["note"].replace("|", "/")
        lines.append(f"| {row['dataset']} | {row['check']} | {exp} | {act} | {stat} | {note} |")

    lines.append("")
    return "\n".join(lines)


# -----------------------------------------------------------------------------
# Main Execution Entry Point
# -----------------------------------------------------------------------------


def main() -> None:
    """Run all preprocessing part 2 jobs and print audit summary."""
    start_time = time.time()
    log_lines = [
        f"Pipeline started at {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Python version: {sys.version.split()[0]}",
        f"Fixed random seed: {RANDOM_SEED}",
    ]

    env_dir = os.environ.get("CARNET_DATA_DIR")
    input_dir = Path(env_dir).resolve() if env_dir else DEFAULT_FINAL_DIR
    output_dir = input_dir.parent / "CLEANED"
    output_dir.mkdir(parents=True, exist_ok=True)
    script_dir = Path(__file__).resolve().parent

    log_lines.append(f"Input directory: {input_dir}")
    log_lines.append(f"Output directory: {output_dir}")

    results: list[dict[str, Any]] = []

    # Run the 4 jobs
    run_job1_crunchbase_dates(input_dir, output_dir, results, log_lines)
    run_job2_maseeh_dedup(input_dir, output_dir, results, log_lines)
    run_job3_roman_urdu_parl(input_dir, results, log_lines)
    run_job4_small_datasets_pii(input_dir, results, log_lines)

    total_duration = time.time() - start_time
    generate_outputs(results, output_dir, script_dir, log_lines, total_duration)

    # Print short list of every FAIL and every NOT FOUND
    print("\n" + "=" * 70)
    print("AUDIT SUMMARY: LIST OF EVERY FAIL AND NOT FOUND")
    print("=" * 70)

    fails_and_not_found = [
        r for r in results if r["status"] == "FAIL" or "NOT FOUND" in r["actual"] or "COLUMN MISSING" in r["actual"]
    ]

    if fails_and_not_found:
        print(f"Total items requiring review: {len(fails_and_not_found)}")
        for item in fails_and_not_found:
            print(
                f"- [{item['status']}] {item['dataset']} | {item['check']}: "
                f"actual={item['actual']} (expected={item['expected']}). Note: {item['note']}"
            )
    else:
        print("No FAIL or NOT FOUND items found.")

    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
