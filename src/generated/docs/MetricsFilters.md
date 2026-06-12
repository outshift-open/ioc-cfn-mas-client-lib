# MetricsFilters


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workspace_id** | **UUID** | Workspace filter (if applied) | [optional] 
**mas_id** | **UUID** | MAS filter (if applied) | [optional] 
**agent_id** | **str** | Agent filter (if applied) | [optional] 
**metric_name** | **str** | Metric name filter (if applied, may include wildcards) | [optional] 

## Example

```python
from generated.models.metrics_filters import MetricsFilters

# TODO update the JSON string below
json = "{}"
# create an instance of MetricsFilters from a JSON string
metrics_filters_instance = MetricsFilters.from_json(json)
# print the JSON string representation of the object
print(MetricsFilters.to_json())

# convert the object into a dict
metrics_filters_dict = metrics_filters_instance.to_dict()
# create an instance of MetricsFilters from a dict
metrics_filters_from_dict = MetricsFilters.from_dict(metrics_filters_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


