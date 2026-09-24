# /Users/anhnt/Documents/pythoncode/warp/quiz_metadata.py


QUIZ_QUESTIONS_MAP = {
   # DIMENSION A: ROOT EXPOSURE
   "Q1": {
       "dimension": "ROOT_EXPOSURE",
       "title": "Mức độ chịu đựng của tóc dưới mũ bảo hiểm",
       "question": "Ngày thường, bạn thường đội mũ bảo hiểm khoảng bao lâu?",
       "options": {
           "A": {
               "label": "Dưới 30 phút",
               "detail": "Áp lực nhiệt và ma sát thấp",
               "exposure_score": 1
           },
           "B": {
               "label": "30 phút – 1 giờ",
               "detail": "Áp lực nhiệt và mồ hôi mức trung bình",
               "exposure_score": 2
           },
           "C": {
               "label": "1 – 2 giờ",
               "detail": "Hầm bí nhiệt, ma sát và tích tụ mồ hôi cao",
               "exposure_score": 3
           },
           "D": {
               "label": "Hơn 2 giờ",
               "detail": "Môi trường cực hạn: bít tắc nang lông, ma sát liên tục",
               "exposure_score": 4
           }
       }
   },
   "Q2": {
       "dimension": "ROOT_EXPOSURE",
       "title": "Môi trường sống và làm việc chính trong ngày",
       "question": "Phần lớn một ngày của bạn diễn ra ở đâu?",
       "options": {
           "A": {
               "label": "Phòng máy lạnh — học/làm trong nhà gần như cả ngày",
               "detail": "Không khí khô hanh, mất cân bằng ẩm",
               "exposure_score": 1
           },
           "B": {
               "label": "Trong nhà nhưng thường xuyên di chuyển ngoài đường",
               "detail": "Sốc nhiệt điều hòa kết hợp khói bụi giao thông",
               "exposure_score": 2
           },
           "C": {
               "label": "Ngoài trời khá nhiều",
               "detail": "Bức xạ UV cao, mồ hôi và khói bụi liên tục",
               "exposure_score": 3
           },
           "D": {
               "label": "Ngoài trời / vận động / công việc thể chất là chính",
               "detail": "Tuyến bã nhờn và mồ hôi quá tải dưới nhiệt độ cao",
               "exposure_score": 4
           }
       }
   },


   # DIMENSION B: CURRENT CONDITION
   "Q3": {
       "dimension": "CURRENT_CONDITION",
       "title": "Tình trạng da đầu cuối ngày",
       "question": "Cuối ngày, tình trạng da đầu của bạn thường giống nhất với mô tả nào?",
       "options": {
           "A": {
               "label": "Vẫn sạch và khô thoáng",
               "signal": "Low oil",
               "profile": "Clean & Balanced",
               "condition_severity": 0
           },
           "B": {
               "label": "Hơi bết nhưng không khó chịu",
               "signal": "Moderate oil",
               "profile": "Moderate Oil",
               "condition_severity": 1
           },
           "C": {
               "label": "Bết rõ, tóc dễ xẹp",
               "signal": "High sebum",
               "profile": "Oil-Prone",
               "condition_severity": 2
           },
           "D": {
               "label": "Bết + ngứa / khó chịu",
               "signal": "Oil + irritation",
               "profile": "Oil & Irritation",
               "condition_severity": 3
           },
           "E": {
               "label": "Có vảy/gàu nhìn thấy được",
               "signal": "Flaking",
               "profile": "Flaking & Dandruff",
               "condition_severity": 3
           }
       }
   },
   "Q4": {
       "dimension": "CURRENT_CONDITION",
       "title": "Nhận thức về mức độ rụng tóc (Perceived Hair-Fall Stress)",
       "question": "Sau khi gội đầu, bạn có thường xuyên gặp tình trạng tóc rụng không?",
       "options": {
           "A": {
               "label": "Gần như không để ý thấy",
               "fall_alert": "Low / Minimal",
               "aging_impact": 0
           },
           "B": {
               "label": "Có vài sợi, bình thường",
               "fall_alert": "Normal Shedding",
               "aging_impact": 1
           },
           "C": {
               "label": "Khá nhiều, bắt đầu để ý",
               "fall_alert": "Moderate Hair-Fall Alert",
               "aging_impact": 3
           },
           "D": {
               "label": "Nhiều đến mức tôi thực sự lo",
               "fall_alert": "High Hair-Fall Stress",
               "aging_impact": 6
           }
       }
   },


   # DIMENSION C: GROOMING BEHAVIOR (Grooming Gap: Stated vs. Actual)
   "Q5": {
       "dimension": "GROOMING_BEHAVIOR",
       "title": "Tiêu chí ưu tiên khi chọn sản phẩm (Stated Value)",
       "question": "Khi chọn một sản phẩm grooming, thứ bạn nhìn vào đầu tiên là gì?",
       "options": {
           "A": {
               "label": "Mùi thơm - thơm là thắng",
               "behavior_score": 0,
               "focus": "Fragrance Only"
           },
           "B": {
               "label": "Cảm giác sau khi dùng (mát lạnh, sảng khoái)",
               "behavior_score": 25,
               "focus": "Sensory Experience"
           },
           "C": {
               "label": "Công dụng - sạch, giảm dầu, giảm gàu...",
               "behavior_score": 60,
               "focus": "Function-Driven"
           },
           "D": {
               "label": "Thành phần / Active ingredients",
               "behavior_score": 85,
               "focus": "Active Ingredients"
           },
           "E": {
               "label": "Combo cả công dụng + thành phần",
               "behavior_score": 100,
               "focus": "Holistic Root Solution"
           }
       }
   },
   "Q6": {
       "dimension": "GROOMING_BEHAVIOR",
       "title": "Hành động thực tế trong phòng tắm (Actual Action - Bathroom Test)",
       "question": "Nếu chai dầu gội/sữa tắm hiện tại hết hôm nay, bạn sẽ...",
       "options": {
           "A": {
               "label": "Lấy đại chai khác trong nhà dùng",
               "action_score": 0,
               "action_type": "Convenience Default"
           },
           "B": {
               "label": "Mua đúng chai cũ",
               "action_score": 40,
               "action_type": "Habitual Routine"
           },
           "C": {
               "label": "Ra cửa hàng chọn chai có mùi mình thích",
               "action_score": 20,
               "action_type": "Scent-Led Impulse"
           },
           "D": {
               "label": "Tìm sản phẩm giải quyết đúng vấn đề mình đang gặp",
               "action_score": 80,
               "action_type": "Problem-Oriented Search"
           },
           "E": {
               "label": "Check thành phần/công dụng rồi mới mua",
               "action_score": 100,
               "action_type": "Informed Active Choice"
           }
       }
   },


   # DIMENSION D: GROOMING MINDSET
   "Q7": {
       "dimension": "GROOMING_MINDSET",
       "title": "Định nghĩa bản lĩnh đàn ông qua Grooming",
       "question": "Theo bạn, Grooming thực chất là gì?",
       "options": {
           "A": {
               "label": "Thơm để người khác thấy dễ chịu",
               "mindset_score": 20,
               "mindset_stage": "Appearance & Scent"
           },
           "B": {
               "label": "Gọn gàng để trông có phong độ",
               "mindset_score": 40,
               "mindset_stage": "Presentability"
           },
           "C": {
               "label": "Chăm sóc bản thân để tự tin hơn",
               "mindset_score": 60,
               "mindset_stage": "Self-Confidence"
           },
           "D": {
               "label": "Hiểu cơ thể mình và giải quyết đúng vấn đề của nó",
               "mindset_score": 85,
               "mindset_stage": "Root Problem-Solving"
           },
           "E": {
               "label": "Không cần ai nhắc — tự biết mình cần gì và chủ động chăm sóc",
               "mindset_score": 100,
               "mindset_stage": "Proactive Mastery"
           }
       }
   }
}


ARCHETYPES_INFO = {
   "cover_up_man": {
       "code": "cover_up_man",
       "title": "THE COVER-UP MAN",
       "subtitle": "Thơm trước. Tính sau.",
       "quote": "Bạn đang dùng grooming để che đi vấn đề nhiều hơn là thực sự xử lý nó.",
       "strength": "Rất nhạy bén với ấn tượng ban đầu, luôn chỉn chu về hương thơm và vẻ ngoài.",
       "blind_spot": "Dễ ưu tiên mùi hương để ngụy trang thay vì nhìn sâu vào vấn đề cốt lõi của da đầu.",
       "product_route": "cover_up_upgrade"
   },
   "routine_man": {
       "code": "routine_man",
       "title": "THE ROUTINE MAN",
       "subtitle": "Biết chăm, nhưng chưa hiểu hết.",
       "quote": "Bạn đã qua giai đoạn 'dùng gì cũng được'. Bước tiếp theo là hiểu cơ thể mình sâu hơn.",
       "strength": "Duy trì thói quen chăm sóc đều đặn, chú trọng sự sạch sẽ và gọn gàng.",
       "blind_spot": "Dễ làm theo quán tính hoặc chọn theo công dụng chung mà chưa hiểu rõ cơ thể cần hoạt chất gì.",
       "product_route": "routine_optimize"
   },
   "root_man": {
       "code": "root_man",
       "title": "THE ROOT MAN",
       "subtitle": "Không đoán. Hiểu rồi xử lý.",
       "quote": "Bạn không chỉ chăm sóc để nhìn ổn. Ông biết đích xác mình đang chăm sóc cái gì.",
       "strength": "Tư duy giải quyết gốc rễ vấn đề, am hiểu hoạt chất và chủ động bảo vệ cơ thể.",
       "blind_spot": "Đôi khi quá tập trung vào bảng thành phần hoặc soi xét vấn đề nhỏ mà quên tận hưởng cảm giác thoải mái.",
       "product_route": "root_ecosystem"
   }
}

