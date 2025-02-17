import os
from pymongo import MongoClient

client = MongoClient()
db = client['student_db']
student_collection = db['students']


def add(student=None):
    print(HERE!!!)
    if not student:
        return 'Invalid student data', 400
    if not student.first_name or not student.last_name:
        return 'Missing required fields', 400

    existing_student = student_collection.find_one({
        'first_name': student.first_name,
        'last_name': student.last_name
    })
    if existing_student:
        return 'already exists', 409

    result = student_collection.insert_one(student.to_dict())
    student.student_id = str(result.inserted_id)
    return student.student_id


def get_by_id(student_id=None, subject=None):
    student = student_collection.find_one({'_id': student_id})
    if not student:
        return 'not found', 404
    student['student_id'] = student_id
    print(student)
    return student


def delete(student_id=None):
    result = student_collection.delete_one({'_id': student_id})
    if result.deleted_count == 0:
        return 'not found', 404
    return student_id