"""
Django models for TalentMap.

Business data (employees, roles, courses) lives in MongoDB via PyMongo.
Django's ORM is used only for the built-in auth User (HR login) and admin.
No business models are defined here by design — see hr/mongo.py instead.
"""
