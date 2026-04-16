# MemoryOperationPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**http_request_type** | **str** | POST, PUT, GET, DELETE, etc. | 
**http_url** | **str** | URL with query parameters (URL encoded) | [optional] 
**http_request_body** | **Dict[str, object]** | JSON payload | [optional] 
**http_headers** | **Dict[str, str]** | Custom headers | [optional] 

## Example

```python
from generated.models.memory_operation_payload import MemoryOperationPayload

# TODO update the JSON string below
json = "{}"
# create an instance of MemoryOperationPayload from a JSON string
memory_operation_payload_instance = MemoryOperationPayload.from_json(json)
# print the JSON string representation of the object
print(MemoryOperationPayload.to_json())

# convert the object into a dict
memory_operation_payload_dict = memory_operation_payload_instance.to_dict()
# create an instance of MemoryOperationPayload from a dict
memory_operation_payload_from_dict = MemoryOperationPayload.from_dict(memory_operation_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


