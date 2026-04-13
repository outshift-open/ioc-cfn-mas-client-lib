# SemanticnegotiationAgentReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **str** | Action is the agent action. Allowed values: \&quot;accept\&quot;, \&quot;reject\&quot;, \&quot;counter_offer\&quot; | [optional] 
**agent_id** | **str** | AgentID is the agent identifier (must match one of the initiated agents). | [optional] 
**offer** | **Dict[str, object]** | Offer is an optional structured offer payload. Required when Action is \&quot;counter_offer\&quot;. | [optional] 

## Example

```python
from generated.models.semanticnegotiation_agent_reply import SemanticnegotiationAgentReply

# TODO update the JSON string below
json = "{}"
# create an instance of SemanticnegotiationAgentReply from a JSON string
semanticnegotiation_agent_reply_instance = SemanticnegotiationAgentReply.from_json(json)
# print the JSON string representation of the object
print(SemanticnegotiationAgentReply.to_json())

# convert the object into a dict
semanticnegotiation_agent_reply_dict = semanticnegotiation_agent_reply_instance.to_dict()
# create an instance of SemanticnegotiationAgentReply from a dict
semanticnegotiation_agent_reply_from_dict = SemanticnegotiationAgentReply.from_dict(semanticnegotiation_agent_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


