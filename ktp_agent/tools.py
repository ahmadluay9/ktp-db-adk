import os
from typing import List, Optional
from pydantic import BaseModel, Field
from copy import deepcopy
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, LlmRequest
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.tool_context import ToolContext
import google.genai.types as types
from google.genai.types import Part
from google import genai
from toolbox_core import ToolboxSyncClient
from datetime import datetime

from .config import GEMINI_FLASH

class ArtifactFilename(BaseModel):
    artifact_filename: str = Field(description="The name of the generated visualization file (e.g., chart.png)")

today_date = datetime.today().strftime("%d-%m-%Y")

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

def censor_pii_callback(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
    """
    Callback to censor sensitive PII using a secondary LLM call.
    """
    agent_name = callback_context.agent_name
    print(f"[Callback] Inspecting model response for agent: {agent_name}")

    # 1. Extract original text
    original_text = ""
    if llm_response.content and llm_response.content.parts:
        # We focus on text parts for censorship
        if llm_response.content.parts[0].text:
            original_text = llm_response.content.parts[0].text
    
    if not original_text:
        return None

    # 2. Use LLM to censor the data
    client = genai.Client()
    
    # Construct prompt for the guardrail LLM
    prompt = f"""
    You are a PII redaction engine. Rewrite the text below by applying these specific censorship rules:
    1. **Name**: Keep only the first 3 characters of the first name. 
        Replace the remaining characters of the first name and all characters of any subsequent names with asterisks (*), 
        preserving the original length and spaces (e.g., "Budi Santoso" becomes "Bud* *******").
    2. **Date of Birth (DOB)**: Replace completely with '******'.
    3. **Place of Birth**: Replace completely with '******'.
    4. **NIK**: Replace completely with '******'.
    5. **Address**: Replace completely with '******'.
    6. **RT/RW**: Replace completely with '******'.
    7. **Kelurahan/Desa**: Replace completely with '******'.
    8. **Kecamatan**: Replace completely with '******'.
    9. Keep all other text and formatting exactly as is.

    Text to censor:
    "{original_text}"

    Censored Text:
    """

    try:
        response = client.models.generate_content(
            model=GEMINI_FLASH,
            contents=[types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
        )

        if response and response.text:
            censored_text = response.text.strip()
            print(f"[Callback] PII Censorship applied via LLM.")
            
            # 3. Construct and return the modified LlmResponse
            # Deep copy parts to avoid side effects
            modified_parts = [deepcopy(part) for part in llm_response.content.parts]
            modified_parts[0].text = censored_text

            return LlmResponse(
                content=types.Content(role="model", parts=modified_parts),
                grounding_metadata=llm_response.grounding_metadata
            )
    except Exception as e:
        print(f"[Callback] Error during PII censorship LLM call: {e}")
        return None # Return original if censorship fails

    return None

def validate_ktp_callback(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
    """
    Callback to validate and fix KTP data using an LLM.
    Specifically enforces NIK format (16 digits) and Date format (DD-MM-YYYY).
    """
    agent_name = callback_context.agent_name
    print(f"[Callback] Validating KTP data for agent: {agent_name}")

    # 1. Extract original text (which should be JSON)
    original_text = ""
    if llm_response.content and llm_response.content.parts:
        if llm_response.content.parts[0].text:
            original_text = llm_response.content.parts[0].text
    
    if not original_text:
        return None

    # 2. Use LLM to validate and fix the data
    client = genai.Client()
    
    # Construct prompt for the validation LLM
    prompt = f"""
    Anda adalah mesin validasi presisi tinggi untuk Kartu Tanda Penduduk (KTP) Indonesia.

    Tanggal hari ini: {today_date}

    Tinjau objek JSON di bawah ini dan validasi field 'nik' dan 'birth_date' menggunakan aturan berikut:

    1. **Struktur NIK & Validasi Wilayah**:
    - Field 'nik' harus terdiri dari tepat 16 digit.
    - **Tindakan**: Gunakan Google Search untuk memverifikasi apakah 6 digit pertama
        (Provinsi, Kabupaten/Kota, Kecamatan) sesuai dengan wilayah administratif yang valid di Indonesia.
    - Digit 1-2: Provinsi | 3-4: Kabupaten/Kota | 5-6: Kecamatan.

    2. **Pemeriksaan Silang NIK & Tanggal Lahir**:
    - Digit ke-7 sampai ke-12 pada NIK merepresentasikan Tanggal Lahir dalam format [DDMMYY].
    - **Aturan Jenis Kelamin**:
        - Jika berjenis kelamin perempuan, nilai 'DD' (digit 7-8) ditambah 40.
        Contoh: tanggal lahir 15 → 55.
    - **Validasi**: Pastikan field 'birth_date' sesuai dengan 6 digit tengah NIK
        setelah memperhitungkan aturan jenis kelamin.

    3. **Validasi Usia**:
    - Hitung usia berdasarkan 'birth_date' dan Tanggal Hari Ini.
    - **Aturan**: Jika usia < 17 tahun, maka data dinyatakan **TIDAK VALID**
        dan harus ditandai sebagai invalid pada hasil JSON.

    4. **Format Data**:
    - 'nik': String, 16 digit, tanpa spasi atau karakter khusus.
    - 'birth_date': String dalam format 'DD-MM-YYYY'.
    - Jika kode wilayah NIK, logika tanggal, atau usia tidak valid,
        tandai atau perbaiki berdasarkan sumber paling tepercaya (hasil pencarian).

    Input JSON:
    {original_text}

    Return ONLY the valid JSON string, no markdown formatting.
    """

    tools = [types.Tool(google_search=types.GoogleSearch())]


    config = types.GenerateContentConfig(
        tools=tools,
        temperature=0.1 
    )

    try:        
        response = client.models.generate_content(
            model=GEMINI_FLASH,
            contents=[types.Content(role="user", parts=[types.Part.from_text(text=prompt)])],
            config=config
        )

        if response and response.text:
            validated_json = response.text.strip()
            
            # Optional: Strip markdown code blocks if the LLM added them
            if validated_json.startswith("```"):
                validated_json = validated_json.strip("`").replace("json\n", "").strip()

            print(f"[Callback] KTP Data validated and formatted.")
            
            # 3. Return modified response
            modified_parts = [deepcopy(part) for part in llm_response.content.parts]
            modified_parts[0].text = validated_json

            return LlmResponse(
                content=types.Content(role="model", parts=modified_parts),
                grounding_metadata=llm_response.grounding_metadata
            )
    except Exception as e:
        print(f"[Callback] Error during KTP validation: {e}")
        return None 

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
management_tools= toolbox.load_toolset('management_toolset')