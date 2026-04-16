# ExtractionPayloadMetadata


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**format** | **str** | Format specifies how the Data field should be interpreted.  Supported values: - \&quot;observe-sdk-otel\&quot;: Data is a JSON array of ExtractionDataRecord - \&quot;openclaw\&quot;: Data is an opaque JSON payload | 

## Example

```python
from generated.models.extraction_payload_metadata import ExtractionPayloadMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of ExtractionPayloadMetadata from a JSON string
extraction_payload_metadata_instance = ExtractionPayloadMetadata.from_json(json)
# print the JSON string representation of the object
print(ExtractionPayloadMetadata.to_json())

# convert the object into a dict
extraction_payload_metadata_dict = extraction_payload_metadata_instance.to_dict()
# create an instance of ExtractionPayloadMetadata from a dict
extraction_payload_metadata_from_dict = ExtractionPayloadMetadata.from_dict(extraction_payload_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


