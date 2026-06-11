# MetricsPeriod


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start** | **datetime** | Start of time range | 
**end** | **datetime** | End of time range | 

## Example

```python
from generated.models.metrics_period import MetricsPeriod

# TODO update the JSON string below
json = "{}"
# create an instance of MetricsPeriod from a JSON string
metrics_period_instance = MetricsPeriod.from_json(json)
# print the JSON string representation of the object
print(MetricsPeriod.to_json())

# convert the object into a dict
metrics_period_dict = metrics_period_instance.to_dict()
# create an instance of MetricsPeriod from a dict
metrics_period_from_dict = MetricsPeriod.from_dict(metrics_period_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


