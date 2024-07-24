# This has a list of all the endpoints and how to hit them.

/api/login/

- **POST**

- **Request**:
  
  - body:
    
    - `username`: string
    - `password`: string

- **Returns**:
  
  - body:
    - `token`: string (Fake)

/api/register/

- **POST**

- **Request**:
  
  - body:
    
    - `username`: string
    - `password`: string

- **Returns**:
  
  - body:
    - `token`: string (Fake)

This endpoint is used to get the summary of a lecture.

### Story Point 1

/api/summary/video/<week_num>/<lecture_num>

- **GET**
- **Returns**: 
  - body:
    - `summary`: string

### Story Point 2

/api/summary/slides/<week_num>/<lecture_num>

- **GET**
- **Returns**: 
  - body:
    - `summary`: string

### Story Point 3

/api/translate/

- **POST**
- **Request**:
  - body:
    - `text`: string
    - `language`: string
- **Returns**: 
  - body:
    - `translation`: string

### Story Point 4 & 10:

This will return a list of questions. These will be stored in the database as well.  POST request generates new questions for the week. GET request returns the previously generated questions for the week.

/api/assignment/generate/theory/<week_num>/

- **POST**

- **Request**:
  
  - body: null

- **Returns**:
  
  - body:
    - `assignment`: list
      - `question_num`: int
      - `question`: string
      - `options`: list 
        - `option_num`: int
        - `option`: string
      - `correct_option`: int

- **GET**

- **Returns**:
  
  - body:
    - `assignment`: list
      - `question_num`: int
      - `question`: string
      - `options`: list 
        - `option_num`: int
        - `option`: string
      - `correct_option`: int

/api/assignment/generate/programming/<week_num>/

- **POST**
- **Request**:
  - body:
    - `week_num`: int
  - Returns: 
    - body:
      - `assignment`: list
        - `question_num`: int
        - `question`: string
        - `test_cases`: list
          - `test_case_num`: int
          - `input`: string
          - `output`: string
- **GET**
- **Returns**: 
  - body:
    - `assignment`: list
      - `question_num`: int
      - `question`: string
      - `test_cases`: list
        - `test_case_num`: int
        - `input`: string
        - `output`: string

/api/assignment/submit/theory/<week_num>/

- **POST**
- **Request**:
  - body:
    - `answer`: list
      - `question_num`: int
      - `answer`: int
- **Returns**: 
  - body:
    - `score`: list
      - `question_num`: int
      - `correct`: boolean

/api/assignment/submit/programming/<week_num>/<question_num>/

- **POST**
- **Request**:
  - body:
    - `answer`: string
  - Returns:
    - body:
      - score: list
        - `public_test_cases`: list
          - `test_case_number`: int
          - `passed`:boolean
        - `test_case_number`: int

/api/assignment/GA/<week_num>/

- **GET**

- **Returns**:
  
  - body:
    - `assignment`: list
      - `question_num`: int
      - `question`: string
      - `options`: list 
        - `option_num`: int
        - `option`: string
      - `correct_option`: int

/api/assignment/GrPA/<week_num>/

- **GET**
- **Returns**:
  - body:
    - `assignment`: list
      - `question_num`: int
        - `question`: string
        - `test_cases`: list
          - `test_case_num`: int
          - `input`: string
          - `output`: string

/api/assignment/submit/GA/<Week_num>/

- **POST**
- **Request**:
  - body:
    - `answer`: list
      - `question_num`: int
      - `answer`: int
- **Returns**:
  - body:
    - `score`: list
      - `question_num`: int
      - `correct`: boolean

/api/assignment/submit/GrPA/<week_num>/<question_num>/

- **POST**
- **Request**:
  - body:
    - `answer`: string
- **Returns**:
  - body:
    - `score`: list
      - `public_test_cases`: list
        - `test_case_number`: int
        - `passed`:boolean
      - `private_test_case`: string (X out of Y test cases)

### Story Point 5 & 11

/api/assignment/feedback/<assignment_type>/<week_num>/

- **POST**

- **Request:**
  
  - **body:**
    - `answers`: list of submitted answers

- **Returns:**
  
  - **body:**
    - `feedback`: list of feedback objects containing:
      - `question_id`: string
      - `correct`: boolean
      - `feedback`: string (detailed explanation of mistakes and tips)
      - `suggestions`: string (optional tips for improvement)

### Story Point 6

Use this endpoint for the programming questions. Generates suggestions before you start solving a question.

/api/assignment/suggestion/<assignment_type>/<week_num>/<question_num>/

- **Returns:**
  
  - **body**:
    - `suggestions`: string

### Story Point 7 & 11

/api/pain_point/

- **GET**

- **Returns**:
  
  - **body**:
    
    - `pain_points`: string
    
    - `revision_plan`: string

### Story Point 8

Handle the speech to text in the front end using some random JS module.

/api/transcript_to_code/

- **POST**

- **Request**
  
  - body:
    
    - `transcript`: string

- **Returns**
  
  - body:
    
    - `code`: string

### Story Point 9

/api/chatbot/query/

- **POST**

- **Request:**
  
  - **body:**
    - `query`: string

- **Returns:**
  
  - **body:**
    - `answer`: string

### Story Point 12

Makes test cases and stores it in the back end. Only for instructors.

/api/assignment/<week_num>/<question_num>/

- **GET**

- Returns:
  
  - body:
    
    - `public_test_cases`: list 
      
      - `test_case_id`: int
      
      - `input`: string
      
      - `output`: string
    
    - `private_test_cases`:
      
      - `test_case_id`: int
      
      - `input`: string
      
      - `output`: string
