# gha-mergify-ci

GitHub Action to:

* junit-process: process JUnit XML files with Mergify CI Insights (Upload and Quarantine)
* scopes: detect and upload pull requests scopes to Mergify Merge Queue

More information on https://mergify.com

## Inputs

<!-- AUTO-DOC-INPUT:START - Do not remove or modify this section -->
```yaml
- uses: Mergifyio/gha-mergify-ci@v13
  id: gha-mergify-ci
  with:
    # The Mergify CI action:
* junit-process: process JUnit XML files with Mergify CI Insights (Upload and Quarantine)
* scopes: detect and upload pull requests scopes to Mergify Merge Queue
* scopes-git-refs: return the base/head git references of the pull request in Merge Queue context
* scopes-upload: upload pull requests scopes to Mergify Merge Queue
* wait-jobs: wait for specified jobs to complete before proceeding

    # Type: string
    # Default: "junit-process"
    action: ''

    # Override the job name, must be used in case of matrix job to avoid
having the same name for all jobs

    # Type: string
    job_name: ''

    # List of jobs to wait for completion
    # Type: string
    jobs: ''

    # URL of the Mergify API
    # Type: string
    # Default: "https://api.mergify.com"
    mergify_api_url: ''

    # Path of the files to upload
    # Type: string
    report_path: ''

    # Comma separated list of scopes to upload
    # Type: string
    scopes: ''

    # Mergify CI token
    # Type: string
    token: ''

```
<!-- AUTO-DOC-INPUT:END --> 
