"""
course_recommender.py — Training recommendation engine (U2).

Given a SkillGap, recommends courses from MongoDB that cover the missing
skills. Uses dictionaries and list comprehensions to build recommendation
cards.
"""
from typing import Dict, List

from hr import mongo
from hr.skill_matcher import SkillGap


class RecommendationError(Exception):
    """Raised when recommendations cannot be generated."""


# Difficulty ordering used to sort recommendations (easier first).
DIFFICULTY_ORDER = {
    'beginner': 1,
    'intermediate': 2,
    'advanced': 3,
    'expert': 4,
}


def _difficulty_rank(level: str) -> int:
    return DIFFICULTY_ORDER.get((level or '').lower(), 99)


def recommend_courses(missing_skills: List[str]) -> List[Dict]:
    """
    Return recommended course dicts covering any of the missing skills.
    Each dict is enriched with `matched_skill` (the missing skill it covers).
    """
    if not missing_skills:
        return []

    # Normalize for matching.
    normalized = [s.lower() for s in missing_skills]
    courses = mongo.find_courses_for_skills(normalized)

    # Build a lookup: normalized skill -> display skill.
    skill_display = {s.lower(): s for s in missing_skills}

    recommendations = []
    seen_course_ids = set()
    for course in courses:
        cid = course.get('_id')
        if cid in seen_course_ids:
            continue
        course_skill_lower = (course.get('skill') or '').lower()
        if course_skill_lower in normalized:
            course = dict(course)
            course['matched_skill'] = skill_display.get(course_skill_lower, course.get('skill'))
            recommendations.append(course)
            seen_course_ids.add(cid)

    # Sort by difficulty (easier first) then by course name.
    recommendations.sort(key=lambda c: (_difficulty_rank(c.get('level', '')), c.get('course_name', '')))
    return recommendations


def recommend_for_gap(gap: SkillGap) -> List[Dict]:
    """Convenience wrapper: recommend courses for a SkillGap object."""
    return recommend_courses(gap.missing_skills)


def recommend_for_employee(employee_mongo_id: str) -> List[Dict]:
    """Analyze an employee then recommend courses for their missing skills."""
    from hr.skill_matcher import analyze_employee
    try:
        gap = analyze_employee(employee_mongo_id)
    except Exception as exc:
        raise RecommendationError(f"Could not analyze employee '{employee_mongo_id}': {exc}") from exc
    return recommend_for_gap(gap)
