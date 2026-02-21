"""
🎬 استديو مهووس الذكي v11.0
واجهة رئيسية محسّنة — أعلى معايير الجودة والدقة
"""

import streamlit as st
import base64
import json
import io
import zipfile
from datetime import datetime
from PIL import Image

from modules.ai_engine import (
    analyze_perfume_image, generate_platform_images,
    generate_all_captions, generate_descriptions,
    generate_hashtags, generate_scenario,
    generate_video_luma, send_to_make,
    generate_perfume_story, build_manual_info,
    PLATFORMS, MAHWOUS_OUTFITS, _get_secrets
)

# ─── Studio CSS ────────────────────────────────────────────────────────────────
STUDIO_CSS = """
<style>
.studio-hero {
    background: linear-gradient(135deg, #1A0E02 0%, #2A1A06 50%, #1A0E02 100%);
    border: 2px solid rgba(212,175,55,0.60);
    border-radius: 1.3rem; padding: 2.8rem 2rem; text-align: center;
    margin-bottom: 2rem; position: relative; overflow: hidden;
}
.studio-hero::before {
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(ellipse 80% 55% at 50% 40%, rgba(212,175,55,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.studio-hero h1 { color: #FFE060; font-size: 2.4rem; margin: 0; position: relative; letter-spacing: -0.01em; font-weight: 900; }
.studio-hero .sub { color: #F0C870; margin: 0.5rem 0 0; font-size: 0.95rem; position: relative; font-weight: 700; }
.studio-hero .version-badge {
    display: inline-block; background: rgba(212,175,55,0.20); border: 1.5px solid rgba(212,175,55,0.55);
    color: #FFE060; padding: 0.25rem 1rem; border-radius: 999px; font-size: 0.75rem; font-weight: 900;
    letter-spacing: 0.08rem; margin-top: 0.8rem; position: relative;
}

.mode-card {
    background: #130D04; border: 2px solid rgba(212,175,55,0.25);
    border-radius: 1rem; padding: 1.6rem; text-align: center; cursor: pointer;
    transition: all 0.25s; position: relative; overflow: hidden;
}
.mode-card:hover, .mode-card.active {
    border-color: #F0CC55; background: rgba(212,175,55,0.08);
    box-shadow: 0 0 24px rgba(212,175,55,0.15);
}
.mode-card .icon { font-size: 2.4rem; display: block; margin-bottom: 0.6rem; }
.mode-card .title { color: #FFE060; font-size: 1.05rem; font-weight: 900; }
.mode-card .desc { color: #E0B870; font-size: 0.85rem; margin-top: 0.35rem; line-height: 1.5; font-weight: 600; }

.analysis-card {
    background: linear-gradient(135deg, #1E1006, #281808);
    border: 2px solid rgba(212,175,55,0.50); border-radius: 1rem; padding: 1.4rem;
}
.analysis-card .brand { color: #FFE060; font-size: 1.5rem; font-weight: 900; }
.analysis-card .name { color: #FFF0D8; font-size: 1.05rem; font-weight: 800; }
.analysis-card .tag {
    display: inline-block; background: rgba(212,175,55,0.18);
    border: 1.5px solid rgba(212,175,55,0.50); color: #FFD840;
    padding: 0.2rem 0.7rem; border-radius: 999px; font-size: 0.78rem; margin: 0.15rem;
    font-weight: 800;
}
.analysis-card .color-dot {
    display: inline-block; width: 16px; height: 16px; border-radius: 50%;
    border: 1.5px solid rgba(255,255,255,0.25); margin: 0 0.2rem; vertical-align: middle;
}

.result-section {
    background: #1E1408; border: 1.5px solid rgba(212,175,55,0.35);
    border-radius: 1rem; padding: 1.6rem; margin-bottom: 1rem;
}
.result-section h3 { color: #FFE060; font-size: 1.1rem; margin: 0 0 1rem; font-weight: 900; }

.caption-block {
    background: #1A1006; border: 1.5px solid rgba(212,175,55,0.30);
    border-radius: 0.8rem; padding: 1rem; margin-bottom: 0.65rem;
}
.caption-header {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 0.5rem;
}
.caption-title { color: #FFE060; font-size: 0.9rem; font-weight: 900; }

.hashtag-pill {
    display: inline-block; background: rgba(212,175,55,0.18);
    border: 1.5px solid rgba(212,175,55,0.45); color: #FFD040;
    padding: 0.25rem 0.7rem; border-radius: 999px; font-size: 0.78rem; margin: 0.18rem;
    font-weight: 800;
}

.scene-card {
    background: #1A1206; border-right: 4px solid #FFD840;
    border-radius: 0.6rem; padding: 1rem; margin-bottom: 0.7rem;
}
.scene-num {
    display: inline-flex; align-items: center; justify-content: center;
    background: #D4AF37; color: #000; width: 1.8rem; height: 1.8rem;
    border-radius: 50%; font-weight: 900; font-size: 0.82rem; margin-left: 0.5rem;
    flex-shrink: 0;
}

.step-badge {
    display: inline-flex; align-items: center; gap: 0.5rem;
    background: rgba(212,175,55,0.20); border: 2px solid rgba(212,175,55,0.60);
    color: #FFE060; padding: 0.4rem 1.1rem; border-radius: 999px;
    font-size: 0.9rem; font-weight: 900; margin-bottom: 0.8rem;
    letter-spacing: 0.02rem;
}

.flow-prompt {
    background: #030200; border: 1px solid rgba(100,200,80,0.30);
    border-radius: 0.55rem; padding: 0.8rem; margin-top: 0.5rem;
    font-family: 'Courier New', monospace; font-size: 0.74rem;
    color: #90D860; line-height: 1.7; direction: ltr; text-align: left;
    white-space: pre-wrap; max-height: 200px; overflow-y: auto;
}

.warning-box {
    background: rgba(251,191,36,0.15); border: 2px solid rgba(251,191,36,0.65);
    border-radius: 0.7rem; padding: 0.9rem; margin-bottom: 0.6rem;
    color: #FFE880; font-size: 0.9rem; font-weight: 800;
}

.service-card {
    background: #130D04; border: 1.5px solid rgba(212,175,55,0.20);
    border-radius: 0.8rem; padding: 1rem; margin-bottom: 0.5rem;
    transition: all 0.2s;
}
.service-card:hover {
    border-color: rgba(212,175,55,0.45);
    background: rgba(212,175,55,0.06);
}

@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
.loading-bar {
    background: linear-gradient(90deg, #1E1004 25%, #4A2800 50%, #1E1004 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
    border-radius: 0.3rem; height: 4px; margin: 0.5rem 0;
}
</style>

<script>
function copyText(id) {
    var el = document.getElementById(id);
    if (el) {
        navigator.clipboard.writeText(el.innerText || el.value);
    }
}
</script>
"""


# ─── Helpers ──────────────────────────────────────────────────────────────────
def _pil_resize(img_bytes: bytes, target_w: int, target_h: int) -> bytes:
    """تغيير حجم الصورة بدقة"""
    try:
        img = Image.open(io.BytesIO(img_bytes))
        img = img.convert("RGB")
        img = img.resize((target_w, target_h), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=95, optimize=True)
        return buf.getvalue()
    except:
        return img_bytes


def _create_zip(images: dict, info: dict) -> bytes:
    """إنشاء ZIP يحتوي جميع الصور"""
    buf = io.BytesIO()
    brand = info.get("brand", "mahwous").replace(" ", "_").lower()
    ts = datetime.now().strftime("%Y%m%d_%H%M")

    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for key, data in images.items():
            if data.get("bytes"):
                resized = _pil_resize(data["bytes"], data["w"], data["h"])
                fname = f"{key}_{data['w']}x{data['h']}.jpg"
                zf.writestr(fname, resized)

        # Add metadata
        meta = {
            "brand":        info.get("brand"),
            "product_name": info.get("product_name"),
            "generated_at": datetime.now().isoformat(),
            "platforms":    list(images.keys()),
            "source":       "Mahwous AI Studio v11.0"
        }
        zf.writestr("info.json", json.dumps(meta, ensure_ascii=False, indent=2))

    buf.seek(0)
    return buf.read()


def _info_card(info: dict):
    """بطاقة معلومات العطر المحللة"""
    colors = info.get("colors", [])
    color_dots = "".join([
        f"<span class='color-dot' style='background:{c};' title='{c}'></span>"
        for c in colors[:4]
    ])
    tags_html = ""
    for tag in [info.get("type"), info.get("size"), info.get("gender"), info.get("style")]:
        if tag:
            tags_html += f"<span class='tag'>{tag}</span>"

    conf = info.get("confidence", 0)
    conf_str = f"🎯 دقة التحليل: {int(conf*100)}%" if conf else ""

    st.markdown(f"""
    <div class="analysis-card">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
                <div class="brand">{info.get('brand', '—')}</div>
                <div class="name">{info.get('product_name', '—')}</div>
                <div style="margin-top:0.5rem;">{tags_html}</div>
            </div>
            <div style="text-align:left; min-width:120px;">
                <div>{color_dots}</div>
                <div style="color:#706040; font-size:0.72rem; margin-top:0.4rem;">{conf_str}</div>
            </div>
        </div>
        <div style="margin-top:0.75rem; color:#A09070; font-size:0.8rem; line-height:1.5;">
            <strong style="color:#906030;">الزجاجة:</strong> {info.get('bottle_shape', '—')}<br>
            <strong style="color:#906030;">المزاج:</strong> {info.get('mood', '—')} · 
            <strong style="color:#906030;">الملاحظات:</strong> {info.get('notes_guess', '—')}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── Platform Selector ────────────────────────────────────────────────────────
def platform_selector() -> list:
    if "selected_platforms" not in st.session_state:
        st.session_state.selected_platforms = ["instagram_post", "instagram_story", "tiktok", "twitter"]

    groups = {
        "📱 عمودي 9:16 — قصص وريلز": ["instagram_story", "tiktok", "youtube_short", "snapchat"],
        "🖼️ مربع 1:1 — منشور إنستجرام": ["instagram_post"],
        "🖥️ أفقي 16:9 — يوتيوب وتويتر": ["twitter", "youtube_thumb", "facebook", "linkedin"],
        "📌 رأسي 2:3 — بينتريست":   ["pinterest"],
    }

    c1, c2, c3 = st.columns([1, 1, 2])
    if c1.button("✅ تحديد الكل", use_container_width=True, key="sel_all"):
        st.session_state.selected_platforms = list(PLATFORMS.keys())
        st.rerun()
    if c2.button("🗑️ مسح الكل", use_container_width=True, key="clr_all"):
        st.session_state.selected_platforms = []
        st.rerun()

    for group_name, plat_keys in groups.items():
        st.markdown(f"<div style='color:#706040; font-size:0.73rem; font-weight:700; margin:0.5rem 0 0.2rem; letter-spacing:0.05rem;'>{group_name}</div>", unsafe_allow_html=True)
        cols = st.columns(len(plat_keys))
        for col, key in zip(cols, plat_keys):
            plat = PLATFORMS[key]
            is_sel = key in st.session_state.selected_platforms
            with col:
                new_val = st.checkbox(
                    f"{plat['emoji']} {plat['label'].split(' ', 1)[-1]}\n{plat['w']}×{plat['h']}",
                    value=is_sel, key=f"plat_{key}"
                )
                if new_val and key not in st.session_state.selected_platforms:
                    st.session_state.selected_platforms.append(key)
                elif not new_val and key in st.session_state.selected_platforms:
                    st.session_state.selected_platforms.remove(key)

    sel_count = len(st.session_state.selected_platforms)
    color = "#34d399" if sel_count > 0 else "#ef4444"
    st.markdown(f"<div style='color:{color}; font-size:0.82rem; font-weight:700; margin-top:0.4rem;'>{'✅' if sel_count else '⚠️'} {sel_count} منصة مختارة</div>", unsafe_allow_html=True)
    return st.session_state.selected_platforms


# ─── Results Display ──────────────────────────────────────────────────────────
def display_images(images: dict, info: dict):
    """عرض الصور المولّدة مع تحميل ZIP"""
    if not images:
        return

    # Stats
    success = sum(1 for v in images.values() if v.get("bytes"))
    failed  = len(images) - success

    col_s, col_f, col_dl = st.columns([1, 1, 2])
    col_s.markdown(f"<div style='color:#34d399; font-size:1.3rem; font-weight:900; text-align:center;'>✅ {success}<div style='font-size:0.7rem; color:#506040;'>ناجحة</div></div>", unsafe_allow_html=True)
    col_f.markdown(f"<div style='color:{'#ef4444' if failed else '#555'}; font-size:1.3rem; font-weight:900; text-align:center;'>{'❌' if failed else '✓'} {failed}<div style='font-size:0.7rem; color:#504040;'>فاشلة</div></div>", unsafe_allow_html=True)

    # ZIP Download
    success_imgs = {k: v for k, v in images.items() if v.get("bytes")}
    if success_imgs:
        zip_bytes = _create_zip(success_imgs, info)
        col_dl.download_button(
            "📦 تحميل جميع الصور (ZIP)",
            zip_bytes,
            file_name=f"mahwous_{info.get('brand','brand').replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.zip",
            mime="application/zip",
            use_container_width=True,
            type="primary"
        )

    st.divider()

    # Group by aspect
    groups = {
        "📱 عمودي (9:16)": {k: v for k, v in success_imgs.items() if v.get("aspect") == "9:16"},
        "🖼️ مربع (1:1)":   {k: v for k, v in success_imgs.items() if v.get("aspect") == "1:1"},
        "🖥️ أفقي (16:9)":  {k: v for k, v in success_imgs.items() if v.get("aspect") in ("16:9", "4:3")},
        "📌 آخرى":          {k: v for k, v in success_imgs.items() if v.get("aspect") == "2:3"},
    }

    for group_name, group in groups.items():
        if not group:
            continue
        st.markdown(f"<div style='color:#806040; font-size:0.8rem; font-weight:800; margin:1.2rem 0 0.6rem; letter-spacing:0.04rem;'>{group_name}</div>", unsafe_allow_html=True)
        cols = st.columns(min(len(group), 3))
        for i, (key, data) in enumerate(group.items()):
            with cols[i % 3]:
                st.markdown(f"<div style='color:#D4AF37; font-size:0.78rem; font-weight:700; margin-bottom:0.3rem;'>{data['emoji']} {data['label']}</div>", unsafe_allow_html=True)
                st.image(data["bytes"], use_container_width=True)
                # Resize and download at correct platform size
                resized = _pil_resize(data["bytes"], data["w"], data["h"])
                st.download_button(
                    f"💾 {data['w']}×{data['h']}",
                    resized,
                    file_name=f"mahwous_{key}_{data['w']}x{data['h']}.jpg",
                    mime="image/jpeg",
                    key=f"dl_{key}_{i}",
                    use_container_width=True
                )
                # Show prompt in expander
                if data.get("prompt"):
                    with st.expander("📋 برومت Google Flow"):
                        st.code(data["prompt"], language="text")

    # Failed platforms
    failed_imgs = {k: v for k, v in images.items() if not v.get("bytes")}
    if failed_imgs:
        with st.expander(f"⚠️ {len(failed_imgs)} منصة لم تُولَّد — انقر لمعرفة السبب"):
            for k, v in failed_imgs.items():
                st.error(f"❌ {PLATFORMS[k]['label']} — تحقق من GEMINI_API_KEY وحد الاستخدام")


def display_captions(captions: dict):
    """عرض الـ Captions بتنسيق أنيق"""
    if not captions or "error" in captions:
        if captions and "error" in captions:
            st.error(captions["error"])
        return

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
                    st.text_area("📝 Caption", cap_data["caption"], height=140, key=f"cap_{key}")
                if "title" in cap_data:
                    st.text_input("📌 العنوان", cap_data["title"], key=f"t_{key}")
                if "description" in cap_data:
                    st.text_area("📄 الوصف", cap_data["description"], height=100, key=f"d_{key}")
                if cap_data.get("hashtags"):
                    st.markdown("**🏷️ الهاشتاقات:**")
                    ht_html = " ".join([f"<span class='hashtag-pill'>{h}</span>" for h in cap_data["hashtags"]])
                    st.markdown(ht_html, unsafe_allow_html=True)
            else:
                st.text_area("", str(cap_data), height=130, key=f"cap_{key}_s")


def display_scenario(scenario: dict):
    """عرض السيناريو بتنسيق سينمائي"""
    if not scenario or "scenes" not in scenario:
        return

    st.markdown(f"""
    <div style='background:#080500; border:1px solid rgba(212,175,55,0.3); border-radius:0.75rem; padding:1rem; margin-bottom:1rem;'>
      <div style='color:#D4AF37; font-size:1.1rem; font-weight:900;'>🎬 {scenario.get('title', 'سيناريو مهووس')}</div>
      <div style='color:#806040; font-size:0.82rem; margin-top:0.3rem;'>
        ⏱️ المدة: {scenario.get('total_duration', '—')} ثانية  |  
        🎯 الهوك: <em style='color:#C8A030;'>"{scenario.get('hook', '')}"</em>
      </div>
    </div>
    """, unsafe_allow_html=True)

    for scene in scenario.get("scenes", []):
        num  = scene.get("number", "?")
        typ  = scene.get("type", "")
        dur  = scene.get("duration", "")
        cam  = scene.get("camera", "")
        mdia = scene.get("mahwous_dialogue", "")
        bdia = scene.get("bottle_dialogue", "")
        vis  = scene.get("visual", "")
        mact = scene.get("mahwous_action", "")
        music = scene.get("music_mood", scene.get("music", ""))

        border_color = "#E94560" if typ in ["ذروة", "climax"] else "#D4AF37"

        st.markdown(f"""
        <div class="scene-card" style="border-right-color:{border_color}">
          <div style="display:flex; align-items:center; gap:0.4rem; margin-bottom:0.5rem;">
            <span class="scene-num">{num}</span>
            <span style="color:#D4AF37; font-weight:800; font-size:0.88rem;">{typ}</span>
            <span style="color:#555; font-size:0.75rem;">⏱ {dur} | 📷 {cam}</span>
          </div>
          <div style="color:#A09070; font-size:0.8rem; margin-bottom:0.4rem;">🎭 {vis}</div>
          <div style="color:#C8B890; font-size:0.8rem; margin-bottom:0.3rem;">🎭 مهووس: {mact}</div>
          {"<div style='background:rgba(212,175,55,0.04); border-right:2px solid #D4AF37; padding:0.35rem 0.65rem; border-radius:0.3rem; margin:0.3rem 0;'><span style='color:#D4AF37; font-size:0.72rem;'>مهووس: </span><em style='color:#F0E0C0; font-size:0.83rem;'>\"" + mdia + "\"</em></div>" if mdia else ""}
          {"<div style='background:rgba(233,69,96,0.05); border-right:2px solid #E94560; padding:0.35rem 0.65rem; border-radius:0.3rem; margin:0.3rem 0;'><span style='color:#E94560; font-size:0.72rem;'>العطر: </span><em style='color:#FFD0C0; font-size:0.83rem;'>\"" + bdia + "\"</em></div>" if bdia else ""}
          <div style="color:#605040; font-size:0.72rem; margin-top:0.3rem;">🎵 {music}</div>
        </div>
        """, unsafe_allow_html=True)

        if scene.get("google_flow_prompt"):
            with st.expander(f"📋 برومت Google Flow — اللقطة {num}"):
                st.code(scene["google_flow_prompt"], language="text")

    # Extra info
    if scenario.get("elevenlabs_voice"):
        st.info(f"🎙️ **ElevenLabs:** {scenario['elevenlabs_voice']}")
    if scenario.get("outro"):
        st.markdown(f"<div style='background:rgba(212,175,55,0.08); border:1px solid rgba(212,175,55,0.2); border-radius:0.5rem; padding:0.75rem; color:#C8A030; font-size:0.85rem;'>🎬 الخاتمة: {scenario['outro']}</div>", unsafe_allow_html=True)
    if scenario.get("editor_notes"):
        with st.expander("✂️ ملاحظات المونتاج"):
            st.markdown(f"<div style='color:#A09070; font-size:0.83rem;'>{scenario['editor_notes']}</div>", unsafe_allow_html=True)

    # Export scenario
    st.markdown("")
    text_export = f"# {scenario.get('title', 'سيناريو مهووس')}\nالمدة: {scenario.get('total_duration')} ثانية\nالهوك: {scenario.get('hook', '')}\n\n"
    for sc in scenario.get("scenes", []):
        text_export += f"━━ اللقطة {sc.get('number')}: {sc.get('type')} · {sc.get('duration')} ━━\n"
        text_export += f"📷 {sc.get('camera')}\n🎭 {sc.get('visual')}\n"
        if sc.get("mahwous_dialogue"):
            text_export += f"مهووس: \"{sc['mahwous_dialogue']}\"\n"
        if sc.get("bottle_dialogue"):
            text_export += f"العطر: \"{sc['bottle_dialogue']}\"\n"
        text_export += f"🎵 {sc.get('music_mood', '')}\n\n"

    st.download_button("📄 تحميل السيناريو كاملاً (.txt)", text_export,
                       file_name=f"scenario_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                       mime="text/plain", use_container_width=True)


# ─── How It Works ─────────────────────────────────────────────────────────────
def _show_how_it_works():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center; margin-bottom:1.5rem;'>
        <span style='color:#F0CC55; font-size:0.95rem; font-weight:900; letter-spacing:0.02rem;'>
            🚀 كيف يعمل الاستديو في 5 خطوات؟
        </span>
    </div>""", unsafe_allow_html=True)
    steps = [
        ("📸", "ارفع صورة العطر", "أو أدخل البيانات يدوياً بدون صورة"),
        ("🔍", "تحليل ذكي فوري", "Gemini 2.0 يقرأ كل تفاصيل العطر"),
        ("🎨", "صور لكل منصة", "Imagen 3 بأعلى دقة ووضوح"),
        ("✍️", "نصوص + سيناريو", "كلود 3.5 يكتب بأسلوب خليجي فاخر"),
        ("🚀", "تحميل أو نشر", "ZIP كامل أو نشر تلقائي عبر Make.com"),
    ]
    cols = st.columns(5)
    for i, (col, (icon, title, sub)) in enumerate(zip(cols, steps)):
        col.markdown(f"""
        <div style='text-align:center; padding:1.1rem 0.5rem; 
             background:linear-gradient(135deg,rgba(212,175,55,0.06),rgba(212,175,55,0.03));
             border:1px solid rgba(212,175,55,0.15); border-radius:0.85rem; position:relative;'>
          <div style='font-size:2rem; margin-bottom:0.5rem;'>{icon}</div>
          <div style='color:#F0CC55; font-size:0.82rem; font-weight:900; line-height:1.4;'>{title}</div>
          <div style='color:#806050; font-size:0.7rem; margin-top:0.25rem; line-height:1.4;'>{sub}</div>
          <div style='position:absolute; top:-10px; right:50%; transform:translateX(50%);
               background:#D4AF37; color:#000; width:1.4rem; height:1.4rem;
               border-radius:50%; display:flex; align-items:center; justify-content:center;
               font-weight:900; font-size:0.7rem;'>{i+1}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


def _generate_weekly_plan(info: dict) -> str:
    """توليد خطة نشر أسبوعية"""
    from modules.ai_engine import _openrouter_chat, _get_secrets
    secrets = _get_secrets()
    brand = info.get("brand", "العطر")
    name  = info.get("product_name", "")
    mood  = info.get("mood", "فاخر")
    prompt = f"""أنت خبير تسويق رقمي لعطور فاخرة. ضع خطة نشر أسبوعية (7 أيام) لعطر "{name}" من "{brand}" ذو طابع {mood}.
لكل يوم: المنصة + نوع المحتوى + التوقيت + الهدف + نبذة عن المحتوى.
اكتب بالعربية باختصار ووضوح. نسّق كجدول نصي جميل."""
    try:
        return _openrouter_chat(prompt, secrets["openrouter"])
    except:
        return f"""📅 خطة النشر الأسبوعية — {brand} {name}

الأحد    | إنستجرام ريلز  | 7م  | توعية  | فيديو تقديمي للعطر بموسيقى هادئة
الاثنين  | تيك توك        | 6م  | تفاعل  | سيناريو الحوار مع العطر
الثلاثاء | تويتر/X        | 12م | محتوى  | تغريدة عن الملاحظات العطرية
الأربعاء | يوتيوب شورت    | 5م  | تعليم  | فيديو: كيف تختار عطرك المثالي
الخميس   | إنستجرام ستوري | 8م  | قصة    | خلف الكواليس — عالم مهووس
الجمعة   | تيليجرام       | 2م  | عروض   | عرض خاص نهاية الأسبوع
السبت    | فيسبوك         | 4م  | مجتمع  | استطلاع: ما عطرك المفضل؟"""


def _generate_email_copy(info: dict) -> str:
    """توليد بريد إلكتروني تسويقي"""
    from modules.ai_engine import _openrouter_chat, _get_secrets
    secrets = _get_secrets()
    brand = info.get("brand", "مهووس")
    name  = info.get("product_name", "العطر")
    mood  = info.get("mood", "فاخر وأنيق")
    prompt = f"""اكتب بريداً إلكترونياً تسويقياً فاخراً لعطر "{name}" من "{brand}".
المزاج: {mood}. الجمهور: محبّو العطور الفاخرة في الخليج.
اشمل: سطر الموضوع + جسم الرسالة + دعوة للعمل.
الأسلوب: راقٍ وعاطفي ومقنع. باللغة العربية الفصحى الجذابة."""
    try:
        return _openrouter_chat(prompt, secrets["openrouter"])
    except:
        return f"""📧 البريد الإلكتروني التسويقي

الموضوع: رحلة عطرية لا تُنسى — {name} من {brand} 🌹

عزيزي محبّ الرقي،

بين طيّات الهواء يسكن سرٌّ عطريٌّ يستحق أن تعيشه...
{name} من {brand} — ليس مجرد عطر، بل تجربة تحمل بصمتك الخاصة.

✨ ملاحظات {info.get('notes_guess', 'فاخرة ومميزة')}
✨ طابع {mood}
✨ يدوم طويلاً ويترك أثراً لا يُنسى

اكتشف عطرك الآن ←

مع تحيات فريق مهووس للعطور 🌹"""


def _generate_ad_copy(info: dict) -> str:
    """توليد نص إعلان مدفوع"""
    from modules.ai_engine import _openrouter_chat, _get_secrets
    secrets = _get_secrets()
    brand = info.get("brand", "مهووس")
    name  = info.get("product_name", "العطر")
    gender = {"masculine":"للرجل","feminine":"للمرأة","unisex":"للجنسين"}.get(info.get("gender","unisex"),"للجميع")
    prompt = f"""اكتب نص إعلان مدفوع متكامل لعطر "{name}" من "{brand}" {gender}.
اشمل:
1. هيدلاين قوي (أقل من 10 كلمات)
2. نص إعلان Meta/Instagram (125 حرف)
3. نص إعلان TikTok (بداية مشوّقة 3 ثوانٍ)
4. دعوة للعمل CTA واضحة
5. نص إعلان Google (العنوان + الوصف)
باللغة العربية، أسلوب تسويقي مقنع وعاطفي."""
    try:
        return _openrouter_chat(prompt, secrets["openrouter"])
    except:
        return f"""📣 نصوص الإعلانات المدفوعة — {name}

━━ هيدلاين الحملة ━━
"عطرٌ واحد يكفي ليُعرَف بك في كل مكان"

━━ إعلان Meta / Instagram ━━
{name} من {brand} — العطر الذي يتركك حاضراً حتى بعد رحيلك. اطلب الآن ✨

━━ بداية إعلان TikTok ━━
"توقف لثانية... هل تعرف الفرق بين عطر عادي وعطر يغيّر يومك؟" 🌹

━━ دعوة للعمل CTA ━━
🛒 اطلب الآن واستلم في 24 ساعة | شحن مجاني

━━ إعلان Google ━━
العنوان: {name} | {brand} الرسمي
الوصف: اكتشف عطرك المثالي من مجموعة {brand} الفاخرة. جودة أصيلة وتوصيل سريع."""


# ─── Main Studio Page ──────────────────────────────────────────────────────────
def show_studio_page():
    st.markdown(STUDIO_CSS, unsafe_allow_html=True)

    st.markdown("""
    <div class="studio-hero">
      <h1>🎬 استديو مهووس الذكي</h1>
      <p class="sub">توليد صور · فيديو · تعليقات · سيناريوهات · هاشتاقات · خطط نشر لجميع المنصات</p>
      <div class="version-badge">v12.0 · GEMINI 2.0 + CLAUDE 3.5 + IMAGEN 3</div>
    </div>
    """, unsafe_allow_html=True)

    secrets = _get_secrets()
    has_gemini    = bool(secrets["gemini"])
    has_openrouter = bool(secrets["openrouter"])

    # API Alerts
    if not has_gemini:
        st.markdown("<div class='warning-box'>⚠️ <strong>GEMINI_API_KEY</strong> غير موجود — توليد الصور وتحليل الصور سيكون معطلاً. أضفه في Settings → Secrets</div>", unsafe_allow_html=True)

    # ─── Step 1: Input Mode ──────────────────────────────────────────────────
    st.markdown('<div class="step-badge">① اختر طريقة الإدخال</div>', unsafe_allow_html=True)

    if "input_mode" not in st.session_state:
        st.session_state.input_mode = "image"

    mode_col1, mode_col2 = st.columns(2)
    with mode_col1:
        is_img = st.session_state.input_mode == "image"
        if st.button(
            f"📸  رفع صورة العطر\n{'← محدد' if is_img else 'انقر للاختيار'}",
            use_container_width=True,
            type="primary" if is_img else "secondary",
            key="mode_image"
        ):
            st.session_state.input_mode = "image"
            st.rerun()
    with mode_col2:
        is_man = st.session_state.input_mode == "manual"
        if st.button(
            f"⌨️  إدخال البيانات يدوياً\n{'← محدد' if is_man else 'انقر للاختيار'}",
            use_container_width=True,
            type="primary" if is_man else "secondary",
            key="mode_manual"
        ):
            st.session_state.input_mode = "manual"
            st.rerun()

    st.markdown("---")

    # ─── Step 2: Input ───────────────────────────────────────────────────────
    perfume_info = None
    image_bytes  = None

    if st.session_state.input_mode == "image":
        st.markdown('<div class="step-badge">② رفع صورة العطر</div>', unsafe_allow_html=True)

        col_img, col_char = st.columns([1, 1])

        with col_img:
            uploaded = st.file_uploader(
                "📸 ارفع صورة العطر (JPG/PNG/WEBP)",
                type=["jpg", "jpeg", "png", "webp"],
                label_visibility="collapsed",
                key="perfume_upload"
            )
            if uploaded:
                st.image(uploaded, use_container_width=True, caption="✅ صورة العطر")
                image_bytes = uploaded.getvalue()

        with col_char:
            st.markdown("**⚙️ إعدادات الجلسة**")
            char_img = st.file_uploader(
                "👤 صورة مرجعية لمهووس (اختياري)",
                type=["jpg", "jpeg", "png"],
                key="char_upload",
                help="mahwous_character.png — يحافظ على ثبات الشخصية"
            )
            if char_img:
                st.image(char_img, caption="✅ مرجع مهووس", use_container_width=True)
                st.session_state.char_reference = char_img.getvalue()

        if not uploaded:
            _show_how_it_works()
            return

        # ── Auto-Analyze ──────────────────────────────────────────────────
        st.markdown("---")
        st.markdown('<div class="step-badge">③ تحليل العطر</div>', unsafe_allow_html=True)

        analyze_key = f"analyzed_{hash(image_bytes)}"
        if analyze_key not in st.session_state:
            if has_gemini:
                with st.spinner("🔍 تحليل صورة العطر بـ Gemini 2.0..."):
                    try:
                        info = analyze_perfume_image(image_bytes)
                        st.session_state[analyze_key] = info
                        st.session_state.gen_count += 1
                    except Exception as e:
                        st.error(f"❌ فشل التحليل: {e}")
                        return
            else:
                # Fallback info
                info = build_manual_info("عطر مهووس", "Mahwous", "EDP", "100ml",
                                          "unisex", "luxury", ["gold", "black"],
                                          "elegant luxury flacon", "فاخر وغامض", "عود وعنبر")
                st.session_state[analyze_key] = info

        perfume_info = st.session_state.get(analyze_key, {})

        # Display analysis card
        _info_card(perfume_info)

        # Allow editing
        with st.expander("✏️ تعديل بيانات التحليل"):
            c1, c2, c3 = st.columns(3)
            perfume_info["product_name"] = c1.text_input("اسم العطر", perfume_info.get("product_name", ""))
            perfume_info["brand"]        = c2.text_input("العلامة التجارية", perfume_info.get("brand", ""))
            perfume_info["type"]         = c3.text_input("النوع", perfume_info.get("type", "EDP"))
            c4, c5, c6 = st.columns(3)
            perfume_info["gender"] = c4.selectbox("الجنس", ["masculine", "feminine", "unisex"],
                                                    index=["masculine","feminine","unisex"].index(perfume_info.get("gender","unisex")) if perfume_info.get("gender","unisex") in ["masculine","feminine","unisex"] else 2)
            perfume_info["style"]  = c5.selectbox("الطابع", ["luxury","oriental","niche","sport","modern","classic"],
                                                    index=0)
            perfume_info["mood"]   = c6.text_input("المزاج", perfume_info.get("mood", "فاخر"))
            perfume_info["bottle_shape"] = st.text_area("شكل الزجاجة", perfume_info.get("bottle_shape", ""), height=60)
            perfume_info["notes_guess"]  = st.text_input("ملاحظات العطر المتوقعة", perfume_info.get("notes_guess", ""))

    else:  # Manual mode
        st.markdown('<div class="step-badge">② إدخال بيانات العطر</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            m_name   = st.text_input("🌹 اسم العطر *", placeholder="مثال: Oud for Greatness")
            m_brand  = st.text_input("🏷️ العلامة التجارية *", placeholder="مثال: Initio")
            m_type   = st.selectbox("💧 النوع", ["EDP", "EDT", "Parfum", "Extrait", "EDC", "Oil"])
            m_size   = st.text_input("📏 الحجم", value="100ml")
        with c2:
            m_gender = st.selectbox("👤 الجنس", ["masculine", "feminine", "unisex"])
            m_style  = st.selectbox("✨ الطابع", ["luxury", "oriental", "niche", "sport", "modern", "classic"])
            m_colors = st.text_input("🎨 الألوان (مفصولة بفاصلة)", placeholder="gold, black, silver")
            m_mood   = st.text_input("🌙 المزاج", placeholder="فاخر وغامض وشرقي")

        m_bottle = st.text_area("🫙 وصف الزجاجة", placeholder="مثال: زجاجة مستطيلة بغطاء أسود لامع وجسم ذهبي نصف شفاف...", height=80)
        m_notes  = st.text_input("🌺 ملاحظات العطر", placeholder="مثال: عود، عنبر، مسك، فانيليا")

        if not m_name or not m_brand:
            st.markdown("<div class='warning-box'>⚠️ أدخل اسم العطر والعلامة التجارية للمتابعة</div>", unsafe_allow_html=True)
            _show_how_it_works()
            return

        colors_list = [c.strip() for c in m_colors.split(",") if c.strip()] or ["gold", "black"]
        perfume_info = build_manual_info(m_name, m_brand, m_type, m_size, m_gender,
                                          m_style, colors_list, m_bottle, m_mood, m_notes)
        _info_card(perfume_info)

    # ─── Step 3: Settings ─────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="step-badge">④ إعدادات الجلسة والمنصات</div>', unsafe_allow_html=True)

    col_char2, col_scene = st.columns(2)
    with col_char2:
        outfit_choice = st.selectbox(
            "👔 زي مهووس",
            options=list(MAHWOUS_OUTFITS.keys()),
            format_func=lambda k: {"suit":"🤵 البدلة الفاخرة — للمحتوى الرسمي",
                                    "hoodie":"🏆 الهودي — لتيك توك والشباب",
                                    "thobe":"👘 الثوب الملكي — للطابع الخليجي",
                                    "casual":"👕 الكاجوال — للمحتوى العاطفي"}[k],
            key="outfit_sel"
        )
        include_char = st.toggle("🧑 تضمين شخصية مهووس في الصور", value=True)
        ramadan_mode = st.toggle("🌙 وضع رمضان الاحتفالي", value=False)

    with col_scene:
        scene_choice = st.selectbox(
            "🎭 مكان المشهد",
            options=["store","beach","desert","studio","garden","rooftop","car"],
            format_func=lambda k: {"store":"🏪 متجر العطور الفاخر",
                                    "beach":"🌅 شاطئ عند الغروب",
                                    "desert":"🏜️ صحراء ذهبية",
                                    "studio":"🎬 استديو تصوير فاخر",
                                    "garden":"🌹 حديقة ملكية",
                                    "rooftop":"🌆 سطح مبنى عالٍ",
                                    "car":"🚗 سيارة فارهة"}[k],
            key="scene_sel"
        )

    st.markdown("---")
    selected_platforms = platform_selector()

    # ─── Step 4: Content Options ──────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="step-badge">⑤ اختر المحتوى المطلوب</div>', unsafe_allow_html=True)

    # ── الخيارات الأساسية (مرئية دائماً) ──
    st.markdown("""
    <div style='background:rgba(212,175,55,0.06); border:1px solid rgba(212,175,55,0.20);
         border-radius:0.75rem; padding:0.9rem 1.2rem; margin-bottom:0.8rem;'>
      <div style='color:#F5D060; font-size:0.9rem; font-weight:900; margin-bottom:0.5rem;'>🎯 المحتوى الأساسي</div>
    </div>
    """, unsafe_allow_html=True)

    bc1, bc2, bc3 = st.columns(3)
    with bc1:
        opt_images   = st.checkbox("🖼️ صور لكل منصة", value=True,
                                    help="يتطلب GEMINI_API_KEY" if not has_gemini else "Imagen 3.0 — أعلى جودة")
    with bc2:
        opt_captions = st.checkbox("📝 تعليقات المنصات", value=True)
    with bc3:
        opt_hashtags = st.checkbox("🏷️ 45 هاشتاق", value=True)

    # ── خيارات متقدمة (مطوية افتراضياً) ──
    with st.expander("⚙️ خيارات متقدمة — نصوص · فيديو · نشر", expanded=False):
        oc1, oc2 = st.columns(2)
        with oc1:
            opt_desc     = st.checkbox("📄 5 أوصاف تسويقية", value=True)
            opt_scenario = st.checkbox("🎬 سيناريو فيديو تيك توك", value=False)
            opt_story    = st.checkbox("📖 قصة عطرية إبداعية", value=False)
        with oc2:
            opt_weekly   = st.checkbox("📅 خطة نشر أسبوعية", value=False)
            opt_email    = st.checkbox("📧 بريد إلكتروني تسويقي", value=False)
            opt_ad_copy  = st.checkbox("📣 نص إعلان مدفوع", value=False)
        pub_col, vid_col = st.columns(2)
        with pub_col:
            opt_publish  = st.checkbox("🚀 نشر تلقائي عبر Make.com", value=False,
                                        help="يتطلب WEBHOOK_PUBLISH_CONTENT")
        with vid_col:
            opt_video    = st.checkbox("🎥 فيديو Luma AI", value=False,
                                        help="يتطلب LUMA_API_KEY")

    if opt_scenario:
        scenario_type = st.selectbox("🎬 نوع السيناريو", [
            "dialogue", "story", "challenge", "review", "unboxing"
        ], format_func=lambda k: {
            "dialogue": "💬 حوار مهووس والعطر",
            "story":    "📖 قصة تحول 3 مشاهد",
            "challenge":"⚔️ مشهد الاكتشاف",
            "review":   "⭐ مراجعة خبير",
            "unboxing": "📦 فتح العلبة السينمائي"
        }[k])
    else:
        scenario_type = "dialogue"

    st.markdown("---")

    # ─── Step 5: Generate Button ──────────────────────────────────────────────
    num_selected = len(selected_platforms)
    btn_disabled = num_selected == 0

    if not btn_disabled:
        tasks = []
        if opt_images and has_gemini:  tasks.append(f"صور ({num_selected})")
        if opt_captions:               tasks.append("تعليقات (12 منصة)")
        if opt_desc:                   tasks.append("5 أوصاف")
        if opt_hashtags:               tasks.append("45 هاشتاق")
        if opt_scenario:               tasks.append("سيناريو")
        if opt_story:                  tasks.append("قصة")
        if opt_weekly:                 tasks.append("خطة أسبوعية")
        if opt_email:                  tasks.append("بريد تسويقي")
        if opt_ad_copy:                tasks.append("إعلان مدفوع")
        if opt_video:                  tasks.append("فيديو")
        btn_label = f"⚡ ابدأ التوليد — {' · '.join(tasks)}"
    else:
        btn_label = "⚠️ اختر منصة واحدة على الأقل لبدء التوليد"

    if st.button(btn_label, type="primary", use_container_width=True, disabled=btn_disabled):
        all_results = {}
        progress_bar = st.progress(0)
        status_text  = st.empty()

        total_steps = sum([
            bool(opt_captions), bool(opt_desc), bool(opt_hashtags),
            bool(opt_scenario), bool(opt_story), bool(opt_weekly),
            bool(opt_email), bool(opt_ad_copy),
            bool(opt_images and has_gemini),
            bool(opt_video), bool(opt_publish)
        ])
        step = 0

        def advance(msg: str):
            nonlocal step
            step += 1
            pct = int((step / max(total_steps, 1)) * 90)
            progress_bar.progress(pct)
            status_text.markdown(f"**{msg}**")

        # === Captions ===
        if opt_captions:
            advance("📝 توليد تعليقات لـ 12 منصة...")
            try:
                all_results["captions"] = generate_all_captions(perfume_info)
            except Exception as e:
                st.warning(f"⚠️ تعليقات: {e}")

        # === Descriptions ===
        if opt_desc:
            advance("📄 توليد 5 أوصاف تسويقية...")
            try:
                all_results["descriptions"] = generate_descriptions(perfume_info)
            except Exception as e:
                st.warning(f"⚠️ أوصاف: {e}")

        # === Hashtags ===
        if opt_hashtags:
            advance("🏷️ توليد 45 هاشتاق...")
            try:
                all_results["hashtags"] = generate_hashtags(perfume_info)
            except Exception as e:
                st.warning(f"⚠️ هاشتاقات: {e}")

        # === Scenario ===
        if opt_scenario:
            advance(f"🎬 توليد سيناريو {scenario_type}...")
            try:
                all_results["scenario"] = generate_scenario(perfume_info, scenario_type)
            except Exception as e:
                st.warning(f"⚠️ سيناريو: {e}")

        # === Creative Story ===
        if opt_story:
            advance("📖 كتابة القصة العطرية...")
            try:
                all_results["story"] = generate_perfume_story(perfume_info)
            except Exception as e:
                st.warning(f"⚠️ قصة: {e}")

        # === Weekly Content Plan ===
        if opt_weekly:
            advance("📅 توليد خطة النشر الأسبوعية...")
            try:
                all_results["weekly_plan"] = _generate_weekly_plan(perfume_info)
            except Exception as e:
                st.warning(f"⚠️ خطة أسبوعية: {e}")

        # === Email Marketing ===
        if opt_email:
            advance("📧 كتابة البريد الإلكتروني التسويقي...")
            try:
                all_results["email"] = _generate_email_copy(perfume_info)
            except Exception as e:
                st.warning(f"⚠️ بريد إلكتروني: {e}")

        # === Paid Ad Copy ===
        if opt_ad_copy:
            advance("📣 كتابة نص الإعلان المدفوع...")
            try:
                all_results["ad_copy"] = _generate_ad_copy(perfume_info)
            except Exception as e:
                st.warning(f"⚠️ إعلان مدفوع: {e}")

        # === Images ===
        if opt_images and has_gemini and selected_platforms:
            advance(f"🖼️ توليد صور لـ {num_selected} منصة...")
            def img_cb(pct, msg):
                progress_bar.progress(int(step / max(total_steps, 1) * 90 - 10 + pct * 10))
                status_text.markdown(f"**{msg}**")
            try:
                all_results["images"] = generate_platform_images(
                    perfume_info, selected_platforms, outfit_choice, scene_choice,
                    include_char, img_cb, ramadan_mode
                )
                st.session_state.img_count += len([v for v in all_results["images"].values() if v.get("bytes")])
            except Exception as e:
                st.warning(f"⚠️ صور: {e}")

        # === Video ===
        if opt_video:
            advance("🎥 توليد فيديو Luma AI (3-5 دقائق)...")
            try:
                vid_aspect = "9:16" if any(p in selected_platforms for p in ["tiktok","instagram_story"]) else "16:9"
                all_results["video"] = generate_video_luma(perfume_info, vid_aspect)
                if "url" not in all_results["video"]:
                    st.warning(f"⚠️ فيديو: {all_results['video'].get('error')}")
            except Exception as e:
                st.warning(f"⚠️ فيديو: {e}")

        # === Publish ===
        if opt_publish:
            advance("📡 إرسال إلى Make.com...")
            payload = {
                **perfume_info,
                "captions":    all_results.get("captions", {}),
                "descriptions": all_results.get("descriptions", {}),
                "hashtags":    all_results.get("hashtags", {}),
                "video_url":   all_results.get("video", {}).get("url", ""),
                "weekly_plan": all_results.get("weekly_plan", ""),
                "email":       all_results.get("email", ""),
                "ad_copy":     all_results.get("ad_copy", ""),
                "platforms":   selected_platforms,
                "timestamp":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source":      "mahwous_studio_v12"
            }
            if send_to_make(payload):
                st.success("✅ تم الإرسال إلى Make.com بنجاح!")
            else:
                st.warning("⚠️ فشل الإرسال — تحقق من WEBHOOK_PUBLISH_CONTENT في الإعدادات")

        progress_bar.progress(100)
        status_text.markdown("✅ **اكتمل التوليد بنجاح!**")
        st.session_state.gen_count += 1

        # === Display Results ===
        _display_all_results(all_results, perfume_info)


def _display_all_results(results: dict, info: dict):
    """عرض كل النتائج"""
    st.markdown("---")
    st.markdown("""
    <div style='background:linear-gradient(135deg,#130A00,#1E1004); border:1px solid rgba(212,175,55,0.35);
         border-radius:1rem; padding:1.5rem; text-align:center; margin-bottom:1.5rem;'>
      <div style='color:#F0CC55; font-size:1.4rem; font-weight:900;'>📦 نتائج التوليد</div>
      <div style='color:#A08060; font-size:0.85rem; margin-top:0.3rem;'>جميع المحتويات جاهزة للتحميل والنشر</div>
    </div>
    """, unsafe_allow_html=True)

    # Product summary
    with st.expander("🧴 ملخص بيانات العطر", expanded=False):
        _info_card(info)
        with st.expander("📋 البيانات الكاملة (JSON)"):
            st.json(info)

    # Images
    if "images" in results:
        with st.expander("🖼️ الصور المولّدة", expanded=True):
            display_images(results["images"], info)

    # Video
    if "video" in results and results["video"].get("url"):
        with st.expander("🎥 الفيديو المولّد", expanded=True):
            st.video(results["video"]["url"])

    # Scenario
    if "scenario" in results and results["scenario"].get("scenes"):
        with st.expander("🎬 سيناريو الفيديو", expanded=True):
            display_scenario(results["scenario"])

    # Captions
    if "captions" in results:
        with st.expander("📱 تعليقات جميع المنصات", expanded=True):
            display_captions(results["captions"])

    # Creative Story
    if "story" in results and results["story"]:
        with st.expander("📖 القصة العطرية الإبداعية", expanded=False):
            st.markdown(f"<div style='background:#0A0600; border:1px solid rgba(212,175,55,0.25); border-radius:0.75rem; padding:1.4rem; color:#F0E0C0; font-size:0.9rem; line-height:1.9; font-style:italic;'>{results['story']}</div>", unsafe_allow_html=True)
            st.download_button("📄 تحميل القصة (.txt)", results["story"],
                               file_name=f"story_{info.get('brand','brand')}.txt", mime="text/plain")

    # Weekly Plan
    if "weekly_plan" in results and results["weekly_plan"]:
        with st.expander("📅 خطة النشر الأسبوعية", expanded=False):
            st.markdown(f"<div style='background:#0A0600; border:1px solid rgba(212,175,55,0.25); border-radius:0.75rem; padding:1.4rem; color:#F0E0C0; font-size:0.85rem; line-height:1.9; direction:rtl;'>{results['weekly_plan'].replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
            st.download_button("📅 تحميل الخطة (.txt)", results["weekly_plan"],
                               file_name=f"weekly_plan_{info.get('brand','brand')}.txt", mime="text/plain")

    # Email Copy
    if "email" in results and results["email"]:
        with st.expander("📧 البريد الإلكتروني التسويقي", expanded=False):
            st.text_area("✉️ محتوى البريد الإلكتروني", results["email"], height=280, key="email_content")
            st.download_button("📧 تحميل البريد (.txt)", results["email"],
                               file_name=f"email_{info.get('brand','brand')}.txt", mime="text/plain")

    # Ad Copy
    if "ad_copy" in results and results["ad_copy"]:
        with st.expander("📣 نصوص الإعلانات المدفوعة", expanded=False):
            st.text_area("📣 نص الإعلان", results["ad_copy"], height=320, key="ad_copy_content")
            st.download_button("📣 تحميل نص الإعلان (.txt)", results["ad_copy"],
                               file_name=f"ad_copy_{info.get('brand','brand')}.txt", mime="text/plain")

    # Descriptions
    if "descriptions" in results and results["descriptions"]:
        desc = results["descriptions"]
        with st.expander("📄 الأوصاف التسويقية الخمسة", expanded=False):
            tabs = st.tabs(["⚡ قصير", "📝 متوسط", "📜 طويل", "🎯 إعلاني", "🔍 SEO"])
            keys_labels = [("short","قصير"),("medium","متوسط"),("long","طويل"),("ad","إعلاني"),("seo","SEO")]
            for tab, (key, label) in zip(tabs, keys_labels):
                with tab:
                    if key == "seo" and isinstance(desc.get("seo"), dict):
                        seo = desc["seo"]
                        st.text_input("العنوان (60 حرف)", seo.get("title",""), key="seo_t")
                        st.text_area("الميتا (155 حرف)", seo.get("meta",""), height=70, key="seo_m")
                        st.text_area("محتوى SEO", seo.get("content",""), height=150, key="seo_c")
                        if seo.get("keywords"):
                            kw_html = " ".join([f"<span class='hashtag-pill'>{k}</span>" for k in seo["keywords"]])
                            st.markdown(kw_html, unsafe_allow_html=True)
                    else:
                        st.text_area("", desc.get(key,""), height=200, key=f"d_{key}")

    # Hashtags
    if "hashtags" in results and results["hashtags"]:
        ht = results["hashtags"]
        with st.expander("🏷️ 45 هاشتاق", expanded=False):
            hc1, hc2, hc3 = st.columns(3)
            with hc1:
                st.markdown("<div style='color:#F0CC55; font-weight:900; font-size:0.88rem; margin-bottom:0.4rem;'>🇸🇦 عربي (20)</div>", unsafe_allow_html=True)
                arabic_ht = " ".join(ht.get("arabic", []))
                st.text_area("", arabic_ht, height=130, key="ht_ar")
            with hc2:
                st.markdown("<div style='color:#F0CC55; font-weight:900; font-size:0.88rem; margin-bottom:0.4rem;'>🌍 إنجليزي (20)</div>", unsafe_allow_html=True)
                eng_ht = " ".join(ht.get("english", []))
                st.text_area("", eng_ht, height=130, key="ht_en")
            with hc3:
                st.markdown("<div style='color:#F0CC55; font-weight:900; font-size:0.88rem; margin-bottom:0.4rem;'>🔥 ترندينج (5)</div>", unsafe_allow_html=True)
                tr_ht = " ".join(ht.get("trending", []))
                st.text_area("", tr_ht, height=130, key="ht_tr")

            all_ht = f"{arabic_ht} {eng_ht} {tr_ht}"
            st.download_button("📋 تحميل كل الهاشتاقات (.txt)", all_ht,
                               file_name="hashtags.txt", mime="text/plain", use_container_width=True)

    # Download All JSON
    st.markdown("---")
    export = {
        "product":      info,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source":       "Mahwous AI Studio v12.0",
        "captions":     results.get("captions", {}),
        "descriptions": results.get("descriptions", {}),
        "hashtags":     results.get("hashtags", {}),
        "scenario":     results.get("scenario", {}),
        "story":        results.get("story", ""),
        "weekly_plan":  results.get("weekly_plan", ""),
        "email":        results.get("email", ""),
        "ad_copy":      results.get("ad_copy", ""),
        "video_url":    results.get("video", {}).get("url", ""),
    }
    brand_clean = info.get("brand", "brand").replace(" ", "_").lower()
    st.download_button(
        "📥 تحميل جميع المحتوى النصي (JSON)",
        json.dumps(export, ensure_ascii=False, indent=2),
        file_name=f"mahwous_{brand_clean}_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
        mime="application/json",
        use_container_width=True
    )
