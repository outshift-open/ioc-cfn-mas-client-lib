# SharedmemoryQueryResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** | Message provides detailed information from the query result | [optional] 
**response_id** | **str** | ID of the response, this gets populated from request_id | [optional] 

## Example

```python
from generated.models.sharedmemory_query_response import SharedmemoryQueryResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SharedmemoryQueryResponse from a JSON string
sharedmemory_query_response_instance = SharedmemoryQueryResponse.from_json(json)
# print the JSON string representation of the object
print(SharedmemoryQueryResponse.to_json())

# convert the object into a dict
sharedmemory_query_response_dict = sharedmemory_query_response_instance.to_dict()
# create an instance of SharedmemoryQueryResponse from a dict
sharedmemory_query_response_from_dict = SharedmemoryQueryResponse.from_dict(sharedmemory_query_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


