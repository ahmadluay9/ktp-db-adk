from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.agent_tool import AgentTool

from ...config import GEMINI_FLASH, retry_config
from ...tools import management_tools

ingestion_agent = LlmAgent(
    model=Gemini(
        model=GEMINI_FLASH,
        retry_options=retry_config
    ),
    name='ingestion_agent',
    description='Asisten yang Bertanggung jawab untuk mendaftarkan, menginput, dan memasukkan data KTP penduduk baru ke dalam database.',
    instruction=(
        "Anda adalah Spesialis Entri Data untuk Sistem Administrasi Kependudukan. "
        "Tanggung jawab utama Anda adalah mencatat data penduduk baru secara akurat ke dalam database "
        "menggunakan tool yang tersedia.\n\n"
        "**Pedoman Operasional:**\n"
        "1. **Sumber Data:** Sumber data berasal dari {extraction_result}.\n"
        "2. **Output:** Setelah tool berhasil dijalankan, cukup konfirmasikan kepada pengguna bahwa data telah terdaftar."
    ),
    tools=management_tools,
    output_key='ingestion_result',
)

ktp_ingestion_tools = AgentTool(agent=ingestion_agent)