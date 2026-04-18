from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

W, H = A4
ML, MR, MT, MB = 18*mm, 18*mm, 14*mm, 14*mm

DARK   = colors.HexColor("#111827")
ACCENT = colors.HexColor("#2563eb")
MID    = colors.HexColor("#374151")
MUTED  = colors.HexColor("#6b7280")
RULE   = colors.HexColor("#e5e7eb")

def S(name, **kw):
    base = dict(fontName="Helvetica", fontSize=9, leading=13,
                textColor=MID, spaceAfter=0, spaceBefore=0)
    base.update(kw)
    return ParagraphStyle(name, **base)

sNAME  = S("name", fontName="Helvetica-Bold", fontSize=21, leading=25, textColor=DARK, alignment=TA_CENTER)
sCONT  = S("cont", fontSize=8.5, textColor=MUTED, alignment=TA_CENTER, leading=12)
sSECH  = S("sech", fontName="Helvetica-Bold", fontSize=9, textColor=ACCENT, leading=12, spaceBefore=4)
sROLE  = S("role", fontName="Helvetica-Bold", fontSize=9, textColor=DARK, leading=12)
sMETA  = S("meta", fontSize=8, textColor=MUTED, leading=11)
sBUL   = S("bul",  fontSize=8.5, leading=13, leftIndent=8, textColor=MID)
sSUM   = S("sum",  fontSize=8.8, leading=14, textColor=MID, alignment=TA_JUSTIFY)
sITAL  = S("ital", fontSize=7.8, textColor=MUTED, leading=11)

def rule():
    return HRFlowable(width="100%", thickness=0.4, color=RULE, spaceAfter=3, spaceBefore=1)

def section(title):
    return [Paragraph(f"<b>{title.upper()}</b>", sSECH), rule()]

def sp(h=3):
    return Spacer(1, h)

def bul(text):
    return Paragraph(f"<bullet>\u2022</bullet> {text}", sBUL)

def skill_row(label, val):
    lp = Paragraph(f"<b>{label}</b>", S("sl", fontName="Helvetica-Bold", fontSize=8.5, textColor=DARK, leading=12))
    vp = Paragraph(val, S("sv", fontSize=8.5, textColor=MID, leading=12))
    t = Table([[lp, vp]], colWidths=[24*mm, 140*mm])
    t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),
                            ("LEFTPADDING",(0,0),(-1,-1),0),
                            ("RIGHTPADDING",(0,0),(-1,-1),0),
                            ("TOPPADDING",(0,0),(-1,-1),1),
                            ("BOTTOMPADDING",(0,0),(-1,-1),1)]))
    return t

# ── url=None means no link shown ──────────────────────────────────────────────
def proj(title, meta, url, bullets, stack):
    tp = Paragraph(f"<b>{title}</b>", sROLE)
    mp = Paragraph(meta, sMETA)
    hdr = Table([[tp, mp]], colWidths=[110*mm, 56*mm])
    hdr.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",(0,0),(-1,-1),0), ("RIGHTPADDING",(0,0),(-1,-1),0),
        ("TOPPADDING",(0,0),(-1,-1),0),  ("BOTTOMPADDING",(0,0),(-1,-1),0),
        ("ALIGN",(1,0),(1,0),"RIGHT"),
    ]))
    items = [hdr]
    if url:
        items.append(Paragraph(
            f'<font color="#2563eb">{url}</font>',
            S("url", fontSize=7.8, textColor=ACCENT, leading=10)))
    items += [bul(b) for b in bullets]
    items.append(Paragraph(f"<i>Stack: {stack}</i>", sITAL))
    items.append(sp(5))
    return KeepTogether(items)

def exp(title, org, date, bullets):
    tp = Paragraph(f"<b>{title}</b>", sROLE)
    dp = Paragraph(date, sMETA)
    hdr = Table([[tp, dp]], colWidths=[120*mm, 46*mm])
    hdr.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",(0,0),(-1,-1),0), ("RIGHTPADDING",(0,0),(-1,-1),0),
        ("TOPPADDING",(0,0),(-1,-1),0),  ("BOTTOMPADDING",(0,0),(-1,-1),0),
        ("ALIGN",(1,0),(1,0),"RIGHT"),
    ]))
    op = Paragraph(org, sMETA)
    return KeepTogether([hdr, op] + [bul(b) for b in bullets] + [sp(5)])

# ─── BUILD ────────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    "XYZ_Resume.pdf",
    pagesize=A4, leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB)
story = []

# ── HEADER ────────────────────────────────────────────────────────────────────
story.append(Paragraph("XYZ", sNAME))
story.append(sp(2))
story.append(Paragraph(
    'xyz@example.com  |  github.com/xyz  |  linkedin.com/in/xyz  |  City, Country',
    sCONT))
story.append(sp(7))

# ── PROFILE ───────────────────────────────────────────────────────────────────
story += section("Profile")
story.append(Paragraph(
    "Computer Science undergraduate (XYZ University, 202X) with a track record of designing, "
    "building, and <b>deploying AI-powered backend systems end-to-end</b>. Proficient in Python and "
    "REST API design; experienced with Linux environments and AWS fundamentals. "
    "Ranked <b>Rank XYZ in XYZ Competition</b> (national competitive programming) and an "
    "active open-source contributor. Seeking XYZ Company Full-Stack Pathway (Batch X, 202X) to "
    "deepen full-stack engineering fundamentals in a global, English-speaking environment.",
    sSUM))
story.append(sp(7))

# ── SKILLS ────────────────────────────────────────────────────────────────────
story += section("Technical Skills")
story.append(skill_row("Languages", "Python (primary), JavaScript / TypeScript, SQL, Bash"))
story.append(skill_row("Backend",   "REST API design, agentic LLM pipelines, FastAPI, Pydantic, OpenAI API, Gemini API"))
story.append(skill_row("Frontend",  "Streamlit (production deployed), React (fundamentals)"))
story.append(skill_row("Data",      "PyPDF2, PDFPlumber, EbookLib, BeautifulSoup4, Pillow, RapidFuzz"))
story.append(skill_row("DevOps",    "Linux / macOS, Git, GitHub Actions, AWS (fundamentals), SSH"))
story.append(skill_row("Security",  "HMAC-SHA-512, RFC 6238 TOTP, HTTP Basic Auth"))
story.append(sp(7))

# ── PROJECTS ─────────────────────────────────────────────────────────────────
story += section("Projects")

story.append(proj(
    "Project 1 — Agentic Resume Tailoring System",
    "Solo  |  Live  |  202X",
    "project1.xyz.app",
    [
        "Designed a two-agent pipeline: a low-temperature LLM <b>Critic</b> audits resumes semantically "
        "against job descriptions to surface keyword gaps; a <b>Strategist</b> agent rewrites targeted "
        "sections using only user-verified evidence — preventing hallucinated content.",
        "Implemented <b>human-in-the-loop verification</b> as a hard gate: no content is generated "
        "until the user approves and contextualises each missing skill, ensuring factual accuracy.",
        "Built a theme-adaptive custom Streamlit UI (sticky headers, card layout, light/dark CSS); "
        "ingests PDF and TXT resumes via PyPDF2; deployed publicly on Streamlit Cloud.",
    ],
    "Python, Streamlit, OpenAI GPT-4o-mini, PyPDF2, python-dotenv"
))

story.append(proj(
    "Project 2 — AI Repository Quality Auditor",
    "Hackathon (XYZ)  |  Live  |  202X",
    "project2.xyz.app",
    [
        "Built an automated tool that evaluates any public GitHub repo against industry standards "
        "(CI/CD presence, test coverage, documentation) and returns a <b>deterministic 0-100 score</b> "
        "plus a phase-based improvement roadmap (Immediate Fixes vs Long-term Architecture).",
        "Integrated PyGithub for <b>recursive file-tree analysis</b>; used GPT-4o-mini in JSON mode "
        "for structured codebase summaries — ensuring parseable, consistent output every call.",
        "Sole developer; won hackathon track; designed scoring heuristics, API layer, and UI end-to-end.",
    ],
    "Python, Streamlit, OpenAI GPT-4o-mini, PyGithub, GitHub API"
))

story.append(proj(
    "Project 3 — xyz",
    "Solo  |  In Progress  |  202X",
    None,
    [
        "Architecting a multi-stage AI pipeline: ingests data extracts structured "
        "character metadata and relationship graphs via Gemini Pro, and persists data in a "
        "<b>Pydantic-validated Series Bible</b> for downstream visual production.",
        "Engineered fuzzy-logic entity resolution (RapidFuzz) to merge character data across volumes; "
        "built a <b>checkpointed bulk processor with auto-resume</b> handling thousands of chapters "
        "without data loss on interruption.",
    ],
    "Python, Google Gemini Pro, EbookLib, PDFPlumber, Pydantic, RapidFuzz, Pillow"
))

# ── EXPERIENCE ────────────────────────────────────────────────────────────────
story += section("Experience")
story.append(exp(
    "cs Intern",
    "XYZ Company — Virtual Internship Program",
    "202X",
    [
        "Built interactive dashboards for KPI tracking and data storytelling using Qlik Sense; "
        "applied associative data modelling on real business datasets.",
        "Practised data pipeline preparation and presenting analytical findings to non-technical stakeholders.",
    ]
))

# ── EDUCATION ─────────────────────────────────────────────────────────────────
story += section("Education")
tp = Paragraph("<b>B.Tech — Computer Science &amp; Engineering</b>", sROLE)
dp = Paragraph("202X – 202X", sMETA)
hdr = Table([[tp, dp]], colWidths=[120*mm, 46*mm])
hdr.setStyle(TableStyle([
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("LEFTPADDING",(0,0),(-1,-1),0), ("RIGHTPADDING",(0,0),(-1,-1),0),
    ("TOPPADDING",(0,0),(-1,-1),0),  ("BOTTOMPADDING",(0,0),(-1,-1),0),
    ("ALIGN",(1,0),(1,0),"RIGHT"),
]))
story.append(hdr)
story.append(Paragraph("XYZ University, City, Country", sMETA))
story.append(sp(7))

# ── ACHIEVEMENTS ──────────────────────────────────────────────────────────────
story += section("Achievements & Open Source")
story.append(bul("<b>Rank XYZ</b> — XYZ Competition (national competitive programming competition)"))
story.append(bul("Active contributor to <b>XYZ</b> — open-source bioinformatics Python library"))
story.append(sp(7))

# ── CERTIFICATIONS ────────────────────────────────────────────────────────────
story += section("Certifications")
story.append(bul("XYZ Professional Certificate — XYZ Platform"))
story.append(bul("XYZ Computer Networking — XYZ Platform"))
story.append(bul("Introduction to xyz — XYZ Platform"))

doc.build(story)
print("Done.")