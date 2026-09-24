# /Users/anhnt/Documents/pythoncode/warp/gemini_quiz_engine.py
import json
import sys
import threading
from pathlib import Path
from typing import Dict, Any

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

SHARED_CONFIG_PATH = CURRENT_DIR.parent / 'shared_config'
if not SHARED_CONFIG_PATH.exists():
    SHARED_CONFIG_PATH = Path.home() / 'Documents/pythoncode/shared_config'
if str(SHARED_CONFIG_PATH) not in sys.path:
    sys.path.append(str(SHARED_CONFIG_PATH))

from gemini_client import get_genai_client  # type: ignore
from quiz_metadata import QUIZ_QUESTIONS_MAP  # type: ignore

GEMINI_SEMAPHORE = threading.BoundedSemaphore(10)

def build_xmen_case_file(quiz_result: Dict[str, Any]) -> str:
    ans = quiz_result.get("raw_answers", {})
    dims = quiz_result.get("dimensions", {})
    arch = quiz_result.get("archetype", {})

    q1_val = QUIZ_QUESTIONS_MAP.get("Q1", {}).get("options", {}).get(ans.get("Q1", "A"), {}).get("label", "")
    q2_val = QUIZ_QUESTIONS_MAP.get("Q2", {}).get("options", {}).get(ans.get("Q2", "A"), {}).get("label", "")
    q3_val = QUIZ_QUESTIONS_MAP.get("Q3", {}).get("options", {}).get(ans.get("Q3", "A"), {}).get("label", "")
    q4_val = QUIZ_QUESTIONS_MAP.get("Q4", {}).get("options", {}).get(ans.get("Q4", "A"), {}).get("label", "")
    q5_val = QUIZ_QUESTIONS_MAP.get("Q5", {}).get("options", {}).get(ans.get("Q5", "A"), {}).get("label", "")
    q6_val = QUIZ_QUESTIONS_MAP.get("Q6", {}).get("options", {}).get(ans.get("Q6", "A"), {}).get("label", "")
    q7_val = QUIZ_QUESTIONS_MAP.get("Q7", {}).get("options", {}).get(ans.get("Q7", "A"), {}).get("label", "")

    return f"""
### HỒ SƠ CHIẾN LƯỢC CỦA NGƯỜI LÀM TEST:
- Tuổi thật: {quiz_result.get('user_age', 24)} | Tuổi chân tóc: {quiz_result.get('hair_stress_age', 26)} (+{quiz_result.get('delta_age', 2)} năm)
- Grooming IQ: {quiz_result.get('grooming_iq', 60)}/100
- Chỉ số Bản Lĩnh Đàn Ông Đích Thực: {quiz_result.get('authentic_man_pct', 60)}%
- Archetype: {arch.get('title', 'THE ROUTINE MAN')} ({arch.get('subtitle', '')})

### CHI TIẾT CÂU TRẢ LỜI THỰC TẾ (RAW ANSWERS):
1. Thời gian đội mũ bảo hiểm (Q1): [{ans.get('Q1')}] "{q1_val}"
2. Không gian hoạt động hàng ngày (Q2): [{ans.get('Q2')}] "{q2_val}"
3. Tình trạng da đầu cuối ngày (Q3): [{ans.get('Q3')}] "{q3_val}"
4. Mức độ rụng tóc (Q4): [{ans.get('Q4')}] "{q4_val}"
5. Tiêu chí chọn sản phẩm lý thuyết (Q5): [{ans.get('Q5')}] "{q5_val}"
6. Hành động thực tế khi hết dầu gội (Q6): [{ans.get('Q6')}] "{q6_val}"
7. Định nghĩa bản lĩnh grooming (Q7): [{ans.get('Q7')}] "{q7_val}"

### 4 TRỤC DỮ LIỆU ĐỊNH LƯỢNG:
- Root Exposure: {dims.get('root_exposure', {}).get('level', 'Moderate')}
- Scalp Profile: {dims.get('current_condition', {}).get('scalp_profile', 'Moderate Oil')}
- Tỷ lệ giải quyết gốc rễ: {dims.get('grooming_behavior', {}).get('root_problem_solving_pct', 50)}%
- Tỷ lệ che đậy hương thơm: {dims.get('grooming_behavior', {}).get('fragrance_masking_pct', 50)}%
"""

def generate_deep_wrapped_payload(quiz_result: Dict[str, Any]) -> Dict[str, Any]:
    client = get_genai_client()
    user_case_file = build_xmen_case_file(quiz_result)
    arch = quiz_result.get("archetype", {})
    ans = quiz_result.get("raw_answers", {})
    is_low_helmet = ans.get("Q1") == "A"
    arch_title = arch.get("title", "THE ROUTINE MAN")

    prompt = f"""
Bạn là Giám đốc Sáng tạo Chiến dịch thương hiệu cho X-Men Wrapped 2026.
Nhiệm vụ: Phân tích hồ sơ trắc nghiệm bên dưới và sinh JSON Wrapped sắc sảo, nam tính, có chất châm biếm nhẹ, hiện đại chuẩn phong cách Spotify Wrapped.

{user_case_file}

QUY TẮC NỘI DUNG:
1. ĐỘI MŨ BẢO HIỂM: Nếu Q1 là A, TUYỆT ĐỐI KHÔNG ghi 'Đội mũ bảo hiểm nhiều' vào thói quen xấu. Thay bằng: 'Lười che chắn khói bụi', 'Gội đầu qua loa', hoặc 'Dùng dầu gội tiện tay'.
2. Chỉ khi Q1 là C hoặc D mới nhắc đến mũ bảo hiểm.
3. Độ dài cực kỳ nghiêm ngặt để vừa khung Mobile:
   - bad_habits: Đúng 2 ý, mỗi ý DƯỚI 20 KÝ TỰ.
   - scalp_impacts: Đúng 2 ý, mỗi ý DƯỚI 20 KÝ TỰ.
   - subtitle: Dưới 30 ký tự, không dấu chấm cuối.
   - quote: Dưới 55 ký tự.
   - strength: Dưới 35 ký tự, có dấu chấm cuối.
   - blind_spot: Dưới 35 ký tự, có dấu chấm cuối.
   - golden_advice: Dưới 55 ký tự.
   - gap_desc: Dưới 35 ký tự.
   - body ở slide_2_exposure_condition: Từ 80 - 130 ký tự.

CHỈ TRẢ VỀ JSON THUẦN (KHÔNG MARKDOWN, KHÔNG ```json):
{{
  "persona_title": "{arch_title}",
  "tagline": "Một câu châm ngôn ngắn sắc lẹm dưới 12 từ",
  "grooming_iq": {quiz_result.get('grooming_iq', 65)},
  "authentic_man_pct": {quiz_result.get('authentic_man_pct', 60)},
  "slides": {{
    "slide_1_age_shock": {{
      "headline": "Tuổi chân tóc: {quiz_result.get('hair_stress_age', 26)}",
      "body": "Áp lực môi trường làm nang tóc già trước tuổi."
    }},
    "slide_2_exposure_condition": {{
      "headline": "Môi trường thử thách",
      "body": "Đoạn 2 câu mô tả áp lực bụi bẩn và dầu nhờn ảnh hưởng nang tóc."
    }},
    "slide_3_grooming_gap": {{
      "headline": "The Grooming Gap",
      "body": "Bóc trần sự lệch pha giữa tiêu chuẩn lý tưởng và thực tế trong phòng tắm.",
      "bad_habits": ["Ý 1 ngắn", "Ý 2 ngắn"],
      "scalp_impacts": ["Tác động 1", "Tác động 2"],
      "gap_desc": "Khoảng cách giữa tiêu chuẩn lý tưởng và hành vi tiện tay."
    }},
    "slide_4_final_card": {{
      "archetype_title": "{arch_title}",
      "subtitle": "Slogan phụ ngắn dí dỏm",
      "quote": "Châm ngôn súc tích về bản lĩnh chăm sóc tóc",
      "strength": "Điểm mạnh nổi bật nhất.",
      "blind_spot": "Điểm mù cần khắc phục.",
      "golden_advice": "Lời khuyên đắt giá giải quyết vấn đề từ gốc.",
      "product_route": "{arch.get('product_route', 'routine_optimize')}"
    }}
  }}
}}
"""

    with GEMINI_SEMAPHORE:
        # Sử dụng model flash trực tiếp, không truyền schema phức tạp để tránh AFC warning và độ trễ
        for model_name in ["gemini-2.5-flash", "gemini-1.5-flash"]:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                        "temperature": 0.6,
                        "max_output_tokens": 800
                    }
                )
                if response and response.text:
                    cleaned_text = response.text.strip()
                    if cleaned_text.startswith("```json"):
                        cleaned_text = cleaned_text[7:]
                    if cleaned_text.startswith("```"):
                        cleaned_text = cleaned_text[3:]
                    if cleaned_text.endswith("```"):
                        cleaned_text = cleaned_text[:-3]
                    return json.loads(cleaned_text.strip())
            except Exception as e:
                print(f"[!] Model {model_name} lỗi: {e}")
                continue

    # Fallback tức thì nếu Gemini quá tải/timeout
    return {
        "persona_title": arch.get("title", "THE ROUTINE MAN"),
        "tagline": arch.get("subtitle", "Hiểu cơ thể để nâng tầm bản lĩnh."),
        "grooming_iq": quiz_result.get("grooming_iq", 65),
        "authentic_man_pct": quiz_result.get("authentic_man_pct", 60),
        "slides": {
            "slide_1_age_shock": {
                "headline": f"Tuổi chân tóc: {quiz_result.get('hair_stress_age', 26)}",
                "body": f"Áp lực môi trường đang khiến nang tóc bạn già hơn tuổi thật {quiz_result.get('delta_age', 2)} năm."
            },
            "slide_2_exposure_condition": {
                "headline": "Môi trường thử thách",
                "body": "Khói bụi và thói quen sinh hoạt hàng ngày tạo áp lực liên tục lên nang tóc mà bạn không để ý."
            },
            "slide_3_grooming_gap": {
                "headline": "Khoảng cách trong thói quen",
                "body": "Có sự chênh lệch giữa tiêu chuẩn bạn mong muốn và hành động thực tế trong phòng tắm.",
                "bad_habits": [
                    "Lười che chắn khói bụi" if is_low_helmet else "Đội mũ bảo hiểm lâu",
                    "Dùng dầu gội tiện tay"
                ],
                "scalp_impacts": [
                    "Tích tụ bã nhờn nang tóc",
                    "Bết dầu nhanh sau 4h"
                ],
                "gap_desc": "Khoảng cách giữa tiêu chuẩn lý tưởng và hành vi tiện tay."
            },
            "slide_4_final_card": {
                "archetype_title": arch.get("title", "THE ROUTINE MAN"),
                "subtitle": arch.get("subtitle", "Biết chăm nhưng chưa hiểu sâu"),
                "quote": arch.get("quote", "Bản lĩnh nằm ở việc hiểu rõ cơ thể mình."),
                "strength": arch.get("strength", "Chăm sóc đều đặn mỗi ngày."),
                "blind_spot": arch.get("blind_spot", "Tiện đâu xài đó."),
                "golden_advice": "Đầu tư giải pháp chuyên sâu làm sạch nang tóc.",
                "product_route": arch.get("product_route", "routine_optimize")
            }
        }
    }