"""
Unit tests for Reporting Service
"""

import pytest
from pathlib import Path
from services.report_service import ReportService
from services.monitoring_service import monitoring_service


def test_generate_csv_reports():
    reporter = ReportService()
    csv_metrics = reporter.generate_csv_metrics()
    assert "Timestamp,CPU %,RAM %,Disk %" in csv_metrics

    csv_events = reporter.generate_csv_events()
    assert "Timestamp,Severity,Event Type" in csv_events


def test_generate_pdf_report(tmp_path):
    reporter = ReportService()
    data = monitoring_service.collect_and_evaluate()
    target_pdf = tmp_path / "test_report.pdf"

    generated_path = reporter.generate_pdf_report(data, output_path=target_pdf)
    assert generated_path.exists()
    assert generated_path.stat().st_size > 500  # PDF should contain binary content
