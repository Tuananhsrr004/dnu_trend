from __future__ import annotations
from typing import List, Dict
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Simple domain knowledge base for majors
MAJOR_DESCRIPTIONS: Dict[str, str] = {
    'Công nghệ thông tin': 'lập trình, phần mềm, dữ liệu, trí tuệ nhân tạo, hệ thống, mạng máy tính, bảo mật',
    'Quản trị kinh doanh': 'kinh doanh, marketing, quản lý, tài chính, bán hàng, khởi nghiệp',
    'Dược học': 'y tế, thuốc, dược phẩm, nghiên cứu lâm sàng, chăm sóc sức khỏe',
    'Ngôn ngữ Anh': 'tiếng Anh, ngôn ngữ, dịch thuật, giao tiếp, văn hóa, sư phạm',
    'Tài chính - Ngân hàng': 'tài chính, ngân hàng, đầu tư, chứng khoán, kế toán, phân tích rủi ro',
}

# Rule-based hint mapping
KEYWORD_TO_MAJOR = {
    'code': 'Công nghệ thông tin', 'lập trình': 'Công nghệ thông tin', 'ai': 'Công nghệ thông tin', 'data': 'Công nghệ thông tin',
    'kinh doanh': 'Quản trị kinh doanh', 'marketing': 'Quản trị kinh doanh', 'quản lý': 'Quản trị kinh doanh',
    'thuốc': 'Dược học', 'y tế': 'Dược học', 'sức khỏe': 'Dược học',
    'tiếng anh': 'Ngôn ngữ Anh', 'ngoại ngữ': 'Ngôn ngữ Anh', 'dịch': 'Ngôn ngữ Anh',
    'tài chính': 'Tài chính - Ngân hàng', 'ngân hàng': 'Tài chính - Ngân hàng', 'đầu tư': 'Tài chính - Ngân hàng',
}


def suggest_majors(text: str, score: float | None = None, top_k: int = 3) -> List[Dict]:
    """Return ranked major suggestions based on interests and optional score."""
    text_norm = (text or '').lower()

    # 1) Rule-based bonus
    rule_bonus = {m: 0.0 for m in MAJOR_DESCRIPTIONS}
    for k, m in KEYWORD_TO_MAJOR.items():
        if k in text_norm:
            rule_bonus[m] += 0.25

    # Optional score-based heuristic (very rough)
    # high score -> STEM/Finance; medium -> Business/Language; lower -> Language/Business
    if score is not None:
        try:
            s = float(score)
            if s >= 24:
                rule_bonus['Công nghệ thông tin'] += 0.2
                rule_bonus['Tài chính - Ngân hàng'] += 0.2
            elif s >= 21:
                rule_bonus['Quản trị kinh doanh'] += 0.15
            else:
                rule_bonus['Ngôn ngữ Anh'] += 0.15
        except Exception:
            pass

    # 2) Embedding with TF-IDF
    majors = list(MAJOR_DESCRIPTIONS.keys())
    corpus = [MAJOR_DESCRIPTIONS[m] for m in majors] + [text_norm]
    vec = TfidfVectorizer().fit_transform(corpus)
    sims = cosine_similarity(vec[-1], vec[:-1]).flatten()

    scores = []
    for m, sim in zip(majors, sims):
        total = float(sim) + rule_bonus.get(m, 0.0)
        scores.append({'major': m, 'score': round(total, 4), 'explain': {
            'similarity': float(sim), 'rule_bonus': round(rule_bonus.get(m, 0.0), 3)
        }})
    scores.sort(key=lambda x: x['score'], reverse=True)
    return scores[:top_k]


def llm_proxy_suggestion(text: str) -> str:
    """Optional: format a prompt that can be sent to an external LLM; here we just return the prompt string.
    Do NOT call external services automatically. Users can take this prompt to their LLM provider.
    """
    prompt = (
        "Bạn là cố vấn hướng nghiệp. Từ mô tả sở thích sau, gợi ý 3 ngành phù hợp ở Đại học Đại Nam, kèm lý do ngắn.\n"
        f"Sở thích/điểm mạnh: {text}\n"
        f"Các ngành: {', '.join(MAJOR_DESCRIPTIONS.keys())}"
    )
    return prompt
