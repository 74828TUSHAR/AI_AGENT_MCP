Jenkins setup for this repository

1. Install these Jenkins plugins:
   - Pipeline
   - Git
   - JUnit
   - Workspace Cleanup
   - Allure Jenkins Plugin, if you want to publish Allure reports from Jenkins

2. Make sure the Jenkins agent machine has:
   - Docker Desktop running
   - access to this Git repository

3. Create two separate Jenkins jobs from the same repository:
   - UI job
   - API job

4. In both jobs, use:
   - Definition: Pipeline script from SCM
   - SCM: Git
   - Script Path: `project_playwright/Jenkins/Jenkinsfile`

5. Set the job parameters:
   - UI job: `SUITE = UI`
   - API job: `SUITE = API`
   - `ENV = qa`
   - `HEADLESS = true`

6. What the pipeline does:
   - checks out the code
   - builds a Playwright Docker image
   - runs only the selected suite
   - archives suite-specific logs, screenshots, downloads, videos, and Allure output
   - publishes a suite-specific `test-results.xml`

7. Where the outputs go:
   - UI artifacts: `project_playwright/ci-artifacts/ui/<build-number>/`
   - API artifacts: `project_playwright/ci-artifacts/api/<build-number>/`

8. Important test selection rules:
   - UI tests are selected from `tests/UI`
   - API tests are selected from `tests/API`
   - the suite markers are added automatically by `conftest.py`

9. To publish Allure:
   - install and configure the Allure Jenkins plugin
   - point it at the archived `allure-results` folder from the selected suite
