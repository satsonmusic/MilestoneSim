import csv
import argparse
import random
import json
from dataclasses import dataclass
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

DATE_FMT = "%Y-%m-%d"

def _lab_root() -> Path:
    """Portable: Uses the folder where the script is located."""
    return Path(__file__).parent.resolve()

def _resolve_io_path(p: str) -> Path:
    path = Path(p)
    if path.is_absolute():
        return path
    return (_lab_root() / path).resolve()

@dataclass
class Task:
    id: str
    program: str
    name: str
    owner: str
    depends_on: List[str]
    min_days: float
    ml_days: float  # most likely
    max_days: float

def parse_date(s: str) -> Optional[date]:
    s = (s or "").strip()
    return datetime.strptime(s, DATE_FMT).date() if s else None

def load_tasks(path: Path) -> Dict[str, Task]:
    if not path.exists():
        raise FileNotFoundError(f"Missing tasks file: {path}")
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        tasks: Dict[str, Task] = {}
        for r in reader:
            tid = (r.get("id") or "").strip()
            tasks[tid] = Task(
                id=tid,
                program=r.get("program", "").strip(),
                name=r.get("name", "").strip(),
                owner=r.get("owner", "").strip(),
                depends_on=[p.strip() for p in (r.get("depends_on") or "").split(",") if p.strip()],
                min_days=float(r.get("min_days") or 0),
                ml_days=float(r.get("ml_days") or 0),
                max_days=float(r.get("max_days") or 0),
            )
    return tasks

def topo_sort(tasks: Dict[str, Task]) -> List[str]:
    """Kahn's algorithm for dependency ordering."""
    in_degree = {tid: 0 for tid in tasks}
    for t in tasks.values():
        for dep in t.depends_on:
            in_degree[t.id] += 1
    
    queue = [tid for tid, deg in in_degree.items() if deg == 0]
    order = []
    while queue:
        u = queue.pop(0)
        order.append(u)
        for tid, t in tasks.items():
            if u in t.depends_on:
                in_degree[tid] -= 1
                if in_degree[tid] == 0:
                    queue.append(tid)
    
    if len(order) != len(tasks):
        raise ValueError("Circular dependency detected in tasks.csv")
    return order

def simulate_once(tasks: Dict[str, Task], order: List[str]) -> Tuple[float, List[str]]:
    finish_times: Dict[str, float] = {}
    crit_pred: Dict[str, Optional[str]] = {}

    for tid in order:
        t = tasks[tid]
        dur = random.triangular(t.min_days, t.max_days, t.ml_days)
        if not t.depends_on:
            start = 0.0
            crit_pred[tid] = None
        else:
            pred = max(t.depends_on, key=lambda p: finish_times[p])
            start = finish_times[pred]
            crit_pred[tid] = pred
        finish_times[tid] = start + dur

    end_task = max(order, key=lambda tid: finish_times[tid])
    
    # Trace critical path
    path, cur = [], end_task
    while cur:
        path.append(cur)
        cur = crit_pred[cur]
    
    return finish_times[end_task], path

def percentile(xs: List[float], p: float) -> float:
    xs_sorted = sorted(xs)
    return xs_sorted[int(len(xs_sorted) * p)]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--tasks", default="tasks.csv")
    p.add_argument("--runs", type=int, default=5000)
    args = p.parse_args()

    tasks = load_tasks(_resolve_io_path(args.tasks))
    order = topo_sort(tasks)
    
    results, paths = [], []
    for _ in range(args.runs):
        days, path = simulate_once(tasks, order)
        results.append(days)
        paths.append(path)

    p50, p80, p90 = percentile(results, 0.5), percentile(results, 0.8), percentile(results, 0.9)
    
    # Calculate frequency of tasks on critical path
    counts = {}
    for path in paths:
        for tid in path:
            counts[tid] = counts.get(tid, 0) + 1
    
    # SORT BY VALUE (frequency), not key
    sorted_drivers = sorted(counts.items(), key=lambda x: x, reverse=True)

    print(f"--- SIMULATION COMPLETE ({args.runs} runs) ---")
    print(f"P50 (Median): {p50:.1f} days")
    print(f"P80 (Confidence): {p80:.1f} days")
    print(f"Top Risk Driver: {sorted_drivers} ({tasks[sorted_drivers].name})")

if __name__ == "__main__":
    main()