import sys
import json
import globus_sdk

output = sys.argv[1]
print(output)

tokens = None
with open("/srv/galaxy/server/database/jobs_directory/.dev-tokens.json") as tokens_file:
    tokens = json.load(tokens_file)

transfer_tokens = tokens["transfer.api.globus.org"]
transfer_access_token = transfer_tokens["access_token"]
transfer_authorizer = globus_sdk.AccessTokenAuthorizer(transfer_access_token)

tc = globus_sdk.TransferClient(authorizer=transfer_authorizer)

# petrel#ncipilot
src_ep = "ebf55996-33bf-11e9-9fa4-0a06afd4a22e"
src_path = "/personal/rick/galaxy-training-data/mutant_R1.fastq"

# fairdata#dev1share (Galaxy instance endpoint)
dst_ep = "bfe3af54-5fcc-11e9-bf34-0edbf3a4e7ee"
dst_path = output

label = "My tutorial transfer"

# TransferData() automatically gets a submission_id for once-and-only-once submission
tdata = globus_sdk.TransferData(tc, src_ep, dst_ep, label=label)
tdata.add_item(src_path, dst_path, recursive=False)

tc.endpoint_autoactivate(src_ep)
tc.endpoint_autoactivate(dst_ep)

try:
    task = tc.submit_transfer(tdata)
except Exception as e:
    sys.stderr.write("Globus transfer from {}{} to {}{} failed due to error: {}".format(
            src_ep, src_path, dst_ep, dst_path, e))
    sys.exit(1)

last_event_time = None
"""
A Globus transfer job (task) can be in one of the three states: ACTIVE, SUCCEEDED, FAILED.
The tool every 20 seconds polls a status of the transfer job (task) from the Globus Transfer service,
with 60 second timeout limit. If the task is ACTIVE after time runs out 'task_wait' returns False,
and True otherwise.
"""
while not tc.task_wait(task["task_id"], 60, 15):
    task = tc.get_task(task["task_id"])
    # Get the last error Globus event
    events = tc.task_event_list(task["task_id"], num_results=1, filter="is_error:1")
    event = events.data[0]
    # Print the error event if it was not yet printed
    if event["time"] != last_event_time:
        last_event_time = event["time"]
        # TODO: printing the error event

"""
The Globus transfer job (task) has been terminated (is not ACTIVE). Check if the transfer
SUCCEEDED or FAILED.
"""
task = tc.get_task(task["task_id"])
if task["status"] == "SUCCEEDED":
    # "Globus transfer {}, from {}{} to {}{} succeeded".format(
    #    task["task_id"], src_ep, src_path, dst_ep, dst_path))
    sys.exit(0)
else:
    sys.stderr.write("Globus Transfer task: {}\n".format(task))
    events = tc.task_event_list(task["task_id"], num_results=1, filter="is_error:1")
    event = events.data[0]
    sys.stderr.write("Globus transfer {}, from {}{} to {}{} failed due to error: '{}'".format(
        task["task_id"], src_ep, src_path, dst_ep, dst_path, event["details"]))
    sys.exit(1)
print("Task ID:", submit_result["task_id"])
