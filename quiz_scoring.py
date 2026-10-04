# quiz_scoring.py
from typing import Dict, Any, Tuple
from quiz_metadata import QUIZ_QUESTIONS_MAP, ARCHETYPES_INFO

def evaluate_root_exposure(q1_opt: str, q2_opt: str) -> Tuple[int, str]:
    """
    Trục A: ROOT EXPOSURE
    Tổng hợp áp lực từ thời gian đội mũ bảo hiểm (Q1) và môi trường sống (Q2).
    """
    score_q1 = QUIZ_QUESTIONS_MAP["Q1"]["options"].get(q1_opt, {}).get("exposure_score", 1)
    score_q2 = QUIZ_QUESTIONS_MAP["Q2"]["options"].get(q2_opt, {}).get("exposure_score", 1)
    total_exposure = score_q1 + score_q2  # Thang từ 2 đến 8

    if total_exposure <= 3:
        level = "Low"
    elif total_exposure <= 5:
        level = "Moderate"
    elif total_exposure <= 7:
        level = "High"
    else:
        level = "Extreme"

    return total_exposure, level

def evaluate_current_condition(q3_opt: str, q4_opt: str) -> Tuple[str, str, int, int]:
    """
    Trục B: CURRENT CONDITION
    Xác định Scalp Profile (Q3) và mức độ lo lắng rụng tóc (Q4).
    """
    q3_data = QUIZ_QUESTIONS_MAP["Q3"]["options"].get(q3_opt, {})
    scalp_profile = q3_data.get("profile", "Clean & Balanced")
    condition_severity = q3_data.get("condition_severity", 0)

    q4_data = QUIZ_QUESTIONS_MAP["Q4"]["options"].get(q4_opt, {})
    hair_fall_alert = q4_data.get("fall_alert", "Normal Shedding")
    aging_impact = q4_data.get("aging_impact", 1)

    return scalp_profile, hair_fall_alert, condition_severity, aging_impact

def calculate_hair_stress_age(user_age: int, exposure_level: str, aging_impact: int) -> Tuple[int, int]:
    """
    Tính Hair Stress Age (Tuổi sinh học chân tóc chịu tải).
    Tạo độ co giãn chênh lệch rõ ràng:
    - Nếu giữ gìn, ít phơi nhiễm: Trẻ hơn tuổi thật (-3 đến -1 tuổi)
    - Nếu phơi nhiễm cao, rụng tóc nhiều: Già hơn tuổi thật (+3 đến +8 tuổi)
    """
    # Mức độ phơi nhiễm môi trường (Q1 + Q2)
    exposure_delta_map = {
        "Low": -2,
        "Moderate": 1,
        "High": 3,
        "Extreme": 5
    }
    exposure_delta = exposure_delta_map.get(exposure_level, 1)

    # Tác động rụng tóc (Q4)
    aging_delta_map = {
        0: -1,  # Gần như không rụng
        1: 0,   # Rụng bình thường
        2: 2,   # Rụng khá nhiều
        3: 4    # Rụng báo động
    }
    fall_delta = aging_delta_map.get(aging_impact, 1)

    delta_age = exposure_delta + fall_delta

    # Khống chế biên độ hợp lý từ -3 tuổi đến +9 tuổi
    delta_age = min(9, max(-3, delta_age))
    hair_stress_age = max(1, user_age + delta_age)

    return hair_stress_age, delta_age

def evaluate_grooming_behavior(q5_opt: str, q6_opt: str) -> Tuple[float, float, int, str]:
    """
    Trục C: GROOMING BEHAVIOR & GROOMING GAP
    Đo lường tỷ lệ Root Problem-Solving vs Fragrance-Masking, đồng thời tìm độ vênh giữa kỳ vọng và thực tế.
    """
    q5_score = QUIZ_QUESTIONS_MAP["Q5"]["options"].get(q5_opt, {}).get("behavior_score", 0)
    q6_score = QUIZ_QUESTIONS_MAP["Q6"]["options"].get(q6_opt, {}).get("action_score", 0)

    # Hành vi thực tế (Q6) có trọng số cao hơn nhận định ban đầu (Q5)
    root_solving_pct = round((q5_score * 0.40) + (q6_score * 0.60), 1)
    fragrance_masking_pct = round(100.0 - root_solving_pct, 1)

    # Đo độ lệch Grooming Gap
    gap_value = q5_score - q6_score
    if gap_value >= 40:
        gap_insight = "Khoảng cách lớn: Coi trọng công dụng/thành phần trên lý thuyết, nhưng thực tế tiện đâu xài đó."
    elif gap_value >= 20:
        gap_insight = "Khoảng cách trung bình: Có nhận thức về giải pháp nhưng hành vi mua sắm còn bị chi phối bởi thói quen."
    elif gap_value <= -20:
        gap_insight = "Hành động vượt kỳ vọng: Chăm sóc thực tế kỹ lưỡng hơn cả tiêu chuẩn tự đặt ra."
    else:
        gap_insight = "Nhất quán cao: Hành động thực tế phản ánh chính xác tiêu chí lựa chọn sản phẩm."

    return root_solving_pct, fragrance_masking_pct, gap_value, gap_insight

def calculate_grooming_iq(mindset_score: int, root_solving_pct: float, condition_severity: int) -> int:
    """
    Trục D: GROOMING MINDSET & GROOMING IQ
    Tổng hợp Grooming IQ (/100) từ Mindset (35%), Hành vi thực tế (45%) và Mức độ kiểm soát da đầu (20%).
    """
    condition_control_score = max(0, 100 - (condition_severity * 25))
    iq = (mindset_score * 0.35) + (root_solving_pct * 0.45) + (condition_control_score * 0.20)
    return int(round(min(100, max(10, iq))))

def determine_archetype(root_solving_pct: float, mindset_score: int, q5_opt: str, q6_opt: str) -> Dict[str, Any]:
    """
    Phân loại 3 Grooming Mindsets:
    1. The Cover-Up Man: Fragrance-Masking chiếm đa số hoặc chọn sp/hành vi thuần mùi thơm.
    2. The Root Man: Nhận thức thành phần, chủ động giải quyết gốc rễ.
    3. The Routine Man: Có thói quen tốt nhưng chọn theo thói quen/công dụng chung.
    """
    if root_solving_pct < 40.0 or (q5_opt == "A" and q6_opt in ["A", "C"]):
        return ARCHETYPES_INFO["cover_up_man"]
    elif root_solving_pct >= 75.0 and mindset_score >= 80:
        return ARCHETYPES_INFO["root_man"]
    else:
        return ARCHETYPES_INFO["routine_man"]

def calculate_quiz_results(user_age: int, answers: Dict[str, str]) -> Dict[str, Any]:
    ans = {k.upper(): v.upper() for k, v in answers.items()}

    # Trục A: Root Exposure
    exposure_points, exposure_level = evaluate_root_exposure(ans.get("Q1", "B"), ans.get("Q2", "B"))

    # Trục B: Current Condition
    scalp_profile, hair_fall_alert, condition_severity, aging_impact = evaluate_current_condition(
        ans.get("Q3", "B"), ans.get("Q4", "B")
    )

    # Hair Stress Age
    hair_stress_age, delta_age = calculate_hair_stress_age(user_age, exposure_level, aging_impact)

    # Trục C: Grooming Behavior & Grooming Gap
    root_solving_pct, fragrance_masking_pct, gap_val, gap_insight = evaluate_grooming_behavior(
        ans.get("Q5", "B"), ans.get("Q6", "B")
    )

    # Trục D: Grooming Mindset & Grooming IQ
    mindset_data = QUIZ_QUESTIONS_MAP["Q7"]["options"].get(ans.get("Q7", "B"), {})
    mindset_score = mindset_data.get("mindset_score", 40)
    mindset_stage = mindset_data.get("mindset_stage", "Presentability")

    grooming_iq = calculate_grooming_iq(mindset_score, root_solving_pct, condition_severity)

    # CHỈ SỐ BẢN LĨNH ĐÀN ÔNG ĐÍCH THỰC (0 - 100%) THEO CHUẨN LEADER
    # Kết hợp giữa mức độ giải quyết gốc rễ (70%) và nhận thức grooming (30%)
    authentic_man_pct = int(round((root_solving_pct * 0.70) + (mindset_score * 0.30)))

    # Phân nhóm Archetype
    archetype = determine_archetype(root_solving_pct, mindset_score, ans.get("Q5", "B"), ans.get("Q6", "B"))

    return {
        "user_age": user_age,
        "hair_stress_age": hair_stress_age,
        "delta_age": delta_age,
        "grooming_iq": grooming_iq,
        "authentic_man_pct": authentic_man_pct,  # <-- Thêm chỉ số % này
        "dimensions": {
            "root_exposure": {
                "score": exposure_points,
                "level": exposure_level
            },
            "current_condition": {
                "scalp_profile": scalp_profile,
                "hair_fall_alert": hair_fall_alert,
                "condition_severity": condition_severity
            },
            "grooming_behavior": {
                "root_problem_solving_pct": root_solving_pct,
                "fragrance_masking_pct": fragrance_masking_pct,
                "grooming_gap_score": gap_val,
                "grooming_gap_insight": gap_insight
            },
            "grooming_mindset": {
                "score": mindset_score,
                "stage": mindset_stage
            }
        },
        "archetype": archetype,
        "raw_answers": ans
    }
