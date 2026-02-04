from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.agent_tool import AgentTool

from ...config import GEMINI_FLASH, retry_config
from ...tools import lookup_tools

lookup_agent = LlmAgent(
    model=Gemini(
        model=GEMINI_FLASH,
        retry_options=retry_config
    ),
    name='lookup_agent',
    description='Asisten untuk mencari data KTP berdasarkan NIK atau atribut lainnya.\n',
    instruction='Gunakan `lookup_tools` untuk mencari data KTP berdasarkan NIK atau atribut lainnya.\n',
    tools=lookup_tools,
    output_key='lookup_result'
)

ktp_lookup_tools = AgentTool(agent=lookup_agent)