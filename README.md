# gha-mergify-ci

GitHub Action to:

* junit-process: process JUnit XML files with Mergify CI Insights (Upload and Quarantine)
* scopes: detect and upload pull requests scopes to Mergify Merge Queue

More information on https://mergify.com

## Usage

Pin the action to a released version (see the [releases](https://github.com/Mergifyio/gha-mergify-ci/releases)):

```yaml
- uses: Mergifyio/gha-mergify-ci@v22
  with:
    action: junit-process
    token: ${{ secrets.MERGIFY_TOKEN }}
    report_path: "**/junit*.xml"
```

Need help setting it up? See the [GitHub Actions setup guide](https://docs.mergify.com/ci-insights/setup/github-actions/) on the Mergify docs.

## Inputs

<!-- AUTO-DOC-INPUT:START - Do not remove or modify this section -->

| Input | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `action` | string | false | `junit-process` | The Mergify CI action:<br>• junit-process: process JUnit XML files with Mergify CI Insights (Upload and Quarantine)<br>• scopes: detect and upload pull requests scopes to Mergify Merge Queue<br>• scopes-git-refs: return the base/head git references of the pull request in Merge Queue context<br>• scopes-upload: upload pull requests scopes to Mergify Merge Queue<br>• wait-jobs: wait for specified jobs to complete before proceeding |
| `base` | string | false |  | Base git reference for scope detection (action: scopes). Overrides the automatic push/pull-request detection. Leave unset to auto-detect. |
| `head` | string | false |  | Head git reference for scope detection (action: scopes). Defaults to HEAD. Leave unset to auto-detect. |
| `job_name` | string | false |  | Override the job name, must be used in case of matrix job to avoid having the same name for all jobs |
| `jobs` | string | false |  | List of jobs to wait for completion |
| `mergify_api_url` | string | false | `https://api.mergify.com` | URL of the Mergify API |
| `mergify_cli_version` | string | false | `2026.6.8.1` | Version of mergify-cli to install. Use `latest` to install the latest released version without pinning. |
| `mergify_config_path` | string | false |  | Path to the Mergify configuration file |
| `report_path` | string | false |  | Path of the files to upload |
| `scopes` | string | false |  | Comma separated list of scopes to upload |
| `test_step_outcome` | string | false |  | Outcome of the test runner step (e.g. steps.<id>.outcome). Pass this to detect silent failures where the test runner crashed but the JUnit report appears clean. Values: 'success', 'failure', 'cancelled', 'skipped', or omit entirely. 'skipped' is treated the same as omitting this input. |
| `token` | string | false |  | Mergify CI token |

<!-- AUTO-DOC-INPUT:END -->

## Outputs

| Output | Description |
| --- | --- |
| `test_results_upload` | Outcome of the JUnit test-results upload to Mergify Test Insights (action: junit-process): `success`, `rejected` (the API refused the upload, e.g. a token without CI Insights access — no test data was recorded) or `failed` (transient upload error). Empty when the junit-process step did not run or the installed mergify-cli predates this output. |
| `scopes` | Stringified JSON mapping with names of all scopes matching any of the changed files |
| `base` | The Merge Queue-aware base SHA of the pull request |
| `head` | The Merge Queue-aware head SHA of the pull request |

A rejected upload does not fail the step — Mergify-side trouble must not break your CI. To surface dead ingest in your workflow, check the output explicitly:

```yaml
- uses: Mergifyio/gha-mergify-ci@v22
  id: mergify-ci
  with:
    action: junit-process
    token: ${{ secrets.MERGIFY_TOKEN }}
    report_path: "**/junit*.xml"

- if: steps.mergify-ci.outputs.test_results_upload == 'rejected'
  run: |
    echo "Test results upload was rejected — check the MERGIFY_TOKEN permissions."
    exit 1
```
