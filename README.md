# gha-mergify-ci

GitHub Action to:

* junit-process: process JUnit XML files with Mergify CI Insights (Upload and Quarantine)
* scopes: detect and upload pull requests scopes to Mergify Merge Queue

More information on https://mergify.com

## Usage

Pin the action to a released version (see the [releases](https://github.com/Mergifyio/gha-mergify-ci/releases)):

```yaml
- uses: Mergifyio/gha-mergify-ci@v19
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
| `job_name` | string | false |  | Override the job name, must be used in case of matrix job to avoid having the same name for all jobs |
| `jobs` | string | false |  | List of jobs to wait for completion |
| `mergify_api_url` | string | false | `https://api.mergify.com` | URL of the Mergify API |
| `mergify_cli_version` | string | false | `2026.5.29.2` | Version of mergify-cli to install. Use `latest` to install the latest released version without pinning. |
| `mergify_config_path` | string | false |  | Path to the Mergify configuration file |
| `report_path` | string | false |  | Path of the files to upload |
| `scopes` | string | false |  | Comma separated list of scopes to upload |
| `test_step_outcome` | string | false |  | Outcome of the test runner step (e.g. steps.<id>.outcome). Pass this to detect silent failures where the test runner crashed but the JUnit report appears clean. Values: 'success', 'failure', 'cancelled', 'skipped', or omit entirely. 'skipped' is treated the same as omitting this input. |
| `token` | string | false |  | Mergify CI token |

<!-- AUTO-DOC-INPUT:END -->
