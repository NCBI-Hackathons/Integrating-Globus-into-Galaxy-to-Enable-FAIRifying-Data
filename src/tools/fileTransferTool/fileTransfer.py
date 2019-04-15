import sys
import globus_sdk

pickled_tokens = base64.b64decode(sys.argv[0])

tokens = pickle.loads(pickled_tokens)
isinstance(tokens, dict)

transfer_access_token = tokens['tokens']['transfer.api.globus.org']['access_token']
transfer_authorizer = globus_sdk.AccessTokenAuthorizer(transfer_access_token)

tc = globus_sdk.TransferClient(authorizer=transfer_authorizer)

source_endpoint_id = "ebf55996-33bf-11e9-9fa4-0a06afd4a22e"
source_path = "/personal/rick/galaxy-training-data/"

dest_endpoint_id = "bfe3af54-5fcc-11e9-bf34-0edbf3a4e7ee"
dest_path = "/"

label = "My tutorial transfer"

# TransferData() automatically gets a submission_id for once-and-only-once submission
tdata = globus_sdk.TransferData(tc, source_endpoint_id, dest_endpoint_id, label=label)
tdata.add_item(source_path, dest_path, recursive=True)

tc.endpoint_autoactivate(source_endpoint_id)
tc.endpoint_autoactivate(dest_endpoint_id)

submit_result = tc.submit_transfer(tdata)
print("Task ID:", submit_result["task_id"])