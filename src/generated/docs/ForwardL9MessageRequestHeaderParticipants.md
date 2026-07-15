# ForwardL9MessageRequestHeaderParticipants


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**actors** | [**List[ForwardL9MessageRequestHeaderParticipantsActorsInner]**](ForwardL9MessageRequestHeaderParticipantsActorsInner.md) |  | 
**groups** | [**ForwardL9MessageRequestHeaderParticipantsGroups**](ForwardL9MessageRequestHeaderParticipantsGroups.md) |  | 

## Example

```python
from generated.models.forward_l9_message_request_header_participants import ForwardL9MessageRequestHeaderParticipants

# TODO update the JSON string below
json = "{}"
# create an instance of ForwardL9MessageRequestHeaderParticipants from a JSON string
forward_l9_message_request_header_participants_instance = ForwardL9MessageRequestHeaderParticipants.from_json(json)
# print the JSON string representation of the object
print(ForwardL9MessageRequestHeaderParticipants.to_json())

# convert the object into a dict
forward_l9_message_request_header_participants_dict = forward_l9_message_request_header_participants_instance.to_dict()
# create an instance of ForwardL9MessageRequestHeaderParticipants from a dict
forward_l9_message_request_header_participants_from_dict = ForwardL9MessageRequestHeaderParticipants.from_dict(forward_l9_message_request_header_participants_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


