import html
import json
from datetime import datetime

import streamlit as st

from src.graph import graph


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Meeting Notes Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROFESSIONAL DESIGN SYSTEM
# ============================================================

st.html(
    """
    <style>

    /* ========================================================
       DESIGN TOKENS
       ======================================================== */

    :root {
        --bg-main: #050816;
        --bg-secondary: #08101f;
        --bg-tertiary: #0d1728;

        --surface: #0b1324;
        --surface-2: #101a2e;
        --surface-3: #16233a;

        --border: rgba(148, 163, 184, 0.16);
        --border-strong: rgba(129, 140, 248, 0.32);

        /* High contrast text system */
        --text-primary: #f8fafc;
        --text-secondary: #d5deea;
        --text-muted: #b6c4d5;
        --text-subtle: #91a2b8;

        --indigo: #6366f1;
        --indigo-light: #818cf8;
        --violet: #8b5cf6;

        --cyan: #22d3ee;
        --cyan-light: #67e8f9;

        --success: #22c55e;
        --warning: #f59e0b;
        --danger: #ef4444;
    }


    /* ========================================================
       GLOBAL APPLICATION
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 5%,
                rgba(99, 102, 241, 0.15),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(34, 211, 238, 0.08),
                transparent 26%
            ),
            linear-gradient(
                135deg,
                var(--bg-main) 0%,
                var(--bg-secondary) 48%,
                var(--bg-tertiary) 100%
            );

        color: var(--text-primary);
    }


    /* ========================================================
       STREAMLIT HEADER
       ======================================================== */

    [data-testid="stHeader"] {
        background: rgba(5, 8, 22, 0.94) !important;
        border-bottom: 1px solid rgba(148, 163, 184, 0.06);
    }

    [data-testid="stToolbar"] {
        background: transparent !important;
    }


    /* ========================================================
       MAIN CONTAINER
       ======================================================== */

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #040813 0%,
                #07101e 55%,
                #0a1424 100%
            ) !important;

        border-right: 1px solid rgba(148, 163, 184, 0.12);
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(148, 163, 184, 0.12) !important;
    }

    [data-testid="stSidebar"] div[style*="color:#64748b"] {
        color: #a5b4c7 !important;
    }

    [data-testid="stSidebar"] div[style*="color:#94a3b8"] {
        color: #b6c4d5 !important;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero {
        position: relative;
        overflow: hidden;

        padding: 3.4rem 3.4rem 3.2rem;

        border-radius: 30px;

        background:
            linear-gradient(
                135deg,
                rgba(27, 39, 91, 0.98),
                rgba(9, 16, 34, 0.98)
            );

        border: 1px solid rgba(129, 140, 248, 0.28);

        box-shadow:
            0 30px 90px rgba(0, 0, 0, 0.42),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }

    .hero-glow-one {
        position: absolute;

        width: 430px;
        height: 430px;

        right: -150px;
        top: -180px;

        border-radius: 50%;

        background: var(--indigo);
        opacity: 0.14;

        filter: blur(100px);
    }

    .hero-glow-two {
        position: absolute;

        width: 320px;
        height: 320px;

        left: -160px;
        bottom: -190px;

        border-radius: 50%;

        background: var(--cyan);
        opacity: 0.10;

        filter: blur(90px);
    }

    .hero-content {
        position: relative;
        z-index: 5;
    }

    .hero-badge {
        display: inline-block;

        padding: 0.48rem 0.9rem;

        border-radius: 999px;

        background: rgba(34, 211, 238, 0.10);
        border: 1px solid rgba(34, 211, 238, 0.28);

        color: var(--cyan-light);

        font-size: 0.74rem;
        font-weight: 800;
        letter-spacing: 0.10em;
        text-transform: uppercase;

        margin-bottom: 1.25rem;
    }

    .hero-title {
        color: #ffffff;

        font-size: clamp(2.5rem, 5vw, 4.8rem);
        font-weight: 850;

        line-height: 1.02;
        letter-spacing: -0.055em;

        margin: 0;
    }

    .hero-highlight {
        background:
            linear-gradient(
                90deg,
                #67e8f9,
                #818cf8,
                #c084fc
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-description {
        max-width: 920px;

        margin-top: 1.4rem;

        color: var(--text-secondary);

        font-size: 1.04rem;
        line-height: 1.8;
    }

    .hero-description strong {
        color: #ffffff;
    }


    /* ========================================================
       SECTION TYPOGRAPHY
       ======================================================== */

    .section-label {
        color: var(--cyan-light);

        font-size: 0.72rem;
        font-weight: 850;

        letter-spacing: 0.12em;
        text-transform: uppercase;

        margin-bottom: 0.4rem;
    }

    .section-title {
        color: var(--text-primary);

        font-size: 1.65rem;
        font-weight: 800;

        letter-spacing: -0.025em;

        margin-bottom: 0.4rem;
    }

    .section-description {
        color: var(--text-secondary);

        font-size: 0.92rem;
        line-height: 1.65;

        margin-bottom: 1.2rem;
    }


    /* ========================================================
       WORKFLOW
       ======================================================== */

    .workflow {
        display: flex;
        align-items: center;

        gap: 0.5rem;

        padding: 1.15rem;
        margin: 1.4rem 0 2.5rem;

        background: rgba(7, 13, 28, 0.82);

        border: 1px solid rgba(99, 102, 241, 0.18);
        border-radius: 20px;
    }

    .workflow-step {
        flex: 1;
        text-align: center;

        padding: 0.7rem;
    }

    .workflow-icon {
        width: 52px;
        height: 52px;

        display: flex;
        align-items: center;
        justify-content: center;

        margin: 0 auto 0.6rem;

        border-radius: 15px;

        background:
            linear-gradient(
                135deg,
                rgba(99, 102, 241, 0.18),
                rgba(34, 211, 238, 0.10)
            );

        border: 1px solid rgba(129, 140, 248, 0.24);

        font-size: 1.4rem;
    }

    .workflow-title {
        color: #f1f5f9;

        font-size: 0.84rem;
        font-weight: 750;
    }

    .workflow-subtitle {
        color: #aebdce;

        font-size: 0.70rem;
        line-height: 1.4;

        margin-top: 0.25rem;
    }

    .workflow-arrow {
        color: #7c8da5;

        font-size: 1.2rem;
        font-weight: 700;
    }


    /* ========================================================
       GENERAL CARDS
       ======================================================== */

    .card {
        background:
            linear-gradient(
                145deg,
                rgba(22, 32, 52, 0.90),
                rgba(10, 17, 31, 0.92)
            );

        border: 1px solid var(--border);

        border-radius: 20px;

        padding: 1.4rem;

        box-shadow:
            0 18px 55px rgba(0, 0, 0, 0.20);
    }

    .card-title {
        color: var(--text-primary);

        font-size: 1rem;
        font-weight: 800;
    }

    .card-text {
        color: var(--text-secondary);

        font-size: 0.82rem;
        line-height: 1.7;

        margin-top: 0.7rem;
    }


    /* ========================================================
       METRIC CARDS
       ======================================================== */

    .metric-card {
        background:
            linear-gradient(
                145deg,
                rgba(25, 35, 55, 0.88),
                rgba(10, 17, 31, 0.90)
            );

        border: 1px solid var(--border);

        border-radius: 18px;

        padding: 1.25rem;

        text-align: center;

        box-shadow:
            0 14px 40px rgba(0, 0, 0, 0.17);
    }

    .metric-value {
        color: #ffffff;

        font-size: 2.1rem;
        font-weight: 850;

        line-height: 1;
    }

    .metric-label {
        color: #aebdce;

        font-size: 0.76rem;

        margin-top: 0.5rem;
    }


    /* ========================================================
       TOPICS
       ======================================================== */

    .topics {
        display: flex;
        flex-wrap: wrap;

        gap: 0.6rem;
    }

    .topic {
        display: inline-block;

        padding: 0.52rem 0.82rem;

        border-radius: 999px;

        background: rgba(99, 102, 241, 0.12);

        border: 1px solid rgba(129, 140, 248, 0.22);

        color: #d2d9ff;

        font-size: 0.80rem;
        font-weight: 700;
    }


    /* ========================================================
       ACTION CARDS
       ======================================================== */

    .action-card {
        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.94),
                rgba(9, 15, 28, 0.92)
            );

        border: 1px solid var(--border);

        border-left: 3px solid var(--indigo);

        border-radius: 16px;

        padding: 1.15rem;

        margin-bottom: 0.8rem;

        transition:
            transform 0.15s ease,
            border-color 0.15s ease,
            box-shadow 0.15s ease;
    }

    .action-card:hover {
        transform: translateY(-2px);

        border-left-color: var(--cyan);

        box-shadow:
            0 12px 35px rgba(0, 0, 0, 0.24);
    }

    .action-number {
        color: var(--indigo-light);

        font-size: 0.72rem;
        font-weight: 850;

        letter-spacing: 0.08em;
    }

    .action-task {
        color: #f8fafc;

        font-size: 0.94rem;
        font-weight: 750;

        line-height: 1.55;

        margin-top: 0.35rem;
    }

    .action-owner {
        color: #9fb0c4;

        font-size: 0.78rem;

        margin-top: 0.6rem;
    }

    .owner {
        color: var(--cyan-light);
        font-weight: 750;
    }


    /* ========================================================
       PRIORITY CARDS
       ======================================================== */

    .priority-card {
        background:
            linear-gradient(
                145deg,
                rgba(20, 29, 49, 0.94),
                rgba(9, 15, 28, 0.92)
            );

        border: 1px solid var(--border);

        border-radius: 18px;

        padding: 1.2rem;

        margin-bottom: 0.8rem;

        transition:
            transform 0.15s ease,
            border-color 0.15s ease;
    }

    .priority-card:hover {
        transform: translateY(-2px);

        border-color: rgba(129, 140, 248, 0.30);
    }

    .priority-row {
        display: flex;
        align-items: center;
        justify-content: space-between;

        gap: 1rem;
    }

    .priority-task {
        color: #f8fafc;

        font-weight: 750;
        line-height: 1.5;
    }

    .priority-owner {
        color: #9fb0c4;

        font-size: 0.78rem;
        margin-top: 0.5rem;
    }

    .priority-reason {
        color: #b6c4d5;

        font-size: 0.80rem;
        line-height: 1.55;

        margin-top: 0.7rem;
        padding-top: 0.7rem;

        border-top: 1px solid rgba(148, 163, 184, 0.10);
    }


    /* ========================================================
       PRIORITY BADGES
       ======================================================== */

    .badge-high,
    .badge-medium,
    .badge-low {
        display: inline-block;

        padding: 0.35rem 0.7rem;

        border-radius: 999px;

        font-size: 0.69rem;
        font-weight: 850;

        letter-spacing: 0.06em;
    }

    .badge-high {
        color: #fca5a5;

        background: rgba(239, 68, 68, 0.13);

        border: 1px solid rgba(248, 113, 113, 0.30);
    }

    .badge-medium {
        color: #fcd34d;

        background: rgba(245, 158, 11, 0.13);

        border: 1px solid rgba(251, 191, 36, 0.30);
    }

    .badge-low {
        color: #93c5fd;

        background: rgba(59, 130, 246, 0.13);

        border: 1px solid rgba(96, 165, 250, 0.30);
    }


    /* ========================================================
       EMPTY STATES
       ======================================================== */

    .empty-state {
        text-align: center;

        padding: 2.5rem 1.5rem;

        background: rgba(10, 17, 31, 0.70);

        border: 1px dashed rgba(148, 163, 184, 0.20);

        border-radius: 18px;
    }

    .empty-icon {
        font-size: 2rem;
    }

    .empty-title {
        color: #e2e8f0;

        font-weight: 800;

        margin-top: 0.55rem;
    }

    .empty-text {
        color: #9fb0c4;

        font-size: 0.80rem;

        line-height: 1.6;

        margin-top: 0.4rem;
    }


    /* ========================================================
       RADIO BUTTONS
       ======================================================== */

    div[data-testid="stRadio"] label {
        color: #d5deea !important;
    }

    div[data-testid="stRadio"] label p {
        color: #d5deea !important;
        font-weight: 650 !important;
    }

    div[data-testid="stRadio"] [data-testid="stMarkdownContainer"] {
        color: #d5deea !important;
    }

    div[data-testid="stRadio"] input {
        accent-color: #22d3ee !important;
    }


    /* ========================================================
       TEXT AREA
       ======================================================== */

    div[data-testid="stTextArea"] label {
        color: #e2e8f0 !important;
    }

    div[data-testid="stTextArea"] div[data-baseweb="textarea"] {
        background: #ffffff !important;
        border-radius: 16px !important;
    }

    div[data-testid="stTextArea"] div[data-baseweb="textarea"] > div {
        background: #ffffff !important;

        border: 1px solid #6366f1 !important;

        border-radius: 16px !important;

        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.12) !important;
    }

    div[data-testid="stTextArea"] textarea {
        background: #ffffff !important;

        color: #111827 !important;

        -webkit-text-fill-color: #111827 !important;

        caret-color: #111827 !important;

        font-size: 0.92rem !important;

        line-height: 1.65 !important;
    }

    div[data-testid="stTextArea"] textarea::placeholder {
        color: #6b7280 !important;

        opacity: 1 !important;

        -webkit-text-fill-color: #6b7280 !important;
    }

    div[data-testid="stTextArea"] textarea:focus {
        background: #ffffff !important;

        color: #111827 !important;

        -webkit-text-fill-color: #111827 !important;

        border-color: #7c3aed !important;

        box-shadow:
            0 0 0 1px #7c3aed !important;
    }


    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    [data-testid="stFileUploader"] {
        background: rgba(8, 14, 28, 0.70) !important;

        border: 1px dashed rgba(129, 140, 248, 0.30) !important;

        border-radius: 16px !important;

        padding: 0.5rem !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: #ffffff !important;

        border-radius: 12px !important;
    }

    [data-testid="stFileUploaderDropzone"] * {
        color: #111827 !important;
    }

    [data-testid="stFileUploaderDropzone"] small {
        color: #4b5563 !important;
    }

    [data-testid="stFileUploaderDropzone"] button {
        background: #ffffff !important;

        color: #111827 !important;

        border: 1px solid #d1d5db !important;

        border-radius: 9px !important;
    }

    [data-testid="stFileUploaderDropzone"] button:hover {
        background: #f3f4f6 !important;

        color: #111827 !important;
    }


    /* ========================================================
       PRIMARY BUTTONS
       ======================================================== */

    .stButton > button {
        border-radius: 12px !important;

        min-height: 46px !important;

        font-weight: 800 !important;

        background:
            linear-gradient(
                135deg,
                #4f46e5,
                #7c3aed
            ) !important;

        border:
            1px solid rgba(129, 140, 248, 0.30) !important;

        color: #ffffff !important;

        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease,
            border-color 0.15s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 12px 32px rgba(99, 102, 241, 0.30);

        border-color: rgba(129, 140, 248, 0.55) !important;
    }

    .stButton > button:focus {
        border-color: #a5b4fc !important;

        box-shadow:
            0 0 0 2px rgba(99, 102, 241, 0.25) !important;
    }


    /* ========================================================
       DOWNLOAD BUTTONS
       ======================================================== */

    .stDownloadButton > button {
        border-radius: 12px !important;

        min-height: 44px !important;

        background:
            rgba(30, 41, 59, 0.90) !important;

        border:
            1px solid rgba(148, 163, 184, 0.20) !important;

        color: #e2e8f0 !important;

        font-weight: 700 !important;
    }

    .stDownloadButton > button:hover {
        background: rgba(51, 65, 85, 0.95) !important;

        border-color: rgba(129, 140, 248, 0.35) !important;
    }


    /* ========================================================
       STATUS / ANALYSIS
       ======================================================== */

    [data-testid="stStatusWidget"] {
        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.98),
                rgba(8, 15, 30, 0.98)
            ) !important;

        border:
            1px solid rgba(99, 102, 241, 0.25) !important;

        border-radius: 14px !important;

        color: #dbeafe !important;

        box-shadow:
            0 12px 35px rgba(0, 0, 0, 0.25) !important;
    }

    [data-testid="stStatusWidget"] * {
        color: #dbeafe !important;
    }

    [data-testid="stStatusWidget"] svg {
        color: #67e8f9 !important;
    }


    /* ========================================================
       ALERTS
       ======================================================== */

    div[data-testid="stAlert"] {
        border-radius: 12px !important;
    }

    [data-testid="stAlert"] p {
        font-weight: 600 !important;
    }


    /* ========================================================
       INPUT STATISTICS
       ======================================================== */

    div[style*="color:#64748b"] {
        color: #91a2b8 !important;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        text-align: center;

        padding-top: 2rem;
        margin-top: 4rem;

        border-top:
            1px solid rgba(148, 163, 184, 0.10);

        color: #91a2b8;

        font-size: 0.76rem;
        line-height: 1.7;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 800px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero {
            padding: 2rem 1.4rem;
        }

        .hero-title {
            font-size: 2.6rem;
        }

        .workflow {
            flex-direction: column;
        }

        .workflow-arrow {
            transform: rotate(90deg);
        }

        .priority-row {
            align-items: flex-start;
            flex-direction: column;
        }

        .metric-card {
            margin-bottom: 0.7rem;
        }
    }

    </style>
    """
)


# ============================================================
# CONSTANTS
# ============================================================

MAX_TRANSCRIPT_CHARACTERS = 30000

SAMPLE_TRANSCRIPT = """John: Thanks everyone for joining. Today we need to discuss the website performance issues and our homepage redesign.

David: The production server is currently slow. I will optimize the database queries immediately.

Sarah: I will redesign the homepage layout before Friday.

John: Good. Let's make sure both tasks are completed this week.

Sarah: We should also review the customer feedback from last month's campaign.

John: Agreed. We can discuss that in the next meeting.
"""


# ============================================================
# SESSION STATE
# ============================================================

if "transcript" not in st.session_state:
    st.session_state.transcript = ""

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def create_initial_state(transcript: str):
    return {
        "transcript": transcript,
        "topics": [],
        "summary": "",
        "action_items": [],
        "has_action_items": False,
        "priorities": [],
        "final_report": {},
    }


def safe_text(value) -> str:
    return html.escape(str(value))


def priority_badge(priority: str) -> str:
    priority = str(priority).strip().lower()

    if priority == "high":
        return '<span class="badge-high">HIGH</span>'

    if priority == "medium":
        return '<span class="badge-medium">MEDIUM</span>'

    return '<span class="badge-low">LOW</span>'


def show_html(content: str):
    st.html(content)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    show_html(
        """
        <div style="padding:0.6rem 0 1.4rem 0;">

            <div style="
                font-size:2.2rem;
                margin-bottom:0.6rem;
            ">
                🤖
            </div>

            <div style="
                color:#f8fafc;
                font-size:1.15rem;
                font-weight:850;
            ">
                Meeting Intelligence
            </div>

            <div style="
                color:#aebdce;
                font-size:0.78rem;
                line-height:1.6;
                margin-top:0.4rem;
            ">
                Transform meeting conversations
                into structured business intelligence.
            </div>

        </div>
        """
    )

    st.divider()

    show_html(
        """
        <div style="
            color:#67e8f9;
            font-size:0.70rem;
            font-weight:850;
            letter-spacing:0.10em;
            text-transform:uppercase;
        ">
            AI Workflow
        </div>

        <div style="
            color:#d5deea;
            font-size:0.84rem;
            line-height:2;
            margin-top:0.55rem;
        ">
            🧠 Topic Extraction<br>
            📝 Meeting Summary<br>
            ⚡ Action Detection<br>
            🎯 Priority Classification<br>
            📊 Final Report
        </div>
        """
    )

    st.divider()

    show_html(
        """
        <div style="
            color:#67e8f9;
            font-size:0.70rem;
            font-weight:850;
            letter-spacing:0.10em;
            text-transform:uppercase;
        ">
            Technology
        </div>

        <div style="
            color:#b6c4d5;
            font-size:0.82rem;
            line-height:1.9;
            margin-top:0.55rem;
        ">
            Gemini AI<br>
            LangChain<br>
            LangGraph<br>
            Pydantic<br>
            Streamlit
        </div>
        """
    )

    st.divider()

    show_html(
        """
        <div style="
            color:#91a2b8;
            font-size:0.74rem;
            line-height:1.65;
        ">

            <strong style="color:#d5deea;">
                Why this app?
            </strong>

            <br><br>

            Important decisions, responsibilities,
            deadlines and follow-up tasks can easily
            disappear inside long meeting transcripts.

            <br><br>

            This application converts that unstructured
            information into a clear action-oriented report.

        </div>
        """
    )


# ============================================================
# HERO
# ============================================================

show_html(
    """
    <div class="hero">

        <div class="hero-glow-one"></div>
        <div class="hero-glow-two"></div>

        <div class="hero-content">

            <div class="hero-badge">
                AI-Powered Meeting Intelligence
            </div>

            <div class="hero-title">
                Turn meetings into
                <span class="hero-highlight">
                    actionable intelligence.
                </span>
            </div>

            <div class="hero-description">

                Long meeting transcripts contain decisions,
                responsibilities, deadlines and important
                discussion points — but finding them manually
                takes time.

                <br><br>

                <strong>
                    AI Meeting Notes Analyzer
                </strong>

                transforms an unstructured meeting transcript
                into a structured report containing

                <strong>
                    key topics, a concise summary,
                    action items, responsible owners,
                    and priority levels.
                </strong>

            </div>

        </div>

    </div>
    """
)


# ============================================================
# WORKFLOW VISUAL
# ============================================================

show_html(
    """
    <div class="workflow">

        <div class="workflow-step">

            <div class="workflow-icon">
                📝
            </div>

            <div class="workflow-title">
                Meeting Transcript
            </div>

            <div class="workflow-subtitle">
                Unstructured conversation
            </div>

        </div>

        <div class="workflow-arrow">
            →
        </div>

        <div class="workflow-step">

            <div class="workflow-icon">
                🧠
            </div>

            <div class="workflow-title">
                Multi-Agent AI
            </div>

            <div class="workflow-subtitle">
                LangGraph orchestration
            </div>

        </div>

        <div class="workflow-arrow">
            →
        </div>

        <div class="workflow-step">

            <div class="workflow-icon">
                ⚡
            </div>

            <div class="workflow-title">
                Actionable Report
            </div>

            <div class="workflow-subtitle">
                Decisions & priorities
            </div>

        </div>

    </div>
    """
)


# ============================================================
# INPUT HEADER
# ============================================================

show_html(
    """
    <div class="section-label">
        START ANALYSIS
    </div>

    <div class="section-title">
        Give the AI your meeting
    </div>

    <div class="section-description">
        Paste a transcript or upload a plain-text meeting file.
        The multi-agent workflow will analyze it automatically.
    </div>
    """
)


# ============================================================
# INPUT MODE
# ============================================================

input_mode = st.radio(
    "Input method",
    [
        "Paste transcript",
        "Upload .txt file",
    ],
    horizontal=True,
    label_visibility="collapsed",
)


# ============================================================
# INPUT AREA
# ============================================================

input_col, info_col = st.columns(
    [2.65, 1],
    gap="large",
)


with input_col:

    if input_mode == "Paste transcript":

        transcript = st.text_area(
            "Meeting transcript",
            key="transcript",
            height=390,
            placeholder=(
                "Paste your meeting transcript here...\n\n"
                "Example:\n"
                "John: We need to improve website performance.\n"
                "David: I will optimize the database queries immediately.\n"
                "Sarah: I will redesign the homepage before Friday."
            ),
            label_visibility="collapsed",
        )

    else:

        uploaded_file = st.file_uploader(
            "Upload meeting transcript",
            type=["txt"],
            help="Upload a plain-text meeting transcript.",
        )

        if uploaded_file is not None:

            transcript = uploaded_file.getvalue().decode(
                "utf-8",
                errors="replace",
            )

            st.session_state.transcript = transcript

        else:

            transcript = st.session_state.transcript


with info_col:

    show_html(
        """
        <div class="card">

            <div style="
                color:#67e8f9;
                font-size:0.70rem;
                font-weight:850;
                letter-spacing:0.10em;
                text-transform:uppercase;
            ">
                What you get
            </div>

            <div class="card-title" style="margin-top:0.65rem;">
                One transcript.
                Complete meeting intelligence.
            </div>

            <div class="card-text">
                ✓ Executive summary<br>
                ✓ Key discussion topics<br>
                ✓ Action items<br>
                ✓ Responsible owners<br>
                ✓ Priority classification<br>
                ✓ Priority reasoning
            </div>

        </div>
        """
    )


# ============================================================
# SAMPLE / CLEAR
# ============================================================

sample_col, clear_col, spacer = st.columns(
    [1, 1, 2]
)


with sample_col:

    if st.button(
        "✨ Load Sample",
        use_container_width=True,
    ):

        st.session_state.transcript = SAMPLE_TRANSCRIPT
        st.session_state.analysis_result = None

        st.rerun()


with clear_col:

    if st.button(
        "↻ Clear",
        use_container_width=True,
    ):

        st.session_state.transcript = ""
        st.session_state.analysis_result = None

        st.rerun()


# ============================================================
# INPUT STATISTICS
# ============================================================

word_count = (
    len(transcript.split())
    if transcript.strip()
    else 0
)

character_count = len(transcript)


show_html(
    f"""
    <div style="
        color:#91a2b8;
        font-size:0.74rem;
        margin-top:0.5rem;
        margin-bottom:1rem;
    ">
        {word_count:,} words
        &nbsp; · &nbsp;
        {character_count:,} characters
        &nbsp; · &nbsp;
        Maximum {MAX_TRANSCRIPT_CHARACTERS:,} characters
    </div>
    """
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze_clicked = st.button(
    "🚀 Analyze Meeting",
    use_container_width=True,
)


# ============================================================
# RUN LANGGRAPH
# ============================================================

if analyze_clicked:

    cleaned_transcript = transcript.strip()

    if not cleaned_transcript:

        st.error(
            "Please provide a meeting transcript before starting the analysis."
        )

    elif len(cleaned_transcript) < 30:

        st.warning(
            "The transcript is too short for a meaningful analysis. "
            "Please provide more meeting content."
        )

    elif len(cleaned_transcript) > MAX_TRANSCRIPT_CHARACTERS:

        st.error(
            "The transcript is too large. "
            f"Please provide a transcript under "
            f"{MAX_TRANSCRIPT_CHARACTERS:,} characters."
        )

    else:

        initial_state = create_initial_state(
            cleaned_transcript
        )

        try:

            with st.status(
                "🤖 Running AI meeting analysis...",
                expanded=True,
                type="compact",
            ):

                st.write(
                    "🧠 Extracting discussion topics..."
                )

                st.write(
                    "📝 Generating meeting summary..."
                )

                st.write(
                    "⚡ Identifying action items and owners..."
                )

                st.write(
                    "🎯 Classifying task priorities..."
                )

                result = graph.invoke(
                    initial_state
                )

                st.session_state.analysis_result = result

            st.success(
                "Analysis completed successfully."
            )

        except Exception as error:

            st.error(
                "The AI workflow could not complete the analysis."
            )

            with st.expander(
                "Technical details"
            ):

                st.exception(error)


# ============================================================
# RESULTS
# ============================================================

if st.session_state.analysis_result is not None:

    result = st.session_state.analysis_result

    report = result.get(
        "final_report",
        {},
    )

    st.divider()


    # ========================================================
    # REPORT HEADER
    # ========================================================

    show_html(
        """
        <div style="margin-top:1.5rem;">

            <div class="section-label">
                AI ANALYSIS COMPLETE
            </div>

            <div class="section-title">
                Meeting Intelligence Report
            </div>

            <div class="section-description">
                Your conversation has been converted into
                structured, actionable intelligence.
            </div>

        </div>
        """
    )


    # ========================================================
    # METRICS
    # ========================================================

    topics = report.get(
        "topics",
        [],
    )

    action_items = report.get(
        "action_items",
        [],
    )

    priorities = report.get(
        "priorities",
        [],
    )


    topic_count = (
        len(topics)
        if isinstance(topics, list)
        else 0
    )

    action_count = (
        len(action_items)
        if isinstance(action_items, list)
        else 0
    )

    priority_count = (
        len(priorities)
        if isinstance(priorities, list)
        else 0
    )


    metric1, metric2, metric3 = st.columns(3)


    with metric1:

        show_html(
            f"""
            <div class="metric-card">

                <div class="metric-value">
                    {topic_count}
                </div>

                <div class="metric-label">
                    KEY TOPICS
                </div>

            </div>
            """
        )


    with metric2:

        show_html(
            f"""
            <div class="metric-card">

                <div class="metric-value">
                    {action_count}
                </div>

                <div class="metric-label">
                    ACTION ITEMS
                </div>

            </div>
            """
        )


    with metric3:

        show_html(
            f"""
            <div class="metric-card">

                <div class="metric-value">
                    {priority_count}
                </div>

                <div class="metric-label">
                    PRIORITIZED TASKS
                </div>

            </div>
            """
        )


    st.markdown("")


    # ========================================================
    # EXECUTIVE SUMMARY
    # ========================================================

    show_html(
        """
        <div class="section-label">
            01 · EXECUTIVE SUMMARY
        </div>

        <div class="section-title">
            What happened?
        </div>

        <div class="section-description">
            A concise overview of the meeting and its outcomes.
        </div>
        """
    )


    summary = safe_text(
        report.get(
            "summary",
            "No summary available.",
        )
    )


    show_html(
        f"""
        <div class="card">

            <div style="
                color:#d5deea;
                font-size:0.98rem;
                line-height:1.85;
            ">
                {summary}
            </div>

        </div>
        """
    )


    # ========================================================
    # TOPICS
    # ========================================================

    show_html(
        """
        <div style="margin-top:2rem;">

            <div class="section-label">
                02 · DISCUSSION INTELLIGENCE
            </div>

            <div class="section-title">
                Key Topics
            </div>

            <div class="section-description">
                The main subjects identified from the conversation.
            </div>

        </div>
        """
    )


    if isinstance(topics, list) and topics:

        topic_html = '<div class="topics">'

        for topic in topics:

            topic_html += (
                '<span class="topic">'
                f"{safe_text(topic)}"
                "</span>"
            )

        topic_html += "</div>"

        show_html(topic_html)

    else:

        show_html(
            """
            <div class="empty-state">

                <div class="empty-icon">
                    —
                </div>

                <div class="empty-title">
                    No topics identified
                </div>

                <div class="empty-text">
                    No meaningful discussion topics were detected.
                </div>

            </div>
            """
        )


    # ========================================================
    # ACTION ITEMS
    # ========================================================

    show_html(
        """
        <div style="margin-top:2.2rem;">

            <div class="section-label">
                03 · EXECUTION
            </div>

            <div class="section-title">
                Action Items & Owners
            </div>

            <div class="section-description">
                Tasks explicitly identified during the meeting
                and their responsible owners.
            </div>

        </div>
        """
    )


    if isinstance(action_items, list) and action_items:

        for index, item in enumerate(
            action_items,
            start=1,
        ):

            task = safe_text(
                item.get(
                    "task",
                    "Task not specified",
                )
            )

            owner = safe_text(
                item.get(
                    "owner",
                    "Not specified",
                )
            )


            show_html(
                f"""
                <div class="action-card">

                    <div class="action-number">
                        TASK {index:02d}
                    </div>

                    <div class="action-task">
                        {task}
                    </div>

                    <div class="action-owner">
                        Responsible owner:
                        <span class="owner">
                            {owner}
                        </span>
                    </div>

                </div>
                """
            )

    else:

        show_html(
            """
            <div class="empty-state">

                <div class="empty-icon">
                    ✓
                </div>

                <div class="empty-title">
                    No action items identified
                </div>

                <div class="empty-text">
                    No clearly assigned follow-up tasks
                    were detected in this meeting.
                </div>

            </div>
            """
        )


    # ========================================================
    # PRIORITIES
    # ========================================================

    show_html(
        """
        <div style="margin-top:2.2rem;">

            <div class="section-label">
                04 · PRIORITY INTELLIGENCE
            </div>

            <div class="section-title">
                What needs attention first?
            </div>

            <div class="section-description">
                Priority levels are based only on urgency,
                deadlines and business context explicitly
                present in the meeting.
            </div>

        </div>
        """
    )


    if isinstance(priorities, list) and priorities:

        for item in priorities:

            task = safe_text(
                item.get(
                    "task",
                    "Task not specified",
                )
            )

            owner = safe_text(
                item.get(
                    "owner",
                    "Not specified",
                )
            )

            priority = safe_text(
                item.get(
                    "priority",
                    "Low",
                )
            )

            reason = safe_text(
                item.get(
                    "reason",
                    "",
                )
            )


            show_html(
                f"""
                <div class="priority-card">

                    <div class="priority-row">

                        <div class="priority-task">
                            {task}
                        </div>

                        <div>
                            {priority_badge(priority)}
                        </div>

                    </div>

                    <div class="priority-owner">
                        Owner:
                        <span class="owner">
                            {owner}
                        </span>
                    </div>

                    <div class="priority-reason">
                        {reason}
                    </div>

                </div>
                """
            )

    else:

        show_html(
            """
            <div class="empty-state">

                <div class="empty-icon">
                    —
                </div>

                <div class="empty-title">
                    No priority analysis required
                </div>

                <div class="empty-text">
                    The Priority Agent was skipped because
                    no action items were identified.
                </div>

            </div>
            """
        )


    # ========================================================
    # EXPORT
    # ========================================================

    show_html(
        """
        <div style="margin-top:2.5rem;">

            <div class="section-label">
                EXPORT
            </div>

            <div class="section-title">
                Save your meeting intelligence
            </div>

            <div class="section-description">
                Download the structured report for documentation,
                sharing or further processing.
            </div>

        </div>
        """
    )


    report_json = json.dumps(
        report,
        indent=4,
        ensure_ascii=False,
    )


    export1, export2 = st.columns(2)


    with export1:

        st.download_button(
            "⬇️ Download JSON Report",
            data=report_json,
            file_name=(
                "meeting_report_"
                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            ),
            mime="application/json",
            use_container_width=True,
        )


    with export2:

        st.download_button(
            "⬇️ Download Transcript",
            data=transcript,
            file_name="meeting_transcript.txt",
            mime="text/plain",
            use_container_width=True,
        )


# ============================================================
# FOOTER
# ============================================================

show_html(
    """
    <div class="footer">

        <strong style="color:#b6c4d5;">
            AI Meeting Notes Analyzer
        </strong>

        &nbsp; · &nbsp;

        Multi-agent AI application built with

        <strong style="color:#b6c4d5;">
            Gemini · LangChain · LangGraph · Streamlit
        </strong>

        <br>

        Turning meeting conversations into
        structured, actionable intelligence.

    </div>
    """
)