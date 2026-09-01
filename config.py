"""办公文档助手配置。"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """全局配置。"""

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    CHAT_MODEL: str = os.getenv("CHAT_MODEL", "gpt-4o-mini")

    # 摘要相关
    SUMMARY_CHAR_LIMIT: int = 3000   # 每块摘要的最大字符数
    DEFAULT_POINTS: int = 3          # 默认要点数量

    @classmethod
    def has_llm(cls) -> bool:
        return bool(cls.OPENAI_API_KEY)
