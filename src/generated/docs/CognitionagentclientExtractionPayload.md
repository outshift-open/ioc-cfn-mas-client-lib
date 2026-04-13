# CognitionagentclientExtractionPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | **object** | Data contains the extraction payload and its structure depends on Metadata.Format.  Supported formats: \&quot;observe-sdk-otel\&quot; and \&quot;openclaw  1. format &#x3D; \&quot;observe-sdk-otel\&quot;    - Data MUST be a JSON array of ExtractionDataRecord objects.    - Example: [   { TraceId, SpanId, ParentSpanId, SpanName, ServiceName, SpanAttributes, Duration } ]  2. format &#x3D; \&quot;openclaw\&quot;    - Data is an opaque JSON payload.    - The structure is not interpreted or validated by this service and is processed as-is.  Clients MUST ensure the Data field matches the structure required by the specified Metadata.Format. | [optional] 
**metadata** | [**CognitionagentclientExtractionPayloadMetadata**](CognitionagentclientExtractionPayloadMetadata.md) | Metadata describes the format and interpretation of the payload. | [optional] 

## Example

```python
from generated.models.cognitionagentclient_extraction_payload import CognitionagentclientExtractionPayload

# TODO update the JSON string below
json = "{}"
# create an instance of CognitionagentclientExtractionPayload from a JSON string
cognitionagentclient_extraction_payload_instance = CognitionagentclientExtractionPayload.from_json(json)
# print the JSON string representation of the object
print(CognitionagentclientExtractionPayload.to_json())

# convert the object into a dict
cognitionagentclient_extraction_payload_dict = cognitionagentclient_extraction_payload_instance.to_dict()
# create an instance of CognitionagentclientExtractionPayload from a dict
cognitionagentclient_extraction_payload_from_dict = CognitionagentclientExtractionPayload.from_dict(cognitionagentclient_extraction_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


