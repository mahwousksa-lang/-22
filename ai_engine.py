"""
🤖 محرك الذكاء الاصطناعي - مهووس v10.0
OpenRouter + Gemini Vision + Imagen 3 + Luma AI
"""

import streamlit as st
import requests
import base64
import json
import time

# ─── API Configs ─────────────────────────────────────────────────────────────
def _get_secrets():
    return {
        "openrouter": st.secrets.get("OPENROUTER_API_KEY", "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"),
        "gemini":     st.secrets.get("GEMINI_API_KEY", ""),
        "luma":       st.secrets.get("LUMA_API_KEY", ""),
        "webhook":    st.secrets.get("WEBHOOK_PUBLISH_CONTENT", ""),
    }

GEMINI_VISION_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"
GEMINI_TEXT_URL   = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
GEMINI_IMAGEN_URL = "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:predict"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "anthropic/claude-3.5-sonnet"

# ─── Platform Sizes ────────────────────────────────────────────────────────
PLATFORMS = {
    "instagram_post":   {"w": 1080, "h": 1080, "label": "📸 Instagram Post",    "aspect": "1:1",  "emoji": "📸"},
    "instagram_story":  {"w": 1080, "h": 1920, "label": "📱 Instagram Story",   "aspect": "9:16", "emoji": "📱"},
    "tiktok":           {"w": 1080, "h": 1920, "label": "🎵 TikTok",            "aspect": "9:16", "emoji": "🎵"},
    "youtube_short":    {"w": 1080, "h": 1920, "label": "▶️ YouTube Short",     "aspect": "9:16", "emoji": "▶️"},
    "youtube_thumb":    {"w": 1280, "h": 720,  "label": "🎬 YouTube Thumbnail", "aspect": "16:9", "emoji": "🎬"},
    "twitter":          {"w": 1200, "h": 675,  "label": "🐦 Twitter/X",         "aspect": "16:9", "emoji": "🐦"},
    "facebook":         {"w": 1200, "h": 630,  "label": "👍 Facebook",          "aspect": "16:9", "emoji": "👍"},
    "snapchat":         {"w": 1080, "h": 1920, "label": "👻 Snapchat",          "aspect": "9:16", "emoji": "👻"},
    "linkedin":         {"w": 1200, "h": 627,  "label": "💼 LinkedIn",          "aspect": "16:9", "emoji": "💼"},
    "pinterest":        {"w": 1000, "h": 1500, "label": "📌 Pinterest",         "aspect": "2:3",  "emoji": "📌"},
}

# ─── Character DNA ─────────────────────────────────────────────────────────
MAHWOUS_DNA = """Photorealistic 3D animated character 'Mahwous' - Middle Eastern Gulf Arab man:
- Black styled hair swept slightly forward, well-groomed
- Short dark neat beard, defined
- Expressive warm brown eyes, thick eyebrows
- Golden-brown skin tone, friendly confident expression
- Pixar/Disney realistic 3D render quality
- Cinematic professional lighting
STRICTLY maintain these exact facial features in every image."""

MAHWOUS_OUTFITS = {
    "suit":   "wearing elegant black luxury suit, gold embroidery on lapels, white dress shirt, gold silk tie, gold pocket square",
    "hoodie": "wearing premium black oversized hoodie with gold MAHWOUS lettering embroidered on chest",
    "thobe":  "wearing pristine white Saudi thobe with black and gold bisht cloak over shoulders",
    "casual": "wearing relaxed white linen shirt, casual elegant style, sleeves rolled up",
}

QUALITY = """Ultra-realistic 3D render, 4K quality, cinematic color grading warm golden tones,
professional studio lighting, rim lights, bokeh background, depth of field, luxury advertisement quality.
NO TEXT on image, NO watermarks, NO subtitles. Clean professional frame."""

# ─── OpenRouter Text Generation ────────────────────────────────────────────
def generate_text_openrouter(prompt: str, system: str = None) -> str:
    """توليد النص عبر OpenRouter"""
    secrets = _get_secrets()
    headers = {
        "Authorization": f"Bearer {secrets['openrouter']}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://mahwousstore.streamlit.app",
        "X-Title": "Mahwous AI Studio"
    }
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
        "max_tokens": 4000,
        "temperature": 0.7
    }
    r = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


def generate_text_gemini(prompt: str) -> str:
    """توليد النص عبر Gemini Flash (احتياطي)"""
    secrets = _get_secrets()
    headers = {"Content-Type": "application/json", "x-goog-api-key": secrets["gemini"]}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    r = requests.post(GEMINI_TEXT_URL, headers=headers, json=payload, timeout=45)
    r.raise_for_status()
    return r.json()["candidates"][0]["content"]["parts"][0]["text"]


def smart_generate_text(prompt: str, system: str = None) -> str:
    """توليد ذكي: OpenRouter أولاً، Gemini كاحتياطي"""
    try:
        return generate_text_openrouter(prompt, system)
    except Exception:
        try:
            full = f"{system}\n\n{prompt}" if system else prompt
            return generate_text_gemini(full)
        except Exception as e:
            raise Exception(f"فشل توليد النص: {e}")


def clean_json(text: str) -> dict:
    """تنظيف واستخراج JSON من الرد"""
    import re
    text = text.strip()
    # Remove markdown code fences
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s*```$", "", text, flags=re.MULTILINE)
    text = text.strip()
    return json.loads(text)


# ─── Gemini Vision ─────────────────────────────────────────────────────────
def analyze_perfume_image(image_bytes: bytes) -> dict:
    """تحليل صورة العطر"""
    secrets = _get_secrets()
    b64 = base64.b64encode(image_bytes).decode()
    headers = {"Content-Type": "application/json", "x-goog-api-key": secrets["gemini"]}

    payload = {"contents": [{"parts": [
        {"inline_data": {"mime_type": "image/jpeg", "data": b64}},
        {"text": """Analyze this perfume image. Return ONLY valid JSON, no extra text:
{
  "product_name": "full perfume name",
  "brand": "brand name",
  "type": "EDP/EDT/Parfum/etc",
  "size": "volume in ml",
  "colors": ["main", "secondary"],
  "bottle_shape": "detailed bottle shape description",
  "bottle_cap": "cap description",
  "style": "luxury/sport/modern/classic/oriental",
  "gender": "masculine/feminine/unisex",
  "mood": "overall mood/character",
  "notes_guess": "guessed scent notes based on visual"
}"""}
    ]}]}

    r = requests.post(GEMINI_VISION_URL, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
    return clean_json(text)


# ─── Gemini Imagen 3 ───────────────────────────────────────────────────────
def generate_image_gemini(prompt: str, aspect_ratio: str = "1:1") -> bytes | None:
    """توليد صورة بـ Gemini Imagen 3"""
    secrets = _get_secrets()
    if not secrets["gemini"]:
        return None

    # Map aspect ratios to Imagen supported ones
    aspect_map = {
        "1:1": "1:1", "9:16": "9:16", "16:9": "16:9",
        "2:3": "3:4", "4:3": "4:3"
    }
    ar = aspect_map.get(aspect_ratio, "1:1")

    headers = {"Content-Type": "application/json", "x-goog-api-key": secrets["gemini"]}
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": ar,
            "safetyFilterLevel": "block_only_high",
            "personGeneration": "allow_adult"
        }
    }

    r = requests.post(GEMINI_IMAGEN_URL, headers=headers, json=payload, timeout=90)
    if r.status_code == 200:
        b64 = r.json()["predictions"][0].get("bytesBase64Encoded", "")
        if b64:
            return base64.b64decode(b64)
    return None


def build_mahwous_product_prompt(info: dict, outfit: str = "suit", scene: str = "store", platform_aspect: str = "1:1") -> str:
    """بناء برومت مهووس مع العطر"""
    outfit_desc = MAHWOUS_OUTFITS.get(outfit, MAHWOUS_OUTFITS["suit"])

    scenes = {
        "store": f"inside a luxury dark perfume boutique, golden shelves of perfumes behind him",
        "beach": "at a dramatic golden hour beach, ocean waves behind, sunset sky",
        "desert": "in an endless golden desert at sunset, dramatic dunes",
        "studio": "in a premium dark studio with bokeh golden particles floating",
        "garden": "in a lush royal garden at magic hour, rose petals falling",
    }
    scene_desc = scenes.get(scene, scenes["store"])

    bottle_desc = f"{info.get('product_name', 'luxury perfume')} by {info.get('brand', 'premium brand')}"
    bottle_shape = info.get('bottle_shape', 'elegant glass perfume bottle')
    colors = ", ".join(info.get('colors', ['gold', 'black']))

    return f"""{MAHWOUS_DNA}
{outfit_desc}
{scene_desc}
He holds the {bottle_desc} perfume bottle carefully with both hands - EXACT original bottle: {bottle_shape}, colors: {colors}.
DO NOT alter the perfume bottle design. Bottle must be photorealistic and match the original.
Expression: expert confidence with warm smile, slightly tilted toward camera.
Aspect ratio: {platform_aspect}. {QUALITY}"""


def build_product_only_prompt(info: dict, platform_aspect: str = "1:1") -> str:
    """برومت العطر وحده بدون الشخصية"""
    bottle_desc = f"{info.get('product_name', 'luxury perfume')} by {info.get('brand', 'premium brand')}"
    bottle_shape = info.get('bottle_shape', 'elegant glass perfume bottle')
    colors = ", ".join(info.get('colors', ['gold', 'black']))

    return f"""Professional luxury perfume photography of {bottle_desc}.
Exact bottle: {bottle_shape}, colors: {colors}.
STRICTLY maintain original bottle shape and design from reference.
Setup: dark dramatic background with golden light rays, marble surface, golden particle bokeh.
Cinematic studio lighting, rim lights, specular highlights on bottle.
Product advertisement quality, ultra-sharp focus on bottle.
Aspect ratio: {platform_aspect}. {QUALITY}"""


# ─── Generate All Platform Images ─────────────────────────────────────────
def generate_platform_images(info: dict, selected_platforms: list, outfit: str, scene: str,
                              include_character: bool = True, progress_callback=None) -> dict:
    """توليد صور لجميع المنصات المختارة"""
    results = {}
    total = len(selected_platforms)

    for i, plat_key in enumerate(selected_platforms):
        plat = PLATFORMS[plat_key]
        if progress_callback:
            progress_callback(i / total, f"توليد {plat['label']}...")

        # Build prompt
        if include_character:
            prompt = build_mahwous_product_prompt(info, outfit, scene, plat["aspect"])
        else:
            prompt = build_product_only_prompt(info, plat["aspect"])

        img_bytes = generate_image_gemini(prompt, plat["aspect"])
        results[plat_key] = {
            "bytes": img_bytes,
            "label": plat["label"],
            "emoji": plat["emoji"],
            "w": plat["w"],
            "h": plat["h"],
            "aspect": plat["aspect"],
        }

    if progress_callback:
        progress_callback(1.0, "✅ اكتملت الصور!")
    return results


# ─── Generate All Platform Captions ───────────────────────────────────────
def generate_all_captions(info: dict) -> dict:
    """توليد Captions لجميع المنصات"""
    system = """أنت خبير تسويق رقمي متخصص في العطور الفاخرة.
اكتب Captions احترافية بالعربية الخليجية الفاخرة. ركز على الانفعال والحضور."""

    prompt = f"""العطر: {info.get('product_name')} من {info.get('brand')}
النوع: {info.get('type')} | الجنس: {info.get('gender')} | الطابع: {info.get('style')}
المزاج: {info.get('mood', 'فاخر')}

اكتب Captions مخصصة لكل منصة. أجب بـ JSON صرف فقط:
{{
  "instagram_post": {{
    "caption": "نص 120-150 كلمة + إيموجي كثير + 25 هاشتاق عربي وإنجليزي",
    "hashtags": ["#هاشتاق1", "#hashtag2"]
  }},
  "instagram_story": {{
    "caption": "نص قصير 30-50 كلمة + 5 هاشتاقات + CTA قوي",
    "hashtags": []
  }},
  "tiktok": {{
    "caption": "150 حرف مثيرة + هوك قوي في البداية + #fyp #viral #عطور",
    "hashtags": ["#fyp", "#عطور", "#viral"]
  }},
  "youtube_short": {{
    "caption": "عنوان جذاب + وصف 100 كلمة",
    "title": "عنوان الفيديو القصير"
  }},
  "youtube_thumb": {{
    "title": "عنوان YouTube مثالي للـ SEO",
    "description": "وصف 200 كلمة للـ YouTube"
  }},
  "twitter": {{
    "caption": "نص 200-250 حرف فقط + 3 هاشتاقات + CTA"
  }},
  "facebook": {{
    "caption": "نص 200-300 كلمة قصصي عاطفي + 5 هاشتاقات"
  }},
  "snapchat": {{
    "caption": "نص عفوي شبابي 50-70 حرف"
  }},
  "linkedin": {{
    "caption": "نص مهني 150-200 كلمة يربط العطر بالشخصية والنجاح"
  }},
  "pinterest": {{
    "caption": "نص وصفي 100-150 كلمة + 15 كلمة مفتاحية"
  }},
  "whatsapp": {{
    "caption": "رسالة ودودة 80-120 كلمة كأنها من صديق"
  }},
  "telegram": {{
    "caption": "نص مفصل 300-400 كلمة + قصة + تنسيق HTML bold italic"
  }}
}}"""

    text = smart_generate_text(prompt, system)
    try:
        return clean_json(text)
    except:
        return {"error": "فشل توليد الـ Captions"}


def generate_descriptions(info: dict) -> dict:
    """توليد 5 نسخ من الوصف"""
    prompt = f"""العطر: {info.get('product_name')} من {info.get('brand')} | {info.get('type')} | {info.get('gender')} | {info.get('style')}

اكتب 5 أوصاف تسويقية باللغة العربية. JSON فقط:
{{
  "short": "وصف 60-80 كلمة للقصص",
  "medium": "وصف 120-150 كلمة للمنشورات",
  "long": "مقال وصفي 250-300 كلمة فاخر",
  "ad": "إعلان مكثف 30-50 كلمة جذاب ومقنع",
  "seo": {{
    "title": "عنوان SEO 60 حرف",
    "meta": "وصف ميتا 155 حرف",
    "content": "محتوى SEO 200 كلمة",
    "keywords": ["كلمة1","كلمة2","كلمة3","كلمة4","كلمة5","كلمة6","كلمة7","كلمة8"]
  }}
}}"""
    text = smart_generate_text(prompt)
    try:
        return clean_json(text)
    except:
        return {}


def generate_hashtags(info: dict) -> dict:
    """توليد 40 هاشتاق"""
    prompt = f"""العطر: {info.get('product_name')} | {info.get('brand')} | {info.get('gender')} | {info.get('style')}

اختر 40 هاشتاق مثالي للوصول الأقصى. JSON فقط:
{{
  "arabic": ["#هاشتاق × 20"],
  "english": ["#hashtag × 20"],
  "trending": ["#أكثر_هاشتاقات_ترندينج × 5"]
}}"""
    text = smart_generate_text(prompt)
    try:
        return clean_json(text)
    except:
        return {}


def generate_scenario(info: dict, scenario_type: str = "dialogue") -> dict:
    """توليد سيناريو فيديو بشخصية مهووس"""
    types = {
        "dialogue": "حوار بين مهووس والعطر (14 ثانية)",
        "story": "قصة قصيرة 3 مشاهد (21 ثانية)",
        "challenge": "مشهد اكتشاف وتحدي (15 ثانية)",
        "review": "مراجعة احترافية من مهووس (20 ثانية)",
    }
    scenario_desc = types.get(scenario_type, types["dialogue"])

    prompt = f"""العطر: {info.get('product_name')} من {info.get('brand')} | {info.get('mood', 'فاخر')}

اكتب سيناريو فيديو TikTok احترافي - النوع: {scenario_desc}
الشخصيات: مهووس (خبير عطور خليجي ثلاثي الأبعاد) + زجاجة العطر المتحركة

JSON فقط:
{{
  "title": "عنوان السيناريو",
  "total_duration": "مدة بالثواني",
  "scenes": [
    {{
      "number": 1,
      "duration": "ثواني",
      "type": "الهوك/كشف/ذروة/خاتمة",
      "camera": "نوع اللقطة والحركة",
      "visual": "وصف المشهد البصري بالتفصيل",
      "mahwous_action": "ما يفعله مهووس",
      "mahwous_dialogue": "ما يقوله مهووس",
      "bottle_action": "ما يفعله العطر",
      "bottle_dialogue": "ما يقوله العطر (إن تكلم)",
      "music": "نوع الموسيقى والمزاج",
      "google_flow_prompt": "برومت جاهز للنسخ إلى Google Flow"
    }}
  ],
  "outro": "مشهد ختامي يظهر شعار مهووس"
}}"""
    text = smart_generate_text(prompt)
    try:
        return clean_json(text)
    except:
        return {}


# ─── Luma AI Video ─────────────────────────────────────────────────────────
def generate_video_luma(info: dict, aspect: str = "9:16") -> dict:
    """توليد فيديو بـ Luma AI"""
    secrets = _get_secrets()
    if not secrets["luma"]:
        return {"error": "LUMA_API_KEY غير موجود"}

    prompt = (
        f"Cinematic luxury perfume advertisement. {MAHWOUS_DNA} "
        f"wearing elegant black suit with gold tie, holding {info.get('product_name')} by {info.get('brand')} "
        f"perfume bottle - {info.get('bottle_shape', 'elegant bottle')}, colors {', '.join(info.get('colors', ['gold']))}. "
        f"MAINTAIN exact bottle design. Slow 360° rotation of bottle, golden particles, "
        f"luxury dark background, cinematic lighting. 5 seconds, {aspect} aspect ratio. "
        f"NO TEXT, professional product advertisement quality."
    )

    headers = {"Authorization": f"Bearer {secrets['luma']}", "Content-Type": "application/json"}
    payload = {"prompt": prompt, "loop": True, "aspect_ratio": aspect}

    try:
        r = requests.post("https://api.lumalabs.ai/dream-machine/v1/generations",
                          headers=headers, json=payload, timeout=30)
        if r.status_code not in (200, 201):
            return {"error": f"Luma API Error: {r.text[:200]}"}

        gen_id = r.json().get("id")
        if not gen_id:
            return {"error": "لم يتم الحصول على Generation ID"}

        # Poll for completion
        for attempt in range(60):
            time.sleep(5)
            poll = requests.get(
                f"https://api.lumalabs.ai/dream-machine/v1/generations/{gen_id}",
                headers=headers, timeout=15
            )
            data = poll.json()
            state = data.get("state", "")
            if state == "completed":
                return {"url": data.get("assets", {}).get("video", ""), "id": gen_id}
            elif state == "failed":
                return {"error": data.get("failure_reason", "فشل توليد الفيديو")}

        return {"error": "انتهت مهلة الانتظار (5 دقائق)"}
    except Exception as e:
        return {"error": str(e)}


# ─── Make.com ──────────────────────────────────────────────────────────────
def send_to_make(payload: dict) -> bool:
    """إرسال البيانات إلى Make.com"""
    secrets = _get_secrets()
    webhook_url = secrets["webhook"]
    if not webhook_url:
        return False
    try:
        r = requests.post(webhook_url, json=payload, timeout=30)
        return r.status_code in (200, 201, 202, 204)
    except:
        return False
