# AlignmentResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** | Status indicates the result of the alignment step. | [optional] 
**message** | **str** | Message provides additional information about the alignment state. | [optional] 
**result** | **Dict[str, object]** | Result contains the pipeline execution result. The structure depends on the semantic alignment library implementation. | [optional] 

## Example

```python
from generated.models.alignment_response import AlignmentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AlignmentResponse from a JSON string
alignment_response_instance = AlignmentResponse.from_json(json)
# print the JSON string representation of the object
print(AlignmentResponse.to_json())

# convert the object into a dict
alignment_response_dict = alignment_response_instance.to_dict()
# create an instance of AlignmentResponse from a dict
alignment_response_from_dict = AlignmentResponse.from_dict(alignment_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


