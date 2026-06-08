Jenkins Runbook

This repository uses a Jenkins Pipeline defined in [Jenkinsfile](Jenkinsfile).
The pipeline is parameterized so you can run separate UI and API builds with the same job definition.

## What This Setup Uses

- Windows Jenkins agent
- Python installed on the Jenkins agent
- Playwright installed through `pip`
- Separate Jenkins jobs for UI and API
- JUnit and Allure reporting

## Prerequisites

- Jenkins Pipeline, Git, JUnit, Workspace Cleanup, and optional Allure Jenkins Plugin
- Jenkins agent with Python installed
- Jenkins agent with network access to GitHub
- Jenkins agent able to run `python`, `pip`, and `python -m playwright install`

## Recommended Job Model

Create two separate Pipeline jobs:

- UI job with `SUITE=UI`
- API job with `SUITE=API`

This keeps execution, logs, and reports isolated per suite.

## Jenkins Job Configuration

Create each job as a `Pipeline` job with `Pipeline script from SCM`.

Use these settings:

- SCM: `Git`
- Repository URL: your GitHub repository
- Credentials: Jenkins Git credentials
- Branch Specifier: `*/master` or your release branch
- Script Path: `project_playwright/Jenkins/Jenkinsfile`

Set job parameters:

- `SUITE=UI` for the UI job
- `SUITE=API` for the API job
- `ENV=qa`
- `HEADLESS=true`

## What The Pipeline Does

The pipeline:

- checks out the repository
- installs Python dependencies
- installs Playwright browsers
- runs only the selected suite
- writes suite-specific logs, screenshots, downloads, video, and Allure output
- publishes `test-results.xml`
- archives the full suite artifact bundle

## Artifact Layout

Each build stores artifacts under:

- UI: `project_playwright/ci-artifacts/ui/<build-number>/`
- API: `project_playwright/ci-artifacts/api/<build-number>/`

Each suite build includes:

- Logs: `project_playwright/logs/`
- Allure results: `project_playwright/allure-results/`
- JUnit XML: `project_playwright/test-results.xml`
- Screenshots: `project_playwright/screenshots/`
- Video: `project_playwright/video/`
- Downloads: `project_playwright/downloads/`

## Test Selection Rules

- UI tests are selected from `tests/UI`
- API tests are selected from `tests/API`
- `conftest.py` applies the `ui` and `api` markers automatically

## Reporting

### JUnit

Configure Jenkins to publish:

- `project_playwright/test-results.xml`

### Allure

If the Allure plugin is installed, point it at:

- `project_playwright/allure-results`

## Job Checklist

- Job type: `Pipeline`
- Definition: `Pipeline script from SCM`
- Script Path: `project_playwright/Jenkins/Jenkinsfile`
- UI job parameter: `SUITE=UI`
- API job parameter: `SUITE=API`
- Environment: `ENV=qa`
- Headless mode: `HEADLESS=true`
- JUnit results: `project_playwright/test-results.xml`
- Allure results: `project_playwright/allure-results`
- Archive artifacts:
  - `project_playwright/logs/**`
  - `project_playwright/screenshots/**`
  - `project_playwright/video/**`
  - `project_playwright/downloads/**`
  - `project_playwright/ci-artifacts/**`

## Step By Step Jenkins Setup

### 1. Install plugins

In Jenkins, go to `Manage Jenkins` -> `Plugins` and install:

- `Pipeline`
- `Git`
- `JUnit`
- `Workspace Cleanup`
- `Allure Jenkins Plugin` if you want Allure inside Jenkins

### 2. Prepare the Jenkins machine

Make sure the Jenkins agent machine has:

- Python installed and available in PATH
- access to the GitHub repository
- permission to run `python -m pip install`
- permission to run `python -m playwright install`

### 3. Create the UI job

1. Click `New Item`
2. Enter a name like `Playwright-UI`
3. Select `Pipeline`
4. Click `OK`
5. In the job configuration, scroll to `Pipeline`
6. Set `Definition` to `Pipeline script from SCM`
7. Set `SCM` to `Git`
8. Set `Repository URL` to your GitHub repo URL
9. Set `Credentials` to your GitHub/Jenkins credential
10. Set `Branch Specifier` to `*/master` or your branch
11. Set `Script Path` to `project_playwright/Jenkins/Jenkinsfile`
12. Click `Save`

### 4. Run the UI job

1. Open the `Playwright-UI` job
2. Click `Build with Parameters`
3. Set:
   - `SUITE = UI`
   - `ENV = qa`
   - `HEADLESS = true`
4. Click `Build`

### 5. Create the API job

1. Click `New Item`
2. Enter a name like `Playwright-API`
3. Select `Pipeline`
4. Click `OK`
5. Use the same SCM settings as the UI job
6. Set `Script Path` to `project_playwright/Jenkins/Jenkinsfile`
7. Click `Save`

### 6. Run the API job

1. Open the `Playwright-API` job
2. Click `Build with Parameters`
3. Set:
   - `SUITE = API`
   - `ENV = qa`
   - `HEADLESS = true`
4. Click `Build`

### 7. Verify reports

After each build, check:

- Console output for the test run
- JUnit results in Jenkins
- Allure results if the plugin is enabled
- Archived build artifacts under `ci-artifacts`

## Notes

- The pipeline currently expects a Windows agent with Python available.
- If you change suite paths or artifact paths, update both the Jenkinsfile and this README together.
- Keep the UI and API jobs separate for cleaner reporting and easier triage.
