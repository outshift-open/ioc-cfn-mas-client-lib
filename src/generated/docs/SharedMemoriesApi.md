# generated.SharedMemoriesApi

All URIs are relative to *http://localhost:9002*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_or_update_shared_memories**](SharedMemoriesApi.md#create_or_update_shared_memories) | **POST** /api/workspaces/{workspaceId}/multi-agentic-systems/{masId}/shared-memories | Create or update shared memories (async)
[**fetch_shared_memories**](SharedMemoriesApi.md#fetch_shared_memories) | **POST** /api/workspaces/{workspaceId}/multi-agentic-systems/{masId}/shared-memories/query | Fetch shared memories
[**onboard_vector_store**](SharedMemoriesApi.md#onboard_vector_store) | **POST** /api/workspaces/{workspaceId}/shared-memories/vector-store | Onboard shared memory vector store


# **create_or_update_shared_memories**
> CreateOrUpdateAcceptedResponse create_or_update_shared_memories(workspace_id, mas_id, create_or_update_request)

Create or update shared memories (async)

Accepts a request to create or update shared memories and processes it asynchronously.
Returns 202 Accepted immediately. The extraction and storage operations run in the background.
The response_id in the response can be used for log correlation.

### Example


```python
import generated
from generated.models.create_or_update_accepted_response import CreateOrUpdateAcceptedResponse
from generated.models.create_or_update_request import CreateOrUpdateRequest
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
    api_instance = generated.SharedMemoriesApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace ID
    mas_id = 'mas_id_example' # str | Multi-Agentic System ID
    create_or_update_request = generated.CreateOrUpdateRequest() # CreateOrUpdateRequest | Create or update shared memories request

    try:
        # Create or update shared memories (async)
        api_response = api_instance.create_or_update_shared_memories(workspace_id, mas_id, create_or_update_request)
        print("The response of SharedMemoriesApi->create_or_update_shared_memories:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SharedMemoriesApi->create_or_update_shared_memories: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace ID | 
 **mas_id** | **str**| Multi-Agentic System ID | 
 **create_or_update_request** | [**CreateOrUpdateRequest**](CreateOrUpdateRequest.md)| Create or update shared memories request | 

### Return type

[**CreateOrUpdateAcceptedResponse**](CreateOrUpdateAcceptedResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Request accepted for asynchronous processing |  -  |
**400** | Invalid request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **fetch_shared_memories**
> QueryResponse fetch_shared_memories(workspace_id, mas_id, query_request)

Fetch shared memories

Queries shared memories for a given workspace and multi-agentic
system using a graph path query.

### Example


```python
import generated
from generated.models.query_request import QueryRequest
from generated.models.query_response import QueryResponse
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
    api_instance = generated.SharedMemoriesApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace ID
    mas_id = 'mas_id_example' # str | Multi-Agentic System ID
    query_request = generated.QueryRequest() # QueryRequest | Query request

    try:
        # Fetch shared memories
        api_response = api_instance.fetch_shared_memories(workspace_id, mas_id, query_request)
        print("The response of SharedMemoriesApi->fetch_shared_memories:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SharedMemoriesApi->fetch_shared_memories: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace ID | 
 **mas_id** | **str**| Multi-Agentic System ID | 
 **query_request** | [**QueryRequest**](QueryRequest.md)| Query request | 

### Return type

[**QueryResponse**](QueryResponse.md)

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

# **onboard_vector_store**
> OnboardVectorStoreResponse onboard_vector_store(workspace_id, onboard_vector_store_request=onboard_vector_store_request)

Onboard shared memory vector store

Creates a vector store for shared memories within a workspace.
This initializes the vector database storage for knowledge graph embeddings.

### Example


```python
import generated
from generated.models.onboard_vector_store_request import OnboardVectorStoreRequest
from generated.models.onboard_vector_store_response import OnboardVectorStoreResponse
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
    api_instance = generated.SharedMemoriesApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace ID
    onboard_vector_store_request = generated.OnboardVectorStoreRequest() # OnboardVectorStoreRequest | Optional onboarding request with metadata (optional)

    try:
        # Onboard shared memory vector store
        api_response = api_instance.onboard_vector_store(workspace_id, onboard_vector_store_request=onboard_vector_store_request)
        print("The response of SharedMemoriesApi->onboard_vector_store:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SharedMemoriesApi->onboard_vector_store: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace ID | 
 **onboard_vector_store_request** | [**OnboardVectorStoreRequest**](OnboardVectorStoreRequest.md)| Optional onboarding request with metadata | [optional] 

### Return type

[**OnboardVectorStoreResponse**](OnboardVectorStoreResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Vector store successfully onboarded |  -  |
**400** | Invalid request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

