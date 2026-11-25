# gha-mergify-ci

GitHub Action to:

* junit-process: process JUnit XML files with Mergify CI Insights (Upload and Quarantine)
* scopes: detect and upload pull requests scopes to Mergify Merge Queue

More information on https://mergify.com

## Usage

Pin the action to a released version (see the
[releases](https://github.com/Mergifyio/gha-mergify-ci/releases)) and grant
the job `id-token: write`:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      # ...
      - uses: Mergifyio/gha-mergify-ci@v30
        with:
          action: junit-process
          report_path: "**/junit*.xml"
```

The job stores no Mergify key. The Mergify CLI the action runs trades the
job's GitHub ID token for a Mergify token that works for one hour, on this
repository only. If you pin `mergify_cli_version`, pin 2026.11.8 or later.

A `permissions` block sets every permission it does not list to `none`, so
list the ones your other steps need too. A job of a reusable workflow gets
`id-token: write` only if its calling job grants it.

Mergify refuses the ID token until a trust policy of your organization
covers the repository. A GitHub organization owner or a CI Admin writes
one, as [OIDC Authentication](https://docs.mergify.com/integrations/gha/oidc/#write-a-trust-policy)
shows. ID token authentication is in Preview.

When Mergify refuses the job a token, `junit-process` fails its step and the
scopes upload is skipped with a warning saying why. On a public repository,
GitHub gives runs for pull requests from forks no ID token: skip the upload
there with
`if: (success() || failure()) && (!github.event.pull_request || github.event.pull_request.head.repo.full_name == github.repository)`.

Need help setting it up? See the [GitHub Actions setup guide](https://docs.mergify.com/ci-insights/setup/github-actions/) on the Mergify docs.

## Use an application key instead

Some jobs need a Mergify application key granted
[CI Reporting](https://docs.mergify.com/api/usage/#ci-reporting):

* runs for pull requests from forks, when your organization sends them
  secrets;
* jobs that run on the base branch (`pull_request_target`, `workflow_run`,
  `issue_comment`): trust policies leave those events out unless they name
  them, and Mergify refuses the scopes a `pull_request_target` job sends with
  its ID token.

Store the key as the `MERGIFY_TOKEN` repository secret and pass it as
`token`, or set `MERGIFY_TOKEN` in the job's environment:

```yaml
- uses: Mergifyio/gha-mergify-ci@v30
  with:
    action: junit-process
    token: ${{ secrets.MERGIFY_TOKEN }}
    report_path: "**/junit*.xml"
```

A key set either way wins over the ID token, so to keep the ID token
everywhere else, set it on those runs only.
[Jobs that keep a key](https://docs.mergify.com/integrations/gha/oidc/#jobs-that-keep-a-key)
shows how for each case. If your workflows store `MERGIFY_TOKEN` today,
[move them off it](https://docs.mergify.com/integrations/gha/oidc/#move-your-workflows-off-mergify_token).

## Merge Queue scopes

Scopes tell the Mergify Merge Queue which parts of the repository a pull
request impacts, so batches with disjoint scopes can merge in parallel. Use
`action: scopes` to detect them from the Mergify configuration file filters,
or `action: scopes-upload` to upload a list you computed yourself (e.g. the
leaf targets of your build graph). Both upload with the job's ID token, so
grant the job `id-token: write` as in [Usage](#usage):

```yaml
- uses: Mergifyio/gha-mergify-ci@v30
  with:
    action: scopes-upload
    scopes: backend,frontend
```

### Adding scopes to the detected ones

When something outside the configuration file filters knows more scopes
(e.g. your build tool), pass them to `action: scopes` with `scopes`. The
action sends one report with the scopes detected from the changed files plus
these:

```yaml
- uses: Mergifyio/gha-mergify-ci@v30
  with:
    action: scopes
    scopes: ${{ steps.build-graph.outputs.scopes }}
```

Mergify adds them only if your configuration declares `manual: null` beside
`files` in `scopes.source`:

```yaml
scopes:
  source:
    files:
      frontend:
        include:
          - apps/web/**/*
    manual: null
```

The Merge Queue then waits for the report of each pull request it queues, so
run the action on every pull request, even with nothing to add. With `files`
alone, Mergify ignores the scopes you send and uses the file filters only.

Send them this way rather than from a second step: each report replaces the
previous one for the same commit, so an `action: scopes` step followed by an
`action: scopes-upload` step keeps only the uploaded scopes.

### Catch-all: declaring a pull request impacts all scopes

Some pull requests impact everything — typically a build-system or CI
configuration change — and enumerating every scope is brittle. Set
`all_scopes: true` to declare it explicitly:

```yaml
- uses: Mergifyio/gha-mergify-ci@v30
  with:
    action: scopes-upload
    all_scopes: true
```

The Merge Queue treats such a pull request as a barrier: it conflicts with
every scope, so it is never batched or merged in parallel with other pull
requests. `all_scopes: true` works with both `action: scopes` and
`action: scopes-upload`, with or without concrete `scopes`. With
`action: scopes`, it counts only if `scopes.source` declares `manual: null`
beside `files`, as for [extra scopes](#adding-scopes-to-the-detected-ones);
with `files` alone, list the files that impact every scope in
`scopes.barrier_files` instead.

## Inputs

<!-- AUTO-DOC-INPUT:START - Do not remove or modify this section -->

| Input | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `action` | string | false | `junit-process` | The Mergify CI action:<br>• junit-process: process JUnit XML files with Mergify CI Insights (Upload and Quarantine)<br>• scopes: detect and upload pull requests scopes to Mergify Merge Queue<br>• scopes-git-refs: return the base/head git references of the pull request in Merge Queue context<br>• scopes-upload: upload pull requests scopes to Mergify Merge Queue<br>• wait-jobs: wait for specified jobs to complete before proceeding |
| `all_scopes` | string | false | `false` | Declare that the pull request impacts all scopes (actions: scopes, scopes-upload). The Merge Queue treats such a pull request as a barrier: it conflicts with every scope, so it is never batched or merged in parallel with other pull requests. Typical use: a build-system or CI configuration change where enumerating every impacted scope is brittle. With action: scopes, it counts only if `scopes.source` declares `manual: null` beside `files`, as for `scopes`; with `files` alone, list such files in `barrier_files` instead. |
| `base` | string | false |  | Base git reference for scope detection (action: scopes). Overrides the automatic push/pull-request detection. Leave unset to auto-detect. |
| `head` | string | false |  | Head git reference for scope detection (action: scopes). Defaults to HEAD. Leave unset to auto-detect. |
| `job_name` | string | false |  | Override the job name, must be used in case of matrix job to avoid having the same name for all jobs |
| `jobs` | string | false |  | List of jobs to wait for completion |
| `mergify_api_url` | string | false | `https://api.mergify.com` | URL of the Mergify API |
| `mergify_cli_version` | string | false |  | Version of mergify-cli to install. Use `latest` to install the latest released version without pinning. Leave unset to use the version pinned by Mergifyio/setup-cli. |
| `mergify_config_path` | string | false |  | Path to the Mergify configuration file |
| `report_path` | string | false |  | Path of the files to upload |
| `scopes` | string | false |  | Comma separated list of scopes to upload (actions: scopes, scopes-upload). With action: scopes, they are added to the scopes detected from the changed files and sent in the same report, e.g. the scopes your build tool knows on top of the configuration file filters. Mergify adds them only if `scopes.source` declares `manual: null` beside `files`, and the Merge Queue then waits for the report of each pull request it queues. With `files` alone, Mergify ignores them and uses the file filters only. |
| `test_step_outcome` | string | false |  | Outcome of the test runner step (e.g. steps.<id>.outcome). Pass this to detect silent failures where the test runner crashed but the JUnit report appears clean. Values: 'success', 'failure', 'cancelled', 'skipped', or omit entirely. 'skipped' is treated the same as omitting this input. |
| `token` | string | false |  | A Mergify application key granted CI Reporting, defaulting to the job's MERGIFY_TOKEN. Optional in a job granted `id-token: write`: without a key, the Mergify CLI trades the job's GitHub ID token for a Mergify token, if a trust policy of your organization allows the job. A key wins over the ID token. |

<!-- AUTO-DOC-INPUT:END -->

## Outputs

| Output | Description |
| --- | --- |
| `test_results_upload` | Outcome of the JUnit test-results upload to Mergify Test Engine (action: junit-process): `success`, `rejected` (the API refused the upload, e.g. a key not granted CI Reporting, and recorded no test data) or `failed` (transient upload error). Empty when the junit-process step did not run or the installed mergify-cli predates this output. |
| `scopes` | Stringified JSON mapping with names of all scopes matching any of the changed files |
| `base` | The Merge Queue-aware base SHA of the pull request |
| `head` | The Merge Queue-aware head SHA of the pull request |

A rejected upload does not fail the step — Mergify-side trouble must not break your CI. To surface dead ingest in your workflow, check the output explicitly:

```yaml
- uses: Mergifyio/gha-mergify-ci@v30
  id: mergify-ci
  with:
    action: junit-process
    report_path: "**/junit*.xml"

- if: steps.mergify-ci.outputs.test_results_upload == 'rejected'
  run: |
    echo "Mergify rejected the test results upload: see the Mergify step's log."
    exit 1
```
