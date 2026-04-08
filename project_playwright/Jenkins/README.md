Jenkins setup for this repository

1. Install these Jenkins plugins:
   - Pipeline
   - Git
   - JUnit
   - Workspace Cleanup
   - Allure Jenkins Plugin (optional but recommended)

2. Make sure the Jenkins agent machine has:
   - Docker Desktop running
   - access to this Git repository

3. Create a new Jenkins job:
   - Item type: Pipeline
   - Definition: Pipeline script from SCM
   - SCM: Git
   - Script Path: Jenkins/Jenkinsfile

4. If Jenkins runs on Windows, use a Windows agent with Docker Desktop.

5. The pipeline will:
   - checkout code
   - build the Docker image from Docker/Dockerfile
   - run all tests headlessly
   - publish test-results.xml
   - archive allure-results, logs, screenshots, and failed-test videos

6. To view Allure inside Jenkins:
   - install the Allure Jenkins plugin
   - configure the Allure command line tool in Jenkins global tools
   - add a post-build Allure step if you want HTML report publishing from archived allure-results
