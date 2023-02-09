# File: cscdomainmanager_connector.py
#
# Copyright (c) 2023 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
    API References:
    https://docs.splunk.com/Documentation/SOAR/current/DevelopApps/AppDevAPIRef#finalize

    # -----------------------------------------
    # Phantom sample App Connector python file
    # -----------------------------------------
"""

# Python 3 Compatibility imports
from __future__ import print_function, unicode_literals

import argparse
import getpass
import json
import sys

import phantom.app as phantom
import requests
from bs4 import BeautifulSoup
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector

import cscdomainmanager_consts as consts


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class CscDomainManagerConnector(BaseConnector):
    """
    Interface with CSC Domain Manager API for searching owned domains and registering unowned
    """

    def __init__(self):
        super().__init__()

        self._state = None
        self._base_url = None
        self._account_number = None
        self._request_headers = {"Accept": "application/json"}

    def _process_empty_response(self, response, action_result):
        if response.status_code == [200, 204]:
            return RetVal(phantom.APP_SUCCESS, {})

        return RetVal(
            action_result.set_status(
                phantom.APP_ERROR, "Empty response and no information in the header, Statuscode: {}".format(response.status_code)
            ),
            None,
        )

    def _process_html_response(self, response, action_result):
        status_code = response.status_code

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            # Remove the script, style, footer and navigation part from the HTML message
            for element in soup(["script", "style", "footer", "nav"]):
                element.extract()
            error_text = soup.text
            split_lines = error_text.split("\n")
            split_lines = [x.strip() for x in split_lines if x.strip()]
            error_text = "\n".join(split_lines)
        except Exception:
            error_text = "Cannot parse error details"

        message = f"Status Code: {status_code}. Data from server:\n{error_text}\n"

        message = message.replace("{", "{{").replace("}", "}}")
        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_json_response(self, response, action_result):
        try:
            resp_json = response.json()
        except Exception as error:
            message = self._get_error_message_from_exception(error)
            return RetVal(
                action_result.set_status(
                    phantom.APP_ERROR,
                    f"Unable to parse JSON response. Error: {message}",
                ),
                None,
            )

        if 200 <= response.status_code < 399:
            return RetVal(phantom.APP_SUCCESS, resp_json)

        message = (
            f"Error from server. Status Code: {response.status_code} "
            f"Data from server: {response.text.replace('{', '{{').replace('}', '}}')}"
        )

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_response(self, response, action_result):
        # store the r_text in debug data, it will get dumped in the logs if the action fails
        if hasattr(action_result, "add_debug_data"):
            action_result.add_debug_data({"r_status_code": response.status_code})
            action_result.add_debug_data({"r_text": response.text})
            action_result.add_debug_data({"r_headers": response.headers})

        # Process each 'Content-Type' of response separately

        # Process a json response
        if "json" in response.headers.get("Content-Type", ""):
            return self._process_json_response(response, action_result)

        # Process an HTML response, Do this no matter what the api talks.
        # There is a high chance of a PROXY in between phantom and the rest of
        # world, in case of errors, PROXY's return HTML, this function parses
        # the error and adds it to the action_result.
        if "html" in response.headers.get("Content-Type", ""):
            return self._process_html_response(response, action_result)

        # it's not content-type that is to be parsed, handle an empty response
        if not response.text:
            return self._process_empty_response(response, action_result)

        # everything else is actually an error at this point
        message = (
            f"Can't process response from server. Status Code: {response.status_code} "
            f"Data from server: {response.text.replace('{', '{{').replace('}', '}}')}"
        )

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _dump_error_log(self, error, message="Exception occurred."):
        self.error_print(message, dump_object=error)

    def _get_error_message_from_exception(self, e):
        """ This method is used to get appropriate error message from the exception.
        :param e: Exception object
        :return: error message
        """

        error_code = None
        error_message = consts.CSC_ERROR_MESSAGE_UNAVAILABLE
        self._dump_error_log(e)
        try:
            if hasattr(e, "args"):
                if len(e.args) > 1:
                    error_code = e.args[0]
                    error_message = e.args[1]
                elif len(e.args) == 1:
                    error_message = e.args[0]
        except Exception as ex:
            self._dump_error_log(ex, "Error occurred while fetching exception information")

        if not error_code:
            error_text = "Error Message: {}".format(error_message)
        else:
            error_text = "Error Code: {}. Error Message: {}".format(error_code, error_message)

        return error_text

    def _make_rest_call(self, endpoint, action_result, method="get", **kwargs):
        config = self.get_config()
        resp_json = None

        try:
            request_func = getattr(requests, method)
            response = request_func(
                f"{self._base_url}{endpoint}",
                verify=config.get("verify_server_cert", True),
                **kwargs,
            )
        except AttributeError:
            return RetVal(
                action_result.set_status(
                    phantom.APP_ERROR, f"Invalid method: {method}"
                ),
                resp_json,
            )
        except Exception as error:
            message = self._get_error_message_from_exception(error)
            return RetVal(
                action_result.set_status(
                    phantom.APP_ERROR, f"Error Connecting to server. Details: {message}"
                ),
                resp_json,
            )

        return self._process_response(response, action_result)

    def _handle_test_connectivity(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))

        self.save_progress(f"Testing connectivity to {self._base_url}")
        ret_val, response = self._make_rest_call(
            "/domains", action_result, params=None, headers=self._request_headers
        )

        if phantom.is_fail(ret_val):
            self.save_progress("Test Connectivity Failed")
            self.error_print(response)
            return action_result.get_status()

        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_get_all_domains(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        self.save_progress("Handling request to get all domains")

        # Set filter parameters for search
        params = None
        if not param.get("custom", None) and param:
            for part in ["selector", "operator", "value"]:
                if not param.get(part, None):
                    self.error_print(
                        f"Inputs were provided but failed to specify required {part}"
                    )
                    self.save_progress(
                        f"Inputs were provided but failed to specify required {part}"
                    )
                    return action_result.set_status(phantom.APP_ERROR)
            params = {
                "filter": param.get("selector") + param.get("operator") + param.get("value")
            }
        elif param.get("custom", None):
            params = {"filter": param.get("custom")}

        retval, response = self._make_rest_call(
            "/domains", action_result, params=params, headers=self._request_headers
        )
        if phantom.is_fail(retval):
            self.save_progress(f"Failed executing {self.get_action_identifier()}")
            self.error_print(response)
            return action_result.get_status()

        self.save_progress("Saving domains found")
        for domain in response.get("domains"):
            action_result.add_data(domain["qualifiedDomainName"])

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_get_specific_domain(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        self.save_progress(f"Handling request to get domain {param.get('fqdn')}")

        retval, response = self._make_rest_call(
            f"/domains/{param.get('fqdn')}",
            action_result,
            params=None,
            headers=self._request_headers,
        )
        if phantom.is_fail(retval) and retval != 404:
            self.save_progress(f"Failed executing {self.get_action_identifier()}")
            self.error_print(response)
            return action_result.get_status()

        if retval == 404:
            self.save_progress(f"No domain found when looking for {param.get('fqdn')}")

        action_result.add_data(response)
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_check_domain_available(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        self.save_progress(f"We have {param.get('fqdn')}")
        self.save_progress(
            f'Handling request to check availability of domains {param.get("fqdn")}'
        )

        retval, response = self._make_rest_call(
            "/domains/availability",
            action_result,
            params={"qualifiedDomainNames": param.get("fqdn")},
            headers=self._request_headers,
        )
        if phantom.is_fail(retval):
            self.save_progress(f"Failed executing {self.get_action_identifier()}")
            self.error_print(response)
            return action_result.get_status()

        for domain in response.get("results"):
            action_result.add_data(domain)
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_register_domain(self, param):
        """
        The details required to register a domain. If an order template is available
        for the account mapped to the bearer token, then only the
        "qualifiedDomainName" property is required.

        Try to register with just qualifiedDomainName and fall back to using
        provided schema as needed
        """

        action_result = self.add_action_result(ActionResult(dict(param)))
        self.save_progress(f"Handling request to register domain with provided {param}")

        registration_schema = {
            "qualifiedDomainName": param.get("qualifieddomainname"),
            "businessUnit": param.get("businessunit"),
            "accountNumber": self._account_number,
            "term": param.get("term", "12"),
            "brand": param.get("brand", ""),
            "whoisContacts": {
                "registrantProfile": param.get("registrantprofile"),
                "adminProfile": param.get("adminprofile"),
                "technicalProfile": param.get("technicalprofile"),
            },
            "nameServers": list(param.get("nameservers").split(",")),
            "dnsType": param.get("dnstype", "CSC_BASIC"),
            "notes": param.get("notes", "Registered by Security Automation"),
            "notifications": {
                "enabled": param.get("notificationsenabled", False),
                "additionalNotificationEmails": list(
                    param.get("additionalnotificationemails", "").split(",")
                ),
            },
            "redactPublicWhois": param.get("redactpublicwhois", False),
        }
        self.save_progress(
            f"Will register domain with {registration_schema} if our bearer token does not have an "
            "existing order template"
        )

        retval, response = self._make_rest_call(
            "/domains/registration",
            action_result,
            method="post",
            json={"qualifiedDomainName": param.get("qualifieddomainname")},
            headers=self._request_headers,
        )
        if phantom.is_fail(retval):
            self.save_progress(
                f"Failed registering {param.get('qualifieddomainname')} with only "
                "specifying the domain.  Trying again with full schema..."
            )
            retval, response = self._make_rest_call(
                "/domains/registration",
                action_result,
                method="post",
                json=registration_schema,
                headers=self._request_headers,
            )
            if phantom.is_fail(retval):
                self.save_progress(f"Failed executing {self.get_action_identifier()}")
                self.error_print(response)
                return action_result.get_status()

        action_result.add_data(response.get("result"))
        return action_result.set_status(phantom.APP_SUCCESS)

    def handle_action(self, param):
        """
        Router for processing requested action
        """

        ret_val = phantom.APP_SUCCESS
        action_id = self.get_action_identifier()
        self.debug_print("action_id", action_id)

        action_map = {
            "test_connectivity": self._handle_test_connectivity,
            "get_all_domains": self._handle_get_all_domains,
            "get_specific_domain": self._handle_get_specific_domain,
            "check_domain_available": self._handle_check_domain_available,
            "register_domain": self._handle_register_domain,
        }

        if action_id in action_map:
            ret_val = action_map[action_id](param)

        return ret_val

    def initialize(self):
        """
        Optional function that can be implemented by the AppConnector.
        It is called once before starting the parameter list iteration,
        for example, before the first call to AppConnector::handle_action()
        """

        self._state = self.load_state()
        # get the asset config
        config = self.get_config()
        self._account_number = config.get("accountNumber")
        self._request_headers["apikey"] = config("apikey")
        self._request_headers["Authorization"] = f"Bearer {config.get('bearer_token')}"
        self._base_url = config.get("endpoint_url", consts.CSC_PRODUCTION_URL).rstrip('/')
        return phantom.APP_SUCCESS

    def finalize(self):
        """
        Optional function that can be implemented by the AppConnector.
        Called by the BaseConnector once all the elements in the parameter list are processed.
        """

        # Save the state, this data is saved across actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


def main():
    """
    Function to locally test connector via CLI
    """

    argparser = argparse.ArgumentParser()
    argparser.add_argument("input_test_json", help="Input Test JSON file")
    argparser.add_argument(
        "-u", "--username", help="Splunk SOAR username", required=False
    )
    argparser.add_argument(
        "-p", "--password", help="Splunk SOAR password", required=False
    )
    argparser.add_argument('-v', '--verify', action='store_true', help='verify', required=False, default=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password
    verify = args.verify

    if args.username is not None and args.password is None:
        # User specified a username but not a password, so ask
        password = getpass.getpass("Splunk SOAR Password: ")

    if username and password:
        try:
            login_url = CscDomainManagerConnector._get_phantom_base_url() + "/login"

            print("Accessing the Login page")
            response = requests.get(login_url, verify=verify, timeout=consts.CSC_DEFAULT_TIMEOUT)  # nosec
            csrftoken = response.cookies["csrftoken"]

            data = {
                "username": username,
                "password": password,
                "csrfmiddlewaretoken": csrftoken,
            }

            headers = {"Cookie": f"csrftoken={csrftoken}", "Referer": login_url}

            print("Logging into Platform to get the session id")
            response = requests.post(  # nosec
                login_url, verify=verify, data=data, headers=headers, timeout=consts.CSC_DEFAULT_TIMEOUT
            )
            session_id = response.cookies["sessionid"]
        except Exception as error:
            print(f"Unable to get session id from the platform. Error: {error}")
            sys.exit(1)

    with open(args.input_test_json) as testfile:
        in_json = testfile.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = CscDomainManagerConnector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json["user_session_token"] = session_id
            connector._set_csrf_info(csrftoken, headers["Referer"])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    sys.exit(0)


if __name__ == "__main__":
    main()
