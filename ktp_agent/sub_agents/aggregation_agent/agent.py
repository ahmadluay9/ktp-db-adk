from pydantic import BaseModel, Field
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.agent_tool import AgentTool

from ..visualization_agent.agent import visualization_agent
from ...config import GEMINI_FLASH, retry_config
from ...tools import aggregation_tools

class ArtifactFilename(BaseModel):
    artifact_filename: str = Field(description="The name of the generated visualization file (e.g., chart.png)")

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