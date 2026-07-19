"""
threading_utils.py — Concurrent report generation (U3).

Generates skill-gap reports for multiple employees simultaneously using
Python's threading module. Results are collected in a thread-safe list
protected by a Lock.
"""
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List

from hr.skill_matcher import analyze_employee, SkillGap, SkillGapError


def _analyze_one(employee_mongo_id: str, results: list, lock: threading.Lock, role_name: str = None):
    """Worker function executed in a thread."""
    try:
        gap = analyze_employee(employee_mongo_id, role_name)
        with lock:
            results.append(gap)
    except SkillGapError as exc:
        with lock:
            results.append({
                'employee_id': employee_mongo_id,
                'error': str(exc),
            })


def generate_reports_threaded(employee_ids: List[str], role_name: str = None, max_workers: int = 4) -> List:
    """
    Generate SkillGap reports for many employees concurrently.

    Returns a list whose items are either SkillGap objects or dicts with an
    'error' key for employees whose analysis failed.
    """
    results: List = []
    lock = threading.Lock()
    threads = []
    for eid in employee_ids:
        t = threading.Thread(
            target=_analyze_one,
            args=(eid, results, lock, role_name),
            daemon=True,
        )
        threads.append(t)
        t.start()
        # Simple bounded concurrency: avoid spawning too many threads at once.
        if len(threads) >= max_workers:
            for t in threads:
                t.join()
            threads = []
    for t in threads:
        t.join()
    return results


def generate_reports_executor(employee_ids: List[str], role_name: str = None, max_workers: int = 4) -> List:
    """
    Same as generate_reports_threaded but using ThreadPoolExecutor for a
    cleaner futures-based API.
    """
    results: List = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {
            executor.submit(analyze_employee, eid, role_name): eid for eid in employee_ids
        }
        for future in as_completed(future_map):
            eid = future_map[future]
            try:
                results.append(future.result())
            except SkillGapError as exc:
                results.append({'employee_id': eid, 'error': str(exc)})
    return results


def generate_reports_for_all(role_name: str = None, max_workers: int = 4) -> List:
    """Generate reports for every employee in the database."""
    from hr import mongo
    docs = mongo.all_employees()
    ids = [doc['_id'] for doc in docs]
    return generate_reports_threaded(ids, role_name=role_name, max_workers=max_workers)
