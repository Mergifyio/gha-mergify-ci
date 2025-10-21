# gha-mergify-ci

GitHub Action to:

* junit-process: process JUnit XML files with Mergify CI Insights (Upload and Quarantine)
* scopes: detect and upload pull requests scopes to Mergify Merge Queue

More information on https://mergify.com

## Inputs

<!-- AUTO-DOC-INPUT:START - Do not remove or modify this section -->

|        INPUT         |  TYPE  | REQUIRED |           DEFAULT           |                                                                                                DESCRIPTION                                                                                                |
|----------------------|--------|----------|-----------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|        action        | string |  false   |      `"junit-process"`      | The Mergify CI action: * junit-process: <br>process JUnit XML files with Mergify <br>CI Insights (Upload and Quarantine) * scopes: detect <br>and upload pull requests scopes to <br>Mergify Merge Queue  |
| flaky_test_detection | string |  false   |          `"false"`          |                                                                    Mark test execution as part of <br>a flaky test detection process                                                                      |
|       job_name       | string |  false   |                             |                                             Override the job name, must be <br>used in case of matrix job <br>to avoid having the same name <br>for all jobs                                              |
|   mergify_api_url    | string |  false   | `"https://api.mergify.com"` |                                                                                          URL of the Mergify API                                                                                           |
|     report_path      | string |  false   |                             |                                                                                        Path of the files to upload                                                                                        |
|        token         | string |  false   |                             |                                                                                             Mergify CI token                                                                                              |

<!-- AUTO-DOC-INPUT:END --> 
