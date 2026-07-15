# generated.L9MessagesApi

All URIs are relative to *http://localhost:9002*

Method | HTTP request | Description
------------- | ------------- | -------------
[**forward_l9_message**](L9MessagesApi.md#forward_l9_message) | **POST** /api/l9/messages | Forward L9 protocol messages to cognition engines


# **forward_l9_message**
> object forward_l9_message(forward_l9_message_request)

Forward L9 protocol messages to cognition engines

Receives L9 (SSTP) protocol messages and routes them to the appropriate
cognition engine based on message kind, subkind, workspace, and MAS.

The handler validates the message, extracts routing information from
participants.groups, finds the matching CE, and forwards the message.

Supported message kinds: intent, contingency, exchange, commit, knowledge.

### Example


```python
import generated
from generated.models.forward_l9_message_request import ForwardL9MessageRequest
from generated.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:9002
# See configuration.py for a list of all supported configuration parameters.
configuration = generated.Configuration(
    host = "http://localhost:9002"
)


# Enter a context with an instance of the API client
with generated.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = generated.L9MessagesApi(api_client)
    forward_l9_message_request = generated.ForwardL9MessageRequest() # ForwardL9MessageRequest | L9 protocol message conforming to SSTP specification

    try:
        # Forward L9 protocol messages to cognition engines
        api_response = api_instance.forward_l9_message(forward_l9_message_request)
        print("The response of L9MessagesApi->forward_l9_message:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling L9MessagesApi->forward_l9_message: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **forward_l9_message_request** | [**ForwardL9MessageRequest**](ForwardL9MessageRequest.md)| L9 protocol message conforming to SSTP specification | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Message successfully routed and processed by CE |  -  |
**400** | Invalid L9 message or validation error |  -  |
**404** | No cognition engine found for the routing criteria |  -  |
**500** | Internal server error or ambiguous routing |  -  |
**502** | Failed to reach cognition engine |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

