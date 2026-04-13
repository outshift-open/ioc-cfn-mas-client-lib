# CognitionagentclientExtractionPayloadMetadata


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**format** | **str** | Format specifies how the Data field should be interpreted.  Supported values: - \&quot;observe-sdk-otel\&quot;: Data is a JSON array of ExtractionDataRecord - \&quot;openclaw\&quot;: Data is an opaque JSON payload | [optional] 

## Example

```python
from generated.models.cognitionagentclient_extraction_payload_metadata import CognitionagentclientExtractionPayloadMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of CognitionagentclientExtractionPayloadMetadata from a JSON string
cognitionagentclient_extraction_payload_metadata_instance = CognitionagentclientExtractionPayloadMetadata.from_json(json)
# print the JSON string representation of the object
print(CognitionagentclientExtractionPayloadMetadata.to_json())

# convert the object into a dict
cognitionagentclient_extraction_payload_metadata_dict = cognitionagentclient_extraction_payload_metadata_instance.to_dict()
# create an instance of CognitionagentclientExtractionPayloadMetadata from a dict
cognitionagentclient_extraction_payload_metadata_from_dict = CognitionagentclientExtractionPayloadMetadata.from_dict(cognitionagentclient_extraction_payload_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


