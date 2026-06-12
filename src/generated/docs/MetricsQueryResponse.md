# MetricsQueryResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**period** | [**MetricsPeriod**](MetricsPeriod.md) |  | 
**filters** | [**MetricsFilters**](MetricsFilters.md) |  | [optional] 
**pagination** | [**MetricsPagination**](MetricsPagination.md) |  | 
**metrics** | [**List[MetricRecord]**](MetricRecord.md) | Array of metric data points | 

## Example

```python
from generated.models.metrics_query_response import MetricsQueryResponse

# TODO update the JSON string below
json = "{}"
# create an instance of MetricsQueryResponse from a JSON string
metrics_query_response_instance = MetricsQueryResponse.from_json(json)
# print the JSON string representation of the object
print(MetricsQueryResponse.to_json())

# convert the object into a dict
metrics_query_response_dict = metrics_query_response_instance.to_dict()
# create an instance of MetricsQueryResponse from a dict
metrics_query_response_from_dict = MetricsQueryResponse.from_dict(metrics_query_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


