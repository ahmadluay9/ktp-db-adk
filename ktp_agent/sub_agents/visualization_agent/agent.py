from google.adk.agents import LlmAgent
from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.models.google_llm import Gemini
from google.adk.tools.agent_tool import AgentTool
from ...config import GEMINI_PRO, retry_config

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

visualization_tools = AgentTool(agent=visualization_agent)