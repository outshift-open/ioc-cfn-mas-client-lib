# DecideRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**session_id** | **str** | SessionID is the session identifier previously provided to the start endpoint. | 
**agent_replies** | [**List[AgentReply]**](AgentReply.md) | AgentReplies are the replies produced by agents since the last step. | 

## Example

```python
from generated.models.decide_request import DecideRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DecideRequest from a JSON string
decide_request_instance = DecideRequest.from_json(json)
# print the JSON string representation of the object
print(DecideRequest.to_json())

# convert the object into a dict
decide_request_dict = decide_request_instance.to_dict()
# create an instance of DecideRequest from a dict
decide_request_from_dict = DecideRequest.from_dict(decide_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


