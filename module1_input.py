# ============================================
# FILE: module1_input.py
# PURPOSE: Module 1 - Multi-language Input & Detection
# ============================================

import streamlit as st
from language_detector import LanguageDetector
from parsers import get_parser

def render_module1():
    st.header("1️⃣ Code Input & Analysis")
    st.markdown("Upload your code files or paste content below. Supporting **Python, JavaScript, TypeScript**.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        tab1, tab2 = st.tabs(["📤 Upload File", "📝 Paste Code"])
        
        code_content = None
        file_name = "pasted_code"
        
        with tab1:
            uploaded_file = st.file_uploader(
                "Choose a code file", 
                type=['py', 'js', 'ts', 'java', 'go', 'cs']
            )
            if uploaded_file:
                code_content = uploaded_file.read().decode('utf-8')
                file_name = uploaded_file.name
        
        with tab2:
            pasted_code = st.text_area("Paste code here", height=300)
            if pasted_code:
                code_content = pasted_code
                
    with col2:
        if code_content:
            # 1. Detect Language
            language = LanguageDetector.detect_language(file_name, code_content)
            
            st.info(f"🔍 Detected Language: **{language.upper()}**")
            st.code(code_content, language=language if language != 'unknown' else 'text')
            
            # 2. Parse Code
            if language != 'unknown':
                parser = get_parser(language)
                if parser:
                    with st.spinner("Parsing code structure..."):
                        functions = parser.parse(code_content)
                        st.success(f"✅ Found {len(functions)} functions/methods")
                        
                        # Store in session state
                        st.session_state.current_code = code_content
                        st.session_state.current_language = language
                        st.session_state.functions_data = functions
                        st.session_state.filename = file_name
                        
                        # Navigation
                        if st.button("Next: Bug Detection ➡", type="primary"):
                            st.session_state.current_module = 2
                            st.rerun()
                else:
                    st.warning(f"Parser for {language} is coming soon!")
            else:
                st.error("Could not detect language. Please check file extension or content.")
    
    # Reset/Clear
    if st.button("🔄 Clear All"):
        st.session_state.current_code = None
        st.rerun()
