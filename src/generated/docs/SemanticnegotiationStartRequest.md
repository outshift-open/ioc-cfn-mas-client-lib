# SemanticnegotiationStartRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agents** | [**List[SemanticnegotiationAgent]**](SemanticnegotiationAgent.md) | Agents is the list of participating agents. | [optional] 
**content_text** | **str** | ContentText is the negotiation prompt/context used to initialize the session. | [optional] 
**n_steps** | **int** | NSteps is the maximum number of negotiation steps. If omitted, defaults to 20. | [optional] 
**session_id** | **str** | SessionID is the client-provided session identifier. Currently assumed globally unique (not scoped by workspace/mas). | [optional] 

## Example

```python
from generated.models.semanticnegotiation_start_request import SemanticnegotiationStartRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SemanticnegotiationStartRequest from a JSON string
semanticnegotiation_start_request_instance = SemanticnegotiationStartRequest.from_json(json)
# print the JSON string representation of the object
print(SemanticnegotiationStartRequest.to_json())

# convert the object into a dict
semanticnegotiation_start_request_dict = semanticnegotiation_start_request_instance.to_dict()
# create an instance of SemanticnegotiationStartRequest from a dict
semanticnegotiation_start_request_from_dict = SemanticnegotiationStartRequest.from_dict(semanticnegotiation_start_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


