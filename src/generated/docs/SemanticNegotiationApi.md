# generated.SemanticNegotiationApi

All URIs are relative to *http://localhost:9002*

Method | HTTP request | Description
------------- | ------------- | -------------
[**decide_semantic_negotiation**](SemanticNegotiationApi.md#decide_semantic_negotiation) | **POST** /api/workspaces/{workspaceId}/multi-agentic-systems/{masId}/semantic-negotiation/decide | Advance semantic negotiation session
[**start_semantic_negotiation**](SemanticNegotiationApi.md#start_semantic_negotiation) | **POST** /api/workspaces/{workspaceId}/multi-agentic-systems/{masId}/semantic-negotiation/start | Start semantic negotiation session


# **decide_semantic_negotiation**
> NegotiationResponse decide_semantic_negotiation(workspace_id, mas_id, decide_request)

Advance semantic negotiation session

Advances an existing semantic negotiation session with agent replies.

### Example


```python
import generated
from generated.models.decide_request import DecideRequest
from generated.models.negotiation_response import NegotiationResponse
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
    api_instance = generated.SemanticNegotiationApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace ID
    mas_id = 'mas_id_example' # str | Multi-Agentic System ID
    decide_request = generated.DecideRequest() # DecideRequest | Semantic negotiation decide request

    try:
        # Advance semantic negotiation session
        api_response = api_instance.decide_semantic_negotiation(workspace_id, mas_id, decide_request)
        print("The response of SemanticNegotiationApi->decide_semantic_negotiation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SemanticNegotiationApi->decide_semantic_negotiation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace ID | 
 **mas_id** | **str**| Multi-Agentic System ID | 
 **decide_request** | [**DecideRequest**](DecideRequest.md)| Semantic negotiation decide request | 

### Return type

[**NegotiationResponse**](NegotiationResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Negotiation step executed successfully |  -  |
**400** | Invalid request |  -  |
**404** | Session not found |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_semantic_negotiation**
> NegotiationResponse start_semantic_negotiation(workspace_id, mas_id, start_request)

Start semantic negotiation session

Initiates a new semantic negotiation session with multiple agents.

### Example


```python
import generated
from generated.models.negotiation_response import NegotiationResponse
from generated.models.start_request import StartRequest
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
    api_instance = generated.SemanticNegotiationApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace ID
    mas_id = 'mas_id_example' # str | Multi-Agentic System ID
    start_request = generated.StartRequest() # StartRequest | Semantic negotiation start request

    try:
        # Start semantic negotiation session
        api_response = api_instance.start_semantic_negotiation(workspace_id, mas_id, start_request)
        print("The response of SemanticNegotiationApi->start_semantic_negotiation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SemanticNegotiationApi->start_semantic_negotiation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace ID | 
 **mas_id** | **str**| Multi-Agentic System ID | 
 **start_request** | [**StartRequest**](StartRequest.md)| Semantic negotiation start request | 

### Return type

[**NegotiationResponse**](NegotiationResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Negotiation session started successfully |  -  |
**400** | Invalid request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

