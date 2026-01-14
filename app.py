import streamlit as st
from g4f.client import Client
import g4f

# --- 1. إعدادات الصفحة والواجهة السيبرانية (Cyber Style) ---
st.set_page_config(page_title="Cyber Guard AI", page_icon="🛡️", layout="wide")

# إضافة CSS لجعل الواجهة تبدو احترافية وسيبرانية
st.markdown("""
    <style>
    /* تغيير الخلفية والألوان لتناسب الأجواء السيبرانية */
    .stApp {
        background-color: #0d1117;
        color: #00ff41; /* لون أخضر Matrix */
    }
    .stTextInput > div > div > input {
        background-color: #161b22;
        color: #00ff41;
        border: 1px solid #00ff41;
    }
    .stButton>button {
        background-color: #00ff41;
        color: black;
        border-radius: 5px;
        font-weight: bold;
    }
    .stSidebar {
        background-color: #010409 !important;
        border-right: 1px solid #00ff41;
    }
    /* تنسيق اسم المطور */
    .dev-name {
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        color: #00ff41;
        border-bottom: 2px solid #00ff41;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. عرض اسم المطور في الأعلى ---
st.markdown("<h1 class='dev-name'>المطور: محمد محمود صويلح 🛠️</h1>", unsafe_allow_html=True)

st.title("🛡️ Cyber Guard Pro Dashboard")
st.write("نظام التحليل السيبراني المتقدم - الإصدار 2.0")

# --- 3. القائمة الجانبية (إعدادات متطورة) ---
st.sidebar.image("https://img.icons8.com/nolan/128/security-shield.png", width=100)
st.sidebar.header("⚙️ مركز التحكم")

# زيادة عدد النماذج
model_choice = st.sidebar.selectbox(
    "اختر محرك الذكاء الاصطناعي:",
    (
        "gpt-4", "gpt-3.5-turbo", 
        "gemini", "gemini-pro",
        "claude-v2", "mixtral-8x7b", 
        "llama-3-70b", "blackboxai"
    )
)

# إضافة ميزة رفع الملفات والصور
st.sidebar.markdown("---")
st.sidebar.subheader("📁 تحليل الملفات")
uploaded_file = st.sidebar.file_uploader("ارفع صورة ثغرة أو ملف برمجي لتحليله:", type=["jpg", "png", "txt", "py", "php", "js"])

if uploaded_file is not None:
    st.sidebar.success(f"تم تحميل: {uploaded_file.name}")
    # هنا يمكن إضافة منطق قراءة الملف إذا أردت لاحقاً

# زر مسح البيانات
if st.sidebar.button("🗑️ تصفير المحادثة"):
    st.session_state.messages = []
    st.rerun()

# --- 4. منطق المحادثة ---

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "أنت خبير أمن سيبراني عالمي. تتحدث بلهجة تقنية احترافية. تساعد في اكتشاف الثغرات، كتابة السكربتات الأمنية، وشرح الهجمات المعقدة لغرض الحماية."}
    ]

# عرض الرسائل بتنسيق سيبراني
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# إدخال المستخدم
if prompt := st.chat_input("أدخل أمر التحليل هنا..."):
    # إذا كان هناك ملف مرفوع، ندمج معلومة الملف مع النص
    full_prompt = prompt
    if uploaded_file:
        full_prompt = f"لدي ملف مرفوع باسم {uploaded_file.name}. " + prompt

    st.session_state.messages.append({"role": "user", "content": full_prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            client = Client()
            response = client.chat.completions.create(
                model=model_choice,
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + " 🟢")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception:
            st.error("⚠️ فشل الاتصال بالنموذج. المحرك قد يكون مشغولاً، جرب اختيار نموذج آخر من القائمة.")
