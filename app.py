"""
🌹 مهووس للعطور - استديو الذكاء الاصطناعي v10.0
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
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&family=Playfair+Display:wght@700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Cairo', sans-serif !important;
    direction: rtl;
}

/* Background */
.stApp {
    background: #060400;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080500 0%, #0F0800 50%, #080500 100%) !important;
    border-left: 1px solid rgba(212,175,55,0.25) !important;
}
[data-testid="stSidebarNav"] { display: none; }

/* Buttons */
div.stButton > button {
    background: linear-gradient(135deg, #8B6914 0%, #D4AF37 45%, #F0D060 55%, #A08020 100%);
    color: #000 !important; border: none; border-radius: 0.6rem;
    font-family: 'Cairo', sans-serif !important;
    font-weight: 800; font-size: 0.9rem;
    letter-spacing: 0.03rem;
    transition: all 0.25s;
    box-shadow: 0 2px 12px rgba(212,175,55,0.2);
    padding: 0.5rem 1.2rem;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(212,175,55,0.35);
}
div.stButton > button[kind="secondary"] {
    background: rgba(212,175,55,0.08) !important;
    color: #D4AF37 !important;
    border: 1px solid rgba(212,175,55,0.3) !important;
}

/* Tabs */
[data-testid="stTabs"] button[role="tab"] {
    font-family: 'Cairo', sans-serif !important;
    color: #806040 !important; font-weight: 600;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #D4AF37 !important;
    border-bottom: 2px solid #D4AF37 !important;
}

/* Inputs */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] > div > div {
    background: #0A0600 !important;
    color: #E8D8B0 !important;
    border-color: rgba(212,175,55,0.25) !important;
    font-family: 'Cairo', sans-serif !important;
}
label { color: #A09070 !important; }

/* Metrics */
[data-testid="stMetricValue"] { color: #D4AF37 !important; font-weight: 900 !important; }
[data-testid="stMetricLabel"] { color: #806040 !important; }

/* Expanders */
.streamlit-expanderHeader {
    background: rgba(212,175,55,0.05) !important;
    border: 1px solid rgba(212,175,55,0.15) !important;
    border-radius: 0.5rem !important;
    color: #D4AF37 !important;
}

/* Alerts */
.stSuccess { background: rgba(52,211,153,0.08) !important; border-color: #34d399 !important; }
.stWarning { background: rgba(251,191,36,0.08) !important; border-color: #fbbf24 !important; }
.stError   { background: rgba(239,68,68,0.08)  !important; border-color: #ef4444 !important; }
.stInfo    { background: rgba(212,175,55,0.06)  !important; border-color: rgba(212,175,55,0.3) !important; }

/* Checkboxes */
[data-testid="stCheckbox"] label { color: #C8B890 !important; }

/* Divider */
hr { border-color: rgba(212,175,55,0.15) !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #060400; }
::-webkit-scrollbar-thumb { background: rgba(212,175,55,0.3); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

from modules.studio import show_studio_page
from modules.character import show_character_page

# ═══ SIDEBAR ═══
with st.sidebar:
    # Logo
    st.markdown("""
    <div style="text-align:center; padding: 1.5rem 0 1rem;">
      <div style="font-size:3.2rem; filter:drop-shadow(0 0 12px rgba(212,175,55,0.7))">🌹</div>
      <div style="font-family:'Playfair Display',serif; font-size:1.8rem;
                  background:linear-gradient(135deg,#A08020,#F0D060,#A08020);
                  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                  background-clip:text; font-weight:900; letter-spacing:0.05rem;">
        مهووس
      </div>
      <div style="font-size:0.65rem; color:#5A4020; letter-spacing:0.3rem; margin-top:-0.2rem;">
        AI CONTENT STUDIO
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:0.5rem 0'>", unsafe_allow_html=True)

    # Navigation
    pages = {
        "🎬 استديو المحتوى":   "studio",
        "🎭 الشخصية والسيناريو": "character",
        "📊 الإحصائيات":       "dashboard",
        "⚙️ الإعدادات":        "settings",
    }

    if "page" not in st.session_state:
        st.session_state.page = "studio"

    for label, key in pages.items():
        active = st.session_state.page == key
        bg = "rgba(212,175,55,0.12)" if active else "transparent"
        border = "rgba(212,175,55,0.5)" if active else "transparent"
        color = "#D4AF37" if active else "#807050"
        st.markdown(f"""
        <div onclick="void(0)" style="background:{bg}; border:1px solid {border};
             border-radius:0.5rem; padding:0.55rem 1rem; margin:0.2rem 0; cursor:pointer;">
          <span style="color:{color}; font-size:0.88rem; font-weight:{'700' if active else '400'};">{label}</span>
        </div>""", unsafe_allow_html=True)
        if st.button(label, key=f"nav_{key}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.page = key
            st.rerun()

    st.markdown("<hr style='margin:0.5rem 0'>", unsafe_allow_html=True)

    # API Status
    st.markdown("<div style='color:#5A4020; font-size:0.72rem; font-weight:700; letter-spacing:0.1rem; margin-bottom:0.5rem;'>🔑 حالة الاتصال</div>", unsafe_allow_html=True)

    or_key = st.secrets.get("OPENROUTER_API_KEY", "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")
    gm_key = st.secrets.get("GEMINI_API_KEY", "")
    lm_key = st.secrets.get("LUMA_API_KEY", "")
    mk_key = st.secrets.get("WEBHOOK_PUBLISH_CONTENT", "")

    def status_row(ok, name, note=""):
        icon = "●" if ok else "○"
        color = "#34d399" if ok else "#ef4444"
        sub = f" <span style='color:#5A4020;font-size:0.68rem;'>{note}</span>" if note and not ok else ""
        return f"<div style='color:{color}; font-size:0.82rem; padding:0.1rem 0;'>{icon} {name}{sub}</div>"

    st.markdown(status_row(bool(or_key), "OpenRouter (نصوص)"), unsafe_allow_html=True)
    st.markdown(status_row(bool(gm_key), "Gemini (صور+تحليل)", "أضف في Secrets"), unsafe_allow_html=True)
    st.markdown(status_row(bool(lm_key), "Luma AI (فيديو)", "اختياري"), unsafe_allow_html=True)
    st.markdown(status_row(bool(mk_key), "Make.com (نشر)", "اختياري"), unsafe_allow_html=True)

    st.markdown("<hr style='margin:0.75rem 0'>", unsafe_allow_html=True)

    # Quick Stats
    if "gen_count" not in st.session_state:
        st.session_state.gen_count = 0
        st.session_state.img_count = 0

    c1, c2 = st.columns(2)
    c1.markdown(f"""<div style='text-align:center; background:rgba(212,175,55,0.06);
        border:1px solid rgba(212,175,55,0.15); border-radius:0.5rem; padding:0.5rem;'>
        <div style='color:#D4AF37; font-size:1.4rem; font-weight:900;'>{st.session_state.gen_count}</div>
        <div style='color:#5A4020; font-size:0.68rem;'>عمليات</div>
    </div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div style='text-align:center; background:rgba(212,175,55,0.06);
        border:1px solid rgba(212,175,55,0.15); border-radius:0.5rem; padding:0.5rem;'>
        <div style='color:#D4AF37; font-size:1.4rem; font-weight:900;'>{st.session_state.img_count}</div>
        <div style='color:#5A4020; font-size:0.68rem;'>صور</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<hr style='margin:0.5rem 0'>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; color:#3A2510; font-size:0.7rem;'>© 2026 مهووس للعطور · v10.0</div>", unsafe_allow_html=True)

# ═══ MAIN CONTENT ═══
page = st.session_state.page

if page == "studio":
    show_studio_page()

elif page == "character":
    show_character_page()

elif page == "dashboard":
    st.markdown("""
    <div style='background:linear-gradient(135deg,#080500,#120900); border:1px solid rgba(212,175,55,0.3);
         border-radius:1rem; padding:2rem; text-align:center; margin-bottom:2rem;'>
      <h1 style='color:#D4AF37; margin:0; font-family:Playfair Display,serif;'>📊 الإحصائيات</h1>
      <p style='color:#806040; margin:0.3rem 0 0;'>متابعة نشاط الاستديو</p>
    </div>
    """, unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    for col,label,val,icon in [
        (c1,"عمليات التوليد",  str(st.session_state.gen_count),"🚀"),
        (c2,"صور مولّدة",       str(st.session_state.img_count),"🖼️"),
        (c3,"فيديوهات",        "0","🎥"),
        (c4,"منشورات تلقائية","0","📡"),
    ]:
        col.markdown(f"""
        <div style='background:#080500; border:1px solid rgba(212,175,55,0.15);
             border-radius:0.75rem; padding:1.25rem; text-align:center;'>
          <div style='font-size:2rem;'>{icon}</div>
          <div style='color:#D4AF37; font-size:2rem; font-weight:900;'>{val}</div>
          <div style='color:#806040; font-size:0.82rem;'>{label}</div>
        </div>""", unsafe_allow_html=True)
    st.info("📈 الإحصائيات تُحدَّث مع كل عملية توليد")

elif page == "settings":
    st.markdown("""
    <div style='background:linear-gradient(135deg,#080500,#120900); border:1px solid rgba(212,175,55,0.3);
         border-radius:1rem; padding:2rem; text-align:center; margin-bottom:2rem;'>
      <h1 style='color:#D4AF37; margin:0; font-family:Playfair Display,serif;'>⚙️ الإعدادات</h1>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🔑 مفاتيح API في Streamlit Cloud Secrets", expanded=True):
        st.code("""# أضف هذه في Streamlit Cloud → Settings → Secrets

GEMINI_API_KEY = "AIza..."          # من aistudio.google.com (مجاني)
OPENROUTER_API_KEY = "sk-or-v1-..." # من openrouter.ai (موجود مسبقاً)
LUMA_API_KEY = "luma-..."           # من lumalabs.ai (اختياري)
WEBHOOK_PUBLISH_CONTENT = "https://hook.eu2.make.com/..."  # Make.com""", language="toml")

    with st.expander("📸 كيفية الحفاظ على ثبات الشخصية"):
        st.markdown("""
        **في Google Flow / Veo / Kling:**
        1. ارفع `mahwous_character.png` → **Add Reference Image** → **Character Consistency**
        2. ارفع صورة الزجاجة الأصلية → **Add Reference Image** → **Product Consistency**
        3. في كل برومت: أضف DNA الشخصية من قسم **🎭 الشخصية والسيناريو**

        **في Streamlit Studio:**
        - ارفع صورة مهووس المرجعية في خانة "صورة مرجعية لمهووس"
        - الاستديو يدمجها تلقائياً في كل برومت
        """)

    with st.expander("🔗 ربط Make.com للنشر التلقائي"):
        st.markdown("""
        1. افتح [make.com](https://make.com) → أنشئ Scenario
        2. ارفع `make_blueprint_studio_v9.json`
        3. أضف Telegram Bot Token + Discord Webhook
        4. انسخ Webhook URL → أضفه في Secrets
        5. فعّل الـ Scenario (ON)
        """)

    with st.expander("💡 نصائح لأفضل جودة"):
        tips = [
            "ارفع صورة العطر بخلفية بيضاء أو شفافة لدقة تحليل أعلى",
            "اختر 3-5 منصات فقط في كل عملية لتوليد أسرع",
            "استخدم زي البدلة للمحتوى الفاخر، والهودي للـ TikTok",
            "أضف صورة مرجعية لمهووس في كل جلسة لثبات الشخصية",
            "سيناريو الحوار هو الأنجح على TikTok وInstagram",
        ]
        for t in tips:
            st.markdown(f"💡 {t}")
