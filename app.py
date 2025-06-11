# book_translator_project/app.py
import streamlit as st
from src.workflow import run_qa
import time
import os
os.environ["STREAMLIT_SERVER_ENABLE_FILE_WATCHER"] = "false"
import asyncio
import sys

if sys.version_info[1] == 9 or sys.version_info[1] == 10:
    # Patch for Python 3.9/3.10 compatibility with Streamlit + PyTorch
    from asyncio import AbstractEventLoopPolicy
    class CompatAsyncIOPolicy(AbstractEventLoopPolicy):
        def get_event_loop(self):
            loop = super().get_event_loop()
            if not loop.is_running():
                return loop
            raise RuntimeError("Cannot get event loop - another loop is already running")
    asyncio.set_event_loop_policy(CompatAsyncIOPolicy())
# Set page config
st.set_page_config(
    page_title=" English - Persian Book Translator",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .header {
        font-size: 36px;
        font-weight: bold;
        color: #2e86c1;
        text-align: center;
        padding: 20px;
    }
    .subheader {
        font-size: 18px;
        color: #5d6d7e;
        text-align: center;
        padding-bottom: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9f9;
    }
    .stButton>button {
        background-color: #1e8449 !important;
        color: white !important;
        font-weight: bold;
        border: none;
        width: 100%;
        padding: 10px;
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        border: 2px solid #2e86c1;
        border-radius: 5px;
        padding: 10px;
    }
    .response-box {
        background-color: #f8f9f9;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        border-left: 5px solid #2e86c1;
    }
    .step-box {
        background-color: #eafaf1;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
        font-size: 14px;
    }
    .footer {
        text-align: center;
        padding: 20px;
        color: #7f8c8d;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'processing' not in st.session_state:
    st.session_state.processing = False


def main():
    # Header
    st.markdown('<div class="header">📚 English-persian Book Translator</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Ask questions about English books in Persian</div>', unsafe_allow_html=True)

    # Sidebar for system info
    with st.sidebar:
        st.header("System Configuration")
        st.markdown("""
        **Models Used:**
        - Translation: MT5 (Persian ↔ English)
        - LLM: Mistral 7B
        - Embeddings: MiniLM-L6-v2
        """)

        st.markdown("""
        **How It Works:**
        1. Ask about any English PDF book in Persian
        2. System translates to English
        3. Retrieves relevant content
        4. Generates English answer
        5. Translates back to Persian
        """)

        st.markdown("""
        **Example Questions:**
        - نویسنده این کتاب کیست؟
        - موضوع اصلی کتاب چیست؟
        - یک نقل قول معروف از کتاب بگویید
        - خلاصه فصل اول چیست؟
        """)

        st.markdown("---")
        st.caption("Developed with LangGraph, LangChain, and Streamlit")

    # Main content area
    col1, col2 = st.columns([3, 1])

    with col1:
        # User input
        user_question = st.text_input("سوال خود را به فارسی وارد کنید:", placeholder="مثلاً: نویسنده این کتاب کیست؟")

        # Process button
        if st.button("پاسخ دریافت کنید", disabled=st.session_state.processing):
            if user_question.strip() == "":
                st.warning("لطفاً یک سوال وارد کنید")
            else:
                st.session_state.processing = True
                st.session_state.conversation.append(("user", user_question))

                try:
                    # Simulate processing steps with progress
                    with st.spinner("در حال پردازش..."):
                        progress_bar = st.progress(0)

                        # Step 1: Translation to English
                        progress_text = st.empty()
                        progress_text.markdown("**مرحله ۱:** ترجمه سوال به انگلیسی")
                        progress_bar.progress(20)
                        time.sleep(1)

                        # Step 2: Document retrieval
                        progress_text.markdown("**مرحله ۲:** جستجو در محتوای کتاب")
                        progress_bar.progress(40)
                        time.sleep(1)

                        # Step 3: Answer generation
                        progress_text.markdown("**مرحله ۳:** تولید پاسخ توسط هوش مصنوعی")
                        progress_bar.progress(70)
                        time.sleep(1)

                        # Step 4: Translation back to Persian
                        progress_text.markdown("**مرحله ۴:** ترجمه پاسخ به فارسی")
                        progress_bar.progress(90)
                        time.sleep(0.5)

                        # Get actual answer
                        answer = run_qa(user_question)
                        st.session_state.conversation.append(("system", answer))

                        progress_bar.progress(100)
                        time.sleep(0.5)

                except Exception as e:
                    st.error(f"خطا در پردازش: {str(e)}")
                finally:
                    st.session_state.processing = False
                    progress_bar.empty()
                    progress_text.empty()


    # Display conversation
    if st.session_state.conversation:
        st.markdown("### گفتگو")
        for i, (speaker, text) in enumerate(st.session_state.conversation):
            if speaker == "user":
                st.markdown(
                    f"<div style='text-align: left; background-color: #e3f2fd; padding: 10px; border-radius: 10px; margin: 10px 0;'><b>شما:</b> {text}</div>",
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    f"<div style='text-align: right; background-color: #e8f5e9; padding: 10px; border-radius: 10px; margin: 10px 0; direction: rtl;'><b>سیستم:</b> {text}</div>",
                    unsafe_allow_html=True)

    # Clear conversation button
    if st.session_state.conversation:
        if st.button("پاک کردن گفتگو", key="clear_chat"):
            st.session_state.conversation = []
            st.experimental_rerun()

    # Footer
    st.markdown("---")
    st.markdown('<div class="footer">سیستم پاسخ‌دهی به سوالات درباره کتاب‌های انگلیسی با استفاده از هوش مصنوعی</div>',
                unsafe_allow_html=True)


if __name__ == "__main__":
    main()