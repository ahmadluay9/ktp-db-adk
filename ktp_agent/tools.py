import os
from typing import List, Optional
from pydantic import BaseModel, Field

from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.models import LlmResponse, LlmRequest
from google.adk.models.google_llm import Gemini
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.tool_context import ToolContext
import google.genai.types as types
from google.genai.types import Part
from google import genai
from toolbox_core import ToolboxSyncClient

from .config import GEMINI_FLASH, GEMINI_PRO, retry_config

class ArtifactFilename(BaseModel):
    artifact_filename: str = Field(description="The name of the generated visualization file (e.g., chart.png)")

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
            model= GEMINI_FLASH,
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

# tool to load image artifact
async def load_image_artifact(tool_context: ToolContext, artifact_filename: str) -> str:
    """
    Loads an image artifact from the current session so the agent can view and analyze it.
    
    Args:
        artifact_filename: The name of the file to load (e.g., 'chart.png').
    """
    try:
        # Load the artifact from the tool context
        print(artifact_filename)
        artifact = await tool_context.load_artifact(filename=artifact_filename)
        
        if not artifact:
            raise ValueError(f"Artifact '{artifact_filename}' not found.")

        # Return as a Part object for the Gemini model to process visually
        return types.Part(
            inline_data=types.Blob(
                mime_type=artifact.inline_data.mime_type,
                data=artifact.inline_data.data
            )
        )
    except Exception as e:
        return f"Error loading image artifact: {e}"
    
# Initialize Toolbox client
TOOLBOX_URL = os.getenv("TOOLBOX_URL", "http://34.101.127.72:5001")

toolbox = ToolboxSyncClient(TOOLBOX_URL)

lookup_tools = toolbox.load_toolset('ktp_lookup_toolset')
aggregation_tools = toolbox.load_toolset('aggregate_toolset')

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

aggregation_agent = LlmAgent(
    model=Gemini(
        model=GEMINI_FLASH,
        retry_options=retry_config
    ),
    name='aggregation_agent',
    description='Asisten untuk melakukan agregasi data KTP seperti menghitung jumlah, rata-rata, dsb.\n',
    instruction='Gunakan `aggregation_tools` untuk melakukan agregasi data KTP sesuai permintaan user.\n',
    tools=aggregation_tools, 
    output_key='aggregation_result'
)   

visualization_agent = LlmAgent(
    model=Gemini(
        model=GEMINI_PRO,
        retry_options=retry_config
    ),
    name='visualization_agent',
    description='Asisten untuk membuat visualisasi data KTP berdasarkan hasil agregasi.\n',
instruction=(
        'Buatkan HANYA SATU (1) chart yang paling relevan dari data KTP menggunakan Python code '
        'berdasarkan {aggregation_result} yang diberikan.\n'
        '\nATURAN VISUALISASI:\n'
        '1. Gunakan Pie Chart jika kategori <= 5, selain itu gunakan Horizontal Bar Chart.\n'
        '2. Jangan gunakan Donut Chart.\n'
        '3. Jangan menampilkan dua chart sekaligus dalam satu output.\n'
        '4. Untuk Bar Chart, urutkan kategori dari yang terbesar ke terkecil.\n'
'\nATURAN STYLING (Matplotlib Code):\n'
        '1. **Warna Gradient**: Gunakan `colors = plt.cm.Greens(np.linspace(0.4, 0.8, len(data)))`.\n'
        '2. **Figure**: Set `plt.figure(figsize=(12, 8))` agar canvas sangat luas untuk label di luar.\n'
        '3. **Urutan**: Urutkan data dari nilai terbesar ke terkecil.\n'
        '4. **Kebersihan UI**:\n'
        '   - Hapus border atas dan kanan (untuk Bar Chart).\n'
        '   - Tambahkan grid tipis `alpha=0.3`.\n'
        '5. **Tipografi & Readability (UKURAN EKSTRA BESAR)**:\n'
        '   - **Judul**: Wajib `fontsize=26`, `fontweight="bold"`, dan `pad=40`.\n'
        '   - **Legend**: Wajib `fontsize=20`, letakkan di samping chart (`bbox_to_anchor=(1, 1)`).\n'
        '   - **Pie Chart Labels (PENTING)**: \n'
        '     - **POSISI**: Label angka/persen WAJIB di LUAR pie. Gunakan `pctdistance=1.15`.\n'
        '     - **UKURAN**: Gunakan `textprops={"fontsize": 20, "color": "black"}`.\n'
        '   - **Bar Chart Labels**: Gunakan `ax.bar_label(..., fontsize=20, padding=5)`.\n'
        '   - **Ticks Label**: Wajib `fontsize=18`.\n'
        '6. Akhiri dengan `plt.tight_layout()` agar label luar tidak terpotong.'
    ),
    code_executor=BuiltInCodeExecutor(
                                    optimize_data_file=True,
                                    stateful=True
                                      ),
    output_key='visualization_result'
)

artifact_agent = LlmAgent(
    model=Gemini(
        model=GEMINI_FLASH,
        retry_options=retry_config
    ),
    name='artifact_agent',
    description='Asisten untuk menyimpan nama artefak gambar visualisasi.',
    instruction=(
        "Simpan nama artefak gambar {visualization_result} ke dalam output schema `ArtifactFilename`.\n"
    ),
    output_schema=ArtifactFilename,
    output_key='artifact_name'
)

summarization_agent = LlmAgent(
    model=Gemini(
        model=GEMINI_FLASH,
        retry_options=retry_config
    ),
    name='summarization_agent',
    description='Asisten untuk membuat ringkasan dari hasil visualisasi data KTP.',
    instruction=(
        "1. Tampilkan {aggregation_result} yang diberikan dalam bentuk tabel Markdown.\n"
        "   - Gunakan header tabel yang jelas.\n"
        "   - Pastikan format Markdown rapi dan mudah dibaca.\n"
        "   - Jika data kosong, tampilkan pesan bahwa tidak ada data yang dapat ditampilkan.\n\n"
        "2. Analisis Visualisasi:\n"
        "   - Ambil nama file gambar dari field 'artifact_filename' di dalam {artifact_name}.\n"
        "   - Berikan ringkasan singkat dan insight yang mendalam berdasarkan visual chart yang Anda lihat.\n"
    ),
    output_key='summary_result'
)

aggregation_pipeline = SequentialAgent(
    name='aggregation_pipeline',
    description=(
        'Pipeline terstruktur untuk memproses data KTP secara end-to-end, '
        'mulai dari melakukan agregasi data, menampilkan hasil dalam bentuk tabel Markdown, '
        'membuat visualisasi berdasarkan hasil agregasi, hingga menyajikan ringkasan insight utama.'
    ),
    sub_agents=[
        aggregation_agent, 
        visualization_agent,
        artifact_agent,
        summarization_agent,        
        ],
)

ktp_aggregation_tools = AgentTool(agent=aggregation_pipeline)
visualization_tools = AgentTool(agent=visualization_agent)