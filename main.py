import requests
import random
import string
import json
import jsonschema
from jsonschema import validate
import pytest
from py.xml import html
import os
import time



base_url_and_port = "http://localhost:8000/"
random_username = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
random_page = ''.join(random.choices(string.digits, k=1))
app_json = "application/json"
header={'Accept': app_json}
auth=(random_username, 'admin')

player_schema = {
    "type": "object",
    "properties": {
        "Name": {"type": "string",
                 "pattern": "\\w+\\s\\w+"},
        "ID": {"type": "number",
               "minLength": 1}
    },
}

def setup_module(module):
    cmd = './twtask &'
    os.system(cmd)
    wait_until_server_up()

def teardown_module(module):
    cmd = "kill $(ps -e | grep 'twtask' | awk '{print $1}')"
    os.system(cmd)


def test_authorization():
    response = requests.get(base_url_and_port + 'players?page=' + random_page, auth=auth)
    assert response.status_code == 401, f"Expected response code {401}. Actual response code {response.status_code}. Bug number 1"

def test_content_type():
    response = requests.get(base_url_and_port + 'players?page=' + random_page, auth=auth, headers=header)
    assert response.status_code == 200, f"Expected response code {200}. Actual response code {response.status_code}."
    response_header = response.headers.get("Content-Type")
    assert response_header == app_json, f"Expected content type is  {app_json}. Actual content type is {response_header}. Bug number 2"

def test_length_of_json_array():
    response = requests.get(base_url_and_port + 'players?page=' + random_page, auth=auth, headers=header)
    assert response.status_code == 200, f"Expected response code {200}. Actual response code {response.status_code}."
    response_length = len(response.json())
    assert response_length == 50, f"Expected number of json objects is {50}. Actual response code {response_length}. Bug number 3"

def test_correctness_of_data():
    response = requests.get(base_url_and_port + 'players?page=' + random_page, auth=auth, headers=header)
    assert response.status_code == 200
    assert validate_json(response.json()), f"Json Schema failed, response contains json objects with incorrect format, e.g. empty name or id, lack of first/last name, incorrect format of json values,... Bug number 4"

def test_response_for_different_http_request_method():
    response = requests.delete(base_url_and_port + 'players?page=' + random_page, auth=auth, headers=header)
    assert response.status_code == 400, f"Response code should be {400} for not implemented http method request (DELETE), but found {response.status_code}. Bug number 5"

def test_response_code_for_incorrect_input():
    response = requests.get(base_url_and_port + 'players?page="' + random_page + '"', auth=auth, headers=header)
    assert response.status_code == 400, f"Response code should be {400} for incorrect request query param, but found {response.status_code}. Bug number 6"

def test_response_error_message_for_incorrect_input():
    response = requests.get(base_url_and_port + 'players?page="' + random_page + '"', auth=auth, headers=header)
    response_error_message = "Your request is incorrect"
    assert response_error_message in response.text, f"Response error message should be: ' {response_error_message} ', for incorrect request query param, but found ' {response.text} '. Bug number 7"


def validate_json(json_data):
        try:
            validate(instance=json_data, schema=player_schema)
        except jsonschema.exceptions.ValidationError as err:
            return False
        return True

def wait_until_server_up():
    iterations = 0
    while iterations < 10:
       try:
            response_code = requests.get(base_url_and_port + 'players?page=' + random_page).status_code
            if response_code == 401 : return True
            time.sleep(1)
            iterations+=1
       except:
           continue
    return False
