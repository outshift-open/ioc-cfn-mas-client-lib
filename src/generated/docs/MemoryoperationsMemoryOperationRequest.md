# MemoryoperationsMemoryOperationRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**header** | **object** |  | [optional] 
**payload** | [**MemoryoperationsMemoryOperationPayload**](MemoryoperationsMemoryOperationPayload.md) |  | [optional] 

## Example

```python
from generated.models.memoryoperations_memory_operation_request import MemoryoperationsMemoryOperationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of MemoryoperationsMemoryOperationRequest from a JSON string
memoryoperations_memory_operation_request_instance = MemoryoperationsMemoryOperationRequest.from_json(json)
# print the JSON string representation of the object
print(MemoryoperationsMemoryOperationRequest.to_json())

# convert the object into a dict
memoryoperations_memory_operation_request_dict = memoryoperations_memory_operation_request_instance.to_dict()
# create an instance of MemoryoperationsMemoryOperationRequest from a dict
memoryoperations_memory_operation_request_from_dict = MemoryoperationsMemoryOperationRequest.from_dict(memoryoperations_memory_operation_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


