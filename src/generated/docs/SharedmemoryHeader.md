# SharedmemoryHeader


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agent_id** | **str** | ID that represents the agent, optional for query operations | [optional] 

## Example

```python
from generated.models.sharedmemory_header import SharedmemoryHeader

# TODO update the JSON string below
json = "{}"
# create an instance of SharedmemoryHeader from a JSON string
sharedmemory_header_instance = SharedmemoryHeader.from_json(json)
# print the JSON string representation of the object
print(SharedmemoryHeader.to_json())

# convert the object into a dict
sharedmemory_header_dict = sharedmemory_header_instance.to_dict()
# create an instance of SharedmemoryHeader from a dict
sharedmemory_header_from_dict = SharedmemoryHeader.from_dict(sharedmemory_header_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


