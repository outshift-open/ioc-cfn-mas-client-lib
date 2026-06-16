# generated.SemanticAlignmentApi

All URIs are relative to *http://localhost:9002*

Method | HTTP request | Description
------------- | ------------- | -------------
[**decide_semantic_alignment**](SemanticAlignmentApi.md#decide_semantic_alignment) | **POST** /api/workspaces/{workspaceId}/multi-agentic-systems/{masId}/semantic-alignment/decide | Advance semantic alignment session
[**start_semantic_alignment**](SemanticAlignmentApi.md#start_semantic_alignment) | **POST** /api/workspaces/{workspaceId}/multi-agentic-systems/{masId}/semantic-alignment/start | Start semantic alignment session


# **decide_semantic_alignment**
> AlignmentResponse decide_semantic_alignment(workspace_id, mas_id, decide_request)

Advance semantic alignment session

Advances an existing semantic alignment session with agent replies.

### Example


```python
import generated
from generated.models.decide_request import DecideRequest
from generated.models.alignment_response import AlignmentResponse
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
    api_instance = generated.SemanticAlignmentApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace ID
    mas_id = 'mas_id_example' # str | Multi-Agentic System ID
    decide_request = generated.DecideRequest() # DecideRequest | Semantic alignment decide request

    try:
        # Advance semantic alignment session
        api_response = api_instance.decide_semantic_alignment(workspace_id, mas_id, decide_request)
        print("The response of SemanticAlignmentApi->decide_semantic_alignment:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SemanticAlignmentApi->decide_semantic_alignment: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace ID | 
 **mas_id** | **str**| Multi-Agentic System ID | 
 **decide_request** | [**DecideRequest**](DecideRequest.md)| Semantic alignment decide request | 

### Return type

[**AlignmentResponse**](AlignmentResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Alignment step executed successfully |  -  |
**400** | Invalid request |  -  |
**404** | Session not found |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_semantic_alignment**
> AlignmentResponse start_semantic_alignment(workspace_id, mas_id, start_request)

Start semantic alignment session

Initiates a new semantic alignment session with multiple agents.

### Example


```python
import generated
from generated.models.alignment_response import AlignmentResponse
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
    api_instance = generated.SemanticAlignmentApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace ID
    mas_id = 'mas_id_example' # str | Multi-Agentic System ID
    start_request = generated.StartRequest() # StartRequest | Semantic alignment start request

    try:
        # Start semantic alignment session
        api_response = api_instance.start_semantic_alignment(workspace_id, mas_id, start_request)
        print("The response of SemanticAlignmentApi->start_semantic_alignment:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SemanticAlignmentApi->start_semantic_alignment: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace ID | 
 **mas_id** | **str**| Multi-Agentic System ID | 
 **start_request** | [**StartRequest**](StartRequest.md)| Semantic alignment start request | 

### Return type

[**AlignmentResponse**](AlignmentResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Alignment session started successfully |  -  |
**400** | Invalid request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

