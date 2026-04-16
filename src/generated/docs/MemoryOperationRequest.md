# MemoryOperationRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**header** | **object** | Reserved for future header extensions | [optional] 
**payload** | [**MemoryOperationPayload**](MemoryOperationPayload.md) |  | 

## Example

```python
from generated.models.memory_operation_request import MemoryOperationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of MemoryOperationRequest from a JSON string
memory_operation_request_instance = MemoryOperationRequest.from_json(json)
# print the JSON string representation of the object
print(MemoryOperationRequest.to_json())

# convert the object into a dict
memory_operation_request_dict = memory_operation_request_instance.to_dict()
# create an instance of MemoryOperationRequest from a dict
memory_operation_request_from_dict = MemoryOperationRequest.from_dict(memory_operation_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


