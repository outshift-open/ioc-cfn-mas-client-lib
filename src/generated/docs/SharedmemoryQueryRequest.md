# SharedmemoryQueryRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**additional_context** | **List[Dict[str, object]]** | AdditionalContext provides optional contextual information to refine query execution. This may include prior conversation state, structured hints, or domain-specific metadata. The contents are treated as opaque by the API and interpreted by downstream components. Each element must be a structured object | [optional] 
**header** | [**SharedmemoryHeader**](SharedmemoryHeader.md) | Header(s) of the request, required (must include agent_id) | [optional] 
**intent** | **str** | User intent or natural-language query describing what information is being requested. This field is required and is the primary signal used to construct and execute the query | [optional] 
**request_id** | **str** | ID of the request, optional. If not provided, a random UUID is used to represent the request | [optional] 
**search_strategy** | **str** | Search strategy to be used when executing the query. Currently supported values: \&quot;semantic_graph_traversal\&quot;. If not specified, defaults to \&quot;semantic_graph_traversal\&quot; | [optional] 

## Example

```python
from generated.models.sharedmemory_query_request import SharedmemoryQueryRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SharedmemoryQueryRequest from a JSON string
sharedmemory_query_request_instance = SharedmemoryQueryRequest.from_json(json)
# print the JSON string representation of the object
print(SharedmemoryQueryRequest.to_json())

# convert the object into a dict
sharedmemory_query_request_dict = sharedmemory_query_request_instance.to_dict()
# create an instance of SharedmemoryQueryRequest from a dict
sharedmemory_query_request_from_dict = SharedmemoryQueryRequest.from_dict(sharedmemory_query_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


