# generated.SharedMemoriesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_workspaces_workspace_id_multi_agentic_systems_mas_id_shared_memories_post**](SharedMemoriesApi.md#api_workspaces_workspace_id_multi_agentic_systems_mas_id_shared_memories_post) | **POST** /api/workspaces/{workspaceId}/multi-agentic-systems/{masId}/shared-memories | Create or update shared memories.
[**api_workspaces_workspace_id_multi_agentic_systems_mas_id_shared_memories_query_post**](SharedMemoriesApi.md#api_workspaces_workspace_id_multi_agentic_systems_mas_id_shared_memories_query_post) | **POST** /api/workspaces/{workspaceId}/multi-agentic-systems/{masId}/shared-memories/query | Fetch shared memories


# **api_workspaces_workspace_id_multi_agentic_systems_mas_id_shared_memories_post**
> SharedmemoryCreateOrUpdateResponse api_workspaces_workspace_id_multi_agentic_systems_mas_id_shared_memories_post(workspace_id, mas_id, body=body)

Create or update shared memories.

Creates or updates shared memories with entries (concepts and relations) extracted from the provided trace or OpenClaw output for a given workspace and multi-agentic system.

### Example


```python
import generated
from generated.models.sharedmemory_create_or_update_request import SharedmemoryCreateOrUpdateRequest
from generated.models.sharedmemory_create_or_update_response import SharedmemoryCreateOrUpdateResponse
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
    api_instance = generated.SharedMemoriesApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace ID
    mas_id = 'mas_id_example' # str | Multi-Agentic System ID
    body = generated.SharedmemoryCreateOrUpdateRequest() # SharedmemoryCreateOrUpdateRequest | Create or update shared memories request (optional)

    try:
        # Create or update shared memories.
        api_response = api_instance.api_workspaces_workspace_id_multi_agentic_systems_mas_id_shared_memories_post(workspace_id, mas_id, body=body)
        print("The response of SharedMemoriesApi->api_workspaces_workspace_id_multi_agentic_systems_mas_id_shared_memories_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SharedMemoriesApi->api_workspaces_workspace_id_multi_agentic_systems_mas_id_shared_memories_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace ID | 
 **mas_id** | **str**| Multi-Agentic System ID | 
 **body** | [**SharedmemoryCreateOrUpdateRequest**](SharedmemoryCreateOrUpdateRequest.md)| Create or update shared memories request | [optional] 

### Return type

[**SharedmemoryCreateOrUpdateResponse**](SharedmemoryCreateOrUpdateResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Shared memories successfully created or updated |  -  |
**400** | Invalid request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_workspaces_workspace_id_multi_agentic_systems_mas_id_shared_memories_query_post**
> SharedmemoryQueryResponse api_workspaces_workspace_id_multi_agentic_systems_mas_id_shared_memories_query_post(workspace_id, mas_id, body)

Fetch shared memories

Queries shared memories for a given workspace and multi-agentic system using a graph path query.

### Example


```python
import generated
from generated.models.sharedmemory_query_request import SharedmemoryQueryRequest
from generated.models.sharedmemory_query_response import SharedmemoryQueryResponse
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
    api_instance = generated.SharedMemoriesApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace ID
    mas_id = 'mas_id_example' # str | Multi-Agentic System ID
    body = generated.SharedmemoryQueryRequest() # SharedmemoryQueryRequest | Query request

    try:
        # Fetch shared memories
        api_response = api_instance.api_workspaces_workspace_id_multi_agentic_systems_mas_id_shared_memories_query_post(workspace_id, mas_id, body)
        print("The response of SharedMemoriesApi->api_workspaces_workspace_id_multi_agentic_systems_mas_id_shared_memories_query_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SharedMemoriesApi->api_workspaces_workspace_id_multi_agentic_systems_mas_id_shared_memories_query_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace ID | 
 **mas_id** | **str**| Multi-Agentic System ID | 
 **body** | [**SharedmemoryQueryRequest**](SharedmemoryQueryRequest.md)| Query request | 

### Return type

[**SharedmemoryQueryResponse**](SharedmemoryQueryResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Query executed successfully |  -  |
**400** | Invalid request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

