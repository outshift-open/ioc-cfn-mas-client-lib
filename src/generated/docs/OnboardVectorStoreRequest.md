# OnboardVectorStoreRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**request_id** | **str** | ID of the request, optional. If not provided, a random UUID is used to represent the request | [optional] 
**header** | [**Header**](Header.md) |  | [optional] 

## Example

```python
from generated.models.onboard_vector_store_request import OnboardVectorStoreRequest

# TODO update the JSON string below
json = "{}"
# create an instance of OnboardVectorStoreRequest from a JSON string
onboard_vector_store_request_instance = OnboardVectorStoreRequest.from_json(json)
# print the JSON string representation of the object
print(OnboardVectorStoreRequest.to_json())

# convert the object into a dict
onboard_vector_store_request_dict = onboard_vector_store_request_instance.to_dict()
# create an instance of OnboardVectorStoreRequest from a dict
onboard_vector_store_request_from_dict = OnboardVectorStoreRequest.from_dict(onboard_vector_store_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


