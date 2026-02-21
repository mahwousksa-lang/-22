"""
🤖 محرك الذكاء الاصطناعي - مهووس v11.0
OpenRouter (Claude 3.5) + Gemini 2.0 Flash + Imagen 3 + Luma AI
أعلى معايير الدقة والجودة
"""

import streamlit as st
import requests
import base64
import json
import time
import re
from datetime import datetime

# ─── API Configs ──────────────────────────────────────────────────────────────
def _get_secrets() -> dict:
    return {
        "openrouter": st.secrets.get("OPENROUTER_API_KEY", "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"),
        "gemini":     st.secrets.get("GEMINI_API_KEY", ""),
        "luma":       st.secrets.get("LUMA_API_KEY", ""),
        "webhook":    st.secrets.get("WEBHOOK_PUBLISH_CONTENT", ""),
    }

# ─── Model Endpoints (أحدث النماذج 2026) ─────────────────────────────────────
GEMINI_BASE     = "https://generativelanguage.googleapis.com/v1beta/models"
GEMINI_VISION   = f"{GEMINI_BASE}/gemini-2.0-flash:generateContent"   # Vision + Text
GEMINI_TEXT     = f"{GEMINI_BASE}/gemini-2.0-flash:generateContent"   # Fast text
GEMINI_IMAGEN   = f"{GEMINI_BASE}/imagen-3.0-generate-002:predict"    # Best image quality

OPENROUTER_URL   = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "anthropic/claude-3.5-sonnet"                      # Best text quality

# ─── Platform Sizes ────────────────────────────────────────────────────────────
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

# ─── Character DNA (مُحسَّن للإصدار 11) ──────────────────────────────────────
MAHWOUS_DNA = """Photorealistic 3D animated character 'Mahwous' — Gulf Arab perfume expert:
FACE (LOCK ALL): Black neatly styled hair swept forward. Short dark groomed beard. Warm expressive brown eyes with thick defined eyebrows. Golden-brown skin. Confident friendly expression.
STYLE: Pixar/Disney premium 3D render quality. Cinematic depth of field. Professional 3-point lighting.
CONSISTENCY: NEVER change any facial feature. SAME face every frame. Reference-locked character."""

MAHWOUS_OUTFITS = {
    "suit":   "wearing elegant black luxury suit with gold embroidery on lapels, crisp white dress shirt, gold silk tie, gold pocket square — ultra-luxury formal look",
    "hoodie": "wearing premium black oversized hoodie with gold MAHWOUS lettering embroidered on chest — contemporary street-luxury",
    "thobe":  "wearing pristine bright white Saudi thobe with black and gold bisht cloak draped over shoulders — royal Arabian elegance",
    "casual": "wearing relaxed white linen shirt, sleeves rolled up, casual yet refined — effortlessly stylish",
}

QUALITY = """Technical specs: 4K ultra-resolution, RAW render quality, 8-bit color depth. 
Lighting: 3-point cinematic — key light warm gold, fill soft, rim metallic.
Color grade: rich warm tones, deep shadows, lifted blacks, golden highlights.
DOF: shallow depth of field, creamy bokeh background.
STRICT: NO TEXT anywhere, NO watermarks, NO subtitles, NO logos, NO UI elements. Clean frame only."""

# Aspect ratio map for Imagen 3
ASPECT_RATIO_MAP = {
    "1:1":  "1:1",
    "9:16": "9:16",
    "16:9": "16:9",
    "2:3":  "3:4",
    "4:3":  "4:3",
}

# ─── Retry Decorator ──────────────────────────────────────────────────────────
def with_retry(func, max_attempts: int = 3, delay: float = 2.0):
    """يحاول تنفيذ الدالة حتى max_attempts مع تأخير تصاعدي"""
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise e
            time.sleep(delay * (attempt + 1))
    return None


# ─── JSON Cleaner (Multi-strategy) ───────────────────────────────────────────
def clean_json(text: str) -> dict:
    """تنظيف واستخراج JSON من الرد - متعدد الاستراتيجيات"""
    if not text:
        raise ValueError("النص فارغ")
    
    text = text.strip()
    
    # 1. Remove markdown fences
    text = re.sub(r"^```(?:json)?\s*\n?", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n?\s*```\s*$", "", text, flags=re.MULTILINE)
    text = text.strip()
    
    # 2. Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # 3. Find first JSON object
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    
    # 4. Find first JSON array
    match = re.search(r'\[[\s\S]*\]', text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    
    # 5. Fix common issues: trailing commas, single quotes
    fixed = re.sub(r',\s*([}\]])', r'\1', text)
    fixed = fixed.replace("'", '"')
    try:
        return json.loads(fixed)
    except:
        raise ValueError(f"فشل تحليل JSON: {text[:200]}")


# ─── OpenRouter Text Generation ───────────────────────────────────────────────
def generate_text_openrouter(prompt: str, system: str = None, temperature: float = 0.75, max_tokens: int = 4096) -> str:
    """توليد النص عبر OpenRouter (Claude 3.5 Sonnet)"""
    secrets = _get_secrets()
    headers = {
        "Authorization": f"Bearer {secrets['openrouter']}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://mahwousstore.streamlit.app",
        "X-Title": "Mahwous AI Studio v11"
    }
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    r = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=90)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


def generate_text_gemini(prompt: str, temperature: float = 0.7) -> str:
    """توليد النص عبر Gemini 2.0 Flash (احتياطي)"""
    secrets = _get_secrets()
    if not secrets["gemini"]:
        raise ValueError("Gemini API key مفقود")
    
    headers = {"Content-Type": "application/json", "x-goog-api-key": secrets["gemini"]}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": temperature, "maxOutputTokens": 4096}
    }
    r = requests.post(GEMINI_TEXT, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]


def smart_generate_text(prompt: str, system: str = None, temperature: float = 0.75) -> str:
    """توليد ذكي: OpenRouter أولاً، Gemini كاحتياطي"""
    def try_openrouter():
        return generate_text_openrouter(prompt, system, temperature)
    
    try:
        return with_retry(try_openrouter)
    except Exception:
        try:
            full_prompt = f"{system}\n\n{prompt}" if system else prompt
            return with_retry(lambda: generate_text_gemini(full_prompt, temperature))
        except Exception as e:
            raise Exception(f"فشل توليد النص عبر جميع النماذج: {e}")


# ─── Gemini 2.0 Flash Vision ──────────────────────────────────────────────────
def analyze_perfume_image(image_bytes: bytes) -> dict:
    """تحليل صورة العطر بدقة عالية باستخدام Gemini 2.0 Flash"""
    secrets = _get_secrets()
    if not secrets["gemini"]:
        raise ValueError("GEMINI_API_KEY مطلوب لتحليل الصور")
    
    b64 = base64.b64encode(image_bytes).decode()
    headers = {"Content-Type": "application/json", "x-goog-api-key": secrets["gemini"]}

    payload = {
        "contents": [{"parts": [
            {"inline_data": {"mime_type": "image/jpeg", "data": b64}},
            {"text": """You are a master perfume expert with 30 years of experience. 
Analyze this perfume bottle image with extreme precision. Return ONLY valid JSON, nothing else:
{
  "product_name": "exact full perfume name from label",
  "brand": "exact brand name",
  "type": "EDP/EDT/Parfum/EDC/Extrait/Oil",
  "size": "volume e.g. 100ml",
  "colors": ["primary color", "secondary color", "accent color"],
  "bottle_shape": "ultra-detailed bottle shape: geometry, curves, proportions, height-to-width ratio",
  "bottle_cap": "cap material, shape, color, finish",
  "bottle_material": "glass type, finish, transparency",
  "label_style": "label design, typography style, colors",
  "style": "luxury/sport/modern/classic/oriental/niche",
  "gender": "masculine/feminine/unisex",
  "mood": "2-3 words for overall vibe",
  "notes_guess": "top/heart/base notes guess from visual",
  "bottle_uniqueness": "what makes this bottle distinctive",
  "image_quality": "good/poor",
  "confidence": 0.0
}"""}
        ]}],
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 1024}
    }

    def do_request():
        r = requests.post(GEMINI_VISION, headers=headers, json=payload, timeout=45)
        r.raise_for_status()
        text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
        return clean_json(text)
    
    return with_retry(do_request)


# ─── Gemini Imagen 3 (v2 — أعلى جودة) ────────────────────────────────────────
def generate_image_gemini(prompt: str, aspect_ratio: str = "1:1",
                           reference_b64: str = None) -> bytes | None:
    """توليد صورة بـ Imagen 3 بأعلى جودة"""
    secrets = _get_secrets()
    if not secrets["gemini"]:
        return None

    ar = ASPECT_RATIO_MAP.get(aspect_ratio, "1:1")
    headers = {"Content-Type": "application/json", "x-goog-api-key": secrets["gemini"]}
    
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": ar,
            "safetyFilterLevel": "block_only_high",
            "personGeneration": "allow_adult",
            "addWatermark": False,
            "enhancePrompt": True,
        }
    }

    def do_request():
        r = requests.post(GEMINI_IMAGEN, headers=headers, json=payload, timeout=120)
        if r.status_code == 200:
            preds = r.json().get("predictions", [])
            if preds:
                b64 = preds[0].get("bytesBase64Encoded", "")
                if b64:
                    return base64.b64decode(b64)
        elif r.status_code == 429:
            time.sleep(8)
            raise Exception("Rate limit - retrying")
        else:
            raise Exception(f"Imagen error {r.status_code}: {r.text[:200]}")
        return None
    
    try:
        return with_retry(do_request, max_attempts=3, delay=4.0)
    except Exception:
        return None


# ─── Prompt Builders ──────────────────────────────────────────────────────────
def build_mahwous_product_prompt(info: dict, outfit: str = "suit",
                                  scene: str = "store", platform_aspect: str = "1:1") -> str:
    """بناء برومت مهووس مع العطر — دقة سينمائية قصوى"""
    outfit_desc = MAHWOUS_OUTFITS.get(outfit, MAHWOUS_OUTFITS["suit"])

    scenes = {
        "store":   "Inside a breathtaking luxury dark perfume boutique — backlit golden shelves of rare fragrances, warm amber spotlights, polished obsidian floor reflecting light",
        "beach":   "At a cinematic golden-hour beach — warm amber sky, gentle foamy waves, dramatic sunset casting long shadows, sand glimmering",
        "desert":  "Vast golden Arabian desert at dusk — towering dunes with razor-sharp edges, amber sky with scattered stars, warm desert breeze particles",
        "studio":  "Inside a minimalist luxury dark studio — floating golden bokeh particles, dramatic rim lighting from above, velvety dark backdrop",
        "garden":  "In a lush royal fragrance garden at magic hour — cascading rose petals, golden mist, ornate marble fountain in background",
        "rooftop": "On a glass-barrier luxury rooftop at night — twinkling city skyline below, starry sky above, ambient evening glow",
        "car":     "Rear seat of a Rolls-Royce Phantom — cream leather interior, city lights blurring past rain-dotted windows, subtle warm console glow",
    }
    scene_desc = scenes.get(scene, scenes["store"])

    product_name = info.get("product_name", "luxury perfume")
    brand = info.get("brand", "premium brand")
    bottle_shape = info.get("bottle_shape", "elegant glass perfume bottle")
    bottle_cap = info.get("bottle_cap", "polished cap")
    colors = ", ".join(info.get("colors", ["gold", "black"]))
    uniqueness = info.get("bottle_uniqueness", "")
    label = info.get("label_style", "elegant label")

    return f"""{MAHWOUS_DNA}
Outfit: {outfit_desc}
Setting: {scene_desc}

He cradles the perfume bottle reverently with both hands at chest height:
— Product: {product_name} by {brand}
— Bottle: {bottle_shape}. Cap: {bottle_cap}. Colors: {colors}. Label: {label}.
{f"— Distinctive: {uniqueness}" if uniqueness else ""}

CRITICAL BOTTLE RULE: The bottle must be 100% photorealistic, matching the original design exactly. NO distortion, NO simplification, NO invented details.

Expression: warm expert confidence, slight knowing smile, eyes engaging camera.
Composition: subject centered, slight 3/4 angle, negative space around bottle.
Aspect ratio: {platform_aspect}.
{QUALITY}"""


def build_product_only_prompt(info: dict, platform_aspect: str = "1:1") -> str:
    """برومت العطر وحده — تصوير منتج احترافي"""
    product_name = info.get("product_name", "luxury perfume")
    brand = info.get("brand", "premium brand")
    bottle_shape = info.get("bottle_shape", "elegant glass bottle")
    bottle_cap = info.get("bottle_cap", "polished cap")
    colors = ", ".join(info.get("colors", ["gold", "black"]))
    material = info.get("bottle_material", "premium glass")
    uniqueness = info.get("bottle_uniqueness", "")

    return f"""Museum-quality luxury perfume product photography.
Subject: {product_name} by {brand}
Bottle: {bottle_shape}. Material: {material}. Cap: {bottle_cap}. Colors: {colors}.
{f"Distinctive: {uniqueness}" if uniqueness else ""}

STRICT: Reproduce the exact original bottle with zero creative liberty.
Placement: centered on aged dark marble slab. Soft golden light from upper-right. Silk fabric draped elegantly beside bottle. Tiny ambient golden particles floating.
Mood: museum-quality product shot — luxurious, aspirational, editorial.
Specular highlights on glass, subtle caustics from bottle. Perfect label legibility.
Aspect ratio: {platform_aspect}.
{QUALITY}"""


def build_ramadan_product_prompt(info: dict, platform_aspect: str = "9:16") -> str:
    """برومت رمضاني فاخر"""
    product_name = info.get("product_name", "luxury perfume")
    brand = info.get("brand", "premium brand")
    colors = ", ".join(info.get("colors", ["gold", "black"]))
    
    return f"""Luxury Ramadan perfume advertisement. 
Subject: {product_name} by {brand} bottle. Colors: {colors}.
Setting: Ornate Ramadan scene — glowing golden crescent moon and fanoos lantern hanging above, scattered rose petals and oud chips, soft warm candlelight.
Bottle centered prominently, surrounded by tasteful Islamic geometric gold ornaments.
Atmosphere: warm amber and deep gold tones, reverent and aspirational.
Aspect ratio: {platform_aspect}.
{QUALITY}"""


# ─── Generate All Platform Images ─────────────────────────────────────────────
def generate_platform_images(info: dict, selected_platforms: list, outfit: str, scene: str,
                               include_character: bool = True, progress_callback=None,
                               ramadan_mode: bool = False) -> dict:
    """توليد صور لجميع المنصات المختارة مع تحسينات الجودة"""
    results = {}
    total = len(selected_platforms)

    for i, plat_key in enumerate(selected_platforms):
        plat = PLATFORMS[plat_key]
        if progress_callback:
            progress_callback(i / total, f"⚡ توليد {plat['label']}...")

        # Build optimized prompt per platform
        if ramadan_mode:
            prompt = build_ramadan_product_prompt(info, plat["aspect"])
        elif include_character:
            prompt = build_mahwous_product_prompt(info, outfit, scene, plat["aspect"])
        else:
            prompt = build_product_only_prompt(info, plat["aspect"])

        img_bytes = generate_image_gemini(prompt, plat["aspect"])
        results[plat_key] = {
            "bytes":   img_bytes,
            "label":   plat["label"],
            "emoji":   plat["emoji"],
            "w":       plat["w"],
            "h":       plat["h"],
            "aspect":  plat["aspect"],
            "prompt":  prompt,
        }

    if progress_callback:
        progress_callback(1.0, "✅ اكتملت جميع الصور!")
    return results


# ─── Generate All Platform Captions ───────────────────────────────────────────
def generate_all_captions(info: dict) -> dict:
    """توليد Captions لجميع المنصات — احترافية وجاذبة"""
    system = """أنت أفضل كاتب محتوى عطور فاخرة في الخليج العربي.
أسلوبك: شعري، عاطفي، فاخر، مع هوك جذاب في كل منصة.
اللغة: عربية خليجية راقية — ليست فصحى متصلبة، ليست عامية ركيكة.
الأيقونات: استخدم إيموجي ذكي ومناسب بحد أقصى 3-4 لكل نص."""

    prompt = f"""العطر: {info.get('product_name', 'عطر فاخر')} من {info.get('brand', 'علامة مميزة')}
النوع: {info.get('type', 'EDP')} | الجنس: {info.get('gender', 'unisex')} | الطابع: {info.get('style', 'luxury')}
المزاج: {info.get('mood', 'فاخر وغامض')} | ملاحظات: {info.get('notes_guess', 'عود وعنبر')}

اكتب Captions احترافية ومخصصة لكل منصة. أجب بـ JSON صرف فقط (لا مقدمة، لا تعليق):
{{
  "instagram_post": {{
    "caption": "نص 120-150 كلمة شعري وجذاب مع إيموجي ذكي وهوك قوي في السطر الأول",
    "hashtags": ["#هاشتاق_عربي × 15", "#english_hashtag × 10"]
  }},
  "instagram_story": {{
    "caption": "نص قصير لا يتجاوز 50 كلمة + CTA قوي (مثل: احفظ هذا! / رابط في البايو)",
    "hashtags": ["#tag1", "#tag2", "#tag3", "#tag4", "#tag5"]
  }},
  "tiktok": {{
    "caption": "150 حرف مثيرة — هوك صادم في أول 3 كلمات + #fyp #viral #عطور_فاخرة",
    "hashtags": ["#fyp", "#viral", "#عطور", "#عطور_فاخرة", "#perfume", "#نيش"]
  }},
  "youtube_short": {{
    "title": "عنوان YouTube Short جذاب 60 حرف",
    "caption": "وصف 80-100 كلمة + CTA للاشتراك + 5 هاشتاقات"
  }},
  "youtube_thumb": {{
    "title": "عنوان YouTube SEO مثالي يحتوي الكلمات المفتاحية",
    "description": "وصف 200-250 كلمة شامل للـ SEO + timestamps + هاشتاقات"
  }},
  "twitter": {{
    "caption": "نص 220 حرف بالضبط + تأثير عاطفي + 2-3 هاشتاقات"
  }},
  "facebook": {{
    "caption": "نص قصصي 200-280 كلمة يروي تجربة شم العطر + 5 هاشتاقات"
  }},
  "snapchat": {{
    "caption": "نص شبابي عفوي 50-60 حرف فقط"
  }},
  "linkedin": {{
    "caption": "نص مهني 150-180 كلمة يربط العطر بالشخصية القيادية والنجاح"
  }},
  "pinterest": {{
    "caption": "وصف SEO تفصيلي 100-130 كلمة + 12 كلمة مفتاحية"
  }},
  "whatsapp": {{
    "caption": "رسالة ودية حميمة 70-90 كلمة كأنها من خبير صديق"
  }},
  "telegram": {{
    "caption": "تحليل عميق 280-350 كلمة + قصة + تنسيق بالرموز"
  }}
}}"""

    text = smart_generate_text(prompt, system, temperature=0.8)
    try:
        return clean_json(text)
    except Exception as e:
        # Fallback: return basic structure
        return {"error": f"فشل توليد Captions: {e}"}


def generate_descriptions(info: dict) -> dict:
    """توليد 5 نسخ من الوصف بأسلوب احترافي"""
    prompt = f"""العطر: {info.get('product_name', 'عطر فاخر')} من {info.get('brand', 'علامة')}
النوع: {info.get('type', 'EDP')} | {info.get('gender', 'unisex')} | {info.get('style', 'luxury')}
المزاج: {info.get('mood', 'فاخر')} | الملاحظات: {info.get('notes_guess', 'عود وعنبر')}

اكتب 5 أوصاف تسويقية باللغة العربية الفصحى الراقية. JSON فقط:
{{
  "short":  "وصف 60-80 كلمة مكثف للقصص والريلز",
  "medium": "وصف 120-150 كلمة للمنشورات الرئيسية",
  "long":   "مقال وصفي عاطفي وشعري 260-300 كلمة",
  "ad":     "إعلان مكثف ومقنع 30-40 كلمة — نقطة واحدة قوية",
  "seo": {{
    "title":    "عنوان SEO 55-60 حرف يحتوي الكلمات المفتاحية",
    "meta":     "وصف ميتا 145-155 حرف جذاب للضغط",
    "content":  "محتوى SEO 200-220 كلمة طبيعي وثري",
    "keywords": ["كلمة1","كلمة2","كلمة3","كلمة4","كلمة5","كلمة6","كلمة7","كلمة8","كلمة9","كلمة10"]
  }}
}}"""
    text = smart_generate_text(prompt, temperature=0.7)
    try:
        return clean_json(text)
    except:
        return {}


def generate_hashtags(info: dict) -> dict:
    """توليد 45 هاشتاق محسوب لأقصى وصول"""
    prompt = f"""العطر: {info.get('product_name')} | {info.get('brand')} | {info.get('gender')} | {info.get('style')} | {info.get('mood')}

اختر 45 هاشتاق مثالي: مزيج من الوصول العالي والمتوسط والمتخصص. JSON فقط:
{{
  "arabic":   ["#هاشتاق_عربي × 20 — مزيج عام ومتخصص"],
  "english":  ["#english_hashtag × 20 — mix of broad and niche"],
  "trending": ["#أكثر_هاشتاقات_ترندينج_الآن × 5"]
}}"""
    text = smart_generate_text(prompt, temperature=0.5)
    try:
        return clean_json(text)
    except:
        return {}


def generate_scenario(info: dict, scenario_type: str = "dialogue") -> dict:
    """توليد سيناريو فيديو TikTok احترافي"""
    types = {
        "dialogue":  "حوار شيق بين مهووس والعطر الناطق — 14 ثانية، 4 مشاهد",
        "story":     "قصة تحول عاطفية 3 مشاهد — 21 ثانية (قبل/الاكتشاف/بعد)",
        "challenge": "مشهد اكتشاف وتحدي درامي — 15 ثانية",
        "review":    "مراجعة خبير من مهووس — 20 ثانية، تحليل احترافي",
        "unboxing":  "فتح العلبة بطريقة سينمائية — 12 ثانية",
    }
    scenario_desc = types.get(scenario_type, types["dialogue"])

    system = """أنت مخرج إبداعي متخصص في فيديوهات TikTok الفاخرة للعطور.
مزاجك: سينمائي، درامي، ومشاعري. كل مشهد له غرض محدد."""

    prompt = f"""العطر: {info.get('product_name')} من {info.get('brand')}
المزاج: {info.get('mood', 'فاخر')} | النوع: {info.get('style', 'oriental')}
ملاحظات: {info.get('notes_guess', 'عود وعنبر')}

اكتب سيناريو TikTok احترافي للنوع: {scenario_desc}

الشخصيات: مهووس (خبير عطور خليجي ثلاثي الأبعاد) + زجاجة العطر المتحركة (عيون + شفاه)

قواعد صارمة:
- فم مهووس مغلق تماماً عند كلام العطر
- زجاجة العطر لا تتغير شكلها أبداً
- لا رش للعطر — استخدم جزيئات ذهبية
- الهوك في أول 2 ثانية

JSON فقط:
{{
  "title": "عنوان السيناريو الجذاب",
  "total_duration": "الثواني الكاملة",
  "hook": "الجملة الأولى الصادمة في أول 2 ثانية",
  "scenes": [
    {{
      "number": 1,
      "duration": "ثواني",
      "type": "هوك/كشف/ذروة/خاتمة",
      "camera": "نوع اللقطة (ECU/CU/MS/WS) + الحركة",
      "visual": "وصف المشهد البصري الكامل بتفاصيل الإضاءة والألوان",
      "mahwous_action": "ما يفعله مهووس بالتفصيل",
      "mahwous_dialogue": "ما يقوله مهووس — باللهجة الخليجية الفاخرة",
      "bottle_action": "ما تفعله الزجاجة",
      "bottle_dialogue": "ما تقوله الزجاجة (إن تكلمت)",
      "sfx": "المؤثرات الصوتية",
      "music_mood": "وصف الموسيقى والمزاج",
      "google_flow_prompt": "برومت انجليزي كامل جاهز للنسخ إلى Google Flow / Veo"
    }}
  ],
  "elevenlabs_voice": "تعليمات صوت ElevenLabs: النبرة، السرعة، الطبقة",
  "outro": "مشهد ختامي: شعار مهووس + 1 ثانية",
  "editor_notes": "ملاحظات للمونتاج والمؤثرات"
}}"""
    text = smart_generate_text(prompt, system, temperature=0.85)
    try:
        return clean_json(text)
    except:
        return {}


def generate_perfume_story(info: dict) -> str:
    """توليد قصة عاطفية قصيرة عن العطر للنشر"""
    prompt = f"""اكتب قصة قصيرة شعرية (80-100 كلمة) عن عطر {info.get('product_name')} من {info.get('brand')}.
المزاج: {info.get('mood', 'فاخر')}. الأسلوب: عاطفي، حسي، يأخذ القارئ في رحلة شم خيالية.
الصوت: ضمير المتكلم — كأن القارئ يشم العطر الآن. النهاية: جملة تُحفّز على التجربة.
اللغة: عربية فصحى راقية مع إيقاع شعري."""
    return smart_generate_text(prompt, temperature=0.9)


# ─── Luma AI Video ────────────────────────────────────────────────────────────
def generate_video_luma(info: dict, aspect: str = "9:16") -> dict:
    """توليد فيديو بـ Luma AI"""
    secrets = _get_secrets()
    if not secrets["luma"]:
        return {"error": "LUMA_API_KEY غير موجود في Secrets"}

    bottle_desc = f"{info.get('product_name')} by {info.get('brand')}"
    colors = ", ".join(info.get("colors", ["gold", "black"]))

    prompt = (
        f"Cinematic luxury perfume advertisement. "
        f"{MAHWOUS_DNA} wearing elegant black suit with gold tie. "
        f"He holds {bottle_desc} perfume bottle — exact original design, colors: {colors}. "
        f"Slow dramatic reveal: bottle rotates 360°, golden particles swirl, "
        f"warm amber lighting with volumetric rays. "
        f"Ultra-cinematic, 4K quality, luxury ad. {aspect} aspect. "
        f"NO TEXT. Professional product advertisement."
    )

    headers = {"Authorization": f"Bearer {secrets['luma']}", "Content-Type": "application/json"}
    payload  = {"prompt": prompt, "loop": True, "aspect_ratio": aspect}

    try:
        r = requests.post("https://api.lumalabs.ai/dream-machine/v1/generations",
                          headers=headers, json=payload, timeout=30)
        if r.status_code not in (200, 201):
            return {"error": f"Luma API Error {r.status_code}: {r.text[:300]}"}

        gen_id = r.json().get("id")
        if not gen_id:
            return {"error": "لم يتم الحصول على Generation ID"}

        # Poll for completion (max 5 min)
        for _ in range(60):
            time.sleep(5)
            poll = requests.get(
                f"https://api.lumalabs.ai/dream-machine/v1/generations/{gen_id}",
                headers=headers, timeout=15
            )
            data = poll.json()
            state = data.get("state", "")
            if state == "completed":
                return {
                    "url":      data.get("assets", {}).get("video", ""),
                    "id":       gen_id,
                    "duration": "5s"
                }
            elif state == "failed":
                return {"error": data.get("failure_reason", "فشل توليد الفيديو")}

        return {"error": "انتهت مهلة الانتظار (5 دقائق)"}
    except Exception as e:
        return {"error": str(e)}


# ─── Make.com Webhook ─────────────────────────────────────────────────────────
def send_to_make(payload: dict) -> bool:
    """إرسال البيانات إلى Make.com"""
    secrets = _get_secrets()
    webhook_url = secrets.get("webhook", "")
    if not webhook_url:
        return False
    try:
        r = requests.post(webhook_url, json=payload, timeout=30)
        return r.status_code in (200, 201, 202, 204)
    except:
        return False


# ─── Manual Perfume Info Builder ──────────────────────────────────────────────
def build_manual_info(name: str, brand: str, perfume_type: str, size: str,
                       gender: str, style: str, colors: list,
                       bottle_shape: str, mood: str, notes: str) -> dict:
    """بناء بيانات العطر يدوياً بدون صورة"""
    return {
        "product_name":    name or "عطر مميز",
        "brand":           brand or "Mahwous",
        "type":            perfume_type or "EDP",
        "size":            size or "100ml",
        "colors":          colors or ["gold", "black"],
        "bottle_shape":    bottle_shape or "elegant luxury flacon with artistic design",
        "bottle_cap":      "polished metallic cap",
        "bottle_material": "premium crystal glass",
        "label_style":     "elegant minimalist label",
        "style":           style or "luxury",
        "gender":          gender or "unisex",
        "mood":            mood or "فاخر وجذاب",
        "notes_guess":     notes or "عود وعنبر ومسك",
        "bottle_uniqueness": "distinctive artistic design",
        "confidence":      1.0,
    }
