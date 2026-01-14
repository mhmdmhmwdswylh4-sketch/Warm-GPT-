import streamlit as st
from g4f.client import Client

# --- 1. إعدادات الصفحة والواجهة السيبرانية (بدون تغيير) ---
st.set_page_config(page_title="Cyber Guard Pro", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #00ff41; }
    .dev-name { 
        text-align: center; font-family: 'Courier New'; color: #00ff41; 
        border-bottom: 2px solid #00ff41; padding: 10px; text-shadow: 0 0 15px #00ff41;
        margin-bottom: 25px;
    }
    .stChatMessage { border: 1px solid #00ff41; border-radius: 10px; background-color: #161b22; }
    .stFileUploader section { background-color: #161b22 !important; border: 1px dashed #00ff41 !important; }
    </style>
    """, unsafe_allow_html=True)

# اسم المطور في الأعلى
st.markdown("<h1 class='dev-name'>المطور: محمد محمود صويلح 🛠️</h1>", unsafe_allow_html=True)

# --- 2. إدارة ذاكرة المحادثة (الاحتفاظ بالنشاط) ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "أنت خبير أمن سيبراني متخصص. اسم مطورك هو محمد محمود صويلح. تذكر دائماً سياق المحادثة السابق لتقديم تحليل دقيق."}
    ]

# --- 3. القائمة الجانبية مع النماذج الموسعة ---
st.sidebar.title("⚙️ إعدادات المحرك")
model_choice = st.sidebar.selectbox(
    "اختر نموذج الذكاء الاصطناعي:",
    (
        "gpt-4o", "gpt-4", "gpt-3.5-turbo", "gemini-pro",
        "claude-v2", "llama-3-70b", "llama-3-8b", 
        "mixtral-8x7b", "blackboxai", "pi"
    )
)

st.sidebar.write(f"💬 عدد الرسائل في الذاكرة: {len(st.session_state.messages) - 1}")

if st.sidebar.button("🗑️ مسح المحادثة والذاكرة"):
    st.session_state.messages = [st.session_state.messages[0]]
    st.rerun()

# --- 4. عرض المحادثة السابقة (لضمان بقائها على الشاشة) ---
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- 5. منطقة الأوامر ورفع الملفات ---
with st.container():
    uploaded_file = st.file_uploader("📎 أرفق ملف التحليل", type=["txt", "py", "js", "php", "jpg", "png"], label_visibility="collapsed")

if prompt := st.chat_input("أدخل أمر التحليل السيبراني هنا..."):
    
    # دمج سياق الملف إذا وجد
    user_input = prompt
    if uploaded_file:
        user_input = f"الملف المرفوع: {uploaded_file.name}. السؤال: {prompt}"

    # 1. إضافة رسالة المستخدم للسجل
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. توليد الرد بناءً على كامل السجل (هنا يكمن سر الاحتفاظ بالمحادثة)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            client = Client()
            # نرسل st.session_state.messages كاملة للذكاء الاصطناعي
            response = client.chat.completions.create(
                model=model_choice,
                messages=st.session_state.messages, 
                stream=True,
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + " 🟢")
            
            message_placeholder.markdown(full_response)
            # 3. إضافة رد الذكاء الاصطناعي للسجل ليتم تذكره في المرة القادمة
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception:
            st.error("⚠️ هذا النموذج غير مستجيب حالياً، جرب نموذجاً آخر.")
