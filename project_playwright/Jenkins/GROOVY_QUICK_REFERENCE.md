# Groovy for Jenkins - Quick Reference Guide

## Essential Groovy Syntax

### 1. Variables & Data Types

```groovy
// String
String name = "Jenkins"
def message = "Hello ${name}"  // String interpolation

// Numbers
int count = 42
double price = 19.99
long bigNumber = 1000000L

// Boolean
boolean isActive = true
boolean isEmpty = false

// Lists
List<String> items = ['a', 'b', 'c']
def list = [1, 2, 3]

// Maps
Map<String, String> config = ['key1': 'value1', 'key2': 'value2']
def map = [name: 'John', age: 30]
```

### 2. String Operations

```groovy
String text = "Hello World"

// Length
text.length()  // 11

// Case conversion
text.toLowerCase()   // "hello world"
text.toUpperCase()   // "HELLO WORLD"

// Substring
text.substring(0, 5)   // "Hello"

// Contains
text.contains("World")   // true

// Replace
text.replace("World", "Groovy")   // "Hello Groovy"

// Split
text.split(" ")   // ["Hello", "World"]

// Trim
"  text  ".trim()   // "text"
```

### 3. Conditionals

```groovy
// If-Else
if (condition) {
    println "True branch"
} else if (otherCondition) {
    println "Other branch"
} else {
    println "Default branch"
}

// Ternary Operator
def result = condition ? "yes" : "no"

// Switch
switch (value) {
    case 1:
        println "One"
        break
    case 2:
        println "Two"
        break
    default:
        println "Other"
}

// Elvis Operator
def name = user?.name ?: "Unknown"
```

### 4. Loops

```groovy
// For Loop
for (int i = 0; i < 5; i++) {
    println i
}

// For-Each
for (item in items) {
    println item
}

// While Loop
while (condition) {
    // Code
}

// Each (Functional)
items.each { item ->
    println item
}

// Times
5.times { i ->
    println i
}
```

### 5. Functions & Methods

```groovy
// Define function
def greet(String name) {
    return "Hello ${name}"
}

// Function with default parameter
def sayHello(String name = "World") {
    println "Hello ${name}"
}

// Function with multiple parameters
def add(int a, int b) {
    return a + b
}

// Function with variable arguments
def printAll(String... args) {
    args.each { println it }
}

// Call function
greet("John")    // "Hello John"
add(5, 3)        // 8
```

### 6. Closures

```groovy
// Simple closure
def myClosure = { println "Hello" }
myClosure()  // Executes closure

// Closure with parameters
def addNumbers = { a, b -> a + b }
addNumbers(5, 3)  // 8

// Closure with implicit parameter (it)
def printItem = { println it }
[1, 2, 3].each(printItem)

// Closure in method
def process(Closure closure) {
    closure("data")
}

process { data ->
    println "Processing: ${data}"
}
```

### 7. Collections

```groovy
// Lists
def list = [1, 2, 3, 4, 5]

list.add(6)           // Add element
list.remove(0)        // Remove by index
list.get(0)           // Get element
list.size()           // Get size
list.contains(3)      // Check existence

// List operations
list.first()          // First element
list.last()           // Last element
list.reverse()        // Reverse
list.sort()           // Sort
list.unique()         // Remove duplicates

// Filtering
list.findAll { it > 2 }        // [3, 4, 5]
list.find { it > 2 }           // 3
list.any { it > 4 }            // true
list.all { it > 0 }            // true

// Mapping
list.collect { it * 2 }        // [2, 4, 6, 8, 10]

// Maps
def map = [name: 'John', age: 30]

map.get('name')       // 'John'
map['age']            // 30
map.name              // 'John'

map.put('city', 'NYC')  // Add entry
map.remove('age')       // Remove entry
map.keys()            // ['name', 'city']
map.values()          // ['John', 'NYC']
map.size()            // 2
```

### 8. Exception Handling

```groovy
// Try-Catch
try {
    // Code that might throw exception
    int result = 10 / 0
} catch (ArithmeticException e) {
    println "Math error: ${e.message}"
} catch (Exception e) {
    println "General error: ${e.message}"
} finally {
    println "Always executed"
}

// Throw exception
if (name == null) {
    throw new IllegalArgumentException("Name cannot be null")
}

// Try with resource
try {
    def file = new File("data.txt")
} finally {
    file?.close()
}
```

### 9. Regular Expressions

```groovy
// Pattern matching
String text = "Hello123World"

if (text =~ /\d+/) {
    println "Contains numbers"
}

// Extract matches
def matches = (text =~ /\d+/).findAll()  // ['123']

// Replace with regex
text.replaceAll(/\d/, 'X')  // "HelloXXXWorld"

// Split with regex
text.split(/\d+/)  // ['Hello', 'World']

// Pattern object
def pattern = ~/\d+/
pattern.matcher(text).find()  // true
```

### 10. File Operations

```groovy
// Read file
def content = new File("data.txt").text
def lines = new File("data.txt").readLines()

// Write file
new File("output.txt").text = "Hello World"
new File("output.txt").write("Content")

// Append to file
new File("log.txt").append("\nNew line")

// Check file exists
new File("data.txt").exists()  // true/false

// List files in directory
new File("src").listFiles().each { println it.name }

// Create directories
new File("path/to/dir").mkdirs()
```

### 11. Operators

```groovy
// Arithmetic
5 + 3        // 8
5 - 3        // 2
5 * 3        // 15
5 / 2        // 2.5
5 % 2        // 1
2 ** 3       // 8 (exponentiation)

// Comparison
5 == 5       // true
5 != 3       // true
5 > 3        // true
5 >= 5       // true
5 < 10       // true
5 <= 5       // true

// Logical
true && true   // true (AND)
true || false  // true (OR)
!true          // false (NOT)

// String operators
"Hello" + " " + "World"   // "Hello World"
"abc" * 3                  // "abcabcabc"
"Hello".startsWith("He")   // true

// In operator
3 in [1, 2, 3]             // true
"a" in "abc"               // true
```

---

## Jenkins-Specific Groovy Patterns

### 1. Environment Variables

```groovy
// Access Jenkins environment
env.BUILD_NUMBER           // Current build number
env.BUILD_ID               // Build ID
env.JOB_NAME               // Job name
env.WORKSPACE              // Jenkins workspace path
env.BUILD_URL              // Build URL
env.BUILD_USER             // User who triggered build
env.BRANCH_NAME            // Branch name

// Set custom variable
env.MY_VAR = "custom value"

// Use in string
echo "Build number: ${env.BUILD_NUMBER}"
```

### 2. Parameters

```groovy
// Access build parameters
params.SUITE               // Parameter value
params.get('SUITE')        // Alternative access
params.HEADLESS            // Boolean parameter

// Use in conditions
if (params.SUITE == 'UI') {
    // UI test logic
}
```

### 3. Current Build

```groovy
// Build information
currentBuild.number        // Build number
currentBuild.displayName   // Build display name
currentBuild.result        // Build result
currentBuild.duration      // Duration in milliseconds
currentBuild.durationString  // Human readable duration

// Set build result
currentBuild.result = 'SUCCESS'
currentBuild.result = 'FAILURE'
currentBuild.result = 'UNSTABLE'

// Build description
currentBuild.description = "Custom build description"
```

### 4. Stages

```groovy
// Define stage
stage('Build') {
    steps {
        echo "Building..."
    }
}

// Stage with when condition
stage('Test') {
    when {
        expression { params.RUN_TESTS == true }
    }
    steps {
        echo "Running tests..."
    }
}

// Parallel stages
stage('Tests') {
    parallel {
        stage('Unit Tests') {
            steps { /* tests */ }
        }
        stage('Integration Tests') {
            steps { /* tests */ }
        }
    }
}
```

### 5. Shell Commands

```groovy
// Execute shell command
sh 'echo "Hello World"'

// With returnStdout
def output = sh(
    script: 'date',
    returnStdout: true
).trim()

// With returnStatus
def status = sh(
    script: 'test -f file.txt',
    returnStatus: true
)

// Multi-line shell script
sh '''
    echo "Line 1"
    echo "Line 2"
    if [ -f "file.txt" ]; then
        echo "File exists"
    fi
'''
```

### 6. Timeouts

```groovy
// Global timeout
options {
    timeout(time: 60, unit: 'MINUTES')
}

// Stage timeout
timeout(time: 10, unit: 'MINUTES') {
    sh 'long-running-command'
}

// Timeout with retry
timeout(time: 5, unit: 'MINUTES') {
    retry(3) {
        sh 'flaky-command'
    }
}
```

### 7. Error Handling

```groovy
// Try-catch in pipeline
try {
    sh 'failing-command'
    echo "✓ Command succeeded"
} catch (Exception e) {
    echo "✗ Error: ${e.message}"
    currentBuild.result = 'FAILURE'
}

// Error function
if (status != 0) {
    error("Command failed with status: ${status}")
}

// Warning with continue
try {
    optional_command()
} catch (Exception e) {
    echo "⚠ Warning: ${e.message}"
    // Continue pipeline
}
```

### 8. Post Actions

```groovy
post {
    // Always executed
    always {
        echo "This always runs"
        junit 'test-results.xml'
    }

    // Only on success
    success {
        echo "Build succeeded"
    }

    // Only on failure
    failure {
        echo "Build failed"
    }

    // On unstable
    unstable {
        echo "Build is unstable"
    }

    // On abort
    aborted {
        echo "Build was aborted"
    }

    // Final cleanup
    cleanup {
        echo "Final cleanup"
        cleanWs()
    }
}
```

### 9. Archive & Store Artifacts

```groovy
// Archive artifacts
archiveArtifacts artifacts: 'logs/**/*',
                   allowEmptyArchive: true,
                   fingerprint: true

// Junit results
junit testResults: 'test-results.xml',
      allowEmptyResults: true

// HTML report
publishHTML([
    reportDir: 'reports',
    reportFiles: 'index.html',
    reportName: 'Test Report'
])
```

### 10. Functions & Reusable Code

```groovy
// Define function
def deployApp(String env) {
    echo "Deploying to ${env}..."
    sh "deploy.sh ${env}"
}

// Call function
deployApp('staging')
deployApp('production')

// Function with return value
def getVersion() {
    def version = sh(
        script: 'cat version.txt',
        returnStdout: true
    ).trim()
    return version
}

def version = getVersion()
echo "Version: ${version}"
```

---

## Common Jenkins Problems & Solutions

### Problem: Variable Not Accessible in Shell

```groovy
// ❌ Wrong - env var not visible in shell
env.MY_VAR = "value"
sh 'echo $MY_VAR'  // Empty

// ✓ Correct - export before using
sh '''
    MY_VAR="value"
    echo $MY_VAR
'''

// ✓ Correct - use env prefix
sh 'echo ${MY_VAR}'  // But still won't work if set in Groovy

// ✓ Correct - set in environment
environment {
    MY_VAR = "value"
}
sh 'echo $MY_VAR'  // Works!
```

### Problem: Build Doesn't Fail on Error

```groovy
// ❌ Script error doesn't fail build
sh 'python script.py || echo "Failed"'

// ✓ Correct - let errors fail the build
sh 'python script.py'

// ✓ Correct - check exit code
def status = sh(
    script: 'python script.py',
    returnStatus: true
)
if (status != 0) {
    error("Script failed!")
}
```

### Problem: Timeout Not Working

```groovy
// ❌ Timeout at pipeline level may not work for all
timeout(time: 10, unit: 'MINUTES') {
    build job: 'other-job'
}

// ✓ Correct - timeout applies to steps
stage('Build') {
    steps {
        timeout(time: 10, unit: 'MINUTES') {
            sh 'long-running-command'
        }
    }
}
```

---

## Performance Tips

1. **Use sh with returnStatus instead of catching errors:**

   ```groovy
   def status = sh(script: 'cmd', returnStatus: true)
   ```

2. **Avoid unnecessary string interpolation:**

   ```groovy
   // Slower
   sh "echo ${var1} ${var2} ${var3}"

   // Faster
   sh '''
       echo $VAR1 $VAR2 $VAR3
   '''
   ```

3. **Cache expensive operations:**

   ```groovy
   @Field String cachedVersion

   def getVersion() {
       if (!cachedVersion) {
           cachedVersion = sh(script: 'version.sh', returnStdout: true).trim()
       }
       return cachedVersion
   }
   ```

4. **Use parallel execution:**
   ```groovy
   parallel(
       'Unit Tests': { sh 'pytest tests/unit' },
       'Integration Tests': { sh 'pytest tests/integration' }
   )
   ```

---

## Resources

- [Apache Groovy Documentation](http://groovy-lang.org/documentation.html)
- [Jenkins Declarative Pipeline Syntax](https://jenkins.io/doc/book/pipeline/syntax/)
- [Jenkins Groovy Hook Scripts](https://plugins.jenkins.io/groovy/)
- [Groovy Collections Documentation](http://groovy-lang.org/collections.html)
