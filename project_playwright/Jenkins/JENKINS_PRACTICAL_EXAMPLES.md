# Jenkins Pipeline - Practical Examples & Extensions

## Table of Contents

1. [Email Notifications](#email-notifications)
2. [Slack Notifications](#slack-notifications)
3. [Performance Testing](#performance-testing)
4. [Parallel Execution](#parallel-execution)
5. [Database Operations](#database-operations)
6. [API Integration](#api-integration)
7. [Advanced Reporting](#advanced-reporting)

---

## Email Notifications

### Basic Email Configuration

Add to your Jenkinsfile post section:

```groovy
post {
    failure {
        script {
            emailext(
                subject: "[FAILED] ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    Test Automation Build Failed

                    Job: ${env.JOB_NAME}
                    Build Number: ${env.BUILD_NUMBER}
                    Build URL: ${env.BUILD_URL}

                    Test Suite: ${params.SUITE}
                    Environment: ${params.ENV}

                    Failed Tests: Check ${env.BUILD_URL}testReport/

                    Please review the logs and fix the failing tests.
                """,
                to: 'qa-team@company.com',
                mimeType: 'text/plain'
            )
        }
    }

    success {
        script {
            emailext(
                subject: "[SUCCESS] ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    Test Automation Build Passed

                    Job: ${env.JOB_NAME}
                    Build Number: ${env.BUILD_NUMBER}
                    Duration: ${currentBuild.durationString}

                    Test Results: ${env.BUILD_URL}testReport/
                    Allure Report: ${env.BUILD_URL}allure/
                """,
                to: 'qa-team@company.com, dev-team@company.com',
                mimeType: 'text/html'
            )
        }
    }
}
```

### Email with Attachments

```groovy
def sendEmailWithAttachments() {
    emailext(
        subject: "[TEST REPORT] Build #${env.BUILD_NUMBER}",
        body: "See attached test results",
        to: 'team@company.com',
        attachmentsPattern: '**/test-results.xml,**/build-log.txt',
        mimeType: 'text/html'
    )
}
```

---

## Slack Notifications

### Basic Slack Integration

```groovy
def notifySlack(String status, String color) {
    slackSend(
        color: color,
        message: """
            *Test Automation Build ${status}*
            Job: ${env.JOB_NAME}
            Build: #${env.BUILD_NUMBER}
            Suite: ${params.SUITE}
            Env: ${params.ENV}
            URL: ${env.BUILD_URL}
        """,
        webhookUrl: "${env.SLACK_WEBHOOK_URL}"
    )
}

post {
    success {
        script { notifySlack('SUCCESS ✓', 'good') }
    }
    failure {
        script { notifySlack('FAILED ✗', 'danger') }
    }
    unstable {
        script { notifySlack('UNSTABLE ⚠', 'warning') }
    }
}
```

### Advanced Slack with Test Results

```groovy
def sendDetailedSlackReport() {
    def testResults = sh(
        script: '''
            echo "$(grep 'passed' test-results.xml | wc -l) passed"
            echo "$(grep 'failed' test-results.xml | wc -l) failed"
        ''',
        returnStdout: true
    ).trim()

    slackSend(
        color: 'good',
        message: """
            *Test Execution Report*
            Suite: ${params.SUITE}
            ${testResults}
            Report: ${env.BUILD_URL}testReport/
        """,
        webhookUrl: "${env.SLACK_WEBHOOK_URL}"
    )
}
```

---

## Performance Testing

### Add Performance Benchmark Stage

```groovy
stage('Performance Analysis') {
    steps {
        dir('project_playwright') {
            script {
                try {
                    echo "Analyzing test performance metrics..."

                    sh '''
                        python -m pytest \
                            "$SUITE_PATH" \
                            -v \
                            --durations=10 \
                            --benchmark-only \
                            --benchmark-save=results-${BUILD_NUMBER}
                    '''

                    echo "✓ Performance analysis completed"
                    echo "Slowest 10 tests identified"

                } catch (Exception e) {
                    echo "⚠ Performance analysis warning: ${e.message}"
                }
            }
        }
    }
}
```

### Performance Comparison

```groovy
def comparePerformance() {
    sh '''
        echo "Comparing with previous build..."

        PREV_BUILD=$((BUILD_NUMBER - 1))
        PREV_RESULTS="ci-artifacts/${SUITE_SLUG}/${PREV_BUILD}/performance.json"
        CURRENT_RESULTS="ci-artifacts/${SUITE_SLUG}/${BUILD_NUMBER}/performance.json"

        if [ -f "$PREV_RESULTS" ]; then
            python scripts/compare_performance.py "$PREV_RESULTS" "$CURRENT_RESULTS"
        fi
    '''
}
```

---

## Parallel Execution

### Run UI and API Tests in Parallel

```groovy
stage('Run Tests') {
    parallel {
        stage('UI Tests') {
            steps {
                script {
                    sh '''
                        python -m pytest tests/UI \
                            -m ui \
                            --junit-xml=ui-results.xml
                    '''
                }
            }
        }

        stage('API Tests') {
            steps {
                script {
                    sh '''
                        python -m pytest tests/API \
                            -m api \
                            --junit-xml=api-results.xml
                    '''
                }
            }
        }
    }
}
```

### Collect Results from Parallel Stages

```groovy
post {
    always {
        script {
            junit testResults: '**/ui-results.xml,**/api-results.xml',
                  allowEmptyResults: true
        }
    }
}
```

---

## Database Operations

### Database Setup Stage

```groovy
stage('Setup Test Database') {
    steps {
        script {
            try {
                echo "Setting up test database..."

                sh '''
                    # Run database migrations
                    python scripts/setup_database.py \
                        --environment $TARGET_ENV \
                        --seed-data true

                    # Verify connection
                    python -c "
                        import sys
                        from config.database import get_connection
                        conn = get_connection()
                        if conn:
                            print('✓ Database connection verified')
                        else:
                            sys.exit(1)
                    "
                '''

            } catch (Exception e) {
                error("✗ Database setup failed: ${e.message}")
            }
        }
    }
}
```

### Database Cleanup

```groovy
stage('Cleanup Database') {
    steps {
        script {
            try {
                sh '''
                    # Clean test data
                    python scripts/cleanup_database.py \
                        --environment $TARGET_ENV \
                        --purge-logs true
                '''
            } catch (Exception e) {
                echo "⚠ Database cleanup warning: ${e.message}"
            }
        }
    }
}
```

---

## API Integration

### API Test Results Publishing

```groovy
stage('Publish API Test Results') {
    steps {
        script {
            try {
                sh '''
                    # Send results to reporting API
                    curl -X POST https://reporting.company.com/api/results \
                        -H "Content-Type: application/json" \
                        -H "Authorization: Bearer ${API_TOKEN}" \
                        -d @api-results.json
                '''
            } catch (Exception e) {
                echo "⚠ API publish warning: ${e.message}"
            }
        }
    }
}
```

### Integration with Test Management System

```groovy
def publishToTestRail() {
    sh '''
        python scripts/testrail_integration.py \
            --run-id "${TESTRAIL_RUN_ID}" \
            --results "test-results.xml" \
            --project "${TESTRAIL_PROJECT}" \
            --api-key "${TESTRAIL_API_KEY}"
    '''
}
```

---

## Advanced Reporting

### Generate Custom HTML Report

```groovy
stage('Generate Custom Report') {
    steps {
        dir('project_playwright') {
            script {
                try {
                    sh '''
                        python scripts/generate_report.py \
                            --test-results test-results.xml \
                            --screenshots screenshots/ \
                            --output report.html \
                            --template professional
                    '''

                    echo "✓ Custom HTML report generated"

                } catch (Exception e) {
                    echo "⚠ Report generation warning: ${e.message}"
                }
            }
        }
    }
}
```

### Publish HTML Report

```groovy
post {
    always {
        publishHTML([
            reportDir: 'project_playwright',
            reportFiles: 'report.html',
            reportName: 'Test Automation Report',
            keepAll: true,
            alwaysLinkToLastBuild: true
        ])
    }
}
```

### Generate Code Coverage Report

```groovy
stage('Code Coverage') {
    steps {
        dir('project_playwright') {
            sh '''
                python -m pytest \
                    tests/ \
                    --cov=. \
                    --cov-report=html \
                    --cov-report=xml
            '''
        }
    }
}

post {
    always {
        step([$class: 'CoberturaPublisher',
              autoUpdateHealth: false,
              autoUpdateStability: false,
              coberturaReportFile: 'project_playwright/coverage.xml',
              failUnhealthy: false,
              failUnstable: false,
              maxNumberOfBuilds: 0,
              onlyStable: false,
              sourceEncoding: 'ASCII',
              zoomCoverageChart: false])
    }
}
```

---

## Advanced Error Handling

### Retry Failed Tests

```groovy
stage('Run Tests with Retry') {
    steps {
        dir('project_playwright') {
            script {
                sh '''
                    python -m pytest \
                        "$SUITE_PATH" \
                        -m "$SUITE_MARKER" \
                        --reruns 2 \
                        --reruns-delay 5 \
                        -v
                '''
            }
        }
    }
}
```

### Continue on Test Failure

```groovy
stage('Run Tests') {
    steps {
        dir('project_playwright') {
            script {
                def testResult = sh(
                    script: 'python -m pytest tests/',
                    returnStatus: true
                )

                if (testResult != 0) {
                    echo "⚠ Some tests failed, continuing with analysis..."
                    currentBuild.result = 'UNSTABLE'
                }
            }
        }
    }
}
```

---

## Build Status Dashboard

### Create Build Status Summary

```groovy
def createBuildSummary() {
    def buildLog = """
    ╔════════════════════════════════════════════════════════════════╗
    ║                    BUILD SUMMARY                               ║
    ╚════════════════════════════════════════════════════════════════╝

    Build Number:        ${env.BUILD_NUMBER}
    Job Name:           ${env.JOB_NAME}
    Build Status:       ${currentBuild.result}
    Build Duration:     ${currentBuild.durationString}

    Test Suite:         ${params.SUITE}
    Environment:        ${params.ENV}
    Headless Mode:      ${params.HEADLESS}

    Git Information:
    ─────────────────────────────────────────────────────────────────
    Branch:             ${env.GIT_BRANCH ?: 'N/A'}
    Commit:             ${env.GIT_COMMIT_SHORT ?: 'N/A'}

    Artifacts:
    ─────────────────────────────────────────────────────────────────
    Build Artifacts:    ${env.BUILD_URL}artifact/
    Test Report:        ${env.BUILD_URL}testReport/
    Allure Report:      ${env.BUILD_URL}allure/

    ╚════════════════════════════════════════════════════════════════╝
    """

    writeFile file: 'build-summary.txt', text: buildLog
}
```

---

## Environment-Specific Configuration

### Load Environment Configuration

```groovy
def loadEnvironmentConfig(String env) {
    def configFile = "config/env_${env}.yaml"

    if (!fileExists(configFile)) {
        error("Config file not found: ${configFile}")
    }

    sh '''
        python -c "
            import yaml
            with open('${configFile}') as f:
                config = yaml.safe_load(f)
            for key, value in config.items():
                print(f'{key}={value}')
        " | tee env-config.txt
    '''
}
```

### Use Environment Configuration

```groovy
sh '''
    source env-config.txt

    python -m pytest tests/ \
        --base-url=$BASE_URL \
        --api-key=$API_KEY \
        --database=$DB_HOST
'''
```

---

## Conclusion

These examples demonstrate:

- ✓ Real-world integration patterns
- ✓ Advanced error handling
- ✓ Professional reporting
- ✓ Scalable architecture
- ✓ Industry best practices

Combine these patterns based on your specific requirements!
