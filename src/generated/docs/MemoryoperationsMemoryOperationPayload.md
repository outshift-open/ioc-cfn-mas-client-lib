# MemoryoperationsMemoryOperationPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**http_headers** | **Dict[str, str]** | Custom headers | [optional] 
**http_request_body** | **Dict[str, object]** | JSON payload | [optional] 
**http_request_type** | **str** | POST, PUT, GET, DELETE, etc. | [optional] 
**http_url** | **str** | URL with query parameters (URL encoded) | [optional] 

## Example

```python
from generated.models.memoryoperations_memory_operation_payload import MemoryoperationsMemoryOperationPayload

# TODO update the JSON string below
json = "{}"
# create an instance of MemoryoperationsMemoryOperationPayload from a JSON string
memoryoperations_memory_operation_payload_instance = MemoryoperationsMemoryOperationPayload.from_json(json)
# print the JSON string representation of the object
print(MemoryoperationsMemoryOperationPayload.to_json())

# convert the object into a dict
memoryoperations_memory_operation_payload_dict = memoryoperations_memory_operation_payload_instance.to_dict()
# create an instance of MemoryoperationsMemoryOperationPayload from a dict
memoryoperations_memory_operation_payload_from_dict = MemoryoperationsMemoryOperationPayload.from_dict(memoryoperations_memory_operation_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


