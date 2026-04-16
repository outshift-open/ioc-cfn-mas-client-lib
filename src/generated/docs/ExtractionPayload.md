# ExtractionPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**ExtractionPayloadMetadata**](ExtractionPayloadMetadata.md) |  | 
**data** | **object** | Data contains the extraction payload and its structure depends on Metadata.Format.  Supported formats: \&quot;observe-sdk-otel\&quot; and \&quot;openclaw\&quot;  1. format &#x3D; \&quot;observe-sdk-otel\&quot;    - Data MUST be a JSON array of ExtractionDataRecord objects.    - Example: [   { TraceId, SpanId, ParentSpanId, SpanName, ServiceName, SpanAttributes, Duration } ]  2. format &#x3D; \&quot;openclaw\&quot;    - Data is an opaque JSON payload.    - The structure is not interpreted or validated by this service and is processed as-is.  Clients MUST ensure the Data field matches the structure required by the specified Metadata.Format. | 

## Example

```python
from generated.models.extraction_payload import ExtractionPayload

# TODO update the JSON string below
json = "{}"
# create an instance of ExtractionPayload from a JSON string
extraction_payload_instance = ExtractionPayload.from_json(json)
# print the JSON string representation of the object
print(ExtractionPayload.to_json())

# convert the object into a dict
extraction_payload_dict = extraction_payload_instance.to_dict()
# create an instance of ExtractionPayload from a dict
extraction_payload_from_dict = ExtractionPayload.from_dict(extraction_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


