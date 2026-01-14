import streamlit as st
from g4f.client import Client
import g4f

# --- 1. إعدادات الواجهة السيبرانية ---
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
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='dev-name'>المطور: محمد محمود صويلح 🛠️</h1>", unsafe_allow_html=True)

# --- 2. إدارة الذاكرة ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "أنت خبير أمن سيبراني متخصص. اسم مطورك هو محمد محمود صويلح."}
    ]

# --- 3. القائمة الجانبية ---
st.sidebar.title("⚙️ إعدادات المحرك")
model_choice = st.sidebar.selectbox(
    "اختر نموذج الذكاء الاصطناعي:",
    ("gpt-4o", "gpt-4", "gemini-pro", "llama-3-70b", "blackboxai", "claude-v3")
)

if st.sidebar.button("🗑️ مسح المحادثة والذاكرة"):
    st.session_state.messages = [st.session_state.messages[0]]
    st.rerun()

# --- 4. عرض المحادثة ---
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- 5. منطقة الأوامر ومعالجة الخطأ ---
with st.container():
    uploaded_file = st.file_uploader("📎 أرفق ملف التحليل", type=["txt", "py", "js", "php", "jpg", "png"], label_visibility="collapsed")

if prompt := st.chat_input("أدخل أمر التحليل السيبراني هنا..."):
    
    user_input = prompt
    if uploaded_file:
        user_input = f"الملف: {uploaded_file.name}. السؤال: {prompt}"

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            client = Client()
            # محاولة جلب الرد
            response = client.chat.completions.create(
                model=model_choice,
                messages=st.session_state.messages,
                stream=True,
                # إضافة معلمة الموفر التلقائي إذا فشل الموفر المحدد
                ignore_working=True 
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + " 🟢")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            # حل بديل عند فشل النموذج المختار: استخدام الموفر الافتراضي العام
            st.warning("⚠️ المحرك المختار مشغول حالياً. جاري التحويل للمحرك الاحتياطي لتجنب الانقطاع...")
            try:
                # محاولة ثانية باستخدام نموذج تلقائي مستقر
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo", # نموذج احتياطي سريع ومستقر
                    messages=st.session_state.messages,
                    stream=False
                )
                full_response = response.choices[0].message.content
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except:
                st.error("❌ عذراً، جميع الموفرين المجانيين يواجهون ضغطاً الآن. يرجى الانتظار دقيقة أو تغيير المتصفح.")
