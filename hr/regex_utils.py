"""
regex_utils.py — Skill normalization helpers.

Cleans and normalizes skill strings so that "python", "PYTHON", "Python "
and "  Python " all collapse to the canonical "Python".
"""
import re

# Common skill aliases mapped to their canonical form.
SKILL_ALIASES = {
    'py': 'Python',
    'python3': 'Python',
    'django': 'Django',
    'flask': 'Flask',
    'js': 'JavaScript',
    'javascript': 'JavaScript',
    'node': 'Node.js',
    'nodejs': 'Node.js',
    'ts': 'TypeScript',
    'typescript': 'TypeScript',
    'sql': 'SQL',
    'mysql': 'MySQL',
    'postgres': 'PostgreSQL',
    'postgresql': 'PostgreSQL',
    'mongo': 'MongoDB',
    'mongodb': 'MongoDB',
    'html5': 'HTML',
    'html': 'HTML',
    'css3': 'CSS',
    'css': 'CSS',
    'react': 'React',
    'reactjs': 'React',
    'vue': 'Vue.js',
    'vuejs': 'Vue.js',
    'angular': 'Angular',
    'aws': 'AWS',
    'gcp': 'GCP',
    'azure': 'Azure',
    'docker': 'Docker',
    'kubernetes': 'Kubernetes',
    'k8s': 'Kubernetes',
    'git': 'Git',
    'github': 'Git',
    'rest': 'REST API',
    'restapi': 'REST API',
    'api': 'REST API',
    'pandas': 'Pandas',
    'numpy': 'NumPy',
    'ml': 'Machine Learning',
    'ai': 'Artificial Intelligence',
    'dl': 'Deep Learning',
    'nlp': 'NLP',
    'tableau': 'Tableau',
    'powerbi': 'Power BI',
    'excel': 'Excel',
    'communication': 'Communication',
    'leadership': 'Leadership',
    'agile': 'Agile',
    'scrum': 'Scrum',
    'devops': 'DevOps',
    'ci/cd': 'CI/CD',
    'cicd': 'CI/CD',
}

# Split on commas, semicolons, pipes, "and", slashes, plus whitespace runs.
_SPLIT_RE = re.compile(r'\s*(?:,|;|\||/|\band\b|\+|\n)\s*')


def normalize_skill(skill):
    """Normalize a single skill token to its canonical form."""
    if not skill:
        return ''
    cleaned = skill.strip()
    # Collapse internal whitespace to a single space.
    cleaned = re.sub(r'\s+', ' ', cleaned)
    key = cleaned.lower()
    if key in SKILL_ALIASES:
        return SKILL_ALIASES[key]
    # Title-case unknown skills (e.g. "data analysis" -> "Data Analysis").
    return cleaned.title()


def parse_skills(raw):
    """Parse a comma/slash separated skill string into a list of normalized skills."""
    if not raw:
        return []
    if isinstance(raw, (list, tuple, set)):
        tokens = []
        for item in raw:
            tokens.extend(_SPLIT_RE.split(str(item)))
    else:
        tokens = _SPLIT_RE.split(str(raw))
    # List comprehension: normalize, drop empties, de-duplicate preserving order.
    seen = set()
    normalized = []
    for token in tokens:
        skill = normalize_skill(token)
        if skill and skill.lower() not in seen:
            seen.add(skill.lower())
            normalized.append(skill)
    return normalized


def normalize_skills_list(skills):
    """Normalize an already-split list/set of skills (alias for parse_skills)."""
    return parse_skills(skills)
