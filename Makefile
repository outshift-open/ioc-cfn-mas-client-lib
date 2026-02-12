OPENAPI_SPEC ?= openapi/openapi.json
OPENAPI_GENERATOR ?= openapi-generator

GEN_PKG ?= generated
GEN_OUT ?= src

.PHONY: gen-openapi
gen-openapi:
	@echo "Generating OpenAPI Python SDK to $(GEN_OUT)"
#	@rm -rf $(GEN_OUT)
	@mkdir -p $(GEN_OUT)
	@$(OPENAPI_GENERATOR) generate \
		-i $(OPENAPI_SPEC) \
		-g python \
		-o $(GEN_OUT) \
		--package-name $(GEN_PKG) \
		--additional-properties=projectName=$(GEN_PKG),packageVersion=0.1.0,generateSourceCodeOnly=true
