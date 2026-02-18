# SharedmemorySharedMemoryUpsertRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**memories** | **List[Dict[str, object]]** |  | [optional] 
**relationships** | **List[Dict[str, object]]** |  | [optional] 

## Example

```python
from generated.models.sharedmemory_shared_memory_upsert_request import SharedmemorySharedMemoryUpsertRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SharedmemorySharedMemoryUpsertRequest from a JSON string
sharedmemory_shared_memory_upsert_request_instance = SharedmemorySharedMemoryUpsertRequest.from_json(json)
# print the JSON string representation of the object
print(SharedmemorySharedMemoryUpsertRequest.to_json())

# convert the object into a dict
sharedmemory_shared_memory_upsert_request_dict = sharedmemory_shared_memory_upsert_request_instance.to_dict()
# create an instance of SharedmemorySharedMemoryUpsertRequest from a dict
sharedmemory_shared_memory_upsert_request_from_dict = SharedmemorySharedMemoryUpsertRequest.from_dict(sharedmemory_shared_memory_upsert_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


