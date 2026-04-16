# OnboardVectorStoreResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**response_id** | **str** | ID of the response, this gets populated from request_id | [optional] 
**status** | **str** | Status of the request | 
**message** | **str** | Optional message providing additional information | [optional] 
**store_id** | **str** | ID of the vector store | [optional] 

## Example

```python
from generated.models.onboard_vector_store_response import OnboardVectorStoreResponse

# TODO update the JSON string below
json = "{}"
# create an instance of OnboardVectorStoreResponse from a JSON string
onboard_vector_store_response_instance = OnboardVectorStoreResponse.from_json(json)
# print the JSON string representation of the object
print(OnboardVectorStoreResponse.to_json())

# convert the object into a dict
onboard_vector_store_response_dict = onboard_vector_store_response_instance.to_dict()
# create an instance of OnboardVectorStoreResponse from a dict
onboard_vector_store_response_from_dict = OnboardVectorStoreResponse.from_dict(onboard_vector_store_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


