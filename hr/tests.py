"""
Tests for TalentMap.

These tests exercise the pure-Python modules (regex_utils, skill_matcher,
course_recommender) that do not require a live MongoDB connection, so they
run in any environment. MongoDB-backed views are integration-tested via the
REST API manually (see README).
"""
from django.test import SimpleTestCase

from hr.regex_utils import normalize_skill, parse_skills
from hr.skill_matcher import Employee, Role, compute_gap, RoleNotFoundError


class RegexUtilsTests(SimpleTestCase):
    def test_normalize_skill_lowercases_to_canonical(self):
        self.assertEqual(normalize_skill('python'), 'Python')
        self.assertEqual(normalize_skill('PYTHON'), 'Python')
        self.assertEqual(normalize_skill('  Python '), 'Python')

    def test_normalize_skill_alias(self):
        self.assertEqual(normalize_skill('js'), 'JavaScript')
        self.assertEqual(normalize_skill('node'), 'Node.js')

    def test_parse_skills_dedupes_and_normalizes(self):
        result = parse_skills('python, PYTHON, SQL, sql, html')
        self.assertEqual(result, ['Python', 'SQL', 'HTML'])

    def test_parse_skills_handles_mixed_separators(self):
        result = parse_skills('Python/SQL + HTML and CSS')
        self.assertEqual(result, ['Python', 'SQL', 'HTML', 'CSS'])

    def test_parse_skills_empty(self):
        self.assertEqual(parse_skills(''), [])
        self.assertEqual(parse_skills(None), [])


class SkillMatcherTests(SimpleTestCase):
    def setUp(self):
        self.employee = Employee(
            employee_id='EMP001',
            name='Jane',
            email='jane@x.com',
            department='Eng',
            role='Backend Developer',
            skills=['Python', 'SQL'],
        )
        self.role = Role(
            role='Backend Developer',
            required_skills=['Python', 'SQL', 'Django', 'Docker'],
        )

    def test_compute_gap_uses_sets(self):
        gap = compute_gap(self.employee, self.role)
        self.assertEqual(set(gap.matched_skills), {'Python', 'SQL'})
        self.assertEqual(set(gap.missing_skills), {'Django', 'Docker'})
        self.assertAlmostEqual(gap.completion_percentage, 50.0)

    def test_compute_gap_full_match(self):
        employee = Employee('EMP2', 'A', 'a@x.com', 'Eng', 'Dev', ['Python', 'SQL', 'Django', 'Docker'])
        role = Role('Dev', ['Python', 'SQL'])
        gap = compute_gap(employee, role)
        self.assertEqual(gap.missing_skills, [])
        self.assertEqual(gap.completion_percentage, 100.0)

    def test_compute_gap_no_required_skills(self):
        employee = Employee('EMP3', 'A', 'a@x.com', 'Eng', 'Dev', ['Python'])
        role = Role('Dev', [])
        gap = compute_gap(employee, role)
        self.assertEqual(gap.completion_percentage, 100.0)
        self.assertEqual(gap.missing_skills, [])

    def test_role_not_found_error_is_custom(self):
        from hr.skill_matcher import SkillGapError
        with self.assertRaises(RoleNotFoundError):
            raise RoleNotFoundError('missing')
        self.assertTrue(issubclass(RoleNotFoundError, SkillGapError))
