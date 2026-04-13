# SemanticnegotiationAgent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | ID is the unique agent identifier. | [optional] 
**name** | **str** | Name is the human-readable agent name. | [optional] 

## Example

```python
from generated.models.semanticnegotiation_agent import SemanticnegotiationAgent

# TODO update the JSON string below
json = "{}"
# create an instance of SemanticnegotiationAgent from a JSON string
semanticnegotiation_agent_instance = SemanticnegotiationAgent.from_json(json)
# print the JSON string representation of the object
print(SemanticnegotiationAgent.to_json())

# convert the object into a dict
semanticnegotiation_agent_dict = semanticnegotiation_agent_instance.to_dict()
# create an instance of SemanticnegotiationAgent from a dict
semanticnegotiation_agent_from_dict = SemanticnegotiationAgent.from_dict(semanticnegotiation_agent_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


