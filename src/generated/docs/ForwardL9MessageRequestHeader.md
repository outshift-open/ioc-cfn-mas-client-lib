# ForwardL9MessageRequestHeader


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**protocol** | **str** |  | 
**version** | **str** |  | 
**subprotocol** | **str** |  | 
**kind** | **str** |  | 
**subkind** | **str** |  | [optional] 
**participants** | [**ForwardL9MessageRequestHeaderParticipants**](ForwardL9MessageRequestHeaderParticipants.md) |  | 

## Example

```python
from generated.models.forward_l9_message_request_header import ForwardL9MessageRequestHeader

# TODO update the JSON string below
json = "{}"
# create an instance of ForwardL9MessageRequestHeader from a JSON string
forward_l9_message_request_header_instance = ForwardL9MessageRequestHeader.from_json(json)
# print the JSON string representation of the object
print(ForwardL9MessageRequestHeader.to_json())

# convert the object into a dict
forward_l9_message_request_header_dict = forward_l9_message_request_header_instance.to_dict()
# create an instance of ForwardL9MessageRequestHeader from a dict
forward_l9_message_request_header_from_dict = ForwardL9MessageRequestHeader.from_dict(forward_l9_message_request_header_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


