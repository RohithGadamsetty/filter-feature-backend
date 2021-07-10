import pytest

from task import (Authentication,
                  Project)


class TestAuthentication:
    """
    Test class for authentication
    """

    def test_login(self):
        payloads = self.get_login_payload_cases()

        for i in range(len(payloads)):
            auth = Authentication(
                payloads[i]["email"], payloads[i]["password"])
            if i == 3:
                response = auth.login()
                assert "token" in response.keys()
            if (i in (0, 1, 2)):
                with pytest.raises(Exception) as exception:
                    response = auth.login()
                    assert response
                    assert str(exception.value) == 'Invalid email or password'

    def get_login_payload_cases(self):
        payloads = [
            # wrong email and password
            {
                "email": "testcase1@gmail.com",
                "password": "testcase@123"
            },
            # wrong email and correct password
            {
                "email": "testcase1@gmail.com",
                "password": "test@123"
            },
            # correct email and wrong password
            {
                "email": "test123@gmail.com",
                "password": "testcase@123"
            },
            # both email and password are correct
            {
                "email": "test123@gmail.com",
                "password": "test@123"
            }
        ]

        return payloads


class TestProjects:
    """
    Test class for projects
    """
    def test_project_lists(self):
        payloads, expected_response = self.get_project_lists_cases()

        for i in range(len(payloads)):
            projects = Project(payloads[i]["filters"])
            if i in (0, 1):
                with pytest.raises(Exception) as exception:
                    assert projects.get_projects()
                    assert str(exception.value) == exception_response[i]

            elif i not in(0, 1):
                response = projects.get_projects()
                assert len(response) == expected_response[i]

    def get_project_lists_cases(self):
        payloads = [
            {
                "filters": [
                    {
                        "name": "noOfEmployees",
                        "filterType": "number",
                        "condition": "in",
                        "value": 1
                    }
                ]
            },
            {
                "filters": [
                    {
                        "name": "clientName",
                        "filterType": "number",
                        "condition": "<=",
                        "value": "client"
                    }
                ]
            },
            {
                "filters": []
            },
            {
                "filters": [
                    {
                        "name": "noOfEmployees",
                        "filterType": "number",
                        "condition": "<=",
                        "value": 1
                    }
                ]
            },
            {
                "filters": [
                    {
                        "name": "projectName",
                        "filterType": "string",
                        "condition": "in",
                        "value": "Se"
                    }
                ]
            },
            {
                "filters": [
                    {
                        "name": "location",
                        "filterType": "string",
                        "condition": "==",
                        "value": "mumbai"
                    }
                ]
            },
            {
                "filters": [
                    {
                        "name": "experienceRequired",
                        "filterType": "number",
                        "condition": ">=",
                        "value": 3
                    }
                ]
            }
        ]

        expected_response = [
            "Invalid name for 'in' filter",
            "Invalid name for '<=' filter",
            10,
            0,
            3,
            4,
            7
        ]
        return payloads, expected_response
