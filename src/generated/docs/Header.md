# Header

Request header containing agent identification

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agent_id** | **str** | ID that represents the agent, optional for query operations | [optional] 

## Example

```python
from generated.models.header import Header

# TODO update the JSON string below
json = "{}"
# create an instance of Header from a JSON string
header_instance = Header.from_json(json)
# print the JSON string representation of the object
print(Header.to_json())

# convert the object into a dict
header_dict = header_instance.to_dict()
# create an instance of Header from a dict
header_from_dict = Header.from_dict(header_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


