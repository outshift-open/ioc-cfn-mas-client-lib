# generated.MetricsApi

All URIs are relative to *http://localhost:9002*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_metrics**](MetricsApi.md#get_metrics) | **GET** /api/cognition-engine/metrics | Query metrics within time range


# **get_metrics**
> MetricsQueryResponse get_metrics(start_time, end_time, workspace_id=workspace_id, mas_id=mas_id, agent_id=agent_id, metric_name=metric_name, limit=limit, offset=offset)

Query metrics within time range

Returns raw metric data points filtered by time and optional dimensions.
Supports filtering by workspace, MAS, agent, and metric name with wildcard support.
Use pagination for large result sets.

### Example


```python
import generated
from generated.models.metrics_query_response import MetricsQueryResponse
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
    api_instance = generated.MetricsApi(api_client)
    start_time = '2026-05-19' # str | Start time (inclusive). Supports multiple formats: - Unix timestamp (seconds): `1716076800` - Unix timestamp (milliseconds): `1716076800000` - RFC3339: `2026-05-19T00:00:00Z` - Date-only: `2026-05-19` (assumes UTC midnight) 
    end_time = '2026-05-20' # str | End time (exclusive). Supports multiple formats: - Unix timestamp (seconds): `1716163200` - Unix timestamp (milliseconds): `1716163200000` - RFC3339: `2026-05-20T00:00:00Z` - Date-only: `2026-05-20` (assumes UTC midnight) 
    workspace_id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Filter by workspace UUID (optional)
    mas_id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Filter by MAS UUID (optional)
    agent_id = 'agent_id_example' # str | Filter by agent ID (optional)
    metric_name = 'llm.token.*' # str | Filter by metric name (supports * wildcard, e.g., llm.token.*) (optional)
    limit = 1000 # int | Maximum results per page (default 1000, max 10000) (optional) (default to 1000)
    offset = 0 # int | Pagination offset (default 0) (optional) (default to 0)

    try:
        # Query metrics within time range
        api_response = api_instance.get_metrics(start_time, end_time, workspace_id=workspace_id, mas_id=mas_id, agent_id=agent_id, metric_name=metric_name, limit=limit, offset=offset)
        print("The response of MetricsApi->get_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MetricsApi->get_metrics: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_time** | **str**| Start time (inclusive). Supports multiple formats: - Unix timestamp (seconds): &#x60;1716076800&#x60; - Unix timestamp (milliseconds): &#x60;1716076800000&#x60; - RFC3339: &#x60;2026-05-19T00:00:00Z&#x60; - Date-only: &#x60;2026-05-19&#x60; (assumes UTC midnight)  | 
 **end_time** | **str**| End time (exclusive). Supports multiple formats: - Unix timestamp (seconds): &#x60;1716163200&#x60; - Unix timestamp (milliseconds): &#x60;1716163200000&#x60; - RFC3339: &#x60;2026-05-20T00:00:00Z&#x60; - Date-only: &#x60;2026-05-20&#x60; (assumes UTC midnight)  | 
 **workspace_id** | **UUID**| Filter by workspace UUID | [optional] 
 **mas_id** | **UUID**| Filter by MAS UUID | [optional] 
 **agent_id** | **str**| Filter by agent ID | [optional] 
 **metric_name** | **str**| Filter by metric name (supports * wildcard, e.g., llm.token.*) | [optional] 
 **limit** | **int**| Maximum results per page (default 1000, max 10000) | [optional] [default to 1000]
 **offset** | **int**| Pagination offset (default 0) | [optional] [default to 0]

### Return type

[**MetricsQueryResponse**](MetricsQueryResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Query successful |  -  |
**400** | Invalid query parameters |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

