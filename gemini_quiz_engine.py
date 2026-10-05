# gemini_quiz_engine.py
import json
import logging
import sys
import threading
from pathlib import Path
from typing import Dict, Any

from gemini_client import get_genai_client  # type: ignore
from quiz_metadata import QUIZ_QUESTIONS_MAP  # type: ignore

# Configure module logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("QUIZ_ENGINE")

# Concurrency throttle for LLM requests
GEMINI_SEMAPHORE = threading.BoundedSemaphore(10)


def build_xmen_case_file(quiz_result: Dict[str, Any]) -> str:
    """Extract and format raw user answers and quantitative metrics into a prompt case file."""
    ans = quiz_result.get("raw_answers", {})
    dims = quiz_result.get("dimensions", {})
    arch = quiz_result.get("archetype", {})

    # 1. Parse raw option labels
    q1_val = QUIZ_QUESTIONS_MAP.get("Q1", {}).get("options", {}).get(ans.get("Q1", "A"), {}).get("label", "")
    q2_val = QUIZ_QUESTIONS_MAP.get("Q2", {}).get("options", {}).get(ans.get("Q2", "A"), {}).get("label", "")
    q3_val = QUIZ_QUESTIONS_MAP.get("Q3", {}).get("options", {}).get(ans.get("Q3", "A"), {}).get("label", "")
    q4_val = QUIZ_QUESTIONS_MAP.get("Q4", {}).get("options", {}).get(ans.get("Q4", "A"), {}).get("label", "")
    q5_val = QUIZ_QUESTIONS_MAP.get("Q5", {}).get("options", {}).get(ans.get("Q5", "A"), {}).get("label", "")
    q6_val = QUIZ_QUESTIONS_MAP.get("Q6", {}).get("options", {}).get(ans.get("Q6", "A"), {}).get("label", "")
    q7_val = QUIZ_QUESTIONS_MAP.get("Q7", {}).get("options", {}).get(ans.get("Q7", "A"), {}).get("label", "")

    # 2. Extract quantitative dimension metrics
    root_exp_level = dims.get("root_exposure", {}).get("level", "Moderate")
    scalp_profile = dims.get("current_condition", {}).get("scalp_profile", "Moderate Oil")
    
    behavior_data = dims.get("grooming_behavior", {})
    root_solving_str = f"{behavior_data.get('root_problem_solving_pct', 50)}%"
    fragrance_masking_str = f"{behavior_data.get('fragrance_masking_pct', 50)}%"

    return (
        f"### HỒ SƠ CHIẾN LƯỢC CỦA NGƯỜI LÀM TEST:\n"
        f"- Tuổi thật: {quiz_result.get('user_age', 24)} | Tuổi chân tóc: {quiz_result.get('hair_stress_age', 26)} (+{quiz_result.get('delta_age', 2)} năm)\n"
        f"- Grooming IQ: {quiz_result.get('grooming_iq', 60)}/100\n"
        f"- Chỉ số Bản Lĩnh Đàn Ông Đích Thực: {quiz_result.get('authentic_man_pct', 60)}%\n"
        f"- Archetype: {arch.get('title', 'THE ROUTINE MAN')} ({arch.get('subtitle', '')})\n\n"
        f"### CHI TIẾT CÂU TRẢ LỜI THỰC TẾ (RAW ANSWERS):\n"
        f"1. Thời gian đội mũ bảo hiểm (Q1): [{ans.get('Q1')}] \"{q1_val}\"\n"
        f"2. Không gian hoạt động hàng ngày (Q2): [{ans.get('Q2')}] \"{q2_val}\"\n"
        f"3. Tình trạng da đầu cuối ngày (Q3): [{ans.get('Q3')}] \"{q3_val}\"\n"
        f"4. Mức độ rụng tóc (Q4): [{ans.get('Q4')}] \"{q4_val}\"\n"
        f"5. Tiêu chí chọn sản phẩm lý thuyết (Q5): [{ans.get('Q5')}] \"{q5_val}\"\n"
        f"6. Hành động thực tế khi hết dầu gội (Q6): [{ans.get('Q6')}] \"{q6_val}\"\n"
        f"7. Định nghĩa bản lĩnh grooming (Q7): [{ans.get('Q7')}] \"{q7_val}\"\n\n"
        f"### 4 TRỤC DỮ LIỆU ĐỊNH LƯỢNG:\n"
        f"- Root Exposure: {root_exp_level}\n"
        f"- Scalp Profile: {scalp_profile}\n"
        f"- Tỷ lệ giải quyết gốc rễ: {root_solving_str}\n"
        f"- Tỷ lệ che đậy hương thơm: {fragrance_masking_str}\n"
    )


def generate_deep_wrapped_payload(quiz_result: Dict[str, Any]) -> Dict[str, Any]:
    """Generate dynamic Spotify-Wrapped story payload via Gemini AI with immediate fallback."""
    client = get_genai_client()
    user_case_file = build_xmen_case_file(quiz_result)
    arch = quiz_result.get("archetype", {})
    arch_title = arch.get("title", "THE ROUTINE MAN")
    hair_stress_age = quiz_result.get("hair_stress_age", 26)
    grooming_iq = quiz_result.get("grooming_iq", 65)
    authentic_man_pct = quiz_result.get("authentic_man_pct", 60)
    product_route = arch.get("product_route", "routine_optimize")

    prompt = (
        "Bạn là Giám đốc Sáng tạo Chiến dịch thương hiệu cho X-Men Wrapped 2026.\n"
        "Nhiệm vụ: Phân tích hồ sơ trắc nghiệm bên dưới và sinh JSON Wrapped sắc sảo, nam tính, có chất châm biếm nhẹ, hiện đại chuẩn phong cách Spotify Wrapped.\n\n"
        + user_case_file + "\n\n"
        "QUY TẮC NỘI DUNG:\n"
        "1. ĐỘI MŨ BẢO HIỂM: Nếu Q1 là A, TUYỆT ĐỐI KHÔNG ghi 'Đội mũ bảo hiểm nhiều' vào thói quen xấu. Thay bằng: 'Lười che chắn khói bụi', 'Gội đầu qua loa', hoặc 'Dùng dầu gội tiện tay'.\n"
        "2. Chỉ khi Q1 là C hoặc D mới nhắc đến mũ bảo hiểm.\n"
        "3. Độ dài cực kỳ nghiêm ngặt để vừa khung Mobile:\n"
        "   - bad_habits: Đúng 2 ý, mỗi ý DƯỚI 20 KÝ TỰ.\n"
        "   - scalp_impacts: Đúng 2 ý, mỗi ý DƯỚI 20 KÝ TỰ.\n"
        "   - subtitle: Dưới 30 ký tự, không dấu chấm cuối.\n"
        "   - quote: Dưới 55 ký tự.\n"
        "   - strength: Dưới 35 ký tự, có dấu chấm cuối.\n"
        "   - blind_spot: Dưới 35 ký tự, có dấu chấm cuối.\n"
        "   - golden_advice: Dưới 55 ký tự.\n"
        "   - gap_desc: Dưới 35 ký tự.\n"
        "   - body ở slide_2_exposure_condition: Từ 80 - 130 ký tự.\n\n"
        "CHỈ TRẢ VỀ JSON THUẦN (KHÔNG MARKDOWN, KHÔNG ```json):\n"
        "{\n"
        f'  "persona_title": "{arch_title}",\n'
        '  "tagline": "Một câu châm ngôn ngắn sắc lẹm dưới 12 từ",\n'
        f'  "grooming_iq": {grooming_iq},\n'
        f'  "authentic_man_pct": {authentic_man_pct},\n'
        '  "slides": {\n'
        '    "slide_1_age_shock": {\n'
        f'      "headline": "Tuổi chân tóc: {hair_stress_age}",\n'
        '      "body": "Áp lực môi trường làm nang tóc già trước tuổi."\n'
        '    },\n'
        '    "slide_2_exposure_condition": {\n'
        '      "headline": "Môi trường thử thách",\n'
        '      "body": "Đoạn 2 câu mô tả áp lực bụi bẩn và dầu nhờn ảnh hưởng nang tóc."\n'
        '    },\n'
        '    "slide_3_grooming_gap": {\n'
        '      "headline": "The Grooming Gap",\n'
        '      "body": "Bóc trần sự lệch pha giữa tiêu chuẩn lý tưởng và thực tế trong phòng tắm.",\n'
        '      "bad_habits": ["Ý 1 ngắn", "Ý 2 ngắn"],\n'
        '      "scalp_impacts": ["Tác động 1", "Tác động 2"],\n'
        '      "gap_desc": "Khoảng cách giữa tiêu chuẩn lý tưởng và hành vi tiện tay."\n'
        '    },\n'
        '    "slide_4_final_card": {\n'
        f'      "archetype_title": "{arch_title}",\n'
        '      "subtitle": "Slogan phụ ngắn dí dỏm",\n'
        '      "quote": "Châm ngôn súc tích về bản lĩnh chăm sóc tóc",\n'
        '      "strength": "Điểm mạnh nổi bật nhất.",\n'
        '      "blind_spot": "Điểm mù cần khắc phục.",\n'
        '      "golden_advice": "Lời khuyên đắt giá giải quyết vấn đề
