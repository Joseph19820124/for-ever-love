# my_test_classification.py

from pydantic import BaseModel, Field
from langchain_xai import ChatXAI
from langchain_core.messages import HumanMessage

# 定义 Pydantic 模型
class Classification(BaseModel):
    """示例：对文本进行情感分类"""
    label: str = Field(..., description="分类标签，如 positive/negative/neutral")
    score: float = Field(..., description="置信度评分，取值范围 0.0–1.0")

# 初始化 xAI Grok LLM
llm = ChatXAI(model="grok-2-1212", api_key="xai-mNspB9zseaONfsKoPdjIzjhgc6YBGSJtROpMig9CRJWvRPfbscKqyFoVvusRZSK22e9Fy2e1YFrVQEDN")  # 替换为真实 API Key

# 使用结构化输出
structured_llm = llm.with_structured_output(Classification)

# 调用并获取结果
response: Classification = structured_llm.invoke(
    [HumanMessage(content="这是一条测试情感分析的文本。")]
)

print("Label:", response.label)
print("Score:", response.score)