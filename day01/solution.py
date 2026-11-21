def score_backlog(items):
    """Score backlog items by value/effort, best score first.

    Items with zero or negative effort are skipped. Ties are broken by id
    ascending.
    """
    scored = []
    for item in items:
        effort = item["effort"]
        if effort <= 0:
            continue
        scored.append((item["id"], round(item["value"] / effort, 2)))

    return sorted(scored, key=lambda entry: (-entry[1], entry[0]))


def validate_user_story(story):
    """Return True when a story follows the user-story template."""
    if not isinstance(story, str) or not story.strip():
        return False
    if not story.startswith("As a "):
        return False

    role, separator, remainder = story[len("As a "):].partition(", I want ")
    if not separator:
        return False

    goal, separator, benefit = remainder.partition(", so that ")
    if not separator:
        return False

    return bool(role.strip() and goal.strip() and benefit.strip())
