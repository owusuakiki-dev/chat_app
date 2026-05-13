import streamlit as st
from openai import OpenAI

# ===================== CONFIG =====================
st.set_page_config(page_title="Llama 3.1 Chat", page_icon="🦙", layout="centered")

st.title("🦙 Llama 3.1 8B Chat")
st.caption("Powered by Hugging Face Router")

# ===================== SIDEBAR =====================
with st.sidebar:
    st.header("Settings")
    token = st.text_input("Hugging Face Token", type="password", value="")
    model_name = st.text_input("Model", value="meta-llama/Llama-3.1-8B-Instruct:novita")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ===================== CHAT HISTORY =====================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ===================== CHAT INPUT =====================
if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                client = OpenAI(
                    base_url="https://router.huggingface.co/v1",
                    api_key=token,
                )

                completion = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    temperature=0.7,
                    max_tokens=2048,
                )

                response = completion.choices[0].message.content
                st.markdown(response)

                # Save assistant response
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )

            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )
