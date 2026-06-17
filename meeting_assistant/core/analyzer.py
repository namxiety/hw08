import json
from openai import OpenAI
from typing import Dict

class MeetingAnalyzer:
    """使用大模型对会议转写文本进行结构化分析"""
    
    SYSTEM_PROMPT = """
你是一个专业的会议纪要整理助手。请根据用户提供的会议转写文本，生成结构化的会议纪要。

输出格式为 JSON，必须包含以下字段：
{
    "title": "会议主题（一句话概括）",
    "date": "会议日期（从文本中推断，若无则填今天）",
    "attendees": ["参会人员名单"],
    "summary": "会议摘要（200字以内，突出重点）",
    "key_points": ["关键观点1", "关键观点2", ...],
    "decisions": ["决策1", "决策2", ...],
    "action_items": [
        {"task": "待办事项", "assignee": "负责人", "deadline": "截止日期"}
    ],
    "next_steps": ["后续步骤1", "后续步骤2"]
}

注意事项：
1. 若文本中未提及某些字段，请合理推断或留空
2. 待办事项必须从原文中提取，不可凭空捏造
3. 输出必须是合法的 JSON 格式
"""
    
    def __init__(self, api_key: str, base_url: str, model: str):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
    
    def analyze(self, transcript: str) -> Dict:
        """分析转写文本，生成结构化纪要"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": f"会议转写文本：\n{transcript}"}
            ],
            temperature=0.3,  # 低温度保证输出稳定
            response_format={"type": "json_object"}  # 强制 JSON 输出
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
