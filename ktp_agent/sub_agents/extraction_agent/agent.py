from typing import Optional
from pydantic import BaseModel, Field
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.agent_tool import AgentTool

from ...config import GEMINI_FLASH, retry_config
from ...tools import validate_ktp_callback

class KTPExtractionResult(BaseModel):
    nik: str = Field(description="Nomor Induk Kependudukan (16 digits)")
    full_name: str = Field(description="Nama lengkap (Full Name)")
    birth_place: str = Field(description="Tempat lahir (Place of Birth)")
    birth_date: str = Field(description="Tanggal lahir (Date of Birth) in DD-MM-YYYY format")
    gender: str = Field(description="Jenis kelamin (Laki-laki/Perempuan)")
    blood_type: str = Field(description="Golongan darah (Blood Type) e.g., A, B, O, AB, or -")
    address: str = Field(description="Alamat lengkap (Full Address)")
    rt_rw: str = Field(description="RT/RW")
    village_kelurahan: str = Field(description="Kelurahan/Desa")
    district_kecamatan: str = Field(description="Kecamatan")
    religion: str = Field(description="Agama (Religion)")
    marital_status: str = Field(description="Status perkawinan (Marital Status)")
    occupation: str = Field(description="Pekerjaan (Occupation)")
    citizenship: str = Field(description="Kewarganegaraan (Citizenship) e.g., WNI")
    expiry_date: str = Field(description="Berlaku hingga (Expiry Date) or 'SEUMUR HIDUP'")

extraction_agent = LlmAgent(
    model=Gemini(
        model=GEMINI_FLASH,
        retry_options=retry_config
    ),
    name='extraction_agent',
    description='Asisten yang membantu mengekstrak data identitas terstruktur dari dokumen KTP Indonesia.',
    instruction=(
    "Anda adalah asisten OCR dan ekstraksi data yang ahli untuk Kartu Tanda Penduduk (KTP) Indonesia. "
    "Tujuan Anda adalah mengekstrak field tertentu dari gambar atau teks KTP yang diberikan.\n\n"
    "1. Analisis dokumen KTP yang disediakan.\n"
    "2. Ekstrak field yang didefinisikan dalam skema output secara akurat.\n"
    "3. Pastikan tanggal diformat sebagai DD-MM-YYYY jika memungkinkan.\n"
    "4. Isi dengan NULL jika informasi tidak tersedia atau tidak dapat diekstrak.\n"
    "5. Field expiry_date harus SELALU diisi dengan 'SEUMUR HIDUP'.\n"
    "6. Kembalikan HANYA objek JSON akhir yang sesuai dengan skema KTPExtractionResult."
),
    output_schema=KTPExtractionResult,
    output_key='extraction_result',
    after_model_callback=validate_ktp_callback
)

ktp_extraction_tools = AgentTool(agent=extraction_agent)