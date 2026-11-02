import os

import streamlit as st

# Copy API keys from Streamlit Secrets (used on Streamlit Cloud) into environment variables,
# so the agent finds them the same way it does on your computer.
try:
    for _name in ("GROQ_API_KEY", "GROQ_MODEL", "OPENAI_API_KEY", "OPENAI_MODEL"):
        if _name in st.secrets and not os.getenv(_name):
            os.environ[_name] = str(st.secrets[_name]).strip()
except Exception:
    pass  # no secrets file locally, that's fine

from agent import llm_status, solve

st.set_page_config(page_title="Reasoning Agent", page_icon="🧠")
st.title("🧠 Multi-Step Reasoning Agent")
st.caption(f"Plan → Execute → Verify  ·  LLM: {llm_status()}")

question = st.text_input("Your question", placeholder="e.g. 45 - 18 + 6")

if st.button("Solve", type="primary") and question.strip():
    result = solve(question)
    if result.get("llm_error"):
        st.warning(f"⚠️ The LLM didn't respond, so built-in rules were used. Reason: {result['llm_error']}")
    if result["status"] == "success":
        st.success(f"**Answer:** {result['answer']}")
    else:
        st.error(result["answer"])
    st.write("**How:**", result["explanation"])
    with st.expander("Debug info"):
        st.json(result["debug"])
