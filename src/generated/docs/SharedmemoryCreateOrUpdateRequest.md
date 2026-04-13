# SharedmemoryCreateOrUpdateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**header** | [**SharedmemoryHeader**](SharedmemoryHeader.md) | Header(s) of the request, optional | [optional] 
**payload** | [**CognitionagentclientExtractionPayload**](CognitionagentclientExtractionPayload.md) | Payload contains the extraction metadata and the raw data to be processed. The structure of the payload data is defined by Payload.Metadata.Format | [optional] 
**request_id** | **str** | ID of the request, optional. If not provided, a random UUID is used to represent the request | [optional] 

## Example

```python
from generated.models.sharedmemory_create_or_update_request import SharedmemoryCreateOrUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SharedmemoryCreateOrUpdateRequest from a JSON string
sharedmemory_create_or_update_request_instance = SharedmemoryCreateOrUpdateRequest.from_json(json)
# print the JSON string representation of the object
print(SharedmemoryCreateOrUpdateRequest.to_json())

# convert the object into a dict
sharedmemory_create_or_update_request_dict = sharedmemory_create_or_update_request_instance.to_dict()
# create an instance of SharedmemoryCreateOrUpdateRequest from a dict
sharedmemory_create_or_update_request_from_dict = SharedmemoryCreateOrUpdateRequest.from_dict(sharedmemory_create_or_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


