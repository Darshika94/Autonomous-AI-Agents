import streamlit as st
import pandas as pd
import time
from agent_logic import process_transaction
from access_control import generate_token  # JWT token generator

# Page setup
st.set_page_config(page_title="Compliance Agent", page_icon="🕵️", layout="centered")
st.title("Real-Time Transaction Flagging Agent")

# 🔐 Show sample JWT tokens
st.markdown("Sample JWT Tokens (for testing)")
roles = ["admin", "agent", "auditor"]
for r in roles:
    with st.expander(f"{r.capitalize()} Token"):
        st.code(generate_token(r), language="bash")

# 🔑 Token input
token = st.text_input("🔑 Paste your JWT token here:")

# 📁 File upload
uploaded_file = st.file_uploader("📂 Upload CSV file (e.g. transactions)", type="csv")

# ⚠️ Warn if token is missing
if uploaded_file and not token:
    st.warning("⚠️ Please paste a valid token to continue.")

# ✅ Main logic
if uploaded_file and token:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip().str.lower()

    st.success("✅ File uploaded successfully!")
    st.subheader("🔁 Streaming Simulation...")

    stream_data = []
    table_placeholder = st.empty()

    for i, txn in df.iterrows():
        result, risk_score = process_transaction(txn, token)

        # ✅ Just the icon as result
        icon = "❌ Fraud" if "Flagged" in result else "✅ Safe"

        stream_data.append({
            "Txn ID": str(i + 1),
            "Amount": str(txn.get("amount", 0)),
            "Risk Score": str(risk_score),
            "Result": icon  # 👈 Only icon
        })

        stream_df = pd.DataFrame(stream_data)
        table_placeholder.dataframe(stream_df, use_container_width=True)

        time.sleep(0.3)

    st.markdown(f"---\n**Total Transactions Processed**: `{len(df)}`")



