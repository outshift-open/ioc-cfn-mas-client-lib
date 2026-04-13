# generated.SemanticNegotiationApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_workspaces_workspace_id_multi_agentic_systems_mas_id_semantic_negotiation_decide_post**](SemanticNegotiationApi.md#api_workspaces_workspace_id_multi_agentic_systems_mas_id_semantic_negotiation_decide_post) | **POST** /api/workspaces/{workspaceId}/multi-agentic-systems/{masId}/semantic-negotiation/decide | Advance semantic negotiation session
[**api_workspaces_workspace_id_multi_agentic_systems_mas_id_semantic_negotiation_start_post**](SemanticNegotiationApi.md#api_workspaces_workspace_id_multi_agentic_systems_mas_id_semantic_negotiation_start_post) | **POST** /api/workspaces/{workspaceId}/multi-agentic-systems/{masId}/semantic-negotiation/start | Start semantic negotiation session


# **api_workspaces_workspace_id_multi_agentic_systems_mas_id_semantic_negotiation_decide_post**
> SemanticnegotiationResponse api_workspaces_workspace_id_multi_agentic_systems_mas_id_semantic_negotiation_decide_post(workspace_id, mas_id, body)

Advance semantic negotiation session

Advances an existing semantic negotiation session with agent replies.

### Example


```python
import generated
from generated.models.semanticnegotiation_decide_request import SemanticnegotiationDecideRequest
from generated.models.semanticnegotiation_response import SemanticnegotiationResponse
from generated.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = generated.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with generated.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = generated.SemanticNegotiationApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace ID
    mas_id = 'mas_id_example' # str | Multi-Agentic System ID
    body = generated.SemanticnegotiationDecideRequest() # SemanticnegotiationDecideRequest | Semantic negotiation decide request

    try:
        # Advance semantic negotiation session
        api_response = api_instance.api_workspaces_workspace_id_multi_agentic_systems_mas_id_semantic_negotiation_decide_post(workspace_id, mas_id, body)
        print("The response of SemanticNegotiationApi->api_workspaces_workspace_id_multi_agentic_systems_mas_id_semantic_negotiation_decide_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SemanticNegotiationApi->api_workspaces_workspace_id_multi_agentic_systems_mas_id_semantic_negotiation_decide_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace ID | 
 **mas_id** | **str**| Multi-Agentic System ID | 
 **body** | [**SemanticnegotiationDecideRequest**](SemanticnegotiationDecideRequest.md)| Semantic negotiation decide request | 

### Return type

[**SemanticnegotiationResponse**](SemanticnegotiationResponse.md)

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

# **api_workspaces_workspace_id_multi_agentic_systems_mas_id_semantic_negotiation_start_post**
> SemanticnegotiationResponse api_workspaces_workspace_id_multi_agentic_systems_mas_id_semantic_negotiation_start_post(workspace_id, mas_id, body)

Start semantic negotiation session

Initiates a new semantic negotiation session with multiple agents.

### Example


```python
import generated
from generated.models.semanticnegotiation_response import SemanticnegotiationResponse
from generated.models.semanticnegotiation_start_request import SemanticnegotiationStartRequest
from generated.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = generated.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with generated.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = generated.SemanticNegotiationApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace ID
    mas_id = 'mas_id_example' # str | Multi-Agentic System ID
    body = generated.SemanticnegotiationStartRequest() # SemanticnegotiationStartRequest | Semantic negotiation start request

    try:
        # Start semantic negotiation session
        api_response = api_instance.api_workspaces_workspace_id_multi_agentic_systems_mas_id_semantic_negotiation_start_post(workspace_id, mas_id, body)
        print("The response of SemanticNegotiationApi->api_workspaces_workspace_id_multi_agentic_systems_mas_id_semantic_negotiation_start_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SemanticNegotiationApi->api_workspaces_workspace_id_multi_agentic_systems_mas_id_semantic_negotiation_start_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace ID | 
 **mas_id** | **str**| Multi-Agentic System ID | 
 **body** | [**SemanticnegotiationStartRequest**](SemanticnegotiationStartRequest.md)| Semantic negotiation start request | 

### Return type

[**SemanticnegotiationResponse**](SemanticnegotiationResponse.md)

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

