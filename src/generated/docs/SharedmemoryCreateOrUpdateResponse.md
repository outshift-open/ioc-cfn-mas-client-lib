# SharedmemoryCreateOrUpdateResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** | Optional message providing additional information | [optional] 
**response_id** | **str** | ID of the response, this gets populated from request_id | [optional] 
**status** | **str** | Status of the request | [optional] 

## Example

```python
from generated.models.sharedmemory_create_or_update_response import SharedmemoryCreateOrUpdateResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SharedmemoryCreateOrUpdateResponse from a JSON string
sharedmemory_create_or_update_response_instance = SharedmemoryCreateOrUpdateResponse.from_json(json)
# print the JSON string representation of the object
print(SharedmemoryCreateOrUpdateResponse.to_json())

# convert the object into a dict
sharedmemory_create_or_update_response_dict = sharedmemory_create_or_update_response_instance.to_dict()
# create an instance of SharedmemoryCreateOrUpdateResponse from a dict
sharedmemory_create_or_update_response_from_dict = SharedmemoryCreateOrUpdateResponse.from_dict(sharedmemory_create_or_update_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


