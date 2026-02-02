import os
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.models import LlmResponse, LlmRequest
from google.adk.models.google_llm import Gemini
from google.adk.tools.agent_tool import AgentTool
from typing import Optional
from google.genai import types 
from google.genai.types import Part
from google import genai
from toolbox_core import ToolboxSyncClient

from .config import GEMINI_MODEL, retry_config

def normalize_user_query_guardrail(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """Inspects/modifies the LLM request or skips the call."""
    agent_name = callback_context.agent_name
    print(f"[Callback] Before model call for agent: {agent_name}")

    # Inspect the last user message in the request contents
    last_user_message = ""
    if llm_request.contents and llm_request.contents[-1].role == 'user':
         if llm_request.contents[-1].parts:
            last_user_message = llm_request.contents[-1].parts[0].text
    print(f"[Callback] Inspecting last user message: '{last_user_message}'")

    if not last_user_message:
        return None

    # Fix typos and expand acronyms in the last user message
    client = genai.Client()
    response = client.models.generate_content(
            model= GEMINI_MODEL,
            contents=[
                Part.from_text(
                    text=f"""Please normalize the following user query by fixing typos and expanding common Indonesian acronyms to their full form.

                    Examples:
                    - "jatim" should become "JAWA TIMUR"
                    - "keb. baru" should become "KEBAYORAN BARU"
                    - "Jaksel" should become "JAKARTA SELATAN"                

                    User query: "{last_user_message}"

                    If no normalization is needed, just return the original user query.

                    Normalized query:"""
                ),
            ],
        )

    if response and response.text:
        normalized_message = response.text.strip()
        print(f"[Callback] Normalized user message to: '{normalized_message}'")
        # Modify the llm_request with the normalized message
        if llm_request.contents and llm_request.contents[-1].role == 'user':
            if llm_request.contents[-1].parts:
                llm_request.contents[-1].parts[0].text = normalized_message
    else:
        print("[Callback] Normalization failed or produced no output.")

    return None

# Initialize Toolbox client
TOOLBOX_URL = os.getenv("TOOLBOX_URL", "http://34.101.127.72:5001")

toolbox = ToolboxSyncClient(TOOLBOX_URL)

lookup_tools = toolbox.load_toolset('ktp_lookup_toolset')
aggregation_tools = toolbox.load_toolset('aggregate_toolset')

lookup_agent = LlmAgent(
    model=Gemini(
        model=GEMINI_MODEL,
        retry_options=retry_config
    ),
    name='lookup_agent',
    description='Asisten untuk mencari data KTP berdasarkan NIK atau atribut lainnya.',
    instruction='Gunakan `lookup_tools` untuk mencari data KTP berdasarkan NIK atau atribut lainnya.',
    tools=lookup_tools,
    output_key='lookup_result'
)

ktp_lookup_tools = AgentTool(agent=lookup_agent)

aggregation_agent = LlmAgent(
    model=Gemini(
        model=GEMINI_MODEL,
        retry_options=retry_config
    ),
    name='aggregation_agent',
    description='Asisten untuk melakukan agregasi data KTP seperti menghitung jumlah, rata-rata, dsb.',
    instruction='Gunakan `aggregation_tools` untuk melakukan agregasi data KTP sesuai permintaan user.',
    tools=aggregation_tools, 
    output_key='aggregation_result'
)   

visualization_agent = LlmAgent(
    model=Gemini(
        model=GEMINI_MODEL,
        retry_options=retry_config
    ),
    name='visualization_agent',
    description='Asisten untuk membuat visualisasi data KTP berdasarkan hasil agregasi.',
    instruction='Buatkan visualisasi data KTP menggunakan Python code berdasarkan {aggregation_result} yang diberikan.'
                'Gunakan library matplotlib atau seaborn untuk membuat visualisasi.'
                'Gunakan pie chart untuk data yang jumlahnya sedikit dan bar chart untuk data yang jumlahnya banyak.',
    tools=[],
    code_executor=BuiltInCodeExecutor(
                                    optimize_data_file=True,
                                    stateful=True
                                      ),
    output_key='visualization_result'
)

summarization_agent = LlmAgent(
    model=Gemini(
        model=GEMINI_MODEL,
        retry_options=retry_config
    ),
    name='summarization_agent',
    description='Asisten untuk membuat ringkasan dari hasil visualisasi data KTP.',
    instruction='Buatkan ringkasan singkat tentang insight yang dapat diambil dari {visualization_result} yang diberikan.',
    output_key='summary_result'
)

aggregation_pipeline = SequentialAgent(
    name='aggregation_pipeline',
    description='Pipeline untuk melakukan agregasi data KTP dan membuat visualisasi berdasarkan hasilnya.',
    sub_agents=[
        aggregation_agent, 
        visualization_agent,
        summarization_agent
        ],
)

ktp_aggregation_tools = AgentTool(agent=aggregation_pipeline)