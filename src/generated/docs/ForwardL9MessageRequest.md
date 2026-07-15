# ForwardL9MessageRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**header** | [**ForwardL9MessageRequestHeader**](ForwardL9MessageRequestHeader.md) |  | 
**payload** | [**ForwardL9MessageRequestPayload**](ForwardL9MessageRequestPayload.md) |  | 

## Example

```python
from generated.models.forward_l9_message_request import ForwardL9MessageRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ForwardL9MessageRequest from a JSON string
forward_l9_message_request_instance = ForwardL9MessageRequest.from_json(json)
# print the JSON string representation of the object
print(ForwardL9MessageRequest.to_json())

# convert the object into a dict
forward_l9_message_request_dict = forward_l9_message_request_instance.to_dict()
# create an instance of ForwardL9MessageRequest from a dict
forward_l9_message_request_from_dict = ForwardL9MessageRequest.from_dict(forward_l9_message_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


