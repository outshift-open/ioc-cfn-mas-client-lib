# CreateOrUpdateResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** | Status of the request | 
**response_id** | **str** | ID of the response, this gets populated from request_id | [optional] 
**message** | **str** | Optional message providing additional information | [optional] 

## Example

```python
from generated.models.create_or_update_response import CreateOrUpdateResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateOrUpdateResponse from a JSON string
create_or_update_response_instance = CreateOrUpdateResponse.from_json(json)
# print the JSON string representation of the object
print(CreateOrUpdateResponse.to_json())

# convert the object into a dict
create_or_update_response_dict = create_or_update_response_instance.to_dict()
# create an instance of CreateOrUpdateResponse from a dict
create_or_update_response_from_dict = CreateOrUpdateResponse.from_dict(create_or_update_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


