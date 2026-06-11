# MetricsPagination


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**limit** | **int** | Maximum results returned | 
**offset** | **int** | Pagination offset | 
**total** | **int** | Total matching records | 

## Example

```python
from generated.models.metrics_pagination import MetricsPagination

# TODO update the JSON string below
json = "{}"
# create an instance of MetricsPagination from a JSON string
metrics_pagination_instance = MetricsPagination.from_json(json)
# print the JSON string representation of the object
print(MetricsPagination.to_json())

# convert the object into a dict
metrics_pagination_dict = metrics_pagination_instance.to_dict()
# create an instance of MetricsPagination from a dict
metrics_pagination_from_dict = MetricsPagination.from_dict(metrics_pagination_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


