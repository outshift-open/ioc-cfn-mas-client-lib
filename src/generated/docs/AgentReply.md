# AgentReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agent_id** | **str** | AgentID is the agent identifier (must match one of the initiated agents). | 
**action** | **str** | Action is the agent action. Allowed values: \&quot;accept\&quot;, \&quot;reject\&quot;, \&quot;counter_offer\&quot; | 
**offer** | **Dict[str, object]** | Offer is an optional structured offer payload. Required when Action is \&quot;counter_offer\&quot;. | [optional] 

## Example

```python
from generated.models.agent_reply import AgentReply

# TODO update the JSON string below
json = "{}"
# create an instance of AgentReply from a JSON string
agent_reply_instance = AgentReply.from_json(json)
# print the JSON string representation of the object
print(AgentReply.to_json())

# convert the object into a dict
agent_reply_dict = agent_reply_instance.to_dict()
# create an instance of AgentReply from a dict
agent_reply_from_dict = AgentReply.from_dict(agent_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


