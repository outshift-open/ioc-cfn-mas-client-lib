# MetricRecord


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**timestamp** | **datetime** | When the metric was recorded | 
**workspace_id** | **UUID** | Workspace identifier | 
**mas_id** | **UUID** | MAS instance identifier | 
**agent_id** | **str** | Agent identifier | 
**metric_name** | **str** | Metric name (dot-notation) | 
**value** | **float** | Numeric metric value | 
**attributes** | **Dict[str, object]** | Flexible metadata stored as JSON | 

## Example

```python
from generated.models.metric_record import MetricRecord

# TODO update the JSON string below
json = "{}"
# create an instance of MetricRecord from a JSON string
metric_record_instance = MetricRecord.from_json(json)
# print the JSON string representation of the object
print(MetricRecord.to_json())

# convert the object into a dict
metric_record_dict = metric_record_instance.to_dict()
# create an instance of MetricRecord from a dict
metric_record_from_dict = MetricRecord.from_dict(metric_record_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


