# MemoryOperationResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**http_status** | **int** | HTTP status code from the remote provider | 
**http_response_body** | **Dict[str, object]** | Response body from the remote provider | [optional] 
**http_headers** | **Dict[str, str]** | Response headers from the remote provider | [optional] 

## Example

```python
from generated.models.memory_operation_response import MemoryOperationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of MemoryOperationResponse from a JSON string
memory_operation_response_instance = MemoryOperationResponse.from_json(json)
# print the JSON string representation of the object
print(MemoryOperationResponse.to_json())

# convert the object into a dict
memory_operation_response_dict = memory_operation_response_instance.to_dict()
# create an instance of MemoryOperationResponse from a dict
memory_operation_response_from_dict = MemoryOperationResponse.from_dict(memory_operation_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


