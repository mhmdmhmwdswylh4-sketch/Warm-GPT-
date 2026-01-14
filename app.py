import streamlit as st
from g4f.client import Client
import g4f

# --- 1. إعدادات الصفحة والواجهة السيبرانية المتقدمة ---
st.set_page_config(page_title="Cyber Guard Pro", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #00ff41; }
    .dev-name { 
        text-align: center; font-family: 'Courier New'; color: #00ff41; 
        border-bottom: 2px solid #00ff41; padding: 10px; text-shadow: 0 0 15px #00ff41;
        margin-bottom: 25px;
    }
    /* تنسيق الرسائل */
    .stChatMessage { border: 1px solid #00ff41; border-radius: 10px; background-color: #161b22; }
    .stFileUploader section { background-color: #161b22 !important; border: 1px dashed #00ff41 !important; }
    </style>
    """, unsafe_allow_html=True)

# عرض اسم المطور في الأعلى
st.markdown("<h1 class='dev-name'>المطور: محمد محمود صويلح 🛠️</h1>", unsafe_allow_html=True)

# --- 2. القائمة الجانبية مع قائمة ضخمة من النماذج ---
st.sidebar.title("⚙️ إعدادات المحرك السيبراني")

# قائمة النماذج الموسعة
model_choice = st.sidebar.selectbox(
    "اختر نموذج الذكاء الاصطناعي:",
    (
        "gpt-4o", 
        "gpt-4", 
        "gpt-3.5-turbo",
        "gemini-pro",
        "claude-v2",
        "llama-3-70b",
        "llama-3-8b",
        "mixtral-8x7b",
        "blackboxai",
        "pi",
        "wizardlm-2-8x22b",
        "dall-e-3"  # لتوليد الصور إذا كان الموزد يدعم
    )
)

st.sidebar.markdown("---")
st.sidebar.info("""
**دليل المحركات:**
- **GPT-4o:** الأحدث والأسرع.
- **Llama-3:** ممتاز في الأكواد البرمجية.
- **Gemini:** قوي في التحليل المنطقي.
- **Blackboxai:** مخصص للمبرمجين والأمن.
""")

if st.sidebar.button("🗑️ مسح المحادثة"):
    st.session_state.messages = []
    st.rerun()

# --- 3. تهيئة المحادثة ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "أنت خبير أمن سيبراني متخصص. اسم مطورك هو محمد محمود صويلح. قدم إجابات تقنية دقيقة حول الثغرات والحماية."}
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- 4. منطقة الأوامر ورفع الملفات ---
with st.container():
    uploaded_file = st.file_uploader("📎 أرفق ملف التحليل", type=["txt", "py", "js", "php", "jpg", "png"], label_visibility="collapsed")

if prompt := st.chat_input("أدخل أمر التحليل السيبراني هنا..."):
    
    # دمج سياق الملف المرفوع
    final_prompt = prompt
    if uploaded_file:
        final_prompt = f"User uploaded a file: {uploaded_file.name}. Question: {prompt}"

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            client = Client()
            response = client.chat.completions.create(
                model=model_choice,
                messages=[{"role": "user", "content": final_prompt}],
                stream=True,
            )
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + " 🟢")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception:
            st.error("⚠️ هذا النموذج غير مستجيب حالياً، يرجى تجربة نموذج آخر من القائمة الجانبية.")
