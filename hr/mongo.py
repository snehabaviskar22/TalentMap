"""
MongoDB integration layer for TalentMap (U4).

Centralizes all PyMongo access. Collections:
  - employees
  - roles
  - courses
"""
from datetime import datetime, timezone

from django.conf import settings
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import PyMongoError


# A single client is reused across requests (PyMongo is thread-safe).
_client = None
_db = None


def _get_db():
    """Return the TalentMap Mongo database handle (lazy singleton)."""
    global _client, _db
    if _db is None:
        _client = MongoClient(settings.MONGO_URI)
        _db = _client[settings.MONGO_DB_NAME]
    return _db


def _oid(doc_id):
    """Convert a string id to ObjectId, returning None on invalid input."""
    from bson.objectid import ObjectId
    try:
        return ObjectId(doc_id)
    except Exception:
        return None


# ---------------------------------------------------------------- employees
def insert_employee(employee_dict):
    """Insert an employee document. Returns the inserted id as a string."""
    db = _get_db()
    doc = dict(employee_dict)
    doc.setdefault('created_at', datetime.now(timezone.utc))
    result = db['employees'].insert_one(doc)
    return str(result.inserted_id)


def find_employee_by_id(employee_id):
    """Fetch a single employee by its Mongo _id. Returns a plain dict or None."""
    db = _get_db()
    oid = _oid(employee_id)
    if oid is None:
        return None
    doc = db['employees'].find_one({'_id': oid})
    if doc:
        doc['id'] = str(doc['_id'])
    return doc


def find_employee_by_employee_code(employee_code):
    """Find an employee by the business `employee_id` field (e.g. EMP001)."""
    db = _get_db()
    doc = db['employees'].find_one({'employee_id': employee_code})
    if doc:
        doc['id'] = str(doc['_id'])
    return doc


def list_employees(search='', department='', role='', page=1, per_page=10):
    """List employees with optional search, filters and pagination."""
    db = _get_db()
    query = {}
    if search:
        query['$or'] = [
            {'name': {'$regex': search, '$options': 'i'}},
            {'employee_id': {'$regex': search, '$options': 'i'}},
            {'email': {'$regex': search, '$options': 'i'}},
        ]
    if department:
        query['department'] = department
    if role:
        query['role'] = role

    total = db['employees'].count_documents(query)
    skip = (page - 1) * per_page
    cursor = db['employees'].find(query).sort('created_at', DESCENDING).skip(skip).limit(per_page)
    items = []
    for doc in cursor:
        doc['id'] = str(doc['_id'])
        items.append(doc)
    return items, total


def all_employees():
    """Return every employee document (used for threaded reports)."""
    db = _get_db()
    docs = []
    for doc in db['employees'].find().sort('created_at', DESCENDING):
        doc['id'] = str(doc['_id'])
        docs.append(doc)
    return docs


def update_employee(employee_id, update_fields):
    """Update an employee document by _id. Returns True if a doc was matched."""
    db = _get_db()
    oid = _oid(employee_id)
    if oid is None:
        return False
    result = db['employees'].update_one({'_id': oid}, {'$set': update_fields})
    return result.matched_count > 0


def delete_employee(employee_id):
    """Delete an employee by _id. Returns True if a document was deleted."""
    db = _get_db()
    oid = _oid(employee_id)
    if oid is None:
        return False
    result = db['employees'].delete_one({'_id': oid})
    return result.deleted_count > 0


def count_employees():
    return _get_db()['employees'].count_documents({})


def departments_list():
    """Distinct departments currently in use across employees."""
    return sorted([d for d in _get_db()['employees'].distinct('department') if d])


# --------------------------------------------------------------------- roles
def insert_role(role_dict):
    db = _get_db()
    doc = dict(role_dict)
    doc.setdefault('created_at', datetime.now(timezone.utc))
    return str(db['roles'].insert_one(doc).inserted_id)


def find_role_by_id(role_id):
    db = _get_db()
    oid = _oid(role_id)
    if oid is None:
        return None
    doc = db['roles'].find_one({'_id': oid})
    if doc:
        doc['id'] = str(doc['_id'])
    return doc


def find_role_by_name(role_name):
    """Role lookup used by the skill matcher. Case-insensitive exact match."""
    db = _get_db()
    doc = db['roles'].find_one({'role': {'$regex': f'^{role_name}$', '$options': 'i'}})
    if doc:
        doc['id'] = str(doc['_id'])
    return doc


def list_roles(search=''):
    db = _get_db()
    query = {}
    if search:
        query['role'] = {'$regex': search, '$options': 'i'}
    docs = []
    for doc in db['roles'].find(query).sort('role', ASCENDING):
        doc['id'] = str(doc['_id'])
        docs.append(doc)
    return docs


def update_role(role_id, update_fields):
    db = _get_db()
    oid = _oid(role_id)
    if oid is None:
        return False
    return db['roles'].update_one({'_id': oid}, {'$set': update_fields}).matched_count > 0


def delete_role(role_id):
    db = _get_db()
    oid = _oid(role_id)
    if oid is None:
        return False
    return db['roles'].delete_one({'_id': oid}).deleted_count > 0


def count_roles():
    return _get_db()['roles'].count_documents({})


# ------------------------------------------------------------------- courses
def insert_course(course_dict):
    db = _get_db()
    doc = dict(course_dict)
    doc.setdefault('created_at', datetime.now(timezone.utc))
    return str(db['courses'].insert_one(doc).inserted_id)


def find_course_by_id(course_id):
    db = _get_db()
    oid = _oid(course_id)
    if oid is None:
        return None
    doc = db['courses'].find_one({'_id': oid})
    if doc:
        doc['id'] = str(doc['_id'])
    return doc


def list_courses(search=''):
    db = _get_db()
    query = {}
    if search:
        query['$or'] = [
            {'course_name': {'$regex': search, '$options': 'i'}},
            {'skill': {'$regex': search, '$options': 'i'}},
        ]
    docs = []
    for doc in db['courses'].find(query).sort('course_name', ASCENDING):
        doc['id'] = str(doc['_id'])
        docs.append(doc)
    return docs


def update_course(course_id, update_fields):
    db = _get_db()
    oid = _oid(course_id)
    if oid is None:
        return False
    return db['courses'].update_one({'_id': oid}, {'$set': update_fields}).matched_count > 0


def delete_course(course_id):
    db = _get_db()
    oid = _oid(course_id)
    if oid is None:
        return False
    return db['courses'].delete_one({'_id': oid}).deleted_count > 0


def count_courses():
    return _get_db()['courses'].count_documents({})


def find_courses_for_skills(skills):
    """Return courses whose `skill` matches any of the provided (normalized) skills."""
    db = _get_db()
    if not skills:
        return []
    # Case-insensitive match against any of the missing skills.
    regex = '|'.join(s.replace('|', r'\|') for s in skills)
    docs = []
    for doc in db['courses'].find({'skill': {'$regex': regex, '$options': 'i'}}):
        doc['id'] = str(doc['_id'])
        docs.append(doc)
    return docs


# --------------------------------------------------------- health / utility
def ping():
    """Return True if the database responds to a ping."""
    try:
        _get_db().command('ping')
        return True
    except PyMongoError:
        return False
