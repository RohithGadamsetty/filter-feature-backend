import mysql.connector
import operator
import re
from collections import OrderedDict

from flask import Flask, request, jsonify
from flask_cors import CORS

from exceptions import (InvalidArguement,
                        InvalidFilter)
from argcheck import (argcheck)

# connection = mysql.connector.connect(host='localhost',
#                                      database='<database_name>',
#                                      user='root',
#                                      password='<database_password>',
#                                      buffered=True)

app = Flask(__name__)
CORS(app)


@argcheck
def validate_token(api_key: 'api_key', token: 'token', test):
    """
    """
    return True


class Authentication:
    """
    User authentication
    """

    def __init__(self, email, password):
        """
        """
        self.email = email
        self.password = password

    def login(self):
        """
        login method
        """

        # result = self.login_verification()
        # if result:
        #     return result

        """
        Manual validation for test login
        """
        if (self.email == 'test123@gmail.com' and
                self.password == 'test@123'):
            token = self.return_token()
            return {
                "token": token
            }

        raise InvalidArguement('Invalid email or password')

    def login_verification(self):
        """
        Fetch information from database
        """
        cursor = connection.cursor()
        cursor.execute('''
    SELECT 1 
    FROM   user_info 
    WHERE  email = %s 
    AND    password = "%s" ''', (self.email, self.password))
        if cursor.rowcount:
            token = self.return_token()
            return {
                "token": token
            }

    def return_token(self):
        """
        Method to generate auth token
        """
        token = 'SCT3kRCwOhjUmQT6GfhXSKstynoQFK27'
        return token


class Project:
    """
    Project details
    """

    def __init__(self, filters):
        self.filters = filters

        projects = [
            ['Search optimisation', 'Google', 1618232566,
                12, 3, 'Angular, React', 'mumbai'],
            ['Building admin web interface ', 'Microsoft',
                1628292166, 20, 4, 'React, NodeJs', 'mumbai'],
            ['Student login', 'Delhi Pubic High School',
                1618262566, 4, 2, 'AngularJs', 'chennai'],
            ['Gym workout listing', 'Culf Fit', 1618292366,
                6, 5, 'Angular, Django', 'delhi'],
            ['Forum mall website', 'Forum', 1618756366, 12, 4,
                'Html, CSS', 'delhi'],
            ['Car wash company site', 'Expert wash', 1618294366,
                9, 2, 'Ionic, Angular, Django', 'chennai'],
            ['Laptop service center', 'Keshav electronics',
                1618283366, 4, 6, 'React, Django', 'delhi'],
            ['Gaming center', 'Cloud9', 1620279366,
                10, 1, 'Html, Javascript', 'mumbai'],
            ['Implement chat bot', 'zoho', 1618262866,
                15, 6, 'Python, Flask', 'mumbai'],
            ['Elastic search', 'Amazon', 1618267266, 5, 8, 'Django', 'chennai']
        ]
        self.projects = []
        for project in projects:
            self.projects.append(
                {
                    "projectName": project[0],
                    "clientName": project[1],
                    "startDate": project[2],
                    "noOfEmployees": project[3],
                    "experienceRequired": project[4],
                    "skillsRequired": project[5],
                    "location": project[6]
                })

    def get_projects(self):
        """
        """
        for _project in self.projects:
            projectValue = _project["startDate"]
            projectValue = projectValue - (projectValue % 86400)
            _project["startDate"] = projectValue
        if len(self.filters) == 0:
            return self.projects
        ops = {
            'in': lambda x, y: re.search(x, y, re.IGNORECASE),
            '==': lambda x, y: x == y,
            '>=': lambda x, y: x <= y,
            '<=': lambda x, y: x >= y
        }
        projects = []

        for _project in self.projects:
            flag = False
            for _filter in self.filters:
                if (_filter["condition"] == "in" and
                    _filter["name"] not in ("projectName", "clientName",
                                            "skillsRequired")):
                    raise InvalidFilter("Invalid name for 'in' filter")

                if (_filter["condition"] == "==" and
                    _filter["name"] not in ("location", "noOfEmployees",
                                            "experienceRequired", "startDate")):
                    raise InvalidFilter("Invalid name for '==' filter")

                if (_filter["condition"] in (">=", "<=") and
                    _filter["name"] not in ("noOfEmployees",
                                            "experienceRequired",
                                            "startDate")):
                    raise InvalidFilter("Invalid name for '>=' or '<=' filter")

                value = _filter["value"]
                projectValue = _project[_filter["name"]]
                operand = _filter["condition"]
                flag = ops[operand](
                    value, projectValue)
                if not flag:
                    break
            if flag:
                projects.append(_project)

        return projects


@app.route('/authentication/login', methods=['POST'])
def user_login():
    """
    To user logins
    """
    api_key = request.get_json().get('apiKey', None)
    email = request.get_json().get('email', None)
    password = request.get_json().get('password', None)

    validate_token(api_key=api_key)

    if not email or not password:
        raise InvalidArguement('Invalid email or password')

    authentication = Authentication(email, password)
    result = authentication.login()

    return jsonify({'result': result})


@app.route('/project-lists', methods=['POST'])
def project_lists():
    """
    Project Lists with details
    """
    api_key = request.get_json().get('apiKey', None)
    token = request.get_json().get('token', None)
    filters = request.get_json().get('filters', [])

    validate_token(api_key=api_key, token=token, test='test')
    projects = Project(filters)
    result = projects.get_projects()

    return jsonify({'result': result})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
