### Gen AI Features

#### 1. API Endpoint: Get Feedback for a Theory Assignment
**API URL being tested:** `https://127.0.0.1:5000/api/v1/assignment/graded/theory/6/generate-feedback`
- **Inputs:**
  - **Request Method:** POST
  - **JSON:**
    ```json
    {
      "assignment_type": "theory",
      "questions": [
        {
          "question_num": 1,
          "correct_option_num": 1,
          "submitted_option_num": 2
        }
      ]
    }
    ```
  - **Header:**
    ```json
    {
      "Content-Type": "application/json"
    }
    ```
- **Expected Output:**
  - **HTTP Status Code:** 200
  - **JSON:**
    ```json
    {
      "feedback": [
        {
          "question_num": 1,
          "correct_option_num": 1,
          "submitted_option_num": 2,
          "feedback": "Incorrect"
        }
      ]
    }
    ```
- **Actual Output:**
  - **HTTP Status Code:** [actual status code]
  - **JSON:** [actual JSON response]
- **Result:** Success/Failure

#### 2. API Endpoint: Generate Test Cases for a Programming Assignment
**API URL being tested:** `https://127.0.0.1:5000/api/v1/assignment/practice/programming/6/generate-test-cases`
- **Inputs:**
  - **Request Method:** POST
  - **JSON:**
    ```json
    {
      "assignment_type": "programming",
      "questions": [
        {
          "question_num": 1,
          "question": "Define a function list_product() that takes a list of integers as input and returns the product",
          "test_cases": {
            "public": [
              {
                "test_input": "[2, 3, 4]",
                "expected_output": "24"
              }
            ],
            "private": [
              {
                "test_input": "[2, -3, 4]",
                "expected_output": "-24"
              }
            ]
          }
        }
      ]
    }
    ```
  - **Header:**
    ```json
    {
      "Content-Type": "application/json"
    }
    ```
- **Expected Output:**
  - **HTTP Status Code:** 200
  - **JSON:**
    ```json
    {
      "test_cases": {
        "public": [
          {
            "test_input": "[2, 3, 4]",
            "expected_output": "24"
          }
        ],
        "private": [
          {
            "test_input": "[2, -3, 4]",
            "expected_output": "-24"
          }
        ]
      }
    }
    ```
- **Actual Output:**
  - **HTTP Status Code:** [actual status code]
  - **JSON:** [actual JSON response]
- **Result:** Success/Failure

### Non-Gen AI Features

#### 1. API Endpoint: Get Assignment List
**API URL being tested:** `https://127.0.0.1:5000/api/v1/assignments`
- **Inputs:**
  - **Request Method:** GET
  - **Header:**
    ```json
    {
      "Accept": "application/json"
    }
    ```
- **Expected Output:**
  - **HTTP Status Code:** 200
  - **JSON:**
    ```json
    [
      {
        "assignment_id": 1,
        "assignment_type": "theory",
        "module_id": 6,
        "due_date": "2024-10-10T23:59:59.000Z"
      }
    ]
    ```
- **Actual Output:**
  - **HTTP Status Code:** [actual status code]
  - **JSON:** [actual JSON response]
- **Result:** Success/Failure

#### 2. API Endpoint: Submit Assignment
**API URL being tested:** `https://127.0.0.1:5000/api/v1/assignment/1/submit`
- **Inputs:**
  - **Request Method:** POST
  - **JSON:**
    ```json
    {
      "assignment_id": 1,
      "submission": "Here is my answer."
    }
    ```
  - **Header:**
    ```json
    {
      "Content-Type": "application/json"
    }
    ```
- **Expected Output:**
  - **HTTP Status Code:** 200
  - **JSON:**
    ```json
    {
      "status": "submitted",
      "assignment_id": 1,
      "submission": "Here is my answer."
    }
    ```
- **Actual Output:**
  - **HTTP Status Code:** [actual status code]
  - **JSON:** [actual JSON response]
- **Result:** Success/Failure

### Other Functionalities

#### 1. API Endpoint: Get Assignment Details
**API URL being tested:** `https://127.0.0.1:5000/api/v1/assignment/1`
- **Inputs:**
  - **Request Method:** GET
  - **Header:**
    ```json
    {
      "Accept": "application/json"
    }
    ```
- **Expected Output:**
  - **HTTP Status Code:** 200
  - **JSON:**
    ```json
    {
      "assignment_id": 1,
      "assignment_type": "theory",
      "module_id": 6,
      "due_date": "2024-10-10T23:59:59.000Z"
    }
    ```
- **Actual Output:**
  - **HTTP Status Code:** [actual status code]
  - **JSON:** [actual JSON response]
- **Result:** Success/Failure

#### 2. API Endpoint: Delete Assignment
**API URL being tested:** `https://127.0.0.1:5000/api/v1/assignment/1`
- **Inputs:**
  - **Request Method:** DELETE
  - **Header:**
    ```json
    {
      "Accept": "application/json"
    }
    ```
- **Expected Output:**
  - **HTTP Status Code:** 200
  - **JSON:**
    ```json
    {
      "status": "deleted",
      "assignment_id": 1
    }
    ```
- **Actual Output:**
  - **HTTP Status Code:** [actual status code]
  - **JSON:** [actual JSON response]
- **Result:** Success/Failure
