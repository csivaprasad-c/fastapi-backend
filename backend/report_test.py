import json

import pytest

import report


@pytest.fixture
def report_json(scope="session"):
    report.generate_report()

    with open("report.json", "r") as f:
        return json.load(f)


def test_generate_report(report_json):
    assert type(report_json) == dict


def test_report_content(report_json):
    assert report_json["timestamp"] == "2026-01-01 10:00:00"
    assert report_json["status"] == "PASSED"
    assert report_json["summary"] == "module.py::test_case"
