from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
import logging

from .config import GEMINI_FLASH, retry_config
from .tools import normalize_user_query_guardrail, \
                ktp_lookup_tools, \
                ktp_aggregation_tools, \
                visualization_tools

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

root_agent = LlmAgent(
    model=Gemini(
        model=GEMINI_FLASH,
        retry_options=retry_config
    ),
    name='root_agent',
    description='Asisten untuk menjawab pertanyaan user seputar data KTP.',
    instruction=(
        '- Jawab pertanyaan user seputar data KTP dengan akurat dan informatif menggukan tools yang tersedia.\n'),
    tools=[
        ktp_lookup_tools,
        ktp_aggregation_tools,
        visualization_tools
        ],
    before_model_callback=normalize_user_query_guardrail
)
