# CreateOrUpdateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**request_id** | **str** | ID of the request, optional. If not provided, a random UUID is used to represent the request | [optional] 
**header** | [**Header**](Header.md) |  | [optional] 
**payload** | [**ExtractionPayload**](ExtractionPayload.md) |  | 

## Example

```python
from generated.models.create_or_update_request import CreateOrUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateOrUpdateRequest from a JSON string
create_or_update_request_instance = CreateOrUpdateRequest.from_json(json)
# print the JSON string representation of the object
print(CreateOrUpdateRequest.to_json())

# convert the object into a dict
create_or_update_request_dict = create_or_update_request_instance.to_dict()
# create an instance of CreateOrUpdateRequest from a dict
create_or_update_request_from_dict = CreateOrUpdateRequest.from_dict(create_or_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


