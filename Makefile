# Copyright 2026 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

# Python command - use python3 if python is not available
PYTHON := $(shell command -v python3 2> /dev/null || echo python)

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

.PHONY: clean
clean:
	@echo "Cleaning build artifacts"
	@rm -rf build/ dist/ *.egg-info src/*.egg-info
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@echo "✓ Clean complete"

.PHONY: build
build: clean
	@echo "Building distribution packages"
	@$(PYTHON) -m pip install --upgrade build
	@$(PYTHON) -m build
	@echo "✓ Build complete"
	@ls -lh dist/

.PHONY: test-install
test-install: build
	@echo "Testing installation in clean environment"
	@$(PYTHON) -m venv /tmp/test-install-env
	@/tmp/test-install-env/bin/pip install dist/*.whl
	@/tmp/test-install-env/bin/python -c "from ioc_cfn_mas_client import Client; print('✓ Import successful!')"
	@rm -rf /tmp/test-install-env
	@echo "✓ Installation test passed"

.PHONY: check-version
check-version:
	@echo "Checking version in pyproject.toml"
	@$(PYTHON) -c "import tomllib; f=open('pyproject.toml','rb'); print('Version:', tomllib.load(f)['project']['version'])"

.PHONY: check-dist
check-dist: build
	@echo "Checking distribution packages"
	@$(PYTHON) -m pip install --upgrade twine
	@$(PYTHON) -m twine check dist/*
	@echo "✓ Distribution check passed"

.PHONY: upload-test
upload-test: build check-dist
	@echo "Uploading to Test PyPI"
	@$(PYTHON) -m twine upload --repository testpypi dist/*
	@echo "✓ Uploaded to Test PyPI"
	@echo "Test install with: pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ ioc-cfn-mas-client-lib"

.PHONY: upload-prod
upload-prod: build check-dist
	@echo "⚠️  WARNING: This will publish to PRODUCTION PyPI"
	@read -p "Are you sure? Type 'yes' to confirm: " confirm && [ "$$confirm" = "yes" ]
	@$(PYTHON) -m twine upload dist/*
	@echo "✓ Published to PyPI"
