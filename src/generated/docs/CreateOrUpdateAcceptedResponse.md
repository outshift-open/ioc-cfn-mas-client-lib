# CreateOrUpdateAcceptedResponse

Response returned when an async upsert request is accepted (202 Accepted)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**response_id** | **str** | ID of the request, can be used for correlation in logs | 
**status** | **str** | Status indicating the request was accepted for processing | 
**message** | **str** | Message providing additional information | 

## Example

```python
from generated.models.create_or_update_accepted_response import CreateOrUpdateAcceptedResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateOrUpdateAcceptedResponse from a JSON string
create_or_update_accepted_response_instance = CreateOrUpdateAcceptedResponse.from_json(json)
# print the JSON string representation of the object
print(CreateOrUpdateAcceptedResponse.to_json())

# convert the object into a dict
create_or_update_accepted_response_dict = create_or_update_accepted_response_instance.to_dict()
# create an instance of CreateOrUpdateAcceptedResponse from a dict
create_or_update_accepted_response_from_dict = CreateOrUpdateAcceptedResponse.from_dict(create_or_update_accepted_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


