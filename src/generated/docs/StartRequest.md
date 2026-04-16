# StartRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**session_id** | **str** | SessionID is the client-provided session identifier. Currently assumed globally unique (not scoped by workspace/mas). | 
**agents** | [**List[Agent]**](Agent.md) | Agents is the list of participating agents. | 
**content_text** | **str** | ContentText is the negotiation prompt/context used to initialize the session. | 
**n_steps** | **int** | NSteps is the maximum number of negotiation steps. If omitted, defaults to 20. | [optional] [default to 20]

## Example

```python
from generated.models.start_request import StartRequest

# TODO update the JSON string below
json = "{}"
# create an instance of StartRequest from a JSON string
start_request_instance = StartRequest.from_json(json)
# print the JSON string representation of the object
print(StartRequest.to_json())

# convert the object into a dict
start_request_dict = start_request_instance.to_dict()
# create an instance of StartRequest from a dict
start_request_from_dict = StartRequest.from_dict(start_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


