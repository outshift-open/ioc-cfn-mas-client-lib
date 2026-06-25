# How to Contribute

Thanks for your interest in contributing to the Internet of Cognition (IOC) Cognition Fabric Node (CFN) MAS Client Library! Here are a few
general guidelines on contributing and reporting bugs that we ask you to review.
Following these guidelines helps to communicate that you respect the time of the
contributors managing and developing this open source project. In return, they
should reciprocate that respect in addressing your issue, assessing changes, and
helping you finalize your pull requests. In that spirit of mutual respect, we
endeavor to review incoming issues and pull requests within 10 days, and will
close any lingering issues or pull requests after 60 days of inactivity.

Please note that all of your interactions in the project are subject to our
[Code of Conduct](/CODE_OF_CONDUCT.md). This includes creation of issues or pull
requests, commenting on issues or pull requests, and extends to all interactions
in any real-time space e.g., Slack, Discord, etc.

## Reporting Issues

Before reporting a new issue, please ensure that the issue was not already
reported or fixed by searching through our [issues
list](https://github.com/outshift-open/ioc-cfn-mas-client-lib/issues).

When creating a new issue, please be sure to include a **title and clear
description**, as much relevant information as possible, and, if possible, a
test case.

**If you discover a security bug, please do not report it through GitHub.
Instead, please see security procedures in [SECURITY.md](/SECURITY.md).**

### Issue Guidelines

- Use the GitHub issue search — check if the issue has already been reported
- Check if the issue has been fixed — try to reproduce it using the latest `main` branch
- Isolate the problem — ideally create a reduced test case
- Include as much information as possible:
  - Python version
  - Library version
  - Operating system
  - Steps to reproduce
  - Expected behavior
  - Actual behavior

## Sending Pull Requests

Before sending a new pull request, take a look at existing pull requests and
issues to see if the proposed change or fix has been discussed in the past, or
if the change was already implemented but not yet released.

We expect new pull requests to include tests for any affected behavior, and, as
we follow semantic versioning, we may reserve breaking changes until the next
major version release.

### Pull Request Process

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** and ensure the code follows the project's coding standards
3. **Add tests** for any new functionality or bug fixes
4. **Ensure all tests pass** by running `uv run pytest`
5. **Update documentation** if you've changed APIs or added features
6. **Write a clear commit message** describing your changes
7. **Submit a pull request** to the `main` branch
8. **Respond to feedback** from maintainers and address any requested changes

### Pull Request Guidelines

- Pull requests should be focused on a single change
- Include tests that cover the new functionality or bug fix
- Follow the existing code style and conventions
- Update documentation as needed
- Keep pull requests small and focused for easier review
- Reference any related issues in your PR description

## Other Ways to Contribute

We welcome anyone that wants to contribute to the IOC CFN MAS Client Library to triage and
reply to open issues to help troubleshoot and fix existing bugs. Here is what
you can do:

- Help ensure that existing issues follows the recommendations from the
  _[Reporting Issues](#reporting-issues)_ section, providing feedback to the
  issue's author on what might be missing.
- Review and update the existing content of our documentation with up-to-date
  instructions and code samples.
- Review existing pull requests, and testing patches against real existing
  applications that use the IOC CFN MAS Client Library.
- Write a test, or add a missing test case to an existing test.

Thanks again for your interest on contributing to the IOC CFN MAS Client Library!

:heart:
