from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


def generate_pdf_report(
    filename,
    ats_score,
    skills,
    recommendations,
    suggestions
):
    """
    Generate a PDF report containing resume analysis,
    job recommendations, skills and improvement suggestions.
    """

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=15,
        spaceAfter=10
    )

    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14
    )

    story = []

    # --------------------------------------------------
    # Title
    # --------------------------------------------------

    story.append(
        Paragraph(
            "AI Job Recommendation Report",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Resume Analysis & Personalized Job Recommendations",
            normal_style
        )
    )

    story.append(Spacer(1, 15))

    # --------------------------------------------------
    # ATS Score
    # --------------------------------------------------

    story.append(
        Paragraph(
            "Resume ATS Score",
            heading_style
        )
    )

    ats_table = Table(
        [["ATS Score", f"{ats_score}/100"]],
        colWidths=[2.5 * inch, 2 * inch]
    )

    ats_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("PADDING", (0, 0), (-1, -1), 8),
        ])
    )

    story.append(ats_table)

    # --------------------------------------------------
    # Detected Skills
    # --------------------------------------------------

    story.append(
        Paragraph(
            "Detected Skills",
            heading_style
        )
    )

    if skills:
        story.append(
            Paragraph(
                ", ".join(skills),
                normal_style
            )
        )
    else:
        story.append(
            Paragraph(
                "No technical skills detected.",
                normal_style
            )
        )

    # --------------------------------------------------
    # Job Recommendations
    # --------------------------------------------------

    story.append(
        Paragraph(
            "Job Recommendations",
            heading_style
        )

    )

    if recommendations:

        table_data = [
            [
                "Job Title",
                "Overall Match",
                "Semantic",
                "Skill Match"
            ]
        ]

        for job in recommendations:
            table_data.append([
                job["job_title"],
                f"{job['final_score']:.2f}%",
                f"{job['semantic_score']:.2f}%",
                f"{job['skill_score']:.2f}%"
            ])

        recommendation_table = Table(
            table_data,
            repeatRows=1,
            colWidths=[
                2.2 * inch,
                1.1 * inch,
                1.1 * inch,
                1.1 * inch
            ]
        )

        recommendation_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.black
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (-1, -1),
                    "CENTER"
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
            ])
        )

        story.append(recommendation_table)

    else:
        story.append(
            Paragraph(
                "No job recommendations available.",
                normal_style
            )
        )

    # --------------------------------------------------
    # Skill Analysis
    # --------------------------------------------------

    story.append(
        Paragraph(
            "Skill Analysis",
            heading_style
        )
    )

    for job in recommendations:

        story.append(
            Paragraph(
                f"<b>{job['job_title']}</b>",
                normal_style
            )
        )

        matched = ", ".join(
            job["matched_skills"]
        ) if job["matched_skills"] else "None"

        missing = ", ".join(
            job["missing_skills"]
        ) if job["missing_skills"] else "None"

        story.append(
            Paragraph(
                f"<b>Matching Skills:</b> {matched}",
                normal_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Missing Skills:</b> {missing}",
                normal_style
            )
        )

        story.append(Spacer(1, 6))

    # --------------------------------------------------
    # Resume Improvement Suggestions
    # --------------------------------------------------

    story.append(
        Paragraph(
            "Resume Improvement Suggestions",
            heading_style
        )
    )

    for suggestion in suggestions:
        story.append(
            Paragraph(
                f"• {suggestion}",
                normal_style
            )
        )

    # --------------------------------------------------
    # Build PDF
    # --------------------------------------------------

    doc.build(story)