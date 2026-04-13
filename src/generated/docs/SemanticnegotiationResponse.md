# SemanticnegotiationResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** | Message provides additional information about the negotiation state. | [optional] 
**result** | **Dict[str, object]** | Result contains the pipeline execution result. The structure depends on the semantic negotiation library implementation. | [optional] 
**status** | **str** | Status indicates the result of the negotiation step. | [optional] 

## Example

```python
from generated.models.semanticnegotiation_response import SemanticnegotiationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SemanticnegotiationResponse from a JSON string
semanticnegotiation_response_instance = SemanticnegotiationResponse.from_json(json)
# print the JSON string representation of the object
print(SemanticnegotiationResponse.to_json())

# convert the object into a dict
semanticnegotiation_response_dict = semanticnegotiation_response_instance.to_dict()
# create an instance of SemanticnegotiationResponse from a dict
semanticnegotiation_response_from_dict = SemanticnegotiationResponse.from_dict(semanticnegotiation_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


