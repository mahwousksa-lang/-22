"""
🎭 استديو الشخصية - مهووس v11.0
DNA الشخصية + مولّد برومتات Google Flow + سيناريوهات مولّدة بالذكاء الاصطناعي
"""

import streamlit as st
import json
from modules.ai_engine import (
    MAHWOUS_DNA, MAHWOUS_OUTFITS, QUALITY,
    smart_generate_text, clean_json, generate_scenario
)

SCENES = {
    "store":   {"label": "🏪 متجر العطور",     "desc": "breathtaking luxury dark perfume boutique, golden backlit shelves, obsidian floor"},
    "beach":   {"label": "🌅 شاطئ الغروب",     "desc": "cinematic golden-hour beach, amber sky, foamy waves, sunset shadows"},
    "desert":  {"label": "🏜️ صحراء ذهبية",    "desc": "vast golden Arabian desert at dusk, towering dunes, stars appearing"},
    "studio":  {"label": "🎬 استديو فاخر",     "desc": "minimalist luxury dark studio, golden bokeh particles, dramatic overhead rim"},
    "garden":  {"label": "🌹 حديقة ملكية",     "desc": "lush royal fragrance garden, cascading rose petals, golden mist, marble fountain"},
    "rooftop": {"label": "🌆 سطح ناطحة سحاب", "desc": "glass-barrier luxury rooftop at night, twinkling city skyline, starry sky"},
    "car":     {"label": "🚗 سيارة فارهة",     "desc": "Rolls-Royce Phantom rear seat, cream leather, city lights blurring past wet windows"},
}

CAMERA_MOVES = {
    "push_in":  "Slow cinematic push-in toward subject (creates intimacy)",
    "zoom":     "Gradual zoom from wide establishing to tight close-up",
    "orbit":    "Smooth slow orbital movement around subject (360° elegance)",
    "static":   "Static locked-off cinematic frame (power and confidence)",
    "low_rise": "Low angle slowly rising upward (hero perspective)",
    "dolly":    "Smooth dolly track gliding alongside subject",
    "crane":    "Slow crane descent from above to eye level (cinematic reveal)",
}

BOTTLE_REPLIES = {
    "oud":     [
        "أنا ذاكرة من لا يُنسى.",
        "العمق لا يُشرح... يُشعر.",
        "أنا الملك الذي لا يتكلم كثيراً.",
        "بعض الأشياء أعمق من الكلمات.",
        "ألف سنة من الحكمة في قطرة واحدة.",
    ],
    "western": [
        "أنا الفرق بين حضور ومرور.",
        "لا تسأل من أنا... اشعر بي.",
        "أنا الثقة التي تبحث عنها.",
        "بعض العظمة لا تحتاج كلاماً.",
        "أنا ما يتذكره الناس بعد رحيلك.",
    ],
    "summer":  [
        "أنا الصيف الذي لا ينتهي.",
        "كل خطوة معي... رحلة.",
        "أنا حريتك — لا ترتدني، عشني.",
        "البحر في جرة صغيرة.",
        "الفرح ليس شعوراً... هو رائحتي.",
    ],
    "winter":  [
        "الدفء ليس درجة حرارة... هو أثر.",
        "أنا ما يبقى بعد الرحيل.",
        "أنا الليل الذي تتذكره دائماً.",
        "الغموض ليس نقصاً... هو جمال.",
        "بعض الأشياء تُشعَل ولا تُطفأ.",
    ],
}

RULES_BROKEN_FIXES = {
    "text_on_screen":     ("❌ نصوص أو watermarks ظهرت على الشاشة", "NO TEXT on screen. NO watermarks. NO subtitles. NO logos. Clean professional frame only."),
    "mouth_open_listen":  ("❌ فم مهووس مفتوح عند استماعه للعطر",   "Mahwous with mouth completely closed, lips sealed together, silent attentive listening expression."),
    "bottle_distorted":   ("❌ الزجاجة تشوهت أو تغيرت",            "STRICTLY MAINTAIN exact original bottle design. Photorealistic product match. DO NOT alter shape, proportions, colors, or label."),
    "character_changed":  ("❌ ملامح مهووس تغيرت أو اختلفت",       "Upload mahwous_character.png as Character Reference image. Include full DNA prompt. LOCK all facial features."),
    "spraying":           ("❌ ظهر رش للعطر",                       "NO SPRAYING. NO mist clouds. Replace with: golden luminous particles floating gently, subtle bottle glow effect."),
    "bad_lighting":       ("❌ إضاءة باردة أو مسطحة",              "Warm golden amber cinematic 3-point lighting. Key light warm gold from front-right. Rim light metallic from behind. Fill soft from left. Rich shadows."),
    "background_wrong":   ("❌ خلفية غير مناسبة أو مشتتة",         "Dark luxury background. Deep shadows. Subtle golden bokeh particles. Clean negative space. No clutter."),
    "character_missing":  ("❌ مهووس لا يظهر في الصورة",            "Include full MAHWOUS_DNA at start of prompt. Add: Mahwous prominently featured, centered, three-quarter view toward camera."),
}


def show_character_page():
    st.markdown("""
    <style>
    .char-hero {
        background: linear-gradient(135deg, #1A0E02 0%, #281808 60%, #1A0E02 100%);
        border: 2px solid rgba(212,175,55,0.55); border-radius: 1.25rem;
        padding: 2rem; text-align: center; margin-bottom: 2rem;
    }
    .char-hero h1 { color: #FFE060; font-size: 2rem; margin: 0; font-weight: 900; }
    .char-hero p  { color: #F0C870; margin: 0.4rem 0 0; font-size: 0.92rem; font-weight: 700; }
    .dna-box {
        background: #1A1006; border: 2px solid rgba(212,175,55,0.40);
        border-radius: 0.75rem; padding: 1.2rem;
        font-family: 'Courier New', monospace; font-size: 0.8rem;
        color: #E8D090; line-height: 1.9; direction: ltr; text-align: left;
        white-space: pre-wrap;
    }
    .rule-chip {
        display: inline-block; background: rgba(239,68,68,0.18);
        border: 1.5px solid rgba(239,68,68,0.50); color: #FFB0B0;
        padding: 0.28rem 0.7rem; border-radius: 999px; font-size: 0.78rem; margin: 0.2rem;
        font-weight: 700;
    }
    .fix-chip {
        display: inline-block; background: rgba(52,211,153,0.15);
        border: 1.5px solid rgba(52,211,153,0.50); color: #80FFD0;
        padding: 0.28rem 0.7rem; border-radius: 999px; font-size: 0.78rem; margin: 0.2rem;
        font-weight: 700;
    }
    .prompt-result {
        background: #1A1006; border: 2px solid rgba(212,175,55,0.40);
        border-radius: 0.75rem; padding: 1.2rem;
        font-family: 'Courier New', monospace; font-size: 0.8rem;
        color: #B0E870; line-height: 1.9; direction: ltr; text-align: left;
        white-space: pre-wrap; max-height: 400px; overflow-y: auto;
    }
    .reply-card {
        background: rgba(212,175,55,0.10); border-right: 3px solid #FFD840;
        border-radius: 0.5rem; padding: 0.7rem 1rem; margin: 0.3rem 0;
        color: #FFF0D0; font-style: italic; font-size: 0.9rem; line-height: 1.6;
        font-weight: 600;
    }
    .outfit-card {
        background: #1E1408; border: 1.5px solid rgba(212,175,55,0.30);
        border-radius: 0.6rem; padding: 0.9rem; margin-bottom: 0.5rem;
    }
    .outfit-label { color: #FFE060; font-weight: 900; font-size: 0.9rem; margin-bottom: 0.3rem; }
    .outfit-use   { color: #D4A860; font-size: 0.78rem; margin-bottom: 0.5rem; font-weight: 600; }
    .scene-card-char {
        background: #1A1206; border-right: 4px solid #FFD840;
        border-radius: 0.5rem; padding: 0.8rem; margin-bottom: 0.55rem;
    }
    .scene-num-char {
        display: inline-flex; align-items: center; justify-content: center;
        background: #D4AF37; color: #000; width: 1.6rem; height: 1.6rem;
        border-radius: 50%; font-weight: 900; font-size: 0.78rem; margin-left: 0.4rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="char-hero">
      <h1>🎭 استديو الشخصية الموحدة</h1>
      <p>DNA مهووس الثابت · مولّد برومتات Google Flow/Veo · سيناريوهات مدعومة بالذكاء الاصطناعي</p>
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
        st.markdown("### 🧬 DNA الثابت — انسخه في بداية كل برومت")
        st.info("📌 هذا الـ DNA يضمن ثبات ملامح مهووس في كل صورة وفيديو على أي نموذج")

        st.markdown(f'<div class="dna-box">{MAHWOUS_DNA}</div>', unsafe_allow_html=True)
        st.code(MAHWOUS_DNA, language="text")
        st.markdown("---")

        # Outfits
        st.markdown("### 👔 الأزياء الرسمية لمهووس")
        outfit_labels = {
            "suit":   ("🤵 البدلة الفاخرة",   "المحتوى الراقي · الإعلانات الرسمية · الفيديوهات الفاخرة"),
            "hoodie": ("🏆 الهودي الأيقوني",  "TikTok الشبابي · المحتوى غير الرسمي · البريالز"),
            "thobe":  ("👘 الثوب الملكي",      "المناسبات الخليجية · رمضان · المحتوى المحلي"),
            "casual": ("👕 الكاجوال الأنيق",  "المشاهد العاطفية · الشاطئ · القصص الصيفية"),
        }
        for key, desc in MAHWOUS_OUTFITS.items():
            label, use = outfit_labels[key]
            st.markdown(f"""
            <div class="outfit-card">
              <div class="outfit-label">{label}</div>
              <div class="outfit-use">أفضل استخدام: {use}</div>
              <div class="dna-box" style="margin-top:0;">{desc}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🔴 القواعد الذهبية غير القابلة للكسر")
        rules = [
            ("الشعر", "أسود دائماً — لا تغيير أبداً"),
            ("اللحية", "قصيرة ومهذبة — لا تطول ولا تختفي"),
            ("العيون", "بنية دافئة في كل المشاهد"),
            ("NO TEXT", "لا نصوص على الشاشة في أي برومت"),
            ("NO SPRAYING", "لا رش — جزيئات ذهبية بديلاً"),
            ("فم مهووس", "مغلق تماماً عند كلام العطر"),
            ("صورة الزجاجة", "ارفع الصورة الأصلية دائماً كـ Reference"),
            ("صورة مهووس", "ارفع mahwous_character.png دائماً كـ Reference"),
        ]
        for field, rule in rules:
            st.markdown(f"🔴 **{field}:** {rule}")

    # ═══ TAB 2: PROMPT BUILDER ═══
    with tab2:
        st.markdown("### ⚡ مولّد برومت Google Flow / Veo")
        st.caption("ملء الحقول → انقر توليد → انسخ البرومت إلى Google Flow مع رفع صور المرجع")

        c1, c2 = st.columns(2)
        with c1:
            pname       = st.text_input("🌹 اسم العطر",        placeholder="Chopard Oud Malaki")
            pbrand      = st.text_input("🏷️ العلامة",         placeholder="Chopard")
            bottle_shape = st.text_input("🫙 شكل الزجاجة",    placeholder="elegant golden flacon with black cap")
            bottle_colors = st.text_input("🎨 ألوان الزجاجة", placeholder="gold, black, transparent")
        with c2:
            duration = st.select_slider("⏱️ المدة", ["5","7","10","12","15","20"], value="7")
            outfit   = st.selectbox("👔 الزي",
                options=list(MAHWOUS_OUTFITS.keys()),
                format_func=lambda k: outfit_labels.get(k, (k, ""))[0] if 'outfit_labels' in dir() else k)
            scene    = st.selectbox("🎭 المكان",
                options=list(SCENES.keys()),
                format_func=lambda k: SCENES[k]["label"])
            camera   = st.selectbox("📷 حركة الكاميرا",
                options=list(CAMERA_MOVES.keys()),
                format_func=lambda k: CAMERA_MOVES[k])

        scene_type = st.radio("نوع المشهد", [
            "مهووس مع العطر", "العطر يتكلم وحده", "مهووس بدون عطر"
        ], horizontal=True)

        mood_extra = st.text_input("✨ إضافات خاصة (اختياري)", placeholder="مثال: golden rain effect, Ramadan lanterns, rose petals falling")

        if st.button("🚀 توليد البرومت", type="primary", use_container_width=True):
            od   = MAHWOUS_OUTFITS.get(outfit, MAHWOUS_OUTFITS["suit"])
            sd   = SCENES[scene]["desc"]
            cd   = CAMERA_MOVES[camera]
            extra = f"\nAdditional: {mood_extra}" if mood_extra else ""

            if scene_type == "مهووس مع العطر":
                prompt = f"""{MAHWOUS_DNA}
Outfit: {od}
Setting: {sd}
He cradles {pname} by {pbrand} perfume bottle reverently with both hands:
— Bottle: {bottle_shape}. Colors: {bottle_colors}.
CRITICAL: DO NOT alter bottle design. Exact photorealistic match to reference image.
Expression: warm expert confidence, knowing smile, eyes engaging camera.
Camera: {cd}. Duration: {duration}s. 9:16 vertical portrait.{extra}
{QUALITY}"""

            elif scene_type == "العطر يتكلم وحده":
                prompt = f"""Cinematic extreme close-up of {pname} by {pbrand} perfume bottle.
STRICTLY MAINTAIN exact original bottle: {bottle_shape}, colors: {bottle_colors}.
The bottle has subtle glowing eyes — warm, intelligent, regal. Elegant lips that move gracefully in sync with a deep royal Arabic voice.
NO distortion to bottle. NO text.
Mahwous visible softly out-of-focus in background, mouth completely closed, listening in awe.
Setting: {sd}
Camera: {cd}. Duration: {duration}s. 9:16 vertical.{extra}
{QUALITY}"""

            else:  # مهووس بدون عطر
                prompt = f"""{MAHWOUS_DNA}
Outfit: {od}
Setting: {sd}
He stands confidently, addressing the camera directly with passionate hand gestures.
Expression: expert enthusiasm, compelling storytelling.
No perfume bottle visible in frame.
Camera: {cd}. Duration: {duration}s. 9:16 vertical.{extra}
{QUALITY}"""

            st.markdown("#### 📋 البرومت الجاهز")
            st.markdown(f'<div class="prompt-result">{prompt}</div>', unsafe_allow_html=True)
            st.code(prompt, language="text")
            st.success("✅ انسخ البرومت أعلاه إلى Google Flow / Veo مع رفع صورتَي المرجع")

            # Instructions
            with st.expander("📌 خطوات الاستخدام في Google Flow / Veo"):
                st.markdown("""
1. افتح **Google Flow** أو **Google Veo**
2. انشئ مشروع جديد → اختر **Character Consistency**
3. ارفع `mahwous_character.png` → حدده كـ **Character Reference**
4. ارفع صورة زجاجة العطر الأصلية → حدده كـ **Product Reference**
5. الصق البرومت أعلاه في خانة **Text Prompt**
6. اضغط **Generate** — انتظر 2-5 دقائق
7. إذا ظهرت مشكلة، راجع تبويب **🔧 حل الأخطاء**
                """)

    # ═══ TAB 3: SCENARIOS ═══
    with tab3:
        st.markdown("### 🎬 مكتبة السيناريوهات + التوليد الذكي")

        gen_col, lib_col = st.tabs(["🤖 توليد بالذكاء الاصطناعي", "📚 المكتبة الجاهزة"])

        with gen_col:
            st.markdown("##### أدخل بيانات العطر وسيولّد الذكاء الاصطناعي سيناريو مخصصاً")
            ai_sc1, ai_sc2 = st.columns(2)
            with ai_sc1:
                ai_name = st.text_input("اسم العطر", "Initio Oud for Greatness", key="ai_name")
                ai_brand = st.text_input("العلامة", "Initio", key="ai_brand")
                ai_mood  = st.text_input("المزاج", "قوي، غامض، فاخر", key="ai_mood")
            with ai_sc2:
                ai_type  = st.selectbox("نوع السيناريو", [
                    "dialogue", "story", "challenge", "review", "unboxing"
                ], format_func=lambda k: {
                    "dialogue": "💬 حوار مهووس والعطر",
                    "story":    "📖 قصة تحول عاطفية",
                    "challenge":"⚔️ مشهد الاكتشاف",
                    "review":   "⭐ مراجعة خبير",
                    "unboxing": "📦 فتح العلبة",
                }[k], key="ai_sc_type")
                ai_notes = st.text_input("ملاحظات", "عود، مسك، سانداوود", key="ai_notes")

            if st.button("🤖 توليد سيناريو بالذكاء الاصطناعي", type="primary", use_container_width=True):
                info_mock = {
                    "product_name": ai_name,
                    "brand": ai_brand,
                    "mood": ai_mood,
                    "style": "luxury",
                    "notes_guess": ai_notes,
                }
                with st.spinner("🎬 الذكاء الاصطناعي يكتب سيناريو مخصصاً..."):
                    try:
                        scenario = generate_scenario(info_mock, ai_type)
                        if scenario and "scenes" in scenario:
                            st.success(f"✅ تم توليد السيناريو: {scenario.get('title', '')}")

                            # Display
                            st.markdown(f"""
                            <div style='background:#080500; border:1px solid rgba(212,175,55,0.3); border-radius:0.75rem; padding:1rem; margin-bottom:1rem;'>
                              <div style='color:#D4AF37; font-size:1rem; font-weight:900;'>🎬 {scenario.get('title')}</div>
                              <div style='color:#806040; font-size:0.8rem; margin-top:0.25rem;'>
                                ⏱️ {scenario.get('total_duration')} ثانية | 🎯 الهوك: <em>"{scenario.get('hook', '')}"</em>
                              </div>
                            </div>""", unsafe_allow_html=True)

                            for scene in scenario.get("scenes", []):
                                num   = scene.get("number", "?")
                                typ   = scene.get("type", "")
                                dur   = scene.get("duration", "")
                                cam   = scene.get("camera", "")
                                mdia  = scene.get("mahwous_dialogue", "")
                                bdia  = scene.get("bottle_dialogue", "")
                                vis   = scene.get("visual", "")

                                st.markdown(f"""
                                <div class="scene-card-char">
                                  <div style="display:flex; align-items:center; gap:0.4rem; margin-bottom:0.4rem;">
                                    <span class="scene-num-char">{num}</span>
                                    <span style="color:#D4AF37; font-weight:800; font-size:0.85rem;">{typ}</span>
                                    <span style="color:#555; font-size:0.73rem;">⏱ {dur} | 📷 {cam}</span>
                                  </div>
                                  <div style="color:#A09070; font-size:0.78rem; margin-bottom:0.35rem;">🎭 {vis}</div>
                                  {"<div style='background:rgba(212,175,55,0.05);border-right:2px solid #D4AF37;padding:0.3rem 0.6rem;border-radius:0.3rem;margin:0.25rem 0;'><span style='color:#D4AF37;font-size:0.7rem;'>مهووس: </span><em style='color:#F0E0C0;font-size:0.82rem;'>\"" + mdia + "\"</em></div>" if mdia else ""}
                                  {"<div style='background:rgba(233,69,96,0.04);border-right:2px solid #E94560;padding:0.3rem 0.6rem;border-radius:0.3rem;margin:0.25rem 0;'><span style='color:#E94560;font-size:0.7rem;'>العطر: </span><em style='color:#FFD0C0;font-size:0.82rem;'>\"" + bdia + "\"</em></div>" if bdia else ""}
                                </div>""", unsafe_allow_html=True)

                                if scene.get("google_flow_prompt"):
                                    with st.expander(f"📋 برومت Google Flow — اللقطة {num}"):
                                        st.code(scene["google_flow_prompt"], language="text")

                            # Export
                            text = f"# {scenario.get('title')}\n"
                            for sc in scenario.get("scenes", []):
                                text += f"\n━━ اللقطة {sc.get('number')}: {sc.get('type')} · {sc.get('duration')} ━━\n"
                                text += f"📷 {sc.get('camera')}\n🎭 {sc.get('visual')}\n"
                                if sc.get("mahwous_dialogue"):
                                    text += f'مهووس: "{sc["mahwous_dialogue"]}"\n'
                                if sc.get("bottle_dialogue"):
                                    text += f'العطر: "{sc["bottle_dialogue"]}"\n'
                            st.download_button("📄 تحميل السيناريو", text,
                                               file_name=f"scenario_{ai_name.replace(' ','_')}.txt",
                                               mime="text/plain", use_container_width=True)
                        else:
                            st.error("فشل توليد السيناريو — أعد المحاولة")
                    except Exception as e:
                        st.error(f"❌ خطأ: {e}")

        with lib_col:
            st.markdown("##### اختر سيناريو جاهزاً من المكتبة")
            perfume_sc = st.text_input("🌹 اسم العطر للسيناريو", "Chopard Oud Malaki", key="lib_perf")
            sc_type = st.radio("نوع السيناريو", [
                "👑 سر الملك (15 ث)",
                "⚔️ التحدي (16 ث)",
                "💬 الحوار الكلاسيكي (14 ث)",
                "📖 قصة التحول (21 ث)"
            ], horizontal=True)

            # Build scene data based on selection
            if "👑" in sc_type:
                scenes_data = [
                    (1,"4 ث","الهوك","Wide Track","مهووس يبحث في الرفوف، يتوقف على الزجاجة بهالة ذهبية","ظننت أني أعرف كل ملوك العطور...","مهووس"),
                    (2,"4 ث","الكشف","Medium CU","مهووس يمسك الزجاجة — تفتح عينيها ببطء وثقة","...من أنت؟","مهووس"),
                    (3,"4 ث","ذروة","ECU Bottle",f"وجه الزجاجة يتكلم بهدوء وفخامة — مهووس في الخلف بفم مغلق تماماً","الملك لا يُعرف بعرشه... بل بحضوره.","العطر"),
                    (4,"3 ث","خاتمة","Medium Reveal",f"مهووس يبتسم ابتسامة الخبير ويرفع الزجاجة نحو الكاميرا ويغمز",f"{perfume_sc}. الحضور الذي لا يغيب.","مهووس"),
                ]
            elif "⚔️" in sc_type:
                scenes_data = [
                    (1,"5 ث","الهوك","Medium Static","مهووس يشم عطوراً متعددة بوجه ملول ويهز رأسه بخيبة","كل العطور... صارت نفس الشيء.","مهووس"),
                    (2,"3 ث","انقلاب","Smash Cut CU","يمسك العطر — تحول لوني درامي. عيناه تتسعان بدهشة","🎵 whoosh + موسيقى تصاعد","مؤثر"),
                    (3,"8 ث","ذروة+خاتمة","Push In","مهووس يرفع الزجاجة للكاميرا بحماس. مكونات العطر تطير حوله",f"إلا هذا! {perfume_sc}... هذا مو عطر عادي — هذا تجربة!","مهووس"),
                ]
            elif "💬" in sc_type:
                scenes_data = [
                    (1,"7 ث","مهووس يبادر","Medium Shot","يمسك العطر بيديه ويخاطبه مباشرة. الزجاجة ساكنة تستمع","أنت تختلف... أشعر بشيء مختلف فيك.","مهووس"),
                    (2,"7 ث","العطر يرد","ECU Bottle","وجه الزجاجة يتكلم بهدوء ملكي. مهووس في الخلف بفم مغلق تماماً","الملك لا يُعرف بعرشه، بل بحضوره.","العطر"),
                ]
            else:  # القصة
                scenes_data = [
                    (1,"7 ث","القبل","Environment Shot","مهووس في موقف عادي — يبدو غير مكتمل","كنت أبحث عن شيء... لا أعرف ما هو.","مهووس"),
                    (2,"7 ث","لحظة الاكتشاف","CU Color Shift","لحظة إمساك العطر — تحول لوني من بارد لذهبي دافئ. موسيقى","🎵 إيقاع عاطفي يصل إلى ذروته","موسيقى"),
                    (3,"7 ث","التحول","Confident Medium",f"مهووس الجديد — واثق، حاضر، مكتمل. يرفع {perfume_sc}",f"بفضل {perfume_sc}... وجدته.","مهووس"),
                ]

            # Display scenes
            for num, dur, sc_t, cam, desc, audio, speaker in scenes_data:
                color = "#D4AF37" if speaker == "مهووس" else "#E94560" if speaker == "العطر" else "#60A5FA"
                st.markdown(f"""
                <div class="scene-card-char">
                  <div style="display:flex; align-items:center; gap:0.4rem; margin-bottom:0.4rem;">
                    <span class="scene-num-char">{num}</span>
                    <span style="color:#D4AF37; font-weight:800; font-size:0.85rem;">{sc_t}</span>
                    <span style="color:#555; font-size:0.73rem;">⏱ {dur} | 📷 {cam}</span>
                  </div>
                  <p style="color:#A09070; font-size:0.8rem; margin:0 0 0.35rem;">{desc}</p>
                  <div style="background:rgba(212,175,55,0.04); border-right:2px solid {color}; padding:0.35rem 0.65rem; border-radius:0.3rem;">
                    <span style="color:{color}; font-size:0.72rem; font-weight:700;">{speaker}: </span>
                    <em style="color:#F0E0C0; font-size:0.83rem;">"{audio}"</em>
                  </div>
                </div>""", unsafe_allow_html=True)

            # Export library scenario
            if st.button("📄 تصدير السيناريو", use_container_width=True, key="export_lib"):
                text = f"# سيناريو: {sc_type.split('(')[0].strip()} | العطر: {perfume_sc}\n\n"
                for num, dur, sc_t, cam, desc, audio, speaker in scenes_data:
                    text += f"━━━ اللقطة {num}: {sc_t} · {dur} ━━━\n📷 {cam}\n🎭 {desc}\n🎙️ {speaker}: \"{audio}\"\n\n"
                st.code(text, language="text")

        # Bottle Replies Library
        st.markdown("---")
        st.markdown("### 💬 مكتبة ردود العطر الجاهزة")
        cats = {"oud":"🔥 عطور العود","western":"💎 العطور الغربية","summer":"🌊 عطور الصيف","winter":"❄️ عطور الشتاء"}
        for cat, label in cats.items():
            with st.expander(label):
                for reply in BOTTLE_REPLIES[cat]:
                    st.markdown(f'<div class="reply-card">❝ {reply} ❞</div>', unsafe_allow_html=True)

    # ═══ TAB 4: ERROR FIXES ═══
    with tab4:
        st.markdown("### 🔧 حل الأخطاء الشائعة فوراً")
        st.caption("وجدت مشكلة في صورة أو فيديو؟ انقر على المشكلة وانسخ الحل وأضفه لبرومتك")

        for key, (problem, fix) in RULES_BROKEN_FIXES.items():
            with st.expander(problem):
                st.markdown("**✅ أضف هذا النص في برومتك:**")
                st.code(fix, language="text")
                st.caption("انسخ النص أعلاه وأضفه في نهاية برومتك، ثم أعد التوليد")

        st.markdown("---")
        st.markdown("### 🏆 أفضل الممارسات للجودة القصوى")
        tips = [
            ("📷", "ارفع صورتين دائماً",  "mahwous_character.png + صورة العطر الأصلية كـ Reference"),
            ("🎨", "DNA أولاً",             "ابدأ كل برومت بـ MAHWOUS_DNA الكامل بدون اختصار"),
            ("🌟", "التفاصيل مهمة",        "صف الزجاجة بدقة: الشكل + المواد + الألوان + التفاصيل الفريدة"),
            ("💡", "الإضاءة الذهبية",       "دائماً اذكر: warm golden amber cinematic 3-point lighting"),
            ("🎬", "حركة الكاميرا",         "حدد حركة الكاميرا لكل مشهد — slow push-in أفضل للعطور"),
            ("✂️", "أقل هو أكثر",           "برومت واضح ومنظم يفوق برومت طويل فوضوي"),
        ]
        for icon, title, detail in tips:
            st.markdown(f"""
            <div style='background:#080500; border:1px solid rgba(212,175,55,0.12); border-radius:0.6rem;
                 padding:0.75rem; margin-bottom:0.4rem; display:flex; gap:0.8rem; align-items:flex-start;'>
              <span style='font-size:1.3rem; flex-shrink:0;'>{icon}</span>
              <div>
                <div style='color:#D4AF37; font-weight:800; font-size:0.85rem;'>{title}</div>
                <div style='color:#806040; font-size:0.78rem; margin-top:0.15rem;'>{detail}</div>
              </div>
            </div>""", unsafe_allow_html=True)
