import streamlit as st
from chains import build_chain
from prompts import style_prompts
from utils import copy_to_clipboard

# ========== PAGE SETUP ==========
st.set_page_config(page_title="English Rewriter", layout="centered", page_icon="📝")

# ========== STYLING ==========
st.markdown("""
    <style>
        .main-title {
            font-size: 2.5em;
            font-weight: 700;
            text-align: center;
            margin-bottom: 10px;
        }
        .sub-title {
            font-size: 1.2em;
            text-align: center;
            color: #666666;
            margin-bottom: 30px;
        }
        .stTextArea > div > textarea {
            font-size: 1.05em;
            padding: 10px;
        }
        .footer {
            position: fixed;
            bottom: 20px;
            text-align: center;
            font-size: 0.9em;
            color: #999999;
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# ========== HEADER ==========
st.markdown('<div class="main-title">📝 English Rewriter</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Rewrite informal English into refined, stylized text with GPT</div>', unsafe_allow_html=True)

# ========== INPUT ==========
user_text = st.text_area("Enter your sentence:", height=120, placeholder="e.g., Hello what you name bor?")

mode = st.radio("Select Mode", ["Rewrite with one style", "Compare all styles"], horizontal=True)

# ========== MODE 1 ==========
if mode == "Rewrite with one style":
    style_options = [s.capitalize() for s in style_prompts.keys() if s != "default"] + ["Custom ✍️"]
    selected_option = st.selectbox("Choose a style:", style_options)

    custom_instruction = ""
    if selected_option == "Custom ✍️":
        custom_instruction = st.text_input("Enter your custom instruction:")

    if st.button("✏️ Rewrite"):
        if not user_text.strip():
            st.warning("Please enter a sentence.")
        else:
            if selected_option == "Custom ✍️":
                style = " " + custom_instruction.strip()
                style_label = "Custom"
            else:
                selected_key = selected_option.lower()
                style = style_prompts.get(selected_key, "")
                style_label = selected_option.capitalize()

            chain = build_chain(style)
            result = chain.invoke({"text": user_text, "style": style})

            st.markdown(f"### 🎯 Style: {style_label}")
            st.text_area("Result", value=result, height=100, label_visibility="collapsed", key="result_single")
            copy_to_clipboard(result, key="single")

# ========== MODE 2 ==========
elif mode == "Compare all styles":
    with st.expander("✍️ Optional: Add custom style"):
        custom_instruction = st.text_input("Custom instruction (e.g., 'Make it poetic like Shakespeare')")

    if st.button("🔁 Compare"):
        if not user_text.strip():
            st.warning("Please enter a sentence.")
        else:
            st.markdown("### ✨ Rewritten Results")
            col1, col2 = st.columns(2)
            styles_to_compare = {k: v for k, v in style_prompts.items() if k != "default"}

            for i, (style_key, style_instruction) in enumerate(styles_to_compare.items()):
                chain = build_chain(style_instruction)
                result = chain.invoke({"text": user_text, "style": style_instruction})
                with (col1 if i % 2 == 0 else col2):
                    st.markdown(f"#### 🎯 {style_key.capitalize()}")
                    st.text_area("", value=result, height=100, key=f"{style_key}_text", label_visibility="collapsed")
                    copy_to_clipboard(result, key=style_key)

            if custom_instruction.strip():
                chain = build_chain(" " + custom_instruction.strip())
                result = chain.invoke({"text": user_text, "style": " " + custom_instruction.strip()})
                st.markdown("#### ✍️ Custom Style")
                st.text_area("", value=result, height=100, key="custom_text", label_visibility="collapsed")
                copy_to_clipboard(result, key="custom")

# ========== FOOTER ==========
st.markdown("""
    <hr style="margin-top: 50px;">
    <div class="footer">
        Created by <a href="https://www.linkedin.com/in/puttisan-chartcharnchai-10a391239/" target="_blank">SXXN</a> | 
        <a href="https://github.com/puttisandev" target="_blank">GitHub Repo</a>
    </div>
""", unsafe_allow_html=True)
