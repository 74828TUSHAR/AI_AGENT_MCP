# Jenkins Pipeline Testing & Demo Guide

## 📋 Table of Contents

1. [Prerequisites Check](#prerequisites-check)
2. [Quick Start (5 minutes)](#quick-start-5-minutes)
3. [Detailed Testing Steps](#detailed-testing-steps)
4. [Verification Checklist](#verification-checklist)
5. [Troubleshooting](#troubleshooting)
6. [Demo Scenario](#demo-scenario)

---

## Prerequisites Check

### ✅ Before You Begin

Run this checklist to verify everything is ready:

```bash
# 1. Check Python is installed
python --version
# Expected output: Python 3.8+ (e.g., Python 3.11.5)

# 2. Check pip is available
pip --version
# Expected output: pip 24.0+ from ...

# 3. Check Git is installed
git --version
# Expected output: git version 2.x+

# 4. Navigate to project
cd c:\Users\TUSHAR\Desktop\Playwright_Framework\project_playwright

# 5. Check requirements.txt exists
type requirements.txt
# Expected: File content showing dependencies

# 6. Check test files exist
dir tests\UI
dir tests\API
# Expected: test_*.py files

# 7. Check Jenkinsfile exists
type ..\Jenkins\Jenkinsfile
# Expected: Pipeline definition
```

---

## Quick Start (5 minutes)

### Option 1: Test Locally (Without Jenkins)

Perfect for quick validation before Jenkins setup:

```bash
# Step 1: Navigate to project
cd c:\Users\TUSHAR\Desktop\Playwright_Framework\project_playwright

# Step 2: Create virtual environment
python -m venv venv
venv\Scripts\activate

# Step 3: Install dependencies
pip install -r requirements.txt
python -m playwright install

# Step 4: Run a quick test
python -m pytest tests/UI -m ui -v --tb=short --co -q
# Expected: Shows list of UI tests (doesn't execute, just lists)

# Step 5: Run actual tests
python -m pytest tests/UI -m ui -v --tb=short -x
# Expected: Tests execute and report results
```

### Option 2: Validate Jenkinsfile Syntax (Without Running)

```bash
# Install Jenkins CLI (if you have Jenkins running locally)
# Or use online validator

# Method 1: Using curl (if Jenkins running on localhost:8080)
curl -X POST -F "jenkinsfile=@Jenkins\Jenkinsfile" \
  http://localhost:8080/pipeline-model-converter/validate

# Expected response: {"status":"ok"} or error details
```

---

## Detailed Testing Steps

### Phase 1: Local Validation (30 seconds)

```bash
cd c:\Users\TUSHAR\Desktop\Playwright_Framework\project_playwright

# 1. Check Python can find pytest
python -m pytest --version
# Expected: pytest 7.x.x

# 2. Check Python can find playwright
python -c "import playwright; print(playwright.__version__)"
# Expected: Version number (e.g., 1.40.0)

# 3. List available tests
python -m pytest tests/ --collect-only -q
# Expected: List of all test items
```

### Phase 2: Quick Test Execution (2-3 minutes)

```bash
cd c:\Users\TUSHAR\Desktop\Playwright_Framework\project_playwright

# Run a single test file to verify setup
python -m pytest tests/UI/test_case_01_register_user.py -v --tb=short

# Watch output for:
# ✓ PASSED tests
# ✗ FAILED tests
# ⚠ WARNINGS
# Collection of test results
```

### Phase 3: Full Suite Test (5-10 minutes)

```bash
cd c:\Users\TUSHAR\Desktop\Playwright_Framework\project_playwright

# Run entire UI test suite
python -m pytest tests/UI -m ui -v --tb=short \
  --junit-xml=test-results.xml \
  --alluredir=allure-results

# After execution, check:
echo.
echo "Test Results XML:"
type test-results.xml | more

echo.
echo "Allure Results Directory:"
dir allure-results
```

---

## Verification Checklist

### ✅ After Each Test Run

#### 1. Check Test Results XML

```bash
# File should exist
if exist test-results.xml (
    echo ✓ test-results.xml found
    findstr /C:"<testcase" test-results.xml | find /C:"<"
    REM Shows number of test cases
) else (
    echo ✗ test-results.xml NOT found
)
```

#### 2. Check Allure Results

```bash
# Directory should contain JSON files
dir allure-results
# Expected: Multiple JSON files (.json, .txt files)

# If you have Allure installed:
allure serve allure-results
# Opens HTML report in browser
```

#### 3. Check Artifact Directories

```bash
# After test execution, these should exist:
if exist logs (echo ✓ logs folder created)
if exist screenshots (echo ✓ screenshots folder created)
if exist video (echo ✓ video folder created)
if exist downloads (echo ✓ downloads folder created)

# List content
echo.
echo "Screenshots captured:"
dir /B screenshots\*.*

echo.
echo "Log files generated:"
dir /B logs\*.*
```

#### 4. Review Console Output

Look for these visual markers in output:

```
✓ = Success
✗ = Failure
⚠ = Warning
════════════════════════════════════════════════════
= Stage separator
```

---

## Demo Scenario

### Scenario 1: Simple UI Test Demo

**Objective:** Run UI tests and verify all pipeline stages work

**Time:** 10-15 minutes

**Steps:**

```bash
# 1. Setup
cd c:\Users\TUSHAR\Desktop\Playwright_Framework\project_playwright
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt -q
python -m playwright install

# 2. Run UI tests
echo "════════════════════════════════════════════════"
echo "STARTING UI TEST SUITE"
echo "════════════════════════════════════════════════"

python -m pytest tests/UI -m ui -v \
  --tb=short \
  --junit-xml=test-results.xml \
  --alluredir=allure-results \
  --color=yes

# 3. Parse results
echo.
echo "════════════════════════════════════════════════"
echo "TEST EXECUTION COMPLETE"
echo "════════════════════════════════════════════════"

# Count test results
for /f "tokens=*" %%A in ('findstr /C:"<testcase" test-results.xml ^| find /C:"<"') do (
    echo Total Tests: %%A
)

# 4. Show artifacts
echo.
echo "Generated Artifacts:"
dir test-results.xml
dir /S allure-results
```

### Scenario 2: Full Pipeline with Reporting

**Objective:** Execute complete pipeline with all reporting

**Time:** 15-20 minutes

```bash
# 1. Clean previous runs
cd c:\Users\TUSHAR\Desktop\Playwright_Framework\project_playwright
if exist test-results.xml del test-results.xml
if exist allure-results rmdir /S /Q allure-results
if exist logs rmdir /S /Q logs
if exist screenshots rmdir /S /Q screenshots

# 2. Setup environment
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt -q

# 3. Pre-test validation
echo.
echo "Pre-Test Validation:"
echo "═════════════════════════════════════════════════"
echo Python: & python --version
echo Pytest: & python -m pytest --version
echo Working Dir: & cd

# 4. Run tests
echo.
echo "Running Test Suite..."
echo "═════════════════════════════════════════════════"
python -m pytest tests/UI -m ui -v --tb=short ^
  --junit-xml=test-results.xml ^
  --alluredir=allure-results

# 5. Post-test analysis
echo.
echo "Post-Test Analysis:"
echo "═════════════════════════════════════════════════"
if exist test-results.xml (
    echo ✓ Test Results Generated
    echo.
    echo Test Results:
    type test-results.xml | findstr /C:"<testcase"
) else (
    echo ✗ Test Results NOT Generated
)

# 6. Artifact summary
echo.
echo "Artifact Summary:"
echo "═════════════════════════════════════════════════"
echo Allure Results: & if exist allure-results dir /B allure-results | find /C "json"
echo Screenshots: & if exist screenshots dir /B screenshots | find /C "png"
echo Logs: & if exist logs dir /B logs | find /C "log"

# 7. Generate Allure report (if installed)
echo.
echo "Generating Allure Report..."
if exist allure-results (
    REM Uncomment if Allure is installed
    REM allure serve allure-results
    echo ✓ Allure results ready
    echo Run: allure serve allure-results
)
```

---

## Visual Verification Guide

### What You Should See

#### ✅ Successful Test Output

```
tests/UI/test_case_01_register_user.py::test_register_new_user PASSED      [ 10%]
tests/UI/test_case_02_login_user.py::test_login_valid_credentials PASSED   [ 20%]
tests/UI/test_case_03_logout_user.py::test_logout_successful PASSED        [ 30%]
...
════════════════════════════════════════════════════════════════════════════
======================== 10 passed in 45.23s ========================
════════════════════════════════════════════════════════════════════════════

Test Results Summary:
Total Tests: 10
Passed: 10
Failed: 0
Skipped: 0
```

#### ✅ Artifacts Created

```
allure-results/
├── 0d8f1234-abc-container.json
├── 12ab5678-def-result.json
├── 34cd9012-ghi-attachment.json
└── ... (multiple files)

logs/
├── test_execution.log
├── errors.log
└── debug.log

screenshots/
├── test_01_screenshot_001.png
├── test_02_screenshot_002.png
└── ... (on failures)
```

#### ✓ Console Markers

```
════════════════════════════════════════════════  ← Section separator
PRE-BUILD VALIDATION                              ← Stage name
════════════════════════════════════════════════

✓ Checkout successful                             ← Success marker
✗ Python not found                                ← Error marker
⚠ Database cleanup warning                        ← Warning marker

═════════════════════════════════════════════════  ← Final separator
BUILD SUCCESSFUL ✓                                ← Build status
═════════════════════════════════════════════════
```

---

## Troubleshooting

### ❌ Problem 1: Python Not Found

**Symptom:**

```
'python' is not recognized as an internal or external command
```

**Solution:**

```bash
# 1. Check Python installation
python --version

# 2. If not found, install from python.org
# Download from: https://www.python.org/downloads/

# 3. Add Python to PATH manually
set PATH=%PATH%;C:\Python311

# 4. Verify
python --version
```

### ❌ Problem 2: Requirements Not Installing

**Symptom:**

```
ERROR: Could not find a version that satisfies the requirement ...
```

**Solution:**

```bash
# 1. Upgrade pip
python -m pip install --upgrade pip

# 2. Check requirements.txt
type requirements.txt

# 3. Install with verbose output
pip install -r requirements.txt -v

# 4. Install individually to find problematic package
pip install pytest
pip install playwright
```

### ❌ Problem 3: Tests Not Found

**Symptom:**

```
ERROR: not found: project_playwright\tests\UI (no such file or directory)
```

**Solution:**

```bash
# 1. Verify directory structure
dir tests\UI
dir tests\API

# 2. Verify test files have correct naming
dir /B tests\UI\test_*.py

# 3. Check if in correct directory
cd c:\Users\TUSHAR\Desktop\Playwright_Framework\project_playwright
dir

# 4. List all tests
python -m pytest --collect-only -q
```

### ❌ Problem 4: Playwright Not Installed

**Symptom:**

```
ModuleNotFoundError: No module named 'playwright'
```

**Solution:**

```bash
# 1. Install Playwright
pip install playwright

# 2. Install browsers
python -m playwright install

# 3. Verify installation
python -c "import playwright; print(playwright.__version__)"
```

### ❌ Problem 5: Test Failures

**Symptom:**

```
FAILED tests/UI/test_case_01_register_user.py::test_register_new_user
```

**Solution:**

```bash
# 1. Run with more verbosity
python -m pytest tests/UI/test_case_01_register_user.py -vv

# 2. Show full traceback
python -m pytest tests/UI/test_case_01_register_user.py --tb=long

# 3. Check screenshots
dir screenshots\

# 4. Review logs
type logs\test_execution.log

# 5. Run in non-headless mode for debugging
# Modify conftest.py or run with:
# --headed (if supported in your setup)
```

---

## Step-by-Step Validation Checklist

### ✅ Pre-Execution Checks (Do This First)

```
[ ] Python installed (python --version)
[ ] pip working (pip --version)
[ ] Project directory exists
[ ] requirements.txt present
[ ] tests/UI folder has test files
[ ] tests/API folder has test files
[ ] Jenkins/Jenkinsfile exists
[ ] Read permissions on all directories
[ ] Enough disk space (at least 1 GB)
```

### ✅ Execution Checks (During Test Run)

```
[ ] Tests are collecting (pytest --collect-only shows items)
[ ] Tests are executing (see test progress)
[ ] No Python errors
[ ] Console shows visual separators (════════)
[ ] Status indicators visible (✓, ✗, ⚠)
[ ] Test output colored (if ANSI color supported)
```

### ✅ Post-Execution Checks (After Completion)

```
[ ] test-results.xml file created
[ ] allure-results directory created with JSON files
[ ] logs directory created with log files
[ ] screenshots directory created (if tests failed)
[ ] Final build status shown (SUCCESS, FAILED, UNSTABLE)
[ ] Build summary displayed
```

### ✅ Jenkins-Specific Checks

```
[ ] Jenkinsfile syntax valid
[ ] Git repository configured
[ ] Build parameters available in UI
[ ] Workspace shows artifacts
[ ] Console output matches local run
[ ] Test report displayed
[ ] Allure report generated
```

---

## Performance Baseline

Use this to measure your pipeline's typical performance:

```
Typical Execution Times:

Stage                    | Expected Time | Acceptable Range
─────────────────────────┼───────────────┼──────────────────
Pre-Build Validation     | 5 seconds     | 2-10 seconds
Checkout                 | 10 seconds    | 5-20 seconds
Initialize Environment   | 2 seconds     | 1-5 seconds
Validate Python          | 5 seconds     | 2-10 seconds
Clean Workspace          | 10 seconds    | 5-20 seconds
Install Dependencies     | 60 seconds    | 40-120 seconds
Validate Configuration   | 5 seconds     | 2-10 seconds
Run Test Suite (UI)      | 120-300 sec   | 60-600 seconds
Collect Results          | 20 seconds    | 10-60 seconds
Generate Reports         | 30 seconds    | 10-60 seconds
Parse Results            | 10 seconds    | 5-20 seconds
─────────────────────────┼───────────────┼──────────────────
Total (UI Suite)         | 250-450 sec   | 150-900 seconds
                         | (4-7 minutes) | (2.5-15 minutes)
```

---

## Success Criteria

### ✅ Your Pipeline is Working if:

1. **Checkout Stage**
   - ✓ Git repository cloned
   - ✓ All files present
   - ✓ Commit hash shown

2. **Environment Setup**
   - ✓ Python version detected
   - ✓ Dependencies installed
   - ✓ Playwright browsers installed

3. **Test Execution**
   - ✓ Tests collected
   - ✓ Tests executed
   - ✓ Results generated

4. **Reporting**
   - ✓ JUnit XML created
   - ✓ Allure results generated
   - ✓ Test statistics shown

5. **Artifacts**
   - ✓ Logs collected
   - ✓ Screenshots captured (on failure)
   - ✓ Results archived

6. **Notifications**
   - ✓ Build status shown
   - ✓ Summary displayed
   - ✓ Email ready (once configured)

---

## Quick Demo Commands

### Quick Demo (2 minutes)

```bash
# Copy-paste this entire block

cd c:\Users\TUSHAR\Desktop\Playwright_Framework\project_playwright
echo.
echo "════════════════════════════════════════════════"
echo "PLAYWRIGHT JENKINS PIPELINE - QUICK DEMO"
echo "════════════════════════════════════════════════"
echo.

echo [1/5] Checking Python...
python --version

echo.
echo [2/5] Listing test files...
dir /B tests\UI\test_*.py | find /C "test_"

echo.
echo [3/5] Collecting tests...
python -m pytest tests/UI --collect-only -q | find /C "test"

echo.
echo [4/5] Running UI tests...
python -m pytest tests/UI -m ui -v --tb=line -x --maxfail=3

echo.
echo [5/5] Checking results...
if exist test-results.xml (
    echo ✓ Test results generated
) else (
    echo ✗ Test results not found
)

echo.
echo "════════════════════════════════════════════════"
echo "DEMO COMPLETE"
echo "════════════════════════════════════════════════"
```

---

## Next: Moving to Jenkins

Once local testing is successful:

1. **Install Jenkins** (if not already)
2. **Create Pipeline Job**
3. **Point to Jenkinsfile**
4. **Configure Git Repository**
5. **Set up Build Triggers**
6. **Configure Email/Slack (optional)**
7. **Run First Build**
8. **Review Console Output**
9. **Check Artifacts & Reports**
10. **Fine-tune as Needed**

---

## Summary

Your pipeline is working correctly if you see:

- ✅ All stages complete
- ✅ Visual separators in output
- ✅ Test results generated
- ✅ Artifacts collected
- ✅ Build status shown

**Start with Local Testing → Then Move to Jenkins**
