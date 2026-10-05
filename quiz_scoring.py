# quiz_scoring.py
from typing import Dict, Any, Tuple
from quiz_metadata import QUIZ_QUESTIONS_MAP, ARCHETYPES_INFO

def evaluate_root_exposure(q1_opt: str, q2_opt: str) -> Tuple[int, str]:
    """
    Dimension A: ROOT EXPOSURE
    Aggregates environmental stressors from helmet-wearing duration (Q1) and daily surroundings (Q2).
    """
    score_q1 = QUIZ_QUESTIONS_MAP["Q1"]["options"].get(q1_opt, {}).get("exposure_score", 1)
    score_q2 = QUIZ_QUESTIONS_MAP["Q2"]["options"].get(q2_opt, {}).get("exposure_score", 1)
    total_exposure = score_q1 + score_q2  # Scale from 2 to 8

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
    Dimension B: CURRENT CONDITION
    Identifies Scalp Profile (Q3) and hair shedding / hair-fall risk level (Q4).
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
    Computes Hair Stress Age (biological scalp stress index).
    Establishes dynamic variance relative to chronological age:
    - Low exposure & healthy care: Younger than actual age (-3 to -1 years)
    - High environmental stress & severe hair shedding: Older than actual age (+3 to +8 years)
    """
    # Environmental exposure adjustment factor (Q1 + Q2)
    exposure_delta_map = {
        "Low": -2,
        "Moderate": 1,
        "High": 3,
        "Extreme": 5
    }
    exposure_delta = exposure_delta_map.get(exposure_level, 1)

    # Hair shedding impact adjustment factor (Q4)
    aging_delta_map = {
        0: -1,  # Minimal / negligible shedding
        1: 0,   # Normal physiological shedding
        2: 2,   # Moderate shedding
        3: 4    # Critical / heavy shedding
    }
    fall_delta = aging_delta_map.get(aging_impact, 1)

    delta_age = exposure_delta + fall_delta

    # Constrain delta range between -3 and +9 years for reasonable variance
    delta_age = min(9, max(-3, delta_age))
    hair_stress_age = max(1, user_age + delta_age)

    return hair_stress_age, delta_age

def evaluate_grooming_behavior(q5_opt: str, q6_opt: str) -> Tuple[float, float, int, str]:
    """
    Dimension C: GROOMING BEHAVIOR & GROOMING GAP
    Measures the ratio of Root Problem-Solving vs. Fragrance-Masking,
    and quantifies the divergence between declared criteria and actual purchasing habit.
    """
    q5_score = QUIZ_QUESTIONS_MAP["Q5"]["options"].get(q5_opt, {}).get("behavior_score", 0)
    q6_score = QUIZ_QUESTIONS_MAP["Q6"]["options"].get(q6_opt, {}).get("action_score", 0)

    # Practical behavior (Q6) carries higher empirical weight than perceived priority (Q5)
    root_solving_pct = round((q5_score * 0.40) + (q6_score * 0.60), 1)
    fragrance_masking_pct = round(100.0 - root_solving_pct, 1)

    # Calculate Grooming Gap disparity metric
    gap_value = q5_score - q6_score
    if gap_value >= 40:
        gap_insight = "High Disparity: Values active ingredients theoretically, but acts on passive convenience."
    elif gap_value >= 20:
        gap_insight = "Moderate Disparity: Solution-aware, but practical choices remain swayed by baseline habits."
    elif gap_value <= -20:
        gap_insight = "Action-Oriented: Practical grooming discipline exceeds self-stated standards."
    else:
        gap_insight = "High Alignment: Practical behavior directly mirrors stated product selection criteria."

    return root_solving_pct, fragrance_masking_pct, gap_value, gap_insight

def calculate_grooming_iq(mindset_score: int, root_solving_pct: float, condition_severity: int) -> int:
    """
    Dimension D: GROOMING MINDSET & GROOMING IQ
    Synthesizes overall Grooming IQ (/100) from Mindset (35%),
    Root-Solving Behavior (45%), and Scalp Condition Management (20%).
    """
    condition_control_score = max(0, 100 - (condition_severity * 25))
    iq = (mindset_score * 0.35) + (root_solving_pct * 0.45) + (condition_control_score * 0.20)
    return int(round(min(100, max(10, iq))))

def determine_archetype(root_solving_pct: float, mindset_score: int, q5_opt: str, q6_opt: str) -> Dict[str, Any]:
    """
    Classifies respondents into 3 core Grooming Mindset Archetypes:
    1. The Cover-Up Man: Fragrance-Masking dominant; prioritizes scent over follicle health.
    2. The Root Man: Ingredient-conscious; actively targets root-cause scalp problems.
    3. The Routine Man: Established hygiene habits, but follows conventional generic routines.
    """
    if root_solving_pct < 40.0 or (q5_opt == "A" and q6_opt in ["A", "C"]):
        return ARCHETYPES_INFO["cover_up_man"]
    elif root_solving_pct >= 75.0 and mindset_score >= 80:
        return ARCHETYPES_INFO["root_man"]
    else:
        return ARCHETYPES_INFO["routine_man"]

def calculate_quiz_results(user_age: int, answers: Dict[str, str]) -> Dict[str, Any]:
    ans = {k.upper(): v.upper() for k, v in answers.items()}

    # Dimension A: Root Exposure
    exposure_points, exposure_level = evaluate_root_exposure(ans.get("Q1", "B"), ans.get("Q2", "B"))

    # Dimension B: Current Condition
    scalp_profile, hair_fall_alert, condition_severity, aging_impact = evaluate_current_condition(
        ans.get("Q3", "B"), ans.get("Q4", "B")
    )

    # Hair Stress Age Calculation
    hair_stress_age, delta_age = calculate_hair_stress_age(user_age, exposure_level, aging_impact)

    # Dimension C: Grooming Behavior & Grooming Gap
    root_solving_pct, fragrance_masking_pct, gap_val, gap_insight = evaluate_grooming_behavior(
        ans.get("Q5", "B"), ans.get("Q6", "B")
    )

    # Dimension D: Grooming Mindset & Grooming IQ
    mindset_data = QUIZ_QUESTIONS_MAP["Q7"]["options"].get(ans.get("Q7", "B"), {})
    mindset_score = mindset_data.get("mindset_score", 40)
    mindset_stage = mindset_data.get("mindset_stage", "Presentability")

    grooming_iq = calculate_grooming_iq(mindset_score, root_solving_pct, condition_severity)

    # AUTHENTIC RESILIENCE INDEX (0 - 100%)
    # Weighted composite of root-cause resolution (70%) and strategic mindset awareness (30%)
    authentic_man_pct = int(round((root_solving_pct * 0.70) + (mindset_score * 0.30)))

    # Archetype Classification
    archetype = determine_archetype(root_solving_pct, mindset_score, ans.get("Q5", "B"), ans.get("Q6", "B"))

    return {
        "user_age": user_age,
        "hair_stress_age": hair_stress_age,
        "delta_age": delta_age,
        "grooming_iq": grooming_iq,
        "authentic_man_pct": authentic_man_pct,
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
