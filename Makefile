# Copyright 2026 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

# OpenAPI spec from ioc-cfn-svc public API
OPENAPI_SPEC ?= openapi/public-api-v1.1.yaml

GEN_PKG ?= generated
GEN_OUT ?= src

.PHONY: gen-openapi
gen-openapi:
	@echo "Generating OpenAPI Python SDK from $(OPENAPI_SPEC)"
	@echo "Using Docker with openapitools/openapi-generator-cli"
	@mkdir -p $(GEN_OUT)
	@docker run --rm \
		-v "$${PWD}:/local" \
		openapitools/openapi-generator-cli generate \
		-i /local/$(OPENAPI_SPEC) \
		-g python \
		-o /local/$(GEN_OUT) \
		--package-name $(GEN_PKG) \
		--additional-properties=projectName=$(GEN_PKG),packageVersion=1.0.0,generateSourceCodeOnly=true
	@echo "✓ SDK generated successfully in $(GEN_OUT)/$(GEN_PKG)"

.PHONY: pull-openapi-generator
pull-openapi-generator:
	@echo "Pulling OpenAPI Generator Docker image"
	@docker pull openapitools/openapi-generator-cli
	@echo "✓ Docker image ready"

.PHONY: add-headers
add-headers:
	@echo "Adding copyright/license headers to all Python files"
	@docker run --rm --volume "$${PWD}:/data" fsfe/reuse annotate \
		--copyright-prefix string \
		--copyright "Cisco Systems, Inc. and its affiliates" \
		-l "Apache-2.0" \
		--skip-existing \
		**/*.py
	@echo "✓ Headers added successfully"

.PHONY: add-headers-generated
add-headers-generated:
	@echo "Adding copyright/license headers to generated Python files"
	@docker run --rm --volume "$${PWD}:/data" fsfe/reuse annotate \
		--copyright-prefix string \
		--copyright "Cisco Systems, Inc. and its affiliates" \
		-l "Apache-2.0" \
		--skip-existing \
		src/generated/**/*.py
	@echo "✓ Headers added to generated files"
