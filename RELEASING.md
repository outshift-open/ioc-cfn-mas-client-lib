# Release Process

This document describes how to release a new version of ioc-cfn-mas-client-lib to PyPI.

## Prerequisites

- Maintainer access to the GitHub repository
- PyPI trusted publisher configured (one-time setup, see below)
- Python 3.10+ installed locally for testing

## PyPI Trusted Publisher Setup (One-Time)

Before the first release, configure PyPI trusted publishing:

1. Go to https://pypi.org and login (or create an account)
2. Navigate to Account → Publishing → "Add a new pending publisher"
3. Fill in the form:
   - **PyPI Project Name**: `ioc-cfn-mas-client-lib`
   - **Owner**: `outshift-open`
   - **Repository name**: `ioc-cfn-mas-client-lib`
   - **Workflow name**: `publish.yaml`
   - **Environment name**: (leave blank)
4. Click "Add"

On the first tagged release, the workflow will create the project on PyPI automatically.

**Note**: No API tokens or secrets are needed. GitHub Actions uses OIDC to authenticate.

## Release Checklist

### 1. Prepare Release

- [ ] All PRs for this release are merged to `main`
- [ ] CI tests are passing on `main`
- [ ] Local tests pass: `uv run pytest`
- [ ] Decide on version number (follow [semver](https://semver.org/))

### 2. Update Version

- [ ] Update `version` in `pyproject.toml`:
  ```toml
  version = "0.1.1"  # Bump version
  ```

- [ ] Update `CHANGELOG.md` with release notes:
  ```markdown
  ## [0.1.1] - 2026-07-15

  ### Added
  - New feature X

  ### Fixed
  - Bug Y in memory operations

  ### Changed
  - Improved Z performance
  ```

- [ ] Commit changes:
  ```bash
  git add pyproject.toml CHANGELOG.md
  git commit -m "Bump version to 0.1.1"
  git push origin main
  ```

### 3. Create and Push Tag

**Important**: Tag must match the version in `pyproject.toml` (with `v` prefix)

```bash
# Format: vMAJOR.MINOR.PATCH
git tag v0.1.1

# Push the tag (this triggers the publish workflow)
git push origin v0.1.1
```

### 4. Monitor Workflow

- [ ] Go to https://github.com/outshift-open/ioc-cfn-mas-client-lib/actions
- [ ] Find the "Publish to PyPI" workflow run
- [ ] Wait for all jobs to complete:
  - ✅ Run Tests Before Publish
  - ✅ Build Package
  - ✅ Publish to PyPI

- [ ] Check for any failures and fix if needed

### 5. Verify on PyPI

- [ ] Visit https://pypi.org/project/ioc-cfn-mas-client-lib/
- [ ] Verify new version appears
- [ ] Check metadata is correct (description, links, classifiers)
- [ ] Test installation in a clean environment:

  ```bash
  # Create clean environment
  python -m venv /tmp/test-pypi
  source /tmp/test-pypi/bin/activate

  # Install from PyPI
  pip install ioc-cfn-mas-client-lib

  # Test import
  python -c "from ioc_cfn_mas_client import Client; print('✓ Success!')"

  # Clean up
  deactivate
  rm -rf /tmp/test-pypi
  ```

### 6. Create GitHub Release

- [ ] Go to https://github.com/outshift-open/ioc-cfn-mas-client-lib/releases/new
- [ ] Select the tag you just created (e.g., `v0.1.1`)
- [ ] Title: `v0.1.1` (or descriptive: `v0.1.1 - Performance Improvements`)
- [ ] Copy the CHANGELOG entry for this version into the description
- [ ] Click "Publish release"

### 7. Announce Release

- [ ] Update project documentation if needed
- [ ] Announce in team channels if applicable
- [ ] Respond to any user feedback

## Semantic Versioning Guide

Follow [semver.org](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes, incompatible API changes
- **MINOR** (0.X.0): New features, backward compatible
- **PATCH** (0.0.X): Bug fixes, backward compatible

### Examples

```
0.1.0 → 0.1.1   # Bug fix
0.1.1 → 0.2.0   # New feature (backward compatible)
0.2.0 → 1.0.0   # First stable release or breaking change
1.0.0 → 1.1.0   # New feature
1.1.0 → 2.0.0   # Breaking change
```

### Pre-release Versions

For alpha/beta/RC releases:

```toml
version = "0.2.0a1"  # Alpha
version = "0.2.0b1"  # Beta
version = "0.2.0rc1" # Release candidate
version = "0.2.0"    # Stable
```

## Local Testing Before Release

Test the build locally before tagging:

```bash
# Clean previous builds
make clean

# Build the package
make build

# Check the distribution
make check-dist

# Test installation
make test-install

# Check version consistency
make check-version
```

## Troubleshooting

### Version Mismatch Error

**Error**: `❌ Version mismatch: pyproject.toml has '0.1.0' but Git tag is '0.1.1'`

**Fix**: Ensure `pyproject.toml` version matches the tag (without `v` prefix):
- Tag: `v0.1.1`
- pyproject.toml: `version = "0.1.1"`

### Workflow Not Triggering

**Cause**: Tag doesn't match pattern `v*`

**Fix**: Tag must start with `v`:
```bash
git tag v0.1.1  # Correct
git tag 0.1.1   # Wrong - won't trigger
```

### Test Failures

**Cause**: Tests failing in CI

**Fix**:
1. Run tests locally: `uv run pytest`
2. Fix failing tests
3. Push fixes to main
4. Delete and recreate the tag:
   ```bash
   git tag -d v0.1.1
   git push origin :refs/tags/v0.1.1
   # Fix and commit
   git tag v0.1.1
   git push origin v0.1.1
   ```

### PyPI Publish Failed

**Common causes**:
1. Trusted publisher not configured
2. Version already exists on PyPI (versions are immutable)
3. Package name already taken

**Fix**:
1. Check PyPI trusted publisher settings
2. Verify version doesn't already exist on PyPI
3. Check workflow logs for specific error:
   - Go to Actions → Failed run → "Publish to PyPI" job

### Build Artifacts Missing

**Error**: `Error: Unable to find any artifacts for the associated workflow`

**Fix**: Ensure the `build` job completed successfully before `publish` job runs

## Rolling Back a Release

**Important**: You cannot delete a version from PyPI once published.

If a release has issues:

1. **Don't panic** - versions are immutable for good reason
2. **Release a patch version** with the fix:
   ```bash
   # If v0.1.1 is broken, release v0.1.2 with fix
   ```
3. **Optionally mark as "yanked"** on PyPI:
   - Go to PyPI project page
   - Find the bad version
   - Click "Options" → "Yank"
   - This hides it from `pip install` but allows direct installs

## Release to Test PyPI (Optional)

For testing the full workflow before production:

1. Set up Test PyPI trusted publisher at https://test.pypi.org
2. Modify workflow to publish to Test PyPI:
   ```yaml
   - name: Publish to Test PyPI
     uses: pypa/gh-action-pypi-publish@release/v1
     with:
       repository-url: https://test.pypi.org/legacy/
       verbose: true
   ```
3. Test installation:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ \
     --extra-index-url https://pypi.org/simple/ \
     ioc-cfn-mas-client-lib
   ```

Note: Need `--extra-index-url` because dependencies aren't on Test PyPI.

## Manual Publishing (Emergency Only)

If GitHub Actions is down, you can publish manually:

```bash
# Build locally
make build

# Upload to PyPI (requires PyPI account and API token)
make upload-prod
```

**Note**: This bypasses the automated checks. Use only in emergencies.

## Quick Reference

```bash
# Version check
make check-version

# Local build and test
make clean build test-install

# Tag and release
git tag v0.1.1
git push origin v0.1.1

# Monitor
open https://github.com/outshift-open/ioc-cfn-mas-client-lib/actions

# Verify
pip install --upgrade ioc-cfn-mas-client-lib
python -c "from ioc_cfn_mas_client import Client"
```

## Support

For questions or issues:
- GitHub Issues: https://github.com/outshift-open/ioc-cfn-mas-client-lib/issues
- Internal team channels (if applicable)
