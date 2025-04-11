# utils.py
import streamlit as st
import uuid

def copy_to_clipboard(text: str, key: str):
    """
    Render a copy-to-clipboard button in Streamlit using HTML+JS
    """
    uid = str(uuid.uuid4()).replace("-", "")
    button_id = f"copy-btn-{key}-{uid}"
    text_id = f"text-{key}-{uid}"

    copy_html = f"""
        <textarea id="{text_id}" style="position: absolute; left: -9999px;">{text}</textarea>
        <button id="{button_id}">📋 Copy</button>
        <script>
        const btn = document.getElementById("{button_id}");
        btn.addEventListener("click", function() {{
            const text = document.getElementById("{text_id}");
            text.select();
            document.execCommand("copy");
            btn.innerText = "✅ Copied!";
            setTimeout(() => (btn.innerText = "📋 Copy"), 2000);
        }});
        </script>
    """

    st.components.v1.html(copy_html, height=40)
