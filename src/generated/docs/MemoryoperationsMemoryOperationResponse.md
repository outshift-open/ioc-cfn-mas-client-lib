# MemoryoperationsMemoryOperationResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**http_headers** | **Dict[str, str]** |  | [optional] 
**http_response_body** | **Dict[str, object]** |  | [optional] 
**http_status** | **int** |  | [optional] 

## Example

```python
from generated.models.memoryoperations_memory_operation_response import MemoryoperationsMemoryOperationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of MemoryoperationsMemoryOperationResponse from a JSON string
memoryoperations_memory_operation_response_instance = MemoryoperationsMemoryOperationResponse.from_json(json)
# print the JSON string representation of the object
print(MemoryoperationsMemoryOperationResponse.to_json())

# convert the object into a dict
memoryoperations_memory_operation_response_dict = memoryoperations_memory_operation_response_instance.to_dict()
# create an instance of MemoryoperationsMemoryOperationResponse from a dict
memoryoperations_memory_operation_response_from_dict = MemoryoperationsMemoryOperationResponse.from_dict(memoryoperations_memory_operation_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


