import streamlit as st
from g4f.client import Client

# إعداد واجهة الصفحة
st.set_page_config(page_title="Cyber Guard AI", page_icon="🛡️")

st.title("🛡️ Cyber Guard AI Assistant")
st.markdown("مساعد ذكي متخصص في الأمن السيبراني (بدون API Key)")

# --- القائمة الجانبية ---
st.sidebar.header("إعدادات النموذج")

# خيار التبديل بين النماذج باستخدام النصوص مباشرة لتجنب AttributeError
model_choice = st.sidebar.selectbox(
    "اختر نموذج الذكاء الاصطناعي:",
    ("gpt-3.5-turbo", "gpt-4", "gemini", "claude-v2")
)

# زر لمسح المحادثة
if st.sidebar.button("مسح المحادثة"):
    st.session_state.messages = []
    st.rerun()

# --- منطق المحادثة ---

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "أنت خبير في الأمن السيبراني والاختبار الأخلاقي. ساعد المستخدم في فهم الثغرات والحماية فقط."}
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("اسأل عن شيء في الأمن السيبراني..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            client = Client()
            # هنا نستخدم اسم النموذج المختار مباشرة
            response = client.chat.completions.create(
                model=model_choice,
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"عذراً، هذا النموذج غير متوفر حالياً. جرب نموذجاً آخر من القائمة الجانبية.")
            # st.write(f"Error detail: {e}") # يمكنك إلغاء التعليق لرؤية الخطأ بالتفصيل
