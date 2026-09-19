"""
AI-RAT-Detection-Dashboard - Report Service
Generates exportable CSV and professional PDF forensic audit reports.
"""

import io
import csv
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether

from config.config import REPORTS_DIR
from database.database import db


class ReportService:
    """Produces CSV data dumps and formatted PDF threat analysis reports."""

    def generate_csv_metrics(self) -> str:
        """Generates a CSV string of recent system metrics."""
        rows = db.get_recent_metrics(limit=500)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Timestamp", "CPU %", "RAM %", "Disk %", "Process Count", "Bytes Sent", "Bytes Received"])
        for r in rows:
            writer.writerow([
                r["timestamp"],
                r["cpu_percent"],
                r["memory_percent"],
                r["disk_percent"],
                r["process_count"],
                r["bytes_sent"],
                r["bytes_recv"],
            ])
        return output.getvalue()

    def generate_csv_events(self) -> str:
        """Generates a CSV string of recent security events."""
        rows = db.get_recent_events(limit=500)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Timestamp", "Severity", "Event Type", "Description", "Source", "PID", "IP", "Port"])
        for r in rows:
            writer.writerow([
                r["timestamp"],
                r["severity"],
                r["event_type"],
                r["description"],
                r["source"],
                r["pid"] or "",
                r["ip"] or "",
                r["port"] or "",
            ])
        return output.getvalue()

    def generate_pdf_report(self, snapshot_data: Dict[str, Any], output_path: Optional[Path] = None) -> Path:
        """
        Creates an executive forensic PDF report using ReportLab.
        """
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        ts_slug = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = output_path or (REPORTS_DIR / f"Security_Report_{ts_slug}.pdf")

        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40,
        )

        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Heading1"],
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=6,
        )
        subtitle_style = ParagraphStyle(
            "ReportSubtitle",
            parent=styles["Normal"],
            fontSize=10,
            textColor=colors.HexColor("#475569"),
            spaceAfter=14,
        )
        h2_style = ParagraphStyle(
            "SectionHeading",
            parent=styles["Heading2"],
            fontSize=13,
            leading=16,
            textColor=colors.HexColor("#1e293b"),
            spaceBefore=12,
            spaceAfter=6,
        )
        body_style = ParagraphStyle(
            "BodyTextCustom",
            parent=styles["Normal"],
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#334155"),
        )
        alert_box_style = ParagraphStyle(
            "AlertBox",
            parent=styles["Normal"],
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#0f172a"),
        )

        elements = []

        # 1. Header
        elements.append(Paragraph("AI RAT Detection & Forensic Security Report", title_style))
        gen_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_info = snapshot_data.get("metrics", {}).get("user_info", {})
        user_display = user_info.get("display", "Local System")
        elements.append(Paragraph(f"Generated on: {gen_time} | Target Host: {user_display}", subtitle_style))
        elements.append(Spacer(1, 10))

        # 2. Executive Threat Assessment Card
        evaluation = snapshot_data.get("evaluation", {})
        score = evaluation.get("risk_score", 0)
        level = evaluation.get("threat_level", "LOW")
        headline = evaluation.get("headline", "System Safe")
        detail = evaluation.get("status_detail", "")

        level_hex = "#10b981" if level == "LOW" else ("#f59e0b" if level == "MEDIUM" else "#ef4444")

        overview_data = [
            [
                Paragraph(f"<b>Overall Risk Score:</b> {score} / 100", body_style),
                Paragraph(f"<b>Threat Level:</b> <font color='{level_hex}'>{level}</font>", body_style),
            ],
            [
                Paragraph(f"<b>Assessment:</b> {headline}", body_style),
                Paragraph(f"<b>Details:</b> {detail}", body_style),
            ],
        ]
        overview_table = Table(overview_data, colWidths=[260, 260])
        overview_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]))
        elements.append(overview_table)
        elements.append(Spacer(1, 14))

        # 3. Behavioral Findings & Reasons
        reasons = evaluation.get("reasons", [])
        elements.append(Paragraph("Behavioral & Heuristic Findings", h2_style))
        if reasons:
            findings_data = [[Paragraph(f"• {r}", alert_box_style)] for r in reasons]
            findings_table = Table(findings_data, colWidths=[520])
            findings_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fff7ed")),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#fdba74")),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            elements.append(findings_table)
        else:
            elements.append(Paragraph("No anomalous behavioral patterns or malicious signatures detected during this session.", body_style))
        elements.append(Spacer(1, 12))

        # 4. Top Active Processes
        elements.append(Paragraph("Active High-Resource Processes", h2_style))
        top_procs = snapshot_data.get("top_processes", [])[:5]
        proc_table_data = [["PID", "Process Name", "CPU %", "Memory %", "Status"]]
        for p in top_procs:
            proc_table_data.append([
                str(p.get("pid")),
                p.get("name")[:25],
                f"{p.get('cpu_percent')}%",
                f"{p.get('memory_percent')}%",
                p.get("status", "running"),
            ])
        proc_table = Table(proc_table_data, colWidths=[60, 200, 80, 80, 100])
        proc_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        elements.append(proc_table)
        elements.append(Spacer(1, 12))

        # 5. Suspicious Ports & Network Sockets
        elements.append(Paragraph("Flagged Network Connections & Ports", h2_style))
        suspicious_ports = snapshot_data.get("suspicious_ports", [])
        if suspicious_ports:
            net_table_data = [["Port", "Process", "Local Address", "Remote Address", "Risk"]]
            for sp in suspicious_ports[:6]:
                net_table_data.append([
                    str(sp.get("port")),
                    sp.get("process")[:18],
                    sp.get("local_address")[:18],
                    sp.get("remote_address")[:18],
                    sp.get("risk_level"),
                ])
            net_table = Table(net_table_data, colWidths=[50, 120, 130, 130, 90])
            net_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fef2f2")]),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            elements.append(net_table)
        else:
            elements.append(Paragraph("No connections bound to known high-risk RAT ports.", body_style))
        elements.append(Spacer(1, 12))

        # 6. Defensive Recommendations
        recs = evaluation.get("recommendations", [])
        elements.append(Paragraph("Defensive Security Recommendations", h2_style))
        rec_data = [[Paragraph(f"&bull;  {rc}", body_style)] for rc in recs]
        rec_table = Table(rec_data, colWidths=[520])
        rec_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f0fdf4")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#86efac")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        elements.append(rec_table)

        doc.build(elements)
        return filepath


# Singleton instance
report_service = ReportService()
