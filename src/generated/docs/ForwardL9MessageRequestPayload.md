# ForwardL9MessageRequestPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**data** | **Dict[str, object]** |  | 

## Example

```python
from generated.models.forward_l9_message_request_payload import ForwardL9MessageRequestPayload

# TODO update the JSON string below
json = "{}"
# create an instance of ForwardL9MessageRequestPayload from a JSON string
forward_l9_message_request_payload_instance = ForwardL9MessageRequestPayload.from_json(json)
# print the JSON string representation of the object
print(ForwardL9MessageRequestPayload.to_json())

# convert the object into a dict
forward_l9_message_request_payload_dict = forward_l9_message_request_payload_instance.to_dict()
# create an instance of ForwardL9MessageRequestPayload from a dict
forward_l9_message_request_payload_from_dict = ForwardL9MessageRequestPayload.from_dict(forward_l9_message_request_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


