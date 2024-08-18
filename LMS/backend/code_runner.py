import re


def run_code(code, test_cases):
    exec(code)

    match = re.search(r"def\s+(\w+)\s*\(", code)

    if match:
        func_name = match.group(1)
    else:
        return [{
            "test_case_id": test_case.test_case_id,
            "result": "Error: Function not found"
        } for test_case in test_cases]

    func = locals()[func_name]

    results = []
    for i, test_case in enumerate(test_cases):
        try:
            result = func(eval(test_case.input_data))
            results.append({
                "test_case_id": test_case.test_case_id,
                "result": str(result) if result else str(None)
            })
        except Exception as e:
            results.append({
                "test_case_id": test_case.test_case_id,
                "result": str(e)
            })

    return results
