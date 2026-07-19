
from dataclasses import dataclass, field
from typing import Dict, List, Set

from hr import mongo
from hr.regex_utils import normalize_skills_list


# --------------------------------------------------------------- exceptions
class SkillGapError(Exception):
    """Base error for the skill matcher module."""

class RoleNotFoundError(SkillGapError):
    """Raised when a required role cannot be located in the database."""

class EmployeeNotFoundError(SkillGapError):
    """Raised when an employee cannot be located in the database."""


# -------------------------------------------------------------------- models
@dataclass
class Employee:
    employee_id: str
    name: str
    email: str
    department: str
    role: str
    skills: List[str] = field(default_factory=list)
    id: str = ''

    @classmethod
    def from_dict(cls, data: Dict) -> 'Employee':
        return cls(
            employee_id=data.get('employee_id', ''),
            name=data.get('name', ''),
            email=data.get('email', ''),
            department=data.get('department', ''),
            role=data.get('role', ''),
            skills=normalize_skills_list(data.get('skills', [])),
            id=str(data.get('_id', '')),
        )

    @property
    def skill_set(self) -> Set[str]:
        return {s.lower() for s in self.skills}


@dataclass
class Role:
    role: str
    required_skills: List[str] = field(default_factory=list)
    id: str = ''

    @classmethod
    def from_dict(cls, data: Dict) -> 'Role':
        return cls(
            role=data.get('role', ''),
            required_skills=normalize_skills_list(data.get('required_skills', [])),
            id=str(data.get('_id', '')),
        )

    @property
    def required_skill_set(self) -> Set[str]:
        return {s.lower() for s in self.required_skills}


@dataclass
class SkillGap:
    employee: Employee
    role: Role
    matched_skills: List[str]
    missing_skills: List[str]
    completion_percentage: float

    def to_dict(self) -> Dict:
        return {
            'employee': {
                'employee_id': self.employee.employee_id,
                'name': self.employee.name,
                'email': self.employee.email,
                'department': self.employee.department,
                'role': self.employee.role,
                'skills': self.employee.skills,
                'id': self.employee.id,
            },
            'role': {
                'role': self.role.role,
                'required_skills': self.role.required_skills,
            },
            'current_skills': self.employee.skills,
            'required_skills': self.role.required_skills,
            'matched_skills': self.matched_skills,
            'missing_skills': self.missing_skills,
            'completion_percentage': round(self.completion_percentage, 2),
        }


# --------------------------------------------------------------- core logic
def load_employee(employee_mongo_id: str) -> Employee:
    data = mongo.find_employee_by_id(employee_mongo_id)
    if not data:
        raise EmployeeNotFoundError(f"Employee with id '{employee_mongo_id}' not found.")
    return Employee.from_dict(data)


def load_role_by_name(role_name: str) -> Role:
    data = mongo.find_role_by_name(role_name)
    if not data:
        raise RoleNotFoundError(f"Role '{role_name}' not found in the roles collection.")
    return Role.from_dict(data)


def compute_gap(employee: Employee, role: Role) -> SkillGap:
    current_set = employee.skill_set
    required_set = role.required_skill_set

    if not required_set:
        matched_lower = set()
        completion = 100.0
    else:
        matched_lower = current_set & required_set
        completion = (len(matched_lower) / len(required_set)) * 100.0

    missing_lower = required_set - current_set

    required_display = {s.lower(): s for s in role.required_skills}
    current_display = {s.lower(): s for s in employee.skills}
    display = {**required_display, **current_display}

    matched_skills = [display[s] for s in matched_lower if s in display]
    missing_skills = [display[s] for s in missing_lower if s in display]

    matched_ordered = [s for s in role.required_skills if s.lower() in matched_lower]
    missing_ordered = [s for s in role.required_skills if s.lower() in missing_lower]
    if matched_ordered:
        matched_skills = matched_ordered
    if missing_ordered:
        missing_skills = missing_ordered

    return SkillGap(
        employee=employee,
        role=role,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        completion_percentage=completion,
    )


def analyze_employee(employee_mongo_id: str, role_name: str = None) -> SkillGap:
    
    employee = load_employee(employee_mongo_id)
    target_role = role_name or employee.role
    if not target_role:
        raise RoleNotFoundError("Employee has no role assigned and none was provided.")
    role = load_role_by_name(target_role)
    return compute_gap(employee, role)


def analyze_employees_batch(employee_ids: List[str], role_name: str = None) -> List[SkillGap]:
   
    results = []
    for eid in employee_ids:
        try:
            results.append(analyze_employee(eid, role_name))
        except SkillGapError as exc:
            # Skip employees whose role/lookup failed; caller can inspect logs.
            results.append(SkillGap(
                employee=Employee(employee_id=eid, name='', email='', department='', role=''),
                role=Role(role=''),
                matched_skills=[],
                missing_skills=[],
                completion_percentage=0.0,
            ))
    return results


def employees_with_gaps() -> int:
    
    count = 0
    for doc in mongo.all_employees():
        try:
            employee = Employee.from_dict(doc)
            if not employee.role:
                continue
            role = load_role_by_name(employee.role)
            gap = compute_gap(employee, role)
            if gap.missing_skills:
                count += 1
        except SkillGapError:
            continue
    return count
