# generated.MemoryOperationsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_workspaces_workspace_id_multi_agentic_systems_mas_id_agents_agent_id_memory_operations_post**](MemoryOperationsApi.md#api_workspaces_workspace_id_multi_agentic_systems_mas_id_agents_agent_id_memory_operations_post) | **POST** /api/workspaces/{workspaceId}/multi-agentic-systems/{masId}/agents/{agentId}/memory-operations | Proxy API requests to a remote memory provider


# **api_workspaces_workspace_id_multi_agentic_systems_mas_id_agents_agent_id_memory_operations_post**
> MemoryoperationsMemoryOperationResponse api_workspaces_workspace_id_multi_agentic_systems_mas_id_agents_agent_id_memory_operations_post(workspace_id, mas_id, agent_id, body)

Proxy API requests to a remote memory provider

Forwards REST API requests to a remote memory provider (Mem0, Graphiti, etc.) for agent-specific memory operations.
The memory provider base URL and auth credentials are auto-resolved from management plane config based on workspace/MAS/agent IDs.
The `http-url` field should contain the relative path and query parameters to append to the provider base URL.

**GET example** — retrieve memories:
```json
{
"header": {},
"payload": {
"http-request-type": "GET",
"http-url": "v1/memories/?user_id=curl-test-user",
"http-request-body": {},
"http-headers": {}
}
}
```

**POST example** — add memories:
```json
{
"header": {},
"payload": {
"http-request-type": "POST",
"http-url": "/v1/memories/",
"http-request-body": {
"messages": [{"role": "user", "content": "I prefer dark mode in all my apps"}],
"user_id": "curl-test-user"
},
"http-headers": {}
}
}
```

### Example


```python
import generated
from generated.models.memoryoperations_memory_operation_request import MemoryoperationsMemoryOperationRequest
from generated.models.memoryoperations_memory_operation_response import MemoryoperationsMemoryOperationResponse
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
    api_instance = generated.MemoryOperationsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace ID
    mas_id = 'mas_id_example' # str | Multi-Agentic System ID
    agent_id = 'agent_id_example' # str | Agent ID
    body = generated.MemoryoperationsMemoryOperationRequest() # MemoryoperationsMemoryOperationRequest | Memory operation request

    try:
        # Proxy API requests to a remote memory provider
        api_response = api_instance.api_workspaces_workspace_id_multi_agentic_systems_mas_id_agents_agent_id_memory_operations_post(workspace_id, mas_id, agent_id, body)
        print("The response of MemoryOperationsApi->api_workspaces_workspace_id_multi_agentic_systems_mas_id_agents_agent_id_memory_operations_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MemoryOperationsApi->api_workspaces_workspace_id_multi_agentic_systems_mas_id_agents_agent_id_memory_operations_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace ID | 
 **mas_id** | **str**| Multi-Agentic System ID | 
 **agent_id** | **str**| Agent ID | 
 **body** | [**MemoryoperationsMemoryOperationRequest**](MemoryoperationsMemoryOperationRequest.md)| Memory operation request | 

### Return type

[**MemoryoperationsMemoryOperationResponse**](MemoryoperationsMemoryOperationResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Proxied response (actual provider status is in http-status field) |  -  |
**400** | Invalid request body or missing http-request-type |  -  |
**404** | Memory provider config not found for agent |  -  |
**502** | Failed to forward request to memory provider |  -  |
**503** | Memory proxy client not configured |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

