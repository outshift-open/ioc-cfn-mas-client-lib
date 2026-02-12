# generated.SharedMemoriesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_workspaces_workspace_id_multi_agentic_systems_system_id_shared_memories_post**](SharedMemoriesApi.md#api_workspaces_workspace_id_multi_agentic_systems_system_id_shared_memories_post) | **POST** /api/workspaces/{workspaceId}/multi-agentic-systems/{systemId}/shared-memories | Upsert shared memories
[**api_workspaces_workspace_id_multi_agentic_systems_system_id_shared_memories_query_post**](SharedMemoriesApi.md#api_workspaces_workspace_id_multi_agentic_systems_system_id_shared_memories_query_post) | **POST** /api/workspaces/{workspaceId}/multi-agentic-systems/{systemId}/shared-memories/query | Query shared memories


# **api_workspaces_workspace_id_multi_agentic_systems_system_id_shared_memories_post**
> object api_workspaces_workspace_id_multi_agentic_systems_system_id_shared_memories_post(workspace_id, system_id, body)

Upsert shared memories

Upserts shared memory entries for a given workspace and multi-agentic system

### Example


```python
import generated
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
    system_id = 'system_id_example' # str | System ID
    body = None # object | Upsert request

    try:
        # Upsert shared memories
        api_response = api_instance.api_workspaces_workspace_id_multi_agentic_systems_system_id_shared_memories_post(workspace_id, system_id, body)
        print("The response of SharedMemoriesApi->api_workspaces_workspace_id_multi_agentic_systems_system_id_shared_memories_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SharedMemoriesApi->api_workspaces_workspace_id_multi_agentic_systems_system_id_shared_memories_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace ID | 
 **system_id** | **str**| System ID | 
 **body** | **object**| Upsert request | 

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
**201** | Created |  -  |
**400** | Bad Request |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_workspaces_workspace_id_multi_agentic_systems_system_id_shared_memories_query_post**
> object api_workspaces_workspace_id_multi_agentic_systems_system_id_shared_memories_query_post(workspace_id, system_id, body)

Query shared memories

Queries shared memory entries for a given workspace and multi-agentic system

### Example


```python
import generated
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
    system_id = 'system_id_example' # str | System ID
    body = None # object | Query request

    try:
        # Query shared memories
        api_response = api_instance.api_workspaces_workspace_id_multi_agentic_systems_system_id_shared_memories_query_post(workspace_id, system_id, body)
        print("The response of SharedMemoriesApi->api_workspaces_workspace_id_multi_agentic_systems_system_id_shared_memories_query_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SharedMemoriesApi->api_workspaces_workspace_id_multi_agentic_systems_system_id_shared_memories_query_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace ID | 
 **system_id** | **str**| System ID | 
 **body** | **object**| Query request | 

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
**200** | OK |  -  |
**400** | Bad Request |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

