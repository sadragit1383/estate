import json
from typing import Optional, List

def parse_location_slugs(raw_slugs: str) -> Optional[List[str]]:
    """
    Parse location slugs from JSON string.
    Expected format: [province_slug, city1_slug, city2_slug, ...]
    Must have at least 1 element (province), can have multiple cities.
    """
    try:
        slugs = json.loads(raw_slugs)
        # Check if it's a list with at least 1 element (province) and all elements are strings
        if isinstance(slugs, list) and len(slugs) >= 1 and all(isinstance(s, str) for s in slugs):
            return slugs
    except json.JSONDecodeError:
        pass
    return None