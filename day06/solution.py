from heapq import heapify, heappop, heappush


def _schedule_tasks(deps):
    """Return the scheduled tasks and the total number of tasks."""
    remaining = dict.fromkeys(deps, 0)
    dependents = {task: [] for task in deps}

    for task, prerequisites in deps.items():
        for prerequisite in prerequisites:
            # Include prerequisites that appear only in a dependency list.
            remaining.setdefault(prerequisite, 0)
            dependents.setdefault(prerequisite, []).append(task)
            remaining[task] += 1

    ready = [task for task, count in remaining.items() if count == 0]
    heapify(ready)

    order = []
    while ready:
        task = heappop(ready)
        order.append(task)

        for dependent in dependents[task]:
            remaining[dependent] -= 1
            if remaining[dependent] == 0:
                heappush(ready, dependent)

    return order, len(remaining)


def has_cycle(deps):
    """Return True if the dependency graph contains a cycle."""
    order, total_tasks = _schedule_tasks(deps)
    return len(order) < total_tasks


def topological_order(deps):
    """Return the lexicographically smallest valid order, or [] on a cycle."""
    order, total_tasks = _schedule_tasks(deps)
    if len(order) < total_tasks:
        return []
    return order


def count_retries(runs):
    """Count all attempts after the first attempt of each run."""
    return sum(max(0, run["attempts"] - 1) for run in runs)


if __name__ == "__main__":
    deps = {
        "score": ["enrich"],
        "enrich": ["ingest"],
        "ingest": [],
        "notify": ["score"],
    }
    cyclic_deps = {"a": ["b"], "b": ["a"]}
    runs = [
        {"task": "ingest", "attempts": 3},
        {"task": "score", "attempts": 1},
    ]

    print(topological_order(deps))
    print(has_cycle(cyclic_deps))
    print(count_retries(runs))
