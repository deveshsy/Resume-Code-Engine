from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

# Config
W, H = A4
ML, MR, MT, MB = 18*mm, 18*mm, 14*mm, 14*mm
CONTENT_W = W - ML - MR
THEME = {"DARK": colors.HexColor("#111827"), "ACCENT": colors.HexColor("#2563eb"), "RULE": colors.HexColor("#e5e7eb")}

def get_style(name, **kw):
    base = dict(fontName="Helvetica", fontSize=9, leading=13, textColor=colors.HexColor("#374151"))
    base.update(kw)
    return ParagraphStyle(name, **base)

styles = {
    "name": get_style("name", fontName="Helvetica-Bold", fontSize=21, alignment=TA_CENTER),
    "contact": get_style("contact", fontSize=8.5, alignment=TA_CENTER),
    "header": get_style("h", fontName="Helvetica-Bold", fontSize=9, textColor=THEME["ACCENT"]),
    "role": get_style("role", fontName="Helvetica-Bold", fontSize=9, textColor=THEME["DARK"]),
    "meta": get_style("meta", fontSize=8, textColor=colors.HexColor("#6b7280")),
    "bullet": get_style("bullet", leftIndent=8),
}

def create_entry(title, org, date, bullets=None):
    tp, dp = Paragraph(f"<b>{title}</b>", styles["role"]), Paragraph(date, styles["meta"])
    hdr = Table([[tp, dp]], colWidths=[CONTENT_W*0.7, CONTENT_W*0.3])
    hdr.setStyle(TableStyle([("ALIGN",(1,0),(1,0),"RIGHT"), ("LEFTPADDING",(0,0),(-1,-1),0)]))
    items = [hdr, Paragraph(org, styles["meta"])]
    if bullets: items += [Paragraph(f"<bullet>•</bullet> {b}", styles["bullet"]) for b in bullets]
    return KeepTogether(items + [Spacer(1, 4*mm)])

def generate(data, out):
    doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB)
    story = [Paragraph(data['name'], styles["name"]), Spacer(1, 2*mm), Paragraph(data['contact'], styles["contact"]), Spacer(1, 6*mm)]
    for sec, content in data['sections'].items():
        story += [Paragraph(f"<b>{sec.upper()}</b>", styles["header"]), HRFlowable(width="100%", thickness=0.4, color=THEME["RULE"]), Spacer(1, 2*mm)]
        for item in content: story.append(create_entry(item['title'], item['org'], item['date'], item.get('bullets')))
    doc.build(story)

if __name__ == "__main__":
    my_data = {
        "name": "Devesh Singh Yadav",
        "contact": "dsy230105@gmail.com | github.com/deveshsy | Bhopal, India",
        "sections": {
            "Experience": [{"title": "Business Analytics Intern", "org": "AICTE x Qlik", "date": "2024", "bullets": ["Built KPI dashboards", "Analyzed datasets"]}],
            "Education": [{"title": "B.Tech CSE", "org": "VIT Bhopal University", "date": "2023 - 2027"}]
        }
    }
    generate(my_data, "resume.pdf")
