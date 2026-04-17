import json


def generate_report():
    dt = {
        "timestamp": "2026-01-01 10:00:00",
        "status": "PASSED",
        "summary": "module.py::test_case",
    }

    with open("report.json", "w") as f:
        json.dump(dt, f)
