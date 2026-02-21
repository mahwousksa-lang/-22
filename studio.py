"""
🎬 استديو مهووس الذكي v10.0
الواجهة الرئيسية - توليد المحتوى لجميع المنصات
"""

import streamlit as st
import base64
import json
import io
from datetime import datetime
from PIL import Image

from modules.ai_engine import (
    analyze_perfume_image, generate_platform_images,
    generate_all_captions, generate_descriptions,
    generate_hashtags, generate_scenario, generate_video_luma,
    send_to_make, PLATFORMS, MAHWOUS_OUTFITS, _get_secrets
)

# ─── CSS المتخصص للاستديو ──────────────────────────────────────────────────
STUDIO_CSS = """
<style>
.studio-hero {
    background: linear-gradient(135deg, #0A0600 0%, #1A0E00 40%, #0F0800 100%);
    border: 1px solid rgba(212,175,55,0.4);
    border-radius: 1.25rem; padding: 2.5rem; text-align: center;
    margin-bottom: 2rem; position: relative; overflow: hidden;
}
.studio-hero::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse 70% 60% at 50% 40%, rgba(212,175,55,0.07) 0%, transparent 70%);
}
.studio-hero h1 { color: #D4AF37; font-size: 2.2rem; margin: 0; position: relative; }
.studio-hero p  { color: #806040; margin: 0.4rem 0 0; font-size: 0.9rem; position: relative; }

.platform-card {
    background: #0F0900; border: 1px solid rgba(212,175,55,0.15);
    border-radius: 0.75rem; padding: 1rem; text-align: center;
    cursor: pointer; transition: all 0.25s;
    user-select: none;
}
.platform-card:hover { border-color: rgba(212,175,55,0.5); background: rgba(212,175,55,0.05); }
.platform-card.selected { border-color: #D4AF37; background: rgba(212,175,55,0.1);
    box-shadow: 0 0 15px rgba(212,175,55,0.15); }
.platform-emoji { font-size: 1.8rem; display: block; margin-bottom: 0.3rem; }
.platform-name { color: #D4AF37; font-size: 0.8rem; font-weight: 700; }
.platform-size { color: #806040; font-size: 0.7rem; margin-top: 0.2rem; }

.result-image-card {
    background: #0A0600; border: 1px solid rgba(212,175,55,0.2);
    border-radius: 0.75rem; overflow: hidden; transition: border-color 0.25s;
}
.result-image-card:hover { border-color: rgba(212,175,55,0.5); }
.result-image-header {
    background: rgba(212,175,55,0.08); padding: 0.5rem 0.75rem;
    display: flex; justify-content: space-between; align-items: center;
    border-bottom: 1px solid rgba(212,175,55,0.15);
}
.result-image-title { color: #D4AF37; font-size: 0.8rem; font-weight: 700; }
.result-size-badge { color: #806040; font-size: 0.7rem; }

.caption-box {
    background: #0A0600; border: 1px solid rgba(212,175,55,0.2);
    border-radius: 0.75rem; padding: 1rem; margin-bottom: 0.75rem;
}
.caption-header {
    color: #D4AF37; font-size: 0.85rem; font-weight: 700;
    margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.4rem;
}

.scenario-scene {
    background: #0A0600; border-right: 3px solid #D4AF37;
    border-radius: 0.5rem; padding: 1rem; margin-bottom: 0.75rem;
}
.scene-num-badge {
    display: inline-flex; align-items: center; justify-content: center;
    background: #D4AF37; color: #000; width: 1.6rem; height: 1.6rem;
    border-radius: 50%; font-weight: 900; font-size: 0.8rem; margin-left: 0.5rem;
}

.step-badge {
    display: inline-block; background: rgba(212,175,55,0.15);
    border: 1px solid rgba(212,175,55,0.3); color: #D4AF37;
    padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.75rem; font-weight: 700;
}

.flow-prompt-box {
    background: #050300; border: 1px solid rgba(212,175,55,0.3);
    border-radius: 0.5rem; padding: 0.75rem; margin-top: 0.5rem;
    font-family: 'Courier New', monospace; font-size: 0.75rem;
    color: #A8C870; line-height: 1.7; direction: ltr; text-align: left;
    white-space: pre-wrap;
}

.progress-steps {
    display: flex; gap: 0.5rem; flex-wrap: wrap;
    margin-bottom: 1rem;
}
.progress-step {
    display: flex; align-items: center; gap: 0.3rem;
    padding: 0.3rem 0.7rem; border-radius: 999px;
    font-size: 0.75rem; font-weight: 600;
}
.step-done { background: rgba(52,211,153,0.15); color: #34d399; border: 1px solid rgba(52,211,153,0.3); }
.step-active { background: rgba(212,175,55,0.2); color: #D4AF37; border: 1px solid rgba(212,175,55,0.4); animation: pulse 1.5s infinite; }
.step-pending { background: rgba(255,255,255,0.03); color: #555; border: 1px solid rgba(255,255,255,0.08); }

@keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.6; } }
</style>
"""


# ─── Platform Selector Component ──────────────────────────────────────────
def platform_selector():
    """مكوّن اختيار المنصات"""
    if "selected_platforms" not in st.session_state:
        st.session_state.selected_platforms = ["instagram_post", "instagram_story", "tiktok", "twitter"]

    st.markdown("#### 📱 اختر المنصات")

    # Group platforms
    groups = {
        "📱 عمودي (9:16)": ["instagram_story", "tiktok", "youtube_short", "snapchat"],
        "🖼️ مربع (1:1)":   ["instagram_post"],
        "🖥️ أفقي (16:9)":  ["twitter", "youtube_thumb", "facebook", "linkedin"],
        "📌 آخرى":          ["pinterest"],
    }

    # Select All / Clear
    c1, c2 = st.columns(2)
    if c1.button("✅ تحديد الكل", use_container_width=True, key="sel_all"):
        st.session_state.selected_platforms = list(PLATFORMS.keys())
        st.rerun()
    if c2.button("🗑️ مسح الكل", use_container_width=True, key="clr_all"):
        st.session_state.selected_platforms = []
        st.rerun()

    for group_name, plat_keys in groups.items():
        st.markdown(f"<div style='color:#806040; font-size:0.75rem; margin:0.5rem 0 0.3rem; font-weight:700;'>{group_name}</div>", unsafe_allow_html=True)
        cols = st.columns(len(plat_keys))
        for col, key in zip(cols, plat_keys):
            plat = PLATFORMS[key]
            is_sel = key in st.session_state.selected_platforms
            with col:
                if st.checkbox(
                    f"{plat['emoji']} {plat['label'].split(' ', 1)[-1]}\n{plat['w']}×{plat['h']}",
                    value=is_sel, key=f"plat_{key}"
                ):
                    if key not in st.session_state.selected_platforms:
                        st.session_state.selected_platforms.append(key)
                else:
                    if key in st.session_state.selected_platforms:
                        st.session_state.selected_platforms.remove(key)

    sel_count = len(st.session_state.selected_platforms)
    st.markdown(f"<div class='step-badge'>✅ {sel_count} منصة مختارة</div>", unsafe_allow_html=True)
    return st.session_state.selected_platforms


# ─── Results Display ───────────────────────────────────────────────────────
def display_images(images: dict):
    """عرض الصور المولّدة"""
    if not images:
        return
    st.markdown("### 🖼️ الصور المولّدة")

    # Group by aspect ratio
    vertical = {k: v for k, v in images.items() if v.get("aspect") == "9:16" and v.get("bytes")}
    square   = {k: v for k, v in images.items() if v.get("aspect") == "1:1" and v.get("bytes")}
    horiz    = {k: v for k, v in images.items() if v.get("aspect") in ("16:9", "4:3") and v.get("bytes")}
    other    = {k: v for k, v in images.items() if v.get("aspect") == "2:3" and v.get("bytes")}

    for group_name, group in [
        ("📱 عمودي (9:16)", vertical),
        ("🖼️ مربع (1:1)", square),
        ("🖥️ أفقي (16:9)", horiz),
        ("📌 آخرى", other),
    ]:
        if not group:
            continue
        st.markdown(f"<div style='color:#806040; font-size:0.8rem; font-weight:700; margin:1rem 0 0.5rem'>{group_name}</div>", unsafe_allow_html=True)
        cols = st.columns(min(len(group), 3))
        for i, (key, data) in enumerate(group.items()):
            with cols[i % 3]:
                st.markdown(f"<div style='color:#D4AF37; font-size:0.8rem; margin-bottom:0.3rem'>{data['emoji']} {data['label']}</div>", unsafe_allow_html=True)
                st.image(data["bytes"], use_container_width=True)
                st.download_button(
                    f"💾 تحميل",
                    data["bytes"],
                    file_name=f"mahwous_{key}_{datetime.now().strftime('%H%M%S')}.jpg",
                    mime="image/jpeg",
                    key=f"dl_{key}_{i}",
                    use_container_width=True
                )

    # Show failures
    failed = {k: v for k, v in images.items() if not v.get("bytes")}
    if failed:
        with st.expander(f"⚠️ {len(failed)} منصة لم تُولَّد"):
            for k in failed:
                st.warning(f"❌ {PLATFORMS[k]['label']} - تحقق من Gemini API Key")


def display_captions(captions: dict):
    """عرض الـ Captions"""
    if not captions or "error" in captions:
        return
    st.markdown("### 📱 Captions المنصات")

    platform_map = {
        "instagram_post":  ("📸", "Instagram Post"),
        "instagram_story": ("📱", "Instagram Story"),
        "tiktok":          ("🎵", "TikTok"),
        "youtube_short":   ("▶️", "YouTube Short"),
        "youtube_thumb":   ("🎬", "YouTube Thumbnail"),
        "twitter":         ("🐦", "Twitter/X"),
        "facebook":        ("👍", "Facebook"),
        "snapchat":        ("👻", "Snapchat"),
        "linkedin":        ("💼", "LinkedIn"),
        "pinterest":       ("📌", "Pinterest"),
        "whatsapp":        ("💬", "WhatsApp"),
        "telegram":        ("✈️", "Telegram"),
    }

    for key, (emoji, name) in platform_map.items():
        if key not in captions:
            continue
        cap_data = captions[key]
        with st.expander(f"{emoji} {name}"):
            if isinstance(cap_data, dict):
                if "caption" in cap_data:
                    st.text_area("Caption", cap_data["caption"], height=130, key=f"cap_{key}")
                if "title" in cap_data:
                    st.text_input("العنوان", cap_data["title"], key=f"title_{key}")
                if "description" in cap_data:
                    st.text_area("الوصف", cap_data["description"], height=100, key=f"desc_cap_{key}")
                if "hashtags" in cap_data and cap_data["hashtags"]:
                    st.code(" ".join(cap_data["hashtags"]), language=None)
            else:
                st.text_area("", str(cap_data), height=130, key=f"cap_{key}_str")


def display_scenario(scenario: dict):
    """عرض السيناريو"""
    if not scenario or "scenes" not in scenario:
        return
    st.markdown("### 🎬 سيناريو الفيديو")
    st.markdown(f"**{scenario.get('title', '')}** | ⏱️ {scenario.get('total_duration', '')} ثانية")

    for scene in scenario.get("scenes", []):
        with st.expander(f"{'◆ ' if scene.get('type') == 'ذروة' else ''}اللقطة {scene.get('number')} · {scene.get('type')} · {scene.get('duration')} ث"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**📷 الكاميرا:** {scene.get('camera', '')}")
                st.markdown(f"**🎭 المشهد:** {scene.get('visual', '')}")
                st.markdown(f"**🎭 مهووس:** {scene.get('mahwous_action', '')}")
            with c2:
                st.markdown(f"**🎙️ مهووس يقول:** _{scene.get('mahwous_dialogue', '')}_")
                if scene.get('bottle_dialogue'):
                    st.markdown(f"**🔊 العطر يقول:** _{scene.get('bottle_dialogue', '')}_")
                st.markdown(f"**🎵 موسيقى:** {scene.get('music', '')}")

            # Google Flow Prompt
            if scene.get("google_flow_prompt"):
                st.markdown("**برومت Google Flow الجاهز:**")
                st.code(scene["google_flow_prompt"], language="text")

    # Outro
    if scenario.get("outro"):
        st.info(f"🎬 الخاتمة: {scenario['outro']}")


# ─── Main Studio Page ──────────────────────────────────────────────────────
def show_studio_page():
    st.markdown(STUDIO_CSS, unsafe_allow_html=True)

    st.markdown("""
    <div class="studio-hero">
      <h1>🎬 استديو مهووس الذكي</h1>
      <p>v10.0 · توليد صور وفيديو ومحتوى لجميع منصات التواصل الاجتماعي · بشخصية مهووس الثابتة</p>
    </div>
    """, unsafe_allow_html=True)

    # Check API Status
    secrets = _get_secrets()
    has_gemini = bool(secrets["gemini"])
    has_openrouter = bool(secrets["openrouter"])

    if not has_gemini:
        st.warning("⚠️ أضف GEMINI_API_KEY في Secrets لتوليد الصور")
    if not has_openrouter:
        st.warning("⚠️ أضف OPENROUTER_API_KEY في Secrets لتوليد النصوص")

    st.markdown("---")

    # ─── STEP 1: Upload Perfume Image ─────────────────────────────────────
    st.markdown('<span class="step-badge">الخطوة 1</span> **رفع صورة العطر**', unsafe_allow_html=True)

    col_img, col_char = st.columns([1, 1])

    with col_img:
        uploaded = st.file_uploader(
            "📸 ارفع صورة العطر (JPG/PNG/WEBP)",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed",
            key="perfume_upload"
        )
        if uploaded:
            st.image(uploaded, use_container_width=True)
            if "perfume_info" not in st.session_state:
                st.session_state.perfume_info = None

    with col_char:
        st.markdown("**👤 إعدادات شخصية مهووس**")

        # Character Reference Upload
        char_img = st.file_uploader(
            "ارفع صورة مرجعية لمهووس (اختياري)",
            type=["jpg", "jpeg", "png"],
            key="char_upload",
            help="صورة mahwous_character.png للحفاظ على ثبات الشخصية"
        )
        if char_img:
            st.image(char_img, caption="مرجع مهووس ✅", use_container_width=True)
            st.session_state.char_reference = char_img.getvalue()
            st.success("✅ تم حفظ صورة مهووس المرجعية")

        outfit_choice = st.selectbox(
            "👔 زي مهووس",
            options=list(MAHWOUS_OUTFITS.keys()),
            format_func=lambda k: {"suit": "🤵 البدلة الفاخرة", "hoodie": "🏆 الهودي الأيقوني",
                                    "thobe": "👘 الثوب الملكي", "casual": "👕 الكاجوال"}[k]
        )
        scene_choice = st.selectbox(
            "🎭 مكان المشهد",
            options=["store", "beach", "desert", "studio", "garden"],
            format_func=lambda k: {"store": "🏪 متجر العطور", "beach": "🌅 شاطئ غروب",
                                    "desert": "🏜️ صحراء ذهبية", "studio": "🎬 استديو فاخر",
                                    "garden": "🌹 حديقة ملكية"}[k]
        )
        include_char = st.toggle("🧑 تضمين شخصية مهووس في الصور", value=True)

    if not uploaded:
        _show_how_it_works()
        return

    st.markdown("---")

    # ─── STEP 2: Select Platforms ──────────────────────────────────────────
    st.markdown('<span class="step-badge">الخطوة 2</span> **اختر المنصات والمحتوى**', unsafe_allow_html=True)

    col_plat, col_opts = st.columns([3, 2])

    with col_plat:
        selected_platforms = platform_selector()

    with col_opts:
        st.markdown("**📦 خيارات المحتوى**")
        opt_images   = st.checkbox("🖼️ توليد صور لكل منصة", value=True)
        opt_captions = st.checkbox("📝 توليد Captions لكل منصة", value=True)
        opt_desc     = st.checkbox("📄 توليد 5 أوصاف", value=True)
        opt_hashtags = st.checkbox("🏷️ توليد 40 هاشتاق", value=True)
        opt_scenario = st.checkbox("🎬 توليد سيناريو فيديو", value=False)
        opt_video    = st.checkbox("🎥 توليد فيديو (Luma AI)", value=False)
        opt_publish  = st.checkbox("🚀 نشر تلقائي (Make.com)", value=False)

        if opt_scenario:
            scenario_type = st.selectbox("نوع السيناريو", [
                "dialogue", "story", "challenge", "review"
            ], format_func=lambda k: {
                "dialogue": "💬 حوار مهووس والعطر",
                "story": "📖 قصة قصيرة 3 مشاهد",
                "challenge": "⚔️ مشهد الاكتشاف",
                "review": "⭐ مراجعة احترافية"
            }[k])
        else:
            scenario_type = "dialogue"

    st.markdown("---")

    # ─── STEP 3: Generate ─────────────────────────────────────────────────
    btn_label = f"🚀 ابدأ التوليد ({len(selected_platforms)} منصة)"
    if st.button(btn_label, type="primary", use_container_width=True, disabled=not selected_platforms):

        image_bytes = uploaded.getvalue()
        all_results = {}

        # Progress tracking
        progress_bar = st.progress(0)
        status_text  = st.empty()

        # === Step 1: Analyze image ===
        status_text.markdown("🔍 **تحليل صورة العطر...**")
        progress_bar.progress(5)
        try:
            if has_gemini:
                info = analyze_perfume_image(image_bytes)
            else:
                # Fallback: manual info
                info = {
                    "product_name": "عطر مهووس",
                    "brand": "Mahwous",
                    "type": "EDP",
                    "size": "100ml",
                    "colors": ["gold", "black"],
                    "bottle_shape": "elegant luxury bottle",
                    "style": "luxury",
                    "gender": "unisex",
                    "mood": "فاخر"
                }
            st.session_state.perfume_info = info
            status_text.markdown(f"✅ **تم تحليل:** {info.get('product_name')} - {info.get('brand')}")
        except Exception as e:
            st.error(f"❌ فشل تحليل الصورة: {e}")
            return

        # === Step 2: Generate Captions ===
        if opt_captions:
            progress_bar.progress(20)
            status_text.markdown("📝 **توليد Captions لجميع المنصات...**")
            try:
                all_results["captions"] = generate_all_captions(info)
                status_text.markdown("✅ **Captions لـ 12 منصة!**")
            except Exception as e:
                st.warning(f"⚠️ فشل توليد Captions: {e}")

        # === Step 3: Generate Descriptions ===
        if opt_desc:
            progress_bar.progress(30)
            status_text.markdown("📄 **توليد الأوصاف...**")
            try:
                all_results["descriptions"] = generate_descriptions(info)
            except Exception as e:
                st.warning(f"⚠️ فشل توليد الأوصاف: {e}")

        # === Step 4: Generate Hashtags ===
        if opt_hashtags:
            progress_bar.progress(35)
            status_text.markdown("🏷️ **توليد الهاشتاقات...**")
            try:
                all_results["hashtags"] = generate_hashtags(info)
            except Exception as e:
                st.warning(f"⚠️ فشل توليد الهاشتاقات: {e}")

        # === Step 5: Generate Scenario ===
        if opt_scenario:
            progress_bar.progress(40)
            status_text.markdown("🎬 **توليد سيناريو الفيديو...**")
            try:
                all_results["scenario"] = generate_scenario(info, scenario_type)
            except Exception as e:
                st.warning(f"⚠️ فشل توليد السيناريو: {e}")

        # === Step 6: Generate Images ===
        if opt_images and has_gemini and selected_platforms:
            progress_bar.progress(45)
            status_text.markdown(f"🖼️ **توليد صور لـ {len(selected_platforms)} منصة...**")

            def img_progress(pct, msg):
                progress_bar.progress(int(45 + pct * 40))
                status_text.markdown(f"🖼️ **{msg}**")

            try:
                all_results["images"] = generate_platform_images(
                    info, selected_platforms, outfit_choice, scene_choice,
                    include_char, img_progress
                )
            except Exception as e:
                st.warning(f"⚠️ فشل توليد الصور: {e}")

        # === Step 7: Generate Video ===
        if opt_video:
            progress_bar.progress(86)
            status_text.markdown("🎥 **توليد الفيديو (3-5 دقائق)...**")
            try:
                vid_aspect = "9:16" if "tiktok" in selected_platforms or "instagram_story" in selected_platforms else "16:9"
                all_results["video"] = generate_video_luma(info, vid_aspect)
                if "url" in all_results["video"]:
                    status_text.markdown("✅ **تم توليد الفيديو!**")
                else:
                    st.warning(f"⚠️ {all_results['video'].get('error', 'فشل الفيديو')}")
            except Exception as e:
                st.warning(f"⚠️ فشل توليد الفيديو: {e}")

        # === Step 8: Publish ===
        if opt_publish:
            progress_bar.progress(95)
            status_text.markdown("📡 **إرسال إلى Make.com...**")
            make_payload = {
                **info,
                "captions": all_results.get("captions", {}),
                "descriptions": all_results.get("descriptions", {}),
                "hashtags": all_results.get("hashtags", {}),
                "video_url": all_results.get("video", {}).get("url", ""),
                "platforms_generated": selected_platforms,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source": "mahwous_studio_v10"
            }
            if send_to_make(make_payload):
                st.success("✅ تم الإرسال إلى Make.com!")
            else:
                st.warning("⚠️ فشل الإرسال - تحقق من Webhook URL")

        progress_bar.progress(100)
        status_text.markdown("✅ **اكتمل التوليد!**")

        # ═══ Display Results ═══
        _display_all_results(all_results, info)


def _display_all_results(results: dict, info: dict):
    """عرض جميع النتائج"""
    st.markdown("---")
    st.markdown("## 📦 نتائج التوليد")

    # ─── Product Info ───
    with st.expander("🧴 معلومات العطر المكتشفة", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("العطر", info.get("product_name", "—"))
        c2.metric("العلامة", info.get("brand", "—"))
        c3.metric("النوع", info.get("type", "—"))
        c4.metric("الجنس", info.get("gender", "—"))
        st.json(info)

    # ─── Images ───
    if "images" in results:
        display_images(results["images"])

    # ─── Video ───
    if "video" in results and results["video"].get("url"):
        st.markdown("### 🎥 الفيديو المولّد")
        st.video(results["video"]["url"])

    # ─── Scenario ───
    if "scenario" in results:
        display_scenario(results["scenario"])

    # ─── Captions ───
    if "captions" in results:
        display_captions(results["captions"])

    # ─── Descriptions ───
    if "descriptions" in results and results["descriptions"]:
        desc = results["descriptions"]
        st.markdown("### 📄 الأوصاف")
        tabs = st.tabs(["قصير", "متوسط", "طويل", "إعلاني", "SEO"])
        for tab, (key, label) in zip(tabs, [
            ("short","قصير"), ("medium","متوسط"), ("long","طويل"), ("ad","إعلاني"), ("seo","SEO")
        ]):
            with tab:
                if key == "seo" and isinstance(desc.get("seo"), dict):
                    seo = desc["seo"]
                    st.text_input("العنوان", seo.get("title",""), key="seo_t")
                    st.text_area("الميتا", seo.get("meta",""), height=80, key="seo_m")
                    st.text_area("المحتوى", seo.get("content",""), height=150, key="seo_c")
                    if seo.get("keywords"):
                        st.code(" · ".join(seo["keywords"]))
                else:
                    st.text_area("", desc.get(key,""), height=180, key=f"d_{key}")

    # ─── Hashtags ───
    if "hashtags" in results and results["hashtags"]:
        ht = results["hashtags"]
        st.markdown("### 🏷️ الهاشتاقات")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**🇸🇦 عربي (20)**")
            st.code(" ".join(ht.get("arabic", [])))
        with c2:
            st.markdown("**🌍 إنجليزي (20)**")
            st.code(" ".join(ht.get("english", [])))
        with c3:
            st.markdown("**🔥 ترندينج**")
            st.code(" ".join(ht.get("trending", [])))

    # ─── Download All JSON ───
    st.markdown("---")
    full_export = {
        "product": info,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "captions": results.get("captions", {}),
        "descriptions": results.get("descriptions", {}),
        "hashtags": results.get("hashtags", {}),
        "scenario": results.get("scenario", {}),
        "video_url": results.get("video", {}).get("url", ""),
    }
    brand = info.get("brand", "brand").replace(" ", "_")
    st.download_button(
        "📥 تحميل كل المحتوى (JSON)",
        json.dumps(full_export, ensure_ascii=False, indent=2),
        file_name=f"mahwous_{brand}_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
        mime="application/json",
        use_container_width=True
    )


def _show_how_it_works():
    """عرض كيف يعمل النظام"""
    st.markdown("---")
    cols = st.columns(5)
    steps = [
        ("📸", "ارفع صورة العطر"),
        ("🔍", "تحليل ذكي تلقائي"),
        ("🎨", "توليد صور لكل منصة"),
        ("✍️", "Captions + سيناريو"),
        ("🚀", "نشر تلقائي"),
    ]
    for col, (icon, title) in zip(cols, steps):
        col.markdown(f"""
        <div style='text-align:center; padding:1rem; background:rgba(212,175,55,0.05);
             border:1px solid rgba(212,175,55,0.15); border-radius:0.75rem;'>
          <div style='font-size:2rem'>{icon}</div>
          <div style='color:#D4AF37; font-size:0.82rem; font-weight:700; margin-top:0.4rem'>{title}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; color:#806040; font-size:0.85rem; padding:1rem;'>
      ⬆️ <strong style='color:#D4AF37'>ارفع صورة العطر للبدء</strong>
    </div>
    """, unsafe_allow_html=True)
