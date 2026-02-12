# generated.CfnApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_cfn_dummy_get**](CfnApi.md#api_v1_cfn_dummy_get) | **GET** /api/v1/cfn/dummy | Get CFN dummy data


# **api_v1_cfn_dummy_get**
> object api_v1_cfn_dummy_get()

Get CFN dummy data

Returns mock CFN data

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
    api_instance = generated.CfnApi(api_client)

    try:
        # Get CFN dummy data
        api_response = api_instance.api_v1_cfn_dummy_get()
        print("The response of CfnApi->api_v1_cfn_dummy_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CfnApi->api_v1_cfn_dummy_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

