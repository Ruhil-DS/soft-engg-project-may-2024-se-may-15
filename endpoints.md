# This has a list of all the endpoints and how to hit them.

This endpoint is used to get the summary of a lecture.
- /summery/video/
  - POST
  - Request:
    - body:
      - week_num: int
      - lecture_num: int
  - Returns: 
    - body:
      - summery: string

- /summery/slides/
  - POST
  - Request:
      - body:
        - week_num: int
        - lecture_num: int
    - Returns: 
        - body:
          - summery: string