#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module backs up all Shell scripts in Intune.
"""

import base64
import os

from ...intunecdlib.check_prefix import check_prefix_match
from ...intunecdlib.clean_filename import clean_filename
from ...intunecdlib.graph_batch import (
    batch_assignment,
    batch_request,
    get_object_assignment,
)
from ...intunecdlib.graph_request import makeapirequest, makeAuditRequest
from ...intunecdlib.process_audit_data import process_audit_data
from ...intunecdlib.remove_keys import remove_keys
from ...intunecdlib.save_output import save_output

# Set MS Graph endpoint
ENDPOINT = "https://graph.microsoft.com/beta/deviceManagement/deviceShellScripts/"
ASSIGNMENT_ENDPOINT = (
    "https://graph.microsoft.com/beta/deviceManagement/deviceManagementScripts"
)


# Get all Shell scripts and save them in specified path
def savebackup(path, output, exclude, token, prefix, append_id, audit):
    """
    Saves all Shell scripts in Intune to a JSON or YAML file and script files.

    :param path: Path to save the backup to
    :param output: Format the backup will be saved as
    :param exclude: If "assignments" is in the list, it will not back up the assignments
    :param token: Token to use for authenticating the request
    """

    results = {"config_count": 0, "outputs": []}
    configpath = path + "/" + "Scripts/Shell/"
    data = makeapirequest(ENDPOINT, token)
    script_ids = []
    for script in data["value"]:
        script_ids.append(script["id"])

    assignment_responses = batch_assignment(
        data, "deviceManagement/deviceShellScripts/", "?$expand=assignments", token
    )
    script_data_responses = batch_request(
        script_ids, "deviceManagement/deviceShellScripts/", "", token
    )

    for script_data in script_data_responses:
        if prefix and not check_prefix_match(script_data["displayName"], prefix):
            continue

        results["config_count"] += 1
        if "assignments" not in exclude:
            assignments = get_object_assignment(script_data["id"], assignment_responses)
            if assignments:
                script_data["assignments"] = assignments

        graph_id = script_data["id"]
        script_data = remove_keys(script_data)

        print("Backing up Shell script: " + script_data["displayName"])

        # Get filename without illegal characters
        fname = clean_filename(script_data["displayName"])
        script_file_name = script_data["fileName"]
        if append_id:
            fname = f"{fname}__{graph_id}"
            script_name = script_data["fileName"].replace(".sh", "")
            script_file_name = f"{script_name}__{graph_id}.sh"

        # Save Shell script as JSON or YAML depending on configured value in "-o"
        save_output(output, configpath, fname, script_data)

        results["outputs"].append(fname)

        if audit:
            audit_data = makeAuditRequest(
                graph_id,
                "",
                token,
            )
            if audit_data:
                process_audit_data(audit_data, path, f"{configpath}{fname}.{output}")

        # Save Shell script data to the script data folder
        if not os.path.exists(configpath + "Script Data/"):
            os.makedirs(configpath + "Script Data/")
        decoded = base64.b64decode(script_data["scriptContent"]).decode("utf-8")
        f = open(configpath + "Script Data/" + script_file_name, "w", encoding="utf-8")
        f.write(decoded)

    return results
