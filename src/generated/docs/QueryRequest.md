# QueryRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**request_id** | **str** | ID of the request, optional. If not provided, a random UUID is used to represent the request | [optional] 
**header** | [**Header**](Header.md) |  | 
**intent** | **str** | User intent or natural-language query describing what information is being requested. This field is required and is the primary signal used to construct and execute the query | 
**search_strategy** | **str** | Search strategy to be used when executing the query. Currently supported values: \&quot;semantic_graph_traversal\&quot;. If not specified, defaults to \&quot;semantic_graph_traversal\&quot; | [optional] [default to 'semantic_graph_traversal']
**additional_context** | **List[Dict[str, object]]** | AdditionalContext provides optional contextual information to refine query execution. This may include prior conversation state, structured hints, or domain-specific metadata. The contents are treated as opaque by the API and interpreted by downstream components. Each element must be a structured object | [optional] 

## Example

```python
from generated.models.query_request import QueryRequest

# TODO update the JSON string below
json = "{}"
# create an instance of QueryRequest from a JSON string
query_request_instance = QueryRequest.from_json(json)
# print the JSON string representation of the object
print(QueryRequest.to_json())

# convert the object into a dict
query_request_dict = query_request_instance.to_dict()
# create an instance of QueryRequest from a dict
query_request_from_dict = QueryRequest.from_dict(query_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


