# NegotiationResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** | Status indicates the result of the negotiation step. | [optional] 
**message** | **str** | Message provides additional information about the negotiation state. | [optional] 
**result** | **Dict[str, object]** | Result contains the pipeline execution result. The structure depends on the semantic negotiation library implementation. | [optional] 

## Example

```python
from generated.models.negotiation_response import NegotiationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of NegotiationResponse from a JSON string
negotiation_response_instance = NegotiationResponse.from_json(json)
# print the JSON string representation of the object
print(NegotiationResponse.to_json())

# convert the object into a dict
negotiation_response_dict = negotiation_response_instance.to_dict()
# create an instance of NegotiationResponse from a dict
negotiation_response_from_dict = NegotiationResponse.from_dict(negotiation_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


