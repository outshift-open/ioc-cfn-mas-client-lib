# SemanticnegotiationDecideRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agent_replies** | [**List[SemanticnegotiationAgentReply]**](SemanticnegotiationAgentReply.md) | AgentReplies are the replies produced by agents since the last step. | [optional] 
**session_id** | **str** | SessionID is the session identifier previously provided to the start endpoint. | [optional] 

## Example

```python
from generated.models.semanticnegotiation_decide_request import SemanticnegotiationDecideRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SemanticnegotiationDecideRequest from a JSON string
semanticnegotiation_decide_request_instance = SemanticnegotiationDecideRequest.from_json(json)
# print the JSON string representation of the object
print(SemanticnegotiationDecideRequest.to_json())

# convert the object into a dict
semanticnegotiation_decide_request_dict = semanticnegotiation_decide_request_instance.to_dict()
# create an instance of SemanticnegotiationDecideRequest from a dict
semanticnegotiation_decide_request_from_dict = SemanticnegotiationDecideRequest.from_dict(semanticnegotiation_decide_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


