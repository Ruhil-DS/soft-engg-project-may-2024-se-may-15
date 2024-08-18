from flask import json
import pytest


def test_base_course_endpoint(test_client, log_in_default_user):
    token = log_in_default_user
    headers = {
        'Authentication-Token': f'{token}'
    }
    response = test_client.get('/api/v1/courses', headers=headers)
    response = json.loads(response.data)
    print(response)
    assert response['message'] == 'No Courses Found'

# def test_invalid_course_id(test_client, log_in_default_user):
#     token = log_in_default_user
#     headers = {
#         'Authentication-Token': f'{token}'
#     }
#     course_id = 'salsa'
#     response = test_client.get(f'/api/v1/courses/{course_id}', headers=headers)
#     response = json.loads(response.data)
#     print(response)
#     assert response['message'] == 'No Courses Found'
