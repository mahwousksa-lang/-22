"""
🌹 مهووس للعطور - استديو الذكاء الاصطناعي v11.0
أعلى معايير الجودة والدقة · Gemini 2.0 + Claude 3.5
"""
import streamlit as st

st.set_page_config(
    page_title="مهووس | استديو الذكاء الاصطناعي",
    page_icon="🌹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══ GLOBAL CSS ═══
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&family=Playfair+Display:ital,wght@0,700;0,900;1,700&display=swap');

html, body, [class*="css"] {
    font-family: 'Cairo', sans-serif !important;
    direction: rtl;
}
.stApp {
    background: #050300;
}

/* ═══ Sidebar ═══ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060400 0%, #0C0700 50%, #060400 100%) !important;
    border-left: 1px solid rgba(212,175,55,0.2) !important;
}
[data-testid="stSidebarNav"] { display: none; }

/* ═══ Buttons ═══ */
div.stButton > button {
    background: linear-gradient(135deg, #7A5810 0%, #C8A030 40%, #ECC850 55%, #906018 100%);
    color: #000 !important; border: none; border-radius: 0.6rem;
    font-family: 'Cairo', sans-serif !important; font-weight: 800;
    font-size: 0.88rem; letter-spacing: 0.02rem;
    transition: all 0.2s ease; box-shadow: 0 2px 10px rgba(212,175,55,0.18);
    padding: 0.5rem 1.2rem;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 22px rgba(212,175,55,0.32);
}
div.stButton > button:active { transform: translateY(0); }
div.stButton > button[kind="secondary"] {
    background: rgba(212,175,55,0.07) !important;
    color: #C8A030 !important;
    border: 1px solid rgba(212,175,55,0.25) !important;
    box-shadow: none !important;
}
div.stButton > button[kind="secondary"]:hover {
    background: rgba(212,175,55,0.12) !important;
    border-color: rgba(212,175,55,0.45) !important;
}

/* ═══ Tabs ═══ */
[data-testid="stTabs"] button[role="tab"] {
    font-family: 'Cairo', sans-serif !important;
    color: #706040 !important; font-weight: 600; font-size: 0.85rem;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #D4AF37 !important;
    border-bottom: 2px solid #D4AF37 !important;
    font-weight: 800 !important;
}

/* ═══ Inputs ═══ */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] > div > div,
[data-testid="stNumberInput"] input {
    background: #080500 !important;
    color: #E8D8B0 !important;
    border: 1px solid rgba(212,175,55,0.2) !important;
    border-radius: 0.5rem !important;
    font-family: 'Cairo', sans-serif !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(212,175,55,0.55) !important;
    box-shadow: 0 0 0 2px rgba(212,175,55,0.1) !important;
}
label, .stSelectbox label { color: #907050 !important; font-size: 0.82rem !important; }

/* ═══ Metrics ═══ */
[data-testid="stMetricValue"] { color: #D4AF37 !important; font-weight: 900 !important; }
[data-testid="stMetricLabel"] { color: #806040 !important; }

/* ═══ Expanders ═══ */
.streamlit-expanderHeader {
    background: rgba(212,175,55,0.04) !important;
    border: 1px solid rgba(212,175,55,0.12) !important;
    border-radius: 0.5rem !important;
    color: #C8A030 !important;
    font-family: 'Cairo', sans-serif !important;
}
.streamlit-expanderContent {
    border: 1px solid rgba(212,175,55,0.08) !important;
    border-top: none !important;
    background: rgba(0,0,0,0.3) !important;
}

/* ═══ Alerts ═══ */
.stSuccess { background: rgba(52,211,153,0.07) !important; border-color: #34d399 !important; border-radius: 0.6rem !important; }
.stWarning { background: rgba(251,191,36,0.07) !important; border-color: #fbbf24 !important; border-radius: 0.6rem !important; }
.stError   { background: rgba(239,68,68,0.07)  !important; border-color: #ef4444 !important; border-radius: 0.6rem !important; }
.stInfo    { background: rgba(212,175,55,0.05)  !important; border-color: rgba(212,175,55,0.25) !important; border-radius: 0.6rem !important; }

/* ═══ Checkboxes & Toggles ═══ */
[data-testid="stCheckbox"] label { color: #C0A880 !important; font-size: 0.85rem !important; }
[data-testid="stToggle"] label { color: #C0A880 !important; }

/* ═══ Divider ═══ */
hr { border-color: rgba(212,175,55,0.12) !important; margin: 1rem 0 !important; }

/* ═══ Progress Bar ═══ */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #A08020, #D4AF37, #F0D060) !important;
}

/* ═══ File Uploader ═══ */
[data-testid="stFileUploader"] {
    border: 2px dashed rgba(212,175,55,0.25) !important;
    border-radius: 0.75rem !important;
    background: rgba(212,175,55,0.02) !important;
    padding: 1rem !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(212,175,55,0.5) !important;
    background: rgba(212,175,55,0.04) !important;
}

/* ═══ Code blocks ═══ */
.stCodeBlock { border-radius: 0.5rem !important; }

/* ═══ Download buttons ═══ */
[data-testid="stDownloadButton"] button {
    background: rgba(212,175,55,0.1) !important;
    color: #D4AF37 !important;
    border: 1px solid rgba(212,175,55,0.3) !important;
    font-size: 0.82rem !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: rgba(212,175,55,0.18) !important;
    border-color: rgba(212,175,55,0.5) !important;
}

/* ═══ Scrollbar ═══ */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #050300; }
::-webkit-scrollbar-thumb { background: rgba(212,175,55,0.25); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: rgba(212,175,55,0.45); }

/* ═══ Select Slider ═══ */
[data-testid="stSlider"] .st-bq { color: #D4AF37 !important; }
</style>
""", unsafe_allow_html=True)

from modules.studio import show_studio_page
from modules.character import show_character_page

# ═══ SIDEBAR ═══
with st.sidebar:
    # Logo
    st.markdown("""
    <div style="text-align:center; padding: 1.5rem 0 1.2rem;">
      <div style="font-size:3.5rem; filter:drop-shadow(0 0 16px rgba(212,175,55,0.65)); margin-bottom:0.3rem;">🌹</div>
      <div style="font-family:'Playfair Display',serif; font-size:2rem;
                  background:linear-gradient(135deg,#906010,#ECC850,#906010);
                  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                  background-clip:text; font-weight:900; letter-spacing:0.03rem; line-height:1;">
        مهووس
      </div>
      <div style="font-size:0.58rem; color:#4A3010; letter-spacing:0.35rem; margin-top:0.2rem; font-weight:700;">
        AI CONTENT STUDIO
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:0.3rem 0 0.8rem'>", unsafe_allow_html=True)

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
        # Visual indicator
        bg     = "rgba(212,175,55,0.1)" if active else "transparent"
        border = "rgba(212,175,55,0.4)" if active else "rgba(255,255,255,0.03)"
        color  = "#D4AF37" if active else "#706050"
        weight = "700" if active else "400"
        dot    = "●" if active else "·"

        st.markdown(f"""
        <div style="background:{bg}; border:1px solid {border}; border-radius:0.5rem;
             padding:0.5rem 0.9rem; margin:0.15rem 0;">
          <span style="color:{color}; font-size:0.85rem; font-weight:{weight};">{dot} {label}</span>
        </div>""", unsafe_allow_html=True)

        if st.button(label, key=f"nav_{key}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.page = key
            st.rerun()

    st.markdown("<hr style='margin:0.8rem 0'>", unsafe_allow_html=True)

    # ═══ API Status ═══
    st.markdown("<div style='color:#4A3010; font-size:0.68rem; font-weight:800; letter-spacing:0.15rem; margin-bottom:0.5rem;'>🔑 حالة الاتصال</div>", unsafe_allow_html=True)

    secrets = {
        "openrouter": st.secrets.get("OPENROUTER_API_KEY", "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"),
        "gemini":     st.secrets.get("GEMINI_API_KEY", ""),
        "luma":       st.secrets.get("LUMA_API_KEY", ""),
        "webhook":    st.secrets.get("WEBHOOK_PUBLISH_CONTENT", ""),
    }

    api_items = [
        (bool(secrets["openrouter"]), "OpenRouter · Claude 3.5", "نصوص + Captions", True),
        (bool(secrets["gemini"]),     "Gemini 2.0 Flash",        "صور + تحليل",     True),
        (bool(secrets["luma"]),       "Luma AI",                 "فيديو (اختياري)", False),
        (bool(secrets["webhook"]),    "Make.com",                "نشر (اختياري)",   False),
    ]

    for ok, name, role, required in api_items:
        icon    = "●" if ok else "○"
        color   = "#34d399" if ok else ("#ef4444" if required else "#4A3010")
        note    = "" if ok else (" — أضف في Secrets" if required else "")
        st.markdown(
            f"<div style='color:{color}; font-size:0.78rem; padding:0.12rem 0; display:flex; justify-content:space-between;'>"
            f"<span>{icon} {name}</span>"
            f"<span style='color:#4A3010; font-size:0.68rem;'>{role}{note}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

    st.markdown("<hr style='margin:0.8rem 0'>", unsafe_allow_html=True)

    # ═══ Session Stats ═══
    if "gen_count" not in st.session_state:
        st.session_state.gen_count = 0
        st.session_state.img_count = 0

    sc1, sc2 = st.columns(2)
    for col, label, val, icon in [
        (sc1, "عمليات",  st.session_state.gen_count, "🚀"),
        (sc2, "صور",     st.session_state.img_count, "🖼️"),
    ]:
        col.markdown(f"""
        <div style='text-align:center; background:rgba(212,175,55,0.05);
             border:1px solid rgba(212,175,55,0.12); border-radius:0.5rem; padding:0.5rem 0.3rem;'>
          <div style='font-size:1rem; margin-bottom:0.1rem;'>{icon}</div>
          <div style='color:#D4AF37; font-size:1.3rem; font-weight:900; line-height:1;'>{val}</div>
          <div style='color:#4A3010; font-size:0.65rem; margin-top:0.1rem;'>{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr style='margin:0.8rem 0'>", unsafe_allow_html=True)

    # Model info
    st.markdown("""
    <div style='text-align:center;'>
      <div style='color:#3A2510; font-size:0.62rem; letter-spacing:0.05rem; line-height:1.8;'>
        🤖 Gemini 2.0 Flash · Imagen 3.0<br>
        ✍️ Claude 3.5 Sonnet (OpenRouter)<br>
        🎥 Luma Dream Machine
      </div>
      <div style='color:#2A1808; font-size:0.58rem; margin-top:0.5rem;'>© 2026 مهووس للعطور · v11.0</div>
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
    <div style='background:linear-gradient(135deg,#060400,#100800); border:1px solid rgba(212,175,55,0.3);
         border-radius:1rem; padding:2rem; text-align:center; margin-bottom:2rem;'>
      <h1 style='color:#D4AF37; margin:0; font-family:Playfair Display,serif;'>📊 الإحصائيات</h1>
      <p style='color:#806040; margin:0.3rem 0 0; font-size:0.88rem;'>متابعة نشاط الاستديو في هذه الجلسة</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    metrics = [
        ("🚀", "عمليات التوليد",   str(st.session_state.gen_count)),
        ("🖼️", "صور مولّدة",       str(st.session_state.img_count)),
        ("🎥", "فيديوهات",         "—"),
        ("📡", "منشورات تلقائية",  "—"),
    ]
    for col, (icon, label, val) in zip(cols, metrics):
        col.markdown(f"""
        <div style='background:#080500; border:1px solid rgba(212,175,55,0.15);
             border-radius:0.75rem; padding:1.5rem; text-align:center;'>
          <div style='font-size:2rem; margin-bottom:0.3rem;'>{icon}</div>
          <div style='color:#D4AF37; font-size:2.2rem; font-weight:900; line-height:1;'>{val}</div>
          <div style='color:#806040; font-size:0.8rem; margin-top:0.3rem;'>{label}</div>
        </div>""", unsafe_allow_html=True)

    st.info("📈 الإحصائيات تُحدَّث تلقائياً مع كل عملية توليد")
    st.caption("ملاحظة: الإحصائيات تُعاد إلى الصفر عند إعادة تحميل الصفحة. لحفظها دائماً، أضف قاعدة بيانات.")

elif page == "settings":
    st.markdown("""
    <div style='background:linear-gradient(135deg,#060400,#100800); border:1px solid rgba(212,175,55,0.3);
         border-radius:1rem; padding:2rem; text-align:center; margin-bottom:2rem;'>
      <h1 style='color:#D4AF37; margin:0; font-family:Playfair Display,serif;'>⚙️ الإعدادات</h1>
      <p style='color:#806040; margin:0.4rem 0 0;'>ضبط API Keys · أدوات الربط · نصائح الجودة</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🔑 إعداد API Keys في Streamlit Cloud Secrets", expanded=True):
        st.markdown("**افتح:** Streamlit Cloud → اختر تطبيقك → Settings → Secrets → أضف:")
        st.code("""# ═══ مطلوب ═══
OPENROUTER_API_KEY = "sk-or-v1-..."       # من openrouter.ai (موجود مسبقاً)
GEMINI_API_KEY     = "AIzaSy..."          # من aistudio.google.com (مجاني)

# ═══ اختياري ═══
LUMA_API_KEY               = "luma-..."  # من lumalabs.ai — لتوليد الفيديو
WEBHOOK_PUBLISH_CONTENT    = "https://hook.eu2.make.com/..."  # Make.com للنشر التلقائي""",
                language="toml")
        st.markdown("""
        **الخطوات:**
        1. [aistudio.google.com](https://aistudio.google.com) → Get API Key → انسخ المفتاح
        2. ألصقه في Secrets كـ `GEMINI_API_KEY`
        3. أعد تشغيل التطبيق
        """)

    with st.expander("🤖 النماذج المستخدمة في v11.0"):
        models_data = [
            ("🔍 Gemini 2.0 Flash",   "تحليل صور العطر",              "سريع ودقيق"),
            ("🎨 Imagen 3.0 v2",      "توليد صور المنصات",            "أعلى جودة"),
            ("✍️ Claude 3.5 Sonnet",  "توليد النصوص والـ Captions",   "عربي فاخر"),
            ("🎥 Luma Dream Machine", "توليد الفيديو",                 "سينمائي"),
        ]
        for icon_name, role, quality in models_data:
            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:center;
                 background:#080500; border:1px solid rgba(212,175,55,0.12);
                 border-radius:0.5rem; padding:0.6rem 0.9rem; margin-bottom:0.35rem;'>
              <span style='color:#D4AF37; font-weight:700; font-size:0.82rem;'>{icon_name}</span>
              <span style='color:#806040; font-size:0.75rem;'>{role}</span>
              <span style='color:#34d399; font-size:0.72rem; font-weight:700;'>✓ {quality}</span>
            </div>""", unsafe_allow_html=True)

    with st.expander("📸 ثبات الشخصية والمنتج — الدليل الكامل"):
        st.markdown("""
        #### في Google Flow / Veo / Kling AI:
        1. أنشئ مشروعاً جديداً
        2. ارفع `mahwous_character.png` → **Character Reference** → نشاط 80%
        3. ارفع صورة الزجاجة الأصلية → **Product Reference** → نشاط 90%
        4. الصق DNA الشخصية كاملاً من قسم **🎭 الشخصية والسيناريو**
        5. إضافة: `STRICTLY maintain character and product consistency`

        #### في Streamlit Studio:
        - ارفع mahwous_character.png في خانة "صورة مرجعية لمهووس"
        - سيُدمج تلقائياً في كل برومت
        """)

    with st.expander("🔗 إعداد Make.com للنشر التلقائي"):
        st.markdown("""
        1. افتح [make.com](https://make.com) → أنشئ Scenario جديداً
        2. Trigger: **Webhook** (Custom) → انسخ الـ URL
        3. أضف وحدات النشر: Telegram · Instagram · TikTok
        4. ألصق الـ URL في Secrets كـ `WEBHOOK_PUBLISH_CONTENT`
        5. شغّل الـ Scenario (ON)
        6. في الاستديو: فعّل "نشر تلقائي (Make.com)"
        """)

    with st.expander("💡 10 نصائح لأعلى جودة"):
        tips = [
            "ارفع صورة العطر بخلفية نظيفة (بيضاء أو شفافة) لتحليل أدق",
            "استخدم دائماً البدلة للمحتوى الرسمي والفاخر",
            "الهودي هو الأنسب لـ TikTok والمحتوى الشبابي",
            "السيناريو 'الحوار' هو الأعلى أداءً على TikTok وInstagram",
            "اختر 3-4 منصات فقط في كل جلسة للسرعة والجودة",
            "ارفع صورة مهووس المرجعية في بداية كل جلسة",
            "مشهد 'متجر العطور' يُنتج أفضل نتائج للبدلة",
            "مشهد 'الشاطئ' مثالي للكاجوال وعطور الصيف",
            "استخدم 'إضافات خاصة' في مولّد البرومت للتخصيص",
            "حمّل الصور بصيغة ZIP لحفظها منظمة",
        ]
        for i, tip in enumerate(tips, 1):
            st.markdown(f"**{i}.** {tip}")
