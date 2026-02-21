"""
🌹 مهووس للعطور - استديو الذكاء الاصطناعي v12.1
أعلى معايير الجودة والدقة · Gemini 2.0 + Claude 3.5
"""
import streamlit as st

st.set_page_config(
    page_title="مهووس | استديو الذكاء الاصطناعي",
    page_icon="🌹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══ GLOBAL CSS — وضوح كامل وتباين عالٍ ═══
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=Playfair+Display:wght@700;900&display=swap');

/* ━━━━ Base ━━━━ */
html, body, [class*="css"] {
    font-family: 'Cairo', sans-serif !important;
    direction: rtl;
    color: #F0E0C0 !important;
}
.stApp { background: #1A1008; }

/* ━━━━ Main content ━━━━ */
.main .block-container {
    background: #1E1408;
    border-radius: 1rem;
    padding: 1.5rem 2rem !important;
    max-width: 1100px;
}

/* ━━━━ كل النصوص العامة ━━━━ */
p, span, div, li, td, th {
    color: #F0E0C0 !important;
    font-family: 'Cairo', sans-serif !important;
}
strong, b { color: #FFE080 !important; font-weight: 900 !important; }
small { color: #D4B880 !important; }

/* ━━━━ Headings ━━━━ */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Cairo', sans-serif !important;
    color: #FFE060 !important;
    font-weight: 900 !important;
}

/* ━━━━ Sidebar ━━━━ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #120A02 0%, #1C1006 50%, #120A02 100%) !important;
    border-left: 2px solid rgba(212,175,55,0.4) !important;
}
[data-testid="stSidebarNav"] { display: none; }
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label {
    color: #F0D8A0 !important;
}

/* ━━━━ Buttons — Primary ━━━━ */
div.stButton > button {
    background: linear-gradient(135deg, #9A7020 0%, #D4AF37 45%, #FFE060 55%, #A07820 100%) !important;
    color: #1A0D00 !important;
    border: none !important;
    border-radius: 0.65rem !important;
    font-family: 'Cairo', sans-serif !important;
    font-weight: 900 !important;
    font-size: 0.92rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 3px 14px rgba(212,175,55,0.30) !important;
    padding: 0.55rem 1.3rem !important;
}
div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 26px rgba(212,175,55,0.50) !important;
    background: linear-gradient(135deg, #B08030 0%, #E8C040 45%, #FFE870 55%, #B08030 100%) !important;
}

/* ━━━━ Buttons — Secondary ━━━━ */
div.stButton > button[kind="secondary"] {
    background: rgba(212,175,55,0.15) !important;
    color: #FFD840 !important;
    border: 1.5px solid rgba(212,175,55,0.50) !important;
    box-shadow: none !important;
    font-weight: 700 !important;
}
div.stButton > button[kind="secondary"]:hover {
    background: rgba(212,175,55,0.25) !important;
    border-color: rgba(212,175,55,0.75) !important;
    color: #FFE860 !important;
}

/* ━━━━ Tabs ━━━━ */
[data-testid="stTabs"] button[role="tab"] {
    font-family: 'Cairo', sans-serif !important;
    color: #D4A860 !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #FFE060 !important;
    border-bottom: 3px solid #D4AF37 !important;
    font-weight: 900 !important;
}
[data-testid="stTabs"] button[role="tab"]:hover {
    color: #FFD040 !important;
}

/* ━━━━ Inputs ━━━━ */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] > div > div,
[data-testid="stNumberInput"] input {
    background: #241808 !important;
    color: #FFF0D0 !important;
    border: 2px solid rgba(212,175,55,0.50) !important;
    border-radius: 0.55rem !important;
    font-family: 'Cairo', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(212,175,55,0.90) !important;
    box-shadow: 0 0 0 3px rgba(212,175,55,0.20) !important;
    outline: none !important;
}

/* ━━━━ Labels ━━━━ */
label,
.stSelectbox label,
.stTextInput label,
.stTextArea label,
.stNumberInput label,
.stSlider label,
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] {
    color: #FFD880 !important;
    font-size: 0.9rem !important;
    font-weight: 800 !important;
    font-family: 'Cairo', sans-serif !important;
}

/* ━━━━ Selectbox text ━━━━ */
[data-testid="stSelectbox"] span,
[data-testid="stSelectbox"] div {
    color: #FFF0D0 !important;
    font-weight: 600 !important;
}

/* ━━━━ Checkboxes & Toggles ━━━━ */
[data-testid="stCheckbox"] label,
[data-testid="stCheckbox"] p,
[data-testid="stCheckbox"] span {
    color: #FFE090 !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
}
[data-testid="stToggle"] label,
[data-testid="stToggle"] p {
    color: #FFE090 !important;
    font-weight: 700 !important;
}

/* ━━━━ Metrics ━━━━ */
[data-testid="stMetricValue"] { color: #FFE060 !important; font-weight: 900 !important; font-size: 2rem !important; }
[data-testid="stMetricLabel"] { color: #D4B870 !important; font-weight: 800 !important; }
[data-testid="stMetricDelta"] { font-weight: 700 !important; }

/* ━━━━ Expanders ━━━━ */
.streamlit-expanderHeader,
[data-testid="stExpander"] summary,
[data-testid="stExpander"] > div:first-child {
    background: rgba(212,175,55,0.12) !important;
    border: 1.5px solid rgba(212,175,55,0.35) !important;
    border-radius: 0.65rem !important;
    color: #FFE060 !important;
    font-family: 'Cairo', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.92rem !important;
    padding: 0.7rem 1rem !important;
}
.streamlit-expanderHeader p,
[data-testid="stExpander"] summary p {
    color: #FFE060 !important;
    font-weight: 800 !important;
}
.streamlit-expanderContent,
[data-testid="stExpander"] > div:last-child {
    border: 1.5px solid rgba(212,175,55,0.20) !important;
    border-top: none !important;
    background: rgba(20,12,4,0.95) !important;
    border-radius: 0 0 0.65rem 0.65rem !important;
    padding: 1rem !important;
}

/* ━━━━ Alerts ━━━━ */
[data-testid="stAlert"],
.stSuccess, .stWarning, .stError, .stInfo {
    font-family: 'Cairo', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    border-radius: 0.65rem !important;
}
.stSuccess { background: rgba(52,211,153,0.15) !important; border-color: #34d399 !important; color: #A0FFE0 !important; }
.stWarning { background: rgba(251,191,36,0.15) !important; border-color: #fbbf24 !important; color: #FFE070 !important; }
.stError   { background: rgba(239,68,68,0.15)  !important; border-color: #ef4444 !important; color: #FFB0B0 !important; }
.stInfo    { background: rgba(212,175,55,0.15)  !important; border-color: rgba(212,175,55,0.60) !important; color: #FFE080 !important; }
[data-testid="stAlert"] p { color: inherit !important; }

/* ━━━━ Divider ━━━━ */
hr { border-color: rgba(212,175,55,0.30) !important; margin: 1.2rem 0 !important; }

/* ━━━━ Progress Bar ━━━━ */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #B09030, #D4AF37, #F5D560, #D4AF37) !important;
    border-radius: 999px !important;
}
.stProgress > div > div {
    background: rgba(212,175,55,0.15) !important;
    border-radius: 999px !important;
}

/* ━━━━ File Uploader ━━━━ */
[data-testid="stFileUploader"] {
    border: 2px dashed rgba(212,175,55,0.55) !important;
    border-radius: 0.85rem !important;
    background: rgba(212,175,55,0.07) !important;
    padding: 1.2rem !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(212,175,55,0.80) !important;
    background: rgba(212,175,55,0.12) !important;
}
[data-testid="stFileUploaderDropzoneInstructions"],
[data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stFileUploaderDropzoneInstructions"] small {
    color: #FFD880 !important;
    font-weight: 700 !important;
}

/* ━━━━ Code blocks ━━━━ */
.stCodeBlock {
    border-radius: 0.6rem !important;
    border: 1.5px solid rgba(212,175,55,0.25) !important;
}
.stCodeBlock code, pre code {
    color: #C8F080 !important;
    font-size: 0.85rem !important;
}

/* ━━━━ Download buttons ━━━━ */
[data-testid="stDownloadButton"] button {
    background: linear-gradient(135deg, rgba(212,175,55,0.18), rgba(212,175,55,0.28)) !important;
    color: #FFE060 !important;
    border: 2px solid rgba(212,175,55,0.60) !important;
    font-size: 0.88rem !important;
    font-weight: 800 !important;
    border-radius: 0.55rem !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: linear-gradient(135deg, rgba(212,175,55,0.30), rgba(212,175,55,0.42)) !important;
    border-color: rgba(212,175,55,0.85) !important;
    transform: translateY(-1px) !important;
    color: #FFF080 !important;
}

/* ━━━━ Scrollbar ━━━━ */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #1A1008; }
::-webkit-scrollbar-thumb { background: rgba(212,175,55,0.45); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(212,175,55,0.70); }

/* ━━━━ Slider ━━━━ */
[data-testid="stSlider"] p,
[data-testid="stSlider"] span {
    color: #FFD840 !important;
    font-weight: 700 !important;
}

/* ━━━━ رابط Gemini ━━━━ */
.gemini-link {
    display: block;
    background: linear-gradient(135deg, rgba(66,133,244,0.20), rgba(52,168,83,0.15));
    border: 2px solid rgba(66,133,244,0.55);
    border-radius: 0.65rem;
    padding: 0.65rem 0.9rem;
    text-align: center;
    text-decoration: none !important;
    margin: 0.4rem 0;
    transition: all 0.2s;
}
.gemini-link:hover {
    background: linear-gradient(135deg, rgba(66,133,244,0.32), rgba(52,168,83,0.25));
    border-color: rgba(66,133,244,0.80);
    transform: translateY(-1px);
    box-shadow: 0 4px 14px rgba(66,133,244,0.25);
}
.gemini-link-text {
    color: #90C8FF !important;
    font-size: 0.85rem !important;
    font-weight: 900 !important;
    letter-spacing: 0.02rem;
}

/* ━━━━ Spinner ━━━━ */
[data-testid="stSpinner"] p { color: #FFD880 !important; font-weight: 700 !important; }

/* ━━━━ Caption / small text ━━━━ */
[data-testid="stCaptionContainer"] p { color: #D4B870 !important; font-weight: 600 !important; }

/* ━━━━ Radio buttons ━━━━ */
[data-testid="stRadio"] label p { color: #FFE090 !important; font-weight: 700 !important; }

/* ━━━━ Multiselect ━━━━ */
[data-testid="stMultiSelect"] span { color: #FFE090 !important; font-weight: 700 !important; }

/* ━━━━ JSON viewer ━━━━ */
[data-testid="stJson"] { color: #D4F090 !important; }
</style>
""", unsafe_allow_html=True)

from modules.studio import show_studio_page
from modules.character import show_character_page

# ═══ SIDEBAR ═══
with st.sidebar:
    # Logo
    st.markdown("""
    <div style="text-align:center; padding: 1.2rem 0 0.9rem;">
      <div style="font-size:3.2rem; filter:drop-shadow(0 0 18px rgba(212,175,55,0.75)); margin-bottom:0.3rem;">🌹</div>
      <div style="font-family:'Playfair Display',serif; font-size:1.9rem;
                  background:linear-gradient(135deg,#A07015,#F0CC55,#A07015);
                  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                  background-clip:text; font-weight:900; letter-spacing:0.03rem; line-height:1;">
        مهووس
      </div>
      <div style="font-size:0.58rem; color:#907050; letter-spacing:0.28rem; margin-top:0.25rem; font-weight:800; text-transform:uppercase;">
        استديو الذكاء الاصطناعي
      </div>
      <div style="margin-top:0.4rem; display:inline-block; background:rgba(212,175,55,0.15);
           border:1px solid rgba(212,175,55,0.3); border-radius:999px;
           padding:0.12rem 0.65rem; font-size:0.6rem; color:#D4AF37; font-weight:800; letter-spacing:0.1rem;">
        v12.1
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:0.2rem 0 0.6rem'>", unsafe_allow_html=True)

    # ═══ Navigation ═══
    pages = {
        "🎬 استديو المحتوى":    "studio",
        "🎭 الشخصية والسيناريو": "character",
        "📊 الإحصائيات":        "dashboard",
        "⚙️ الإعدادات":         "settings",
    }

    if "page" not in st.session_state:
        st.session_state.page = "studio"

    for label, key in pages.items():
        active = st.session_state.page == key
        bg     = "rgba(212,175,55,0.12)" if active else "transparent"
        border = "rgba(212,175,55,0.45)" if active else "rgba(255,255,255,0.04)"
        color  = "#F0CC55" if active else "#907060"
        weight = "800" if active else "400"
        dot    = "▶" if active else "·"

        st.markdown(f"""
        <div style="background:{bg}; border:1px solid {border}; border-radius:0.5rem;
             padding:0.45rem 0.85rem; margin:0.12rem 0;">
          <span style="color:{color}; font-size:0.85rem; font-weight:{weight};">{dot} {label}</span>
        </div>""", unsafe_allow_html=True)

        if st.button(label, key=f"nav_{key}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.page = key
            st.rerun()

    st.markdown("<hr style='margin:0.6rem 0'>", unsafe_allow_html=True)

    # ═══ رابط Gemini AI Studio ═══
    st.markdown("""
    <div style='color:#A08060; font-size:0.70rem; font-weight:900; letter-spacing:0.12rem; margin-bottom:0.4rem;'>
        🤖 روابط سريعة
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <a href="https://aistudio.google.com" target="_blank" class="gemini-link">
        <span class="gemini-link-text">✨ Gemini AI Studio — مجاني</span>
    </a>
    <a href="https://openrouter.ai/keys" target="_blank" class="gemini-link" style="border-color:rgba(212,175,55,0.35);">
        <span class="gemini-link-text" style="color:#F0D080 !important;">🔑 OpenRouter — المفاتيح</span>
    </a>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:0.6rem 0'>", unsafe_allow_html=True)

    # ═══ API Status ═══
    st.markdown("<div style='color:#A08060; font-size:0.70rem; font-weight:900; letter-spacing:0.12rem; margin-bottom:0.5rem;'>🔑 حالة الاتصال</div>", unsafe_allow_html=True)

    # ── تهيئة المفاتيح ──
    if "openrouter_key" not in st.session_state:
        st.session_state.openrouter_key = st.secrets.get("OPENROUTER_API_KEY", "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")
    if "gemini_key" not in st.session_state:
        st.session_state.gemini_key = st.secrets.get("GEMINI_API_KEY", "")

    secrets = {
        "openrouter": st.session_state.openrouter_key,
        "gemini":     st.session_state.gemini_key,
        "luma":       st.secrets.get("LUMA_API_KEY", ""),
        "webhook":    st.secrets.get("WEBHOOK_PUBLISH_CONTENT", ""),
    }

    api_items = [
        (bool(secrets["openrouter"]), "كلود 3.5 (نصوص)", True),
        (bool(secrets["gemini"]),     "جيميني 2.0 (صور)", True),
        (bool(secrets["luma"]),       "Luma (فيديو)",     False),
        (bool(secrets["webhook"]),    "Make.com (نشر)",   False),
    ]

    for ok, name, required in api_items:
        icon   = "🟢" if ok else ("🔴" if required else "⚪")
        status = "متصل" if ok else ("أضف المفتاح" if required else "اختياري")
        color  = "#80FFD0" if ok else ("#FF9090" if required else "#806050")
        st.markdown(
            f"<div style='background:rgba(212,175,55,0.06); border:1px solid rgba(212,175,55,0.18); border-radius:0.4rem;"
            f"padding:0.32rem 0.6rem; margin-bottom:0.28rem; display:flex; justify-content:space-between; align-items:center;'>"
            f"<span style='color:#E0C890; font-size:0.78rem; font-weight:700;'>{icon} {name}</span>"
            f"<span style='color:{color}; font-size:0.70rem; font-weight:700;'>{status}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

    st.markdown("<hr style='margin:0.6rem 0'>", unsafe_allow_html=True)

    # ═══ Session Stats ═══
    if "gen_count" not in st.session_state:
        st.session_state.gen_count = 0
        st.session_state.img_count = 0

    st.markdown("<div style='color:#A08060; font-size:0.70rem; font-weight:900; letter-spacing:0.12rem; margin-bottom:0.5rem;'>📊 إحصائيات الجلسة</div>", unsafe_allow_html=True)

    sc1, sc2 = st.columns(2)
    for col, label, val, icon in [
        (sc1, "عمليات",  st.session_state.gen_count, "🚀"),
        (sc2, "صور",     st.session_state.img_count, "🖼️"),
    ]:
        col.markdown(f"""
        <div style='text-align:center; background:rgba(212,175,55,0.08);
             border:1px solid rgba(212,175,55,0.22); border-radius:0.6rem; padding:0.55rem 0.3rem;'>
          <div style='font-size:1rem; margin-bottom:0.15rem;'>{icon}</div>
          <div style='color:#F5D060; font-size:1.4rem; font-weight:900; line-height:1;'>{val}</div>
          <div style='color:#C0A060; font-size:0.68rem; margin-top:0.15rem; font-weight:700;'>{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr style='margin:0.6rem 0'>", unsafe_allow_html=True)

    # Model info
    st.markdown("""
    <div style='text-align:center;'>
      <div style='color:#907060; font-size:0.66rem; letter-spacing:0.03rem; line-height:2;'>
        🤖 Gemini 2.0 · Imagen 3.0<br>
        ✍️ Claude 3.5 Sonnet<br>
        🎥 Luma Dream Machine
      </div>
      <div style='color:#604030; font-size:0.58rem; margin-top:0.4rem;'>© 2026 مهووس للعطور · v12.1</div>
    </div>
    """, unsafe_allow_html=True)


# ═══ MAIN CONTENT ═══
page = st.session_state.page

if page == "studio":
    show_studio_page()

elif page == "character":
    show_character_page()

elif page == "dashboard":
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0F0A04,#1E1206); border:1px solid rgba(212,175,55,0.35);
         border-radius:1.2rem; padding:2.5rem; text-align:center; margin-bottom:2rem;'>
      <h1 style='color:#F5D060; margin:0; font-family:Cairo,sans-serif; font-size:2rem;'>📊 لوحة الإحصائيات</h1>
      <p style='color:#C0A060; margin:0.4rem 0 0; font-size:0.92rem;'>متابعة نشاط الاستديو في هذه الجلسة</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    metrics = [
        ("🚀", "عمليات التوليد",   str(st.session_state.gen_count), "#F5D060"),
        ("🖼️", "صور مولّدة",       str(st.session_state.img_count), "#6FE8B8"),
        ("🎥", "فيديوهات",         "—", "#C0A0FF"),
        ("📡", "منشورات تلقائية",  "—", "#FF9060"),
    ]
    for col, (icon, label, val, color) in zip(cols, metrics):
        col.markdown(f"""
        <div style='background:linear-gradient(135deg,#120C04,#1E1408); border:1px solid rgba(212,175,55,0.22);
             border-radius:0.9rem; padding:1.8rem 1rem; text-align:center; transition:all 0.2s;'>
          <div style='font-size:2.2rem; margin-bottom:0.4rem;'>{icon}</div>
          <div style='color:{color}; font-size:2.4rem; font-weight:900; line-height:1;'>{val}</div>
          <div style='color:#C0A060; font-size:0.82rem; margin-top:0.4rem; font-weight:700;'>{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("📈 الإحصائيات تُحدَّث تلقائياً مع كل عملية توليد — تُعاد عند إعادة تحميل الصفحة")
    
    # Quick tips
    st.markdown("""
    <div style='background:rgba(212,175,55,0.06); border:1px solid rgba(212,175,55,0.20); 
         border-radius:0.75rem; padding:1.2rem; margin-top:1rem;'>
      <div style='color:#F5D060; font-size:0.95rem; font-weight:900; margin-bottom:0.8rem;'>💡 نصائح لأسرع أداء</div>
      <div style='color:#D0B070; font-size:0.85rem; line-height:2;'>
        ✓ اختر 3–4 منصات فقط لكل جلسة<br>
        ✓ ارفع صورة العطر بدقة عالية وخلفية بيضاء<br>
        ✓ فعّل وضع رمضان في المناسبات<br>
        ✓ حمّل ZIP بعد كل جلسة لحفظ الصور
      </div>
    </div>
    """, unsafe_allow_html=True)

elif page == "settings":
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1A1006,#281808); border:2px solid rgba(212,175,55,0.45);
         border-radius:1.2rem; padding:2rem; text-align:center; margin-bottom:1.5rem;'>
      <h1 style='color:#FFE060; margin:0; font-family:Cairo,sans-serif; font-size:2rem; font-weight:900;'>⚙️ الإعدادات</h1>
      <p style='color:#D4B870; margin:0.4rem 0 0; font-size:0.95rem; font-weight:700;'>ضبط مفاتيح API · أدوات الربط · نصائح الجودة</p>
    </div>
    """, unsafe_allow_html=True)

    # ── حقل إدخال المفاتيح مباشرة ──
    st.markdown("""
    <div style='background:linear-gradient(135deg,rgba(212,175,55,0.12),rgba(212,175,55,0.06));
         border:2px solid rgba(212,175,55,0.50); border-radius:1rem; padding:1.4rem 1.6rem;
         margin-bottom:1.5rem;'>
      <div style='color:#FFE060; font-size:1.05rem; font-weight:900; margin-bottom:0.3rem;'>🔑 أدخل مفاتيح API مباشرة</div>
      <div style='color:#D4B870; font-size:0.85rem;'>يُحفظ المفتاح في الجلسة الحالية فقط</div>
    </div>
    """, unsafe_allow_html=True)

    k1, k2 = st.columns(2)
    with k1:
        new_or = st.text_input(
            "🤖 OpenRouter API Key",
            value=st.session_state.get("openrouter_key", ""),
            type="password",
            placeholder="sk-or-v1-...",
            help="من openrouter.ai/keys — لتوليد النصوص والتعليقات",
            key="or_input"
        )
        if new_or and new_or != st.session_state.get("openrouter_key", ""):
            st.session_state.openrouter_key = new_or
            st.success("✅ تم حفظ مفتاح OpenRouter!")
    with k2:
        new_gem = st.text_input(
            "✨ Gemini API Key",
            value=st.session_state.get("gemini_key", ""),
            type="password",
            placeholder="AIzaSy...",
            help="من aistudio.google.com — مجاني بالكامل",
            key="gem_input"
        )
        if new_gem and new_gem != st.session_state.get("gemini_key", ""):
            st.session_state.gemini_key = new_gem
            st.success("✅ تم حفظ مفتاح Gemini!")

    # عرض حالة المفاتيح الحالية
    or_ok  = bool(st.session_state.get("openrouter_key", ""))
    gem_ok = bool(st.session_state.get("gemini_key", ""))
    s1, s2 = st.columns(2)
    s1.markdown(f"""
    <div style='background:{"rgba(52,211,153,0.12)" if or_ok else "rgba(239,68,68,0.12)"};
         border:1.5px solid {"#34d399" if or_ok else "#ef4444"};
         border-radius:0.65rem; padding:0.7rem 1rem; text-align:center;'>
      <div style='color:{"#A0FFD8" if or_ok else "#FFB0B0"}; font-size:0.9rem; font-weight:900;'>
        {"🟢 OpenRouter متصل" if or_ok else "🔴 OpenRouter — أدخل المفتاح"}
      </div>
    </div>""", unsafe_allow_html=True)
    s2.markdown(f"""
    <div style='background:{"rgba(52,211,153,0.12)" if gem_ok else "rgba(239,68,68,0.12)"};
         border:1.5px solid {"#34d399" if gem_ok else "#ef4444"};
         border-radius:0.65rem; padding:0.7rem 1rem; text-align:center;'>
      <div style='color:{"#A0FFD8" if gem_ok else "#FFB0B0"}; font-size:0.9rem; font-weight:900;'>
        {"🟢 Gemini متصل" if gem_ok else "🔴 Gemini — أدخل المفتاح"}
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── رابط Gemini بارز في الإعدادات ──
    st.markdown("""
    <div style='background:linear-gradient(135deg,rgba(66,133,244,0.12),rgba(52,168,83,0.08));
         border:2px solid rgba(66,133,244,0.45); border-radius:1rem; padding:1.2rem 1.5rem;
         margin-bottom:1.5rem; display:flex; align-items:center; gap:1rem;'>
      <div style='font-size:2.2rem;'>✨</div>
      <div style='flex:1;'>
        <div style='color:#7EB8FF; font-size:1rem; font-weight:900; margin-bottom:0.25rem;'>
          Gemini AI Studio — مجاني بالكامل
        </div>
        <div style='color:#A0C0E0; font-size:0.82rem;'>
          احصل على مفتاح GEMINI_API_KEY مجاناً من Google
        </div>
      </div>
      <a href="https://aistudio.google.com" target="_blank"
         style='background:rgba(66,133,244,0.25); border:1.5px solid rgba(66,133,244,0.55);
                border-radius:0.6rem; padding:0.5rem 1.1rem; color:#7EB8FF !important;
                text-decoration:none !important; font-weight:900; font-size:0.85rem;
                white-space:nowrap;'>
        افتح الآن ←
      </a>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🔑 إعداد مفاتيح API في Streamlit Cloud", expanded=True):
        st.markdown("""
        <div style='color:#D0B070; font-size:0.9rem; margin-bottom:0.8rem;'>
        <strong style='color:#F5D060;'>الخطوة:</strong> افتح Streamlit Cloud ← اختر تطبيقك ← Settings ← Secrets ← أضف:
        </div>
        """, unsafe_allow_html=True)
        st.code("""# ━━━━ مطلوب ━━━━
OPENROUTER_API_KEY = "sk-or-v1-..."    # من openrouter.ai
GEMINI_API_KEY     = "AIzaSy..."       # من aistudio.google.com (مجاني)

# ━━━━ اختياري ━━━━
LUMA_API_KEY            = "luma-..."   # من lumalabs.ai — لتوليد الفيديو
WEBHOOK_PUBLISH_CONTENT = "https://hook.eu2.make.com/..."  # للنشر التلقائي""",
                language="toml")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            <div style='background:rgba(66,133,244,0.10); border:1px solid rgba(66,133,244,0.30);
                 border-radius:0.6rem; padding:0.9rem;'>
              <div style='color:#7EB8FF; font-weight:900; margin-bottom:0.5rem;'>🆓 Gemini مجاني</div>
              <div style='color:#C0D8F0; font-size:0.82rem; line-height:1.8;'>
                1. افتح <a href="https://aistudio.google.com" target="_blank" style="color:#7EB8FF;">aistudio.google.com</a><br>
                2. انقر Get API Key<br>
                3. انسخ والصق في Secrets
              </div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div style='background:rgba(212,175,55,0.08); border:1px solid rgba(212,175,55,0.2);
                 border-radius:0.6rem; padding:0.9rem;'>
              <div style='color:#F5D060; font-weight:900; margin-bottom:0.5rem;'>🤖 OpenRouter</div>
              <div style='color:#D0B870; font-size:0.82rem; line-height:1.8;'>
                1. افتح <a href="https://openrouter.ai/keys" target="_blank" style="color:#F5D060;">openrouter.ai</a><br>
                2. Keys → Create Key<br>
                3. انسخ والصق في Secrets
              </div>
            </div>
            """, unsafe_allow_html=True)

    with st.expander("🤖 النماذج المستخدمة في v12.1"):
        models_data = [
            ("🔍", "Gemini 2.0 Flash",   "تحليل صور العطر",             "#6FE8B8"),
            ("🎨", "Imagen 3.0 v2",      "توليد صور المنصات",           "#C0A0FF"),
            ("✍️", "Claude 3.5 Sonnet",  "توليد النصوص والتعليقات",     "#F5D060"),
            ("🎥", "Luma Dream Machine", "توليد الفيديو السينمائي",      "#FF9060"),
        ]
        for icon, name, role, color in models_data:
            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:center;
                 background:#120C04; border:1px solid rgba(212,175,55,0.18);
                 border-radius:0.55rem; padding:0.7rem 1rem; margin-bottom:0.4rem;'>
              <span style='color:{color}; font-weight:800; font-size:0.88rem;'>{icon} {name}</span>
              <span style='color:#C0A060; font-size:0.8rem;'>{role}</span>
              <span style='color:#6FE8B8; font-size:0.75rem; font-weight:700;'>✓ نشط</span>
            </div>""", unsafe_allow_html=True)

    with st.expander("📸 ثبات الشخصية — الدليل الكامل"):
        st.markdown("""
        <div style='color:#D0B070; font-size:0.88rem; line-height:2;'>
        <strong style='color:#F5D060;'>في Google Flow / Veo / Kling AI:</strong><br>
        1️⃣ أنشئ مشروعاً جديداً<br>
        2️⃣ ارفع <code>mahwous_character.png</code> ← Character Reference ← نشاط 80%<br>
        3️⃣ ارفع صورة الزجاجة الأصلية ← Product Reference ← نشاط 90%<br>
        4️⃣ الصق DNA الشخصية كاملاً من قسم الشخصية والسيناريو<br>
        5️⃣ أضف: STRICTLY maintain character and product consistency<br><br>
        <strong style='color:#F5D060;'>في الاستديو:</strong><br>
        ارفع mahwous_character.png في خانة "صورة مرجعية لمهووس" — سيُدمج تلقائياً
        </div>
        """, unsafe_allow_html=True)

    with st.expander("🔗 إعداد Make.com للنشر التلقائي"):
        st.markdown("""
        <div style='color:#D0B070; font-size:0.88rem; line-height:2;'>
        1️⃣ افتح make.com ← أنشئ سيناريو جديداً<br>
        2️⃣ Trigger: Webhook (Custom) ← انسخ الرابط<br>
        3️⃣ أضف وحدات النشر: تيليجرام · إنستجرام · تيك توك<br>
        4️⃣ ألصق الرابط في Secrets كـ WEBHOOK_PUBLISH_CONTENT<br>
        5️⃣ فعّل السيناريو (ON)<br>
        6️⃣ في الاستديو: فعّل "نشر تلقائي"
        </div>
        """, unsafe_allow_html=True)

    with st.expander("💡 10 نصائح للحصول على أعلى جودة"):
        tips = [
            ("📸", "ارفع صورة العطر بخلفية بيضاء أو شفافة لتحليل أدق"),
            ("🤵", "استخدم البدلة للمحتوى الرسمي والفاخر دائماً"),
            ("🏆", "الهودي هو الأنسب لـ TikTok والمحتوى الشبابي الديناميكي"),
            ("💬", "سيناريو الحوار هو الأعلى أداءً على TikTok وإنستجرام"),
            ("📱", "اختر 3-4 منصات فقط في كل جلسة للسرعة والجودة"),
            ("👤", "ارفع صورة مهووس المرجعية في بداية كل جلسة"),
            ("🏪", "مشهد متجر العطور يُنتج أفضل نتائج مع البدلة"),
            ("🌅", "مشهد الشاطئ مثالي للكاجوال وعطور الصيف"),
            ("✏️", "استخدم حقل الإضافات الخاصة في مولّد البرومت"),
            ("📦", "حمّل الصور بصيغة ZIP لحفظها منظمة ومصنّفة"),
        ]
        for i, (icon, tip) in enumerate(tips, 1):
            st.markdown(f"""
            <div style='display:flex; align-items:flex-start; gap:0.6rem; 
                 background:rgba(212,175,55,0.04); border-radius:0.5rem;
                 padding:0.6rem 0.8rem; margin-bottom:0.35rem;'>
              <span style='font-size:1.1rem;'>{icon}</span>
              <span style='color:#D0B870; font-size:0.85rem; line-height:1.5;'>
                <strong style='color:#F5D060;'>{i}.</strong> {tip}
              </span>
            </div>""", unsafe_allow_html=True)
