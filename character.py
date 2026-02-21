"""
🎭 استديو الشخصية - مهووس v10.0
DNA الشخصية + مولّد برومتات Google Flow
"""

import streamlit as st
import json
from modules.ai_engine import MAHWOUS_DNA, MAHWOUS_OUTFITS, QUALITY, smart_generate_text, clean_json

SCENES = {
    "store":   {"label": "🏪 متجر العطور",     "desc": "luxury dark perfume boutique, golden shelves behind"},
    "beach":   {"label": "🌅 شاطئ الغروب",     "desc": "dramatic golden hour sunset beach, ocean waves"},
    "desert":  {"label": "🏜️ صحراء ذهبية",    "desc": "endless golden desert at sunset, dramatic dunes"},
    "studio":  {"label": "🎬 استديو فاخر",     "desc": "premium dark studio, golden bokeh particles floating"},
    "garden":  {"label": "🌹 حديقة ملكية",     "desc": "royal garden at magic hour, rose petals falling"},
    "rooftop": {"label": "🌆 سطح ناطحة سحاب", "desc": "luxury rooftop at night, city lights below, starry sky"},
    "car":     {"label": "🚗 سيارة فارهة",     "desc": "inside Rolls-Royce, city lights blur past windows"},
}

CAMERA_MOVES = {
    "push_in":  "slow push-in toward subject",
    "zoom":     "gradual zoom from wide to close",
    "orbit":    "slow orbital movement around subject",
    "static":   "static cinematic frame",
    "low_rise": "low angle slowly rising up",
    "dolly":    "smooth dolly track alongside subject",
}

RULES_BROKEN_FIXES = {
    "text_on_screen":     ("❌ نصوص ظهرت على الشاشة",      "أضف: NO TEXT on screen, NO subtitles, NO watermarks, clean frame"),
    "mouth_open_listen":  ("❌ فم مهووس مفتوح عند الاستماع", "أضف: Mahwous with mouth completely closed, lips sealed, listening"),
    "bottle_distorted":   ("❌ الزجاجة تشوهت",              "أضف: STRICTLY MAINTAIN exact original bottle design from reference image, photorealistic product"),
    "character_changed":  ("❌ ملامح مهووس تغيرت",          "ارفع صورة مهووس كـ Reference + أضف DNA الشخصية كاملاً"),
    "spraying":           ("❌ ظهر رش للعطر",               "أضف: NO SPRAYING, show golden particles or bottle glow instead"),
    "bad_lighting":       ("❌ إضاءة سيئة أو باردة",        "أضف: warm golden amber cinematic lighting, luxury color grading, rim lights, dramatic shadows"),
}

BOTTLE_REPLIES = {
    "oud":     ["أنا ذاكرة من لا ينسى.", "العمق لا يُشرح... يُشعر.", "أنا الملك الذي لا يتكلم كثيراً.", "بعض الأشياء أعمق من الكلام."],
    "western": ["بعض العظمة لا تحتاج كلاماً.", "أنا الفرق بين حضور ومرور.", "لا تسأل من أنا... اشعر بي.", "أنا الثقة التي تبحث عنها."],
    "summer":  ["أنا الصيف الذي لا ينتهي.", "كل خطوة معي... رحلة.", "أنا حريتك.", "البحر في جرة صغيرة."],
    "winter":  ["الدفء ليس درجة حرارة... هو أثر.", "أنا ما يبقى بعد الرحيل.", "أنا الليل الذي تتذكره.", "الغموض جمال."],
}


def show_character_page():
    st.markdown("""
    <style>
    .char-hero {
        background: linear-gradient(135deg, #0A0600 0%, #150900 60%, #0A0600 100%);
        border: 1px solid rgba(212,175,55,0.35);
        border-radius: 1.25rem; padding: 2rem; text-align: center; margin-bottom: 2rem;
    }
    .char-hero h1 { color: #D4AF37; font-size: 1.9rem; margin: 0; }
    .char-hero p  { color: #806040; margin: 0.3rem 0 0; font-size: 0.88rem; }
    .dna-box {
        background: #050300; border: 1px solid rgba(212,175,55,0.25);
        border-radius: 0.75rem; padding: 1.1rem;
        font-family: 'Courier New', monospace; font-size: 0.78rem;
        color: #B8A050; line-height: 1.8; direction: ltr; text-align: left;
    }
    .rule-chip {
        display: inline-block; background: rgba(239,68,68,0.12);
        border: 1px solid rgba(239,68,68,0.3); color: #fc8181;
        padding: 0.2rem 0.6rem; border-radius: 999px; font-size: 0.75rem; margin: 0.2rem;
    }
    .fix-chip {
        display: inline-block; background: rgba(52,211,153,0.1);
        border: 1px solid rgba(52,211,153,0.3); color: #34d399;
        padding: 0.2rem 0.6rem; border-radius: 999px; font-size: 0.75rem; margin: 0.2rem;
    }
    .prompt-result {
        background: #030200; border: 1px solid rgba(212,175,55,0.35);
        border-radius: 0.75rem; padding: 1.1rem;
        font-family: 'Courier New', monospace; font-size: 0.77rem;
        color: #90C870; line-height: 1.8; direction: ltr; text-align: left;
        white-space: pre-wrap; max-height: 380px; overflow-y: auto;
    }
    .reply-card {
        background: rgba(212,175,55,0.04); border-right: 2px solid #D4AF37;
        border-radius: 0.4rem; padding: 0.6rem 0.8rem; margin: 0.3rem 0;
        color: #F0E0C0; font-style: italic; font-size: 0.88rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="char-hero">
      <h1>🎭 استديو الشخصية الموحدة</h1>
      <p>DNA مهووس الثابت · مولّد برومتات Google Flow · مكتبة السيناريوهات</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "🧬 DNA الشخصية",
        "⚡ مولّد البرومت",
        "🎬 السيناريوهات",
        "🔧 حل الأخطاء"
    ])

    # ═══ TAB 1: DNA ═══
    with tab1:
        st.markdown("### 🧬 الجزء الثابت · انسخه في بداية كل برومت")
        st.info("📌 هذا الـ DNA يحافظ على ثبات مهووس في كل صورة وفيديو")
        st.markdown(f'<div class="dna-box">{MAHWOUS_DNA}</div>', unsafe_allow_html=True)

        with st.expander("📋 نسخ DNA"):
            st.code(MAHWOUS_DNA, language="text")

        st.divider()
        st.markdown("### 👔 أزياء مهووس الرسمية")
        for key, desc in MAHWOUS_OUTFITS.items():
            labels = {"suit": "🤵 البدلة الفاخرة", "hoodie": "🏆 الهودي الأيقوني",
                      "thobe": "👘 الثوب الملكي", "casual": "👕 الكاجوال"}
            uses = {"suit": "للمشاهد الرسمية والفاخرة", "hoodie": "للمحتوى الشبابي وTikTok",
                    "thobe": "للمناسبات والمحلية", "casual": "للمشاهد العاطفية"}
            with st.expander(f"{labels[key]} · {uses[key]}"):
                st.markdown(f'<div class="dna-box">{desc}</div>', unsafe_allow_html=True)

        st.divider()
        st.markdown("### 🚫 القواعد الذهبية")
        rules = ["الشعر **أسود دائماً** بدون استثناء",
                 "اللحية **لا تختفي** ولا تطول كثيراً",
                 "العيون **بنية** في كل المشاهد",
                 "**NO TEXT on screen** في كل برومت",
                 "**NO SPRAYING** استخدم جزيئات ذهبية بدلاً",
                 "فم مهووس **مغلق** عند كلام العطر",
                 "ارفع **صورة الزجاجة الأصلية** كـ Reference دائماً",
                 "ارفع **mahwous_character.png** كـ Reference دائماً"]
        for r in rules:
            st.markdown(f"🔴 {r}")

    # ═══ TAB 2: PROMPT BUILDER ═══
    with tab2:
        st.markdown("### ⚡ مولّد برومت Google Flow / Veo")

        c1, c2 = st.columns(2)
        with c1:
            pname = st.text_input("🌹 اسم العطر", "Chopard Oud Malaki")
            pbrand = st.text_input("🏷️ العلامة", "Chopard")
            duration = st.select_slider("⏱️ المدة (ثانية)", ["5", "7", "10", "12", "15"], value="7")
        with c2:
            outfit = st.selectbox("👔 الزي",
                options=list(MAHWOUS_OUTFITS.keys()),
                format_func=lambda k: {"suit":"🤵 البدلة","hoodie":"🏆 الهودي","thobe":"👘 الثوب","casual":"👕 الكاجوال"}[k])
            scene = st.selectbox("🎭 المكان",
                options=list(SCENES.keys()),
                format_func=lambda k: SCENES[k]["label"])
            camera = st.selectbox("📷 حركة الكاميرا",
                options=list(CAMERA_MOVES.keys()),
                format_func=lambda k: CAMERA_MOVES[k])

        bottle_shape = st.text_input("🫙 شكل الزجاجة (من تحليل الصورة)", "elegant golden flacon with black cap")
        bottle_colors = st.text_input("🎨 ألوان الزجاجة", "gold, black")
        scene_type = st.radio("نوع المشهد", ["مهووس مع العطر", "العطر يتكلم وحده", "مهووس بدون عطر"], horizontal=True)

        if st.button("✨ توليد البرومت", type="primary", use_container_width=True):
            outfit_desc = MAHWOUS_OUTFITS[outfit]
            scene_desc  = SCENES[scene]["desc"]
            cam_desc    = CAMERA_MOVES[camera]

            if scene_type == "مهووس مع العطر":
                prompt = f"""{MAHWOUS_DNA}
{outfit_desc}
Location: {scene_desc}
He carefully holds {pname} by {pbrand} perfume bottle - EXACT ORIGINAL bottle: {bottle_shape}, colors: {bottle_colors}.
DO NOT alter perfume bottle design. Bottle must match reference exactly.
Expression: expert confidence, warm smile. Lips moving naturally as he speaks.
Camera: {cam_desc}. Duration: {duration} seconds. 9:16 vertical portrait.
{QUALITY}"""

            elif scene_type == "العطر يتكلم وحده":
                prompt = f"""Cinematic extreme close-up of {pname} by {pbrand} perfume bottle.
STRICTLY MAINTAIN exact original bottle: {bottle_shape}, colors: {bottle_colors}.
The bottle has subtle glowing eyes and elegant lips that move gracefully.
Lips sync with a deep royal Arabic voice. NO TEXT.
Mahwous visible blurred in background with mouth completely closed.
Camera: {cam_desc}. Duration: {duration} seconds. 9:16 vertical.
{QUALITY}"""
            else:
                prompt = f"""{MAHWOUS_DNA}
{outfit_desc}
Location: {scene_desc}
He stands confidently looking at camera, hand gesturing expressively.
No perfume bottle visible. Expression: speaking with passion and expertise.
Camera: {cam_desc}. Duration: {duration} seconds. 9:16 vertical.
{QUALITY}"""

            st.markdown("#### 📋 البرومت الجاهز")
            st.markdown(f'<div class="prompt-result">{prompt}</div>', unsafe_allow_html=True)
            with st.expander("🖱️ نسخ البرومت كاملاً"):
                st.code(prompt, language="text")
            st.success("✅ جاهز! الصقه في Google Flow أو Veo مع رفع صور المرجع")

    # ═══ TAB 3: SCENARIOS ═══
    with tab3:
        st.markdown("### 🎬 مكتبة السيناريوهات")

        perfume_sc = st.text_input("🌹 اسم العطر للسيناريو", "Chopard Oud Malaki")
        sc_type = st.radio("نوع السيناريو", [
            "👑 سر الملك (14 ث)", "⚔️ التحدي (16 ث)", "💬 الحوار الكلاسيكي (14 ث)", "📖 القصة (21 ث)"
        ], horizontal=True)

        if "👑" in sc_type:
            scenes_data = [
                (1, "4 ث", "الهوك", "Wide Track", "مهووس يبحث في رفوف العطور ببطء، يتوقف على الزجاجة تسطع هالة ذهبية", "ظننت أني أعرف كل ملوك العطور...", "مهووس"),
                (2, "4 ث", "الكشف", "Medium CU", "مهووس يمسك الزجاجة، تفتح عينيها فجأة ببطء. دهشة+إعجاب", "...من أنت؟", "مهووس"),
                (3, "4 ث", "ذروة", "ECU Bottle", f"الزجاجة تتكلم. مهووس في الخلف out-of-focus بفم مغلق", "الملك لا يُعرف بعرشه... بل بحضوره.", "العطر"),
                (4, "3 ث", "خاتمة", "Medium Reveal", "مهووس يبتسم ويرفع الزجاجة نحو الكاميرا ويغمز", f"{perfume_sc}. الحضور الذي لا يغيب.", "مهووس"),
            ]
        elif "⚔️" in sc_type:
            scenes_data = [
                (1, "5 ث", "الهوك", "Medium Static", "مهووس يشم عطوراً متعددة بوجه ملول ويهز رأسه", "كل العطور صارت... نفس الشيء.", "مهووس"),
                (2, "3 ث", "انقلاب", "Smash Cut CU", "يمسك العطر المستهدف. تحول لوني درامي. عيناه تتسعان", "🎵 whoosh + موسيقى تتصاعد", "مؤثر"),
                (3, "8 ث", "ذروة+خاتمة", "Push In", "مهووس يرفع الزجاجة للكاميرا بحماس. خلفه مكونات تطير", f"إلا هذا! {perfume_sc}... هذا مو عطر عادي!", "مهووس"),
            ]
        elif "💬" in sc_type:
            scenes_data = [
                (1, "7 ث", "مهووس يتكلم", "Medium Shot", "يمسك العطر بيديه ويخاطبه مباشرة. الزجاجة ساكنة", "[تعليق مهووس على العطر]", "مهووس"),
                (2, "7 ث", "العطر يرد", "ECU Bottle", "وجه الزجاجة يتكلم بهدوء. مهووس في الخلف بفم مغلق", "الملك لا يُعرف بعرشه، بل بحضوره.", "العطر"),
            ]
        else:
            scenes_data = [
                (1, "7 ث", "البداية", "Environment", "مهووس في موقف عادي قبل العطر", "[وصف الحاجة]", "مهووس"),
                (2, "7 ث", "التحول", "CU Color Shift", "تحول لوني. العطر يغير كل شيء", "🎵 إيقاع يتصاعد", "موسيقى"),
                (3, "7 ث", "النتيجة", "Confident Medium", f"مهووس جديد يرفع {perfume_sc}", f"بفضل {perfume_sc}.", "مهووس"),
            ]

        for num, dur, sc_t, cam, desc, audio, speaker in scenes_data:
            color = "#D4AF37" if speaker == "مهووس" else "#E94560" if speaker == "العطر" else "#60A5FA"
            st.markdown(f"""
            <div style='background:#0A0600; border-right:3px solid #D4AF37; border-radius:0.5rem; padding:0.9rem; margin-bottom:0.6rem;'>
              <div style='display:flex; gap:0.5rem; align-items:center; margin-bottom:0.4rem;'>
                <span style='background:#D4AF37; color:#000; width:1.5rem; height:1.5rem; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-weight:900; font-size:0.75rem;'>{num}</span>
                <span style='color:#D4AF37; font-weight:700; font-size:0.85rem;'>{sc_t}</span>
                <span style='color:#555; font-size:0.75rem;'>⏱ {dur} | 📷 {cam}</span>
              </div>
              <p style='color:#A09070; font-size:0.83rem; margin:0 0 0.4rem;'>{desc}</p>
              <div style='background:rgba(212,175,55,0.04); border-right:2px solid {color}; padding:0.4rem 0.7rem; border-radius:0.3rem;'>
                <span style='color:{color}; font-size:0.72rem; font-weight:700;'>{speaker}: </span>
                <span style='color:#F0E0C0; font-style:italic; font-size:0.85rem;'>"{audio}"</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

        # Export scenario
        if st.button("📄 تصدير السيناريو كاملاً", use_container_width=True):
            text = f"# سيناريو: {sc_type.split('(')[0].strip()} | العطر: {perfume_sc}\n\n"
            for num, dur, sc_t, cam, desc, audio, speaker in scenes_data:
                text += f"━━━ اللقطة {num}: {sc_t} · {dur} ━━━\n📷 {cam}\n🎭 {desc}\n🎙️ {speaker}: \"{audio}\"\n\n"
            st.code(text, language="text")

        # Bottle replies
        st.divider()
        st.markdown("### 💬 ردود العطر الجاهزة")
        for cat, replies in BOTTLE_REPLIES.items():
            labels = {"oud":"🔥 العود","western":"💎 الغربية","summer":"🌊 الصيفية","winter":"❄️ الشتوية"}
            with st.expander(labels[cat]):
                for r in replies:
                    st.markdown(f'<div class="reply-card">"{r}"</div>', unsafe_allow_html=True)

    # ═══ TAB 4: ERROR FIXES ═══
    with tab4:
        st.markdown("### 🔧 حل الأخطاء الشائعة فوراً")
        for key, (problem, fix) in RULES_BROKEN_FIXES.items():
            with st.expander(problem):
                st.markdown(f"**✅ الحل:**")
                st.code(fix, language="text")
                st.info("أضف هذا النص في برومتك وأعد التوليد")
