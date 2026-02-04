from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
import logging

from .config import GEMINI_FLASH, retry_config
from .sub_agents.aggregation_agent.agent import ktp_aggregation_tools
from .sub_agents.extraction_agent.agent import ktp_extraction_tools
from .sub_agents.lookup_agent.agent import ktp_lookup_tools
from .sub_agents.ingestion_agent.agent import ktp_ingestion_tools
from .sub_agents.visualization_agent.agent import visualization_tools
from .tools import normalize_user_query_guardrail, \
                censor_pii_callback

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
        ktp_extraction_tools,
        ktp_ingestion_tools,
        visualization_tools
        ],
    before_model_callback=normalize_user_query_guardrail,
    after_model_callback=censor_pii_callback
)