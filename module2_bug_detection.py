# ============================================
# FILE: module2_bug_detection.py
# PURPOSE: Module 2 - AI Bug Detection & Fixing
# ============================================

import streamlit as st
from api_manager import api_client

def render_module2():
    st.header("2️⃣ AI Bug Detection & Fixing")
    
    if 'current_code' not in st.session_state:
        st.warning("Please upload code in Module 1 first.")
        if st.button("⬅ Go to Module 1"):
            st.session_state.current_module = 1
            st.rerun()
        return

    code = st.session_state.current_code
    language = st.session_state.current_language
    
    st.markdown(f"Analying **{language}** code for bugs, errors, and optimizations...")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Original Code")
        st.code(code, language=language)
        
    with col2:
        st.subheader("AI Analysis")
        
        # Analyze Button
        if 'bug_report' not in st.session_state:
            if st.button("🔍 Run AI Analysis", type="primary"):
                with st.spinner("Consulting AI experts (Gemini/Groq)..."):
                    prompt = f"""
                    Analyze this {language} code for bugs, syntax errors, and logical issues.
                    Return ONLY a valid JSON object.
                    
                    CRITICAL rules for JSON:
                    1. Use double quotes for all keys and strings.
                    2. Escape all newlines in the 'fixed_code' string with \\n (literal backslash n).
                    3. Escape double quotes inside strings with \\".
                    4. No trailing commas.
                    5. No markdown formatting (just the raw JSON string).
                    
                    Expected Structure:
                    {{
                        "issues": ["issue1", "issue2"],
                        "fixed_code": "import os\\nwith open('file') as f:\\n    print(f.read())",
                        "summary": "Added proper file handling"
                    }}
                    
                    CODE:
                    {code}
                    """
                    
                    # Call API
                    response, provider = api_client.generate_content(prompt)
                    
                    if response:
                        import json
                        import re
                        
                        try:
                            # 1. Strip Markdown
                            json_str = response.strip()
                            if '```' in json_str:
                                # Try to match json block first
                                match = re.search(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', json_str)
                                if match:
                                    json_str = match.group(1)
                                else:
                                    # Just find the brace content
                                    match = re.search(r'\{[\s\S]*\}', json_str)
                                    if match:
                                        json_str = match.group(0)
                            
                            # 2. Heuristic Code Cleanup (Fix unescaped newlines in fixed_code)
                            # This is a common AI error with Llama models
                            if '"fixed_code": "' in json_str and '\n' in json_str:
                                # We try to strictly parse first, if it fails, we clean
                                pass

                            try:
                                data = json.loads(json_str, strict=False)
                            except json.JSONDecodeError:
                                # Fallback: The AI likely put real newlines inside the string. 
                                # We'll assume the JSON structure is simple: key: "value".
                                # This is a risky regex but handles the specific case of "fixed_code": "..."
                                # escaping newlines inside the fixed_code value
                                
                                # Pattern finds "fixed_code": "VALUE", and escapes newlines in VALUE
                                def escape_newlines(m):
                                    key = m.group(1)
                                    content = m.group(2)
                                    # Escape newlines and quotes
                                    content = content.replace('\n', '\\n').replace('\r', '').replace('"', '\\"')
                                    return f'{key}"{content}"'
                                
                                # This regex is too hard to get right safely for arbitrary code.
                                # Plan B: Use a manual parser or `demjson` if we had it.
                                # Plan C: Just show the error and let user modify.
                                
                                # Better Plan: Try to sanitize control characters
                                json_str_clean = json_str.replace('\t', '\\t') # minimal cleaning
                                # If it's the "real newline in string" issue:
                                # We can try to use eval() if valid python dict, but it's JSON boolean (true/false) mismatch.
                                
                                # Ultimate Fallback: Extract fixed_code manually if JSON fails completely
                                fixed_code_match = re.search(r'"fixed_code"\s*:\s*"(.*?)"\s*(?:,|\})', json_str, re.DOTALL)
                                if fixed_code_match:
                                    # If we can extract the code, we can reconstruct the object
                                    fixed_code_raw = fixed_code_match.group(1)
                                    # But we can't easily parse the rest.
                                    pass

                                # Re-raise to trigger the error block which shows raw response
                                raise

                            st.session_state.bug_report = data
                            st.session_state.ai_provider = provider
                            st.rerun()
                        except json.JSONDecodeError as e:
                            st.error(f"❌ Failed to parse AI response as JSON")
                            st.warning("The AI returned invalid JSON (likely unescaped code).")
                            with st.expander("🔍 View Raw AI Response (Copy this code manually if needed)"):
                                st.code(response)
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
                            with st.expander("🔍 View Raw AI Response"):
                                st.code(response)
                    else:
                        st.error("❌ AI Analysis failed. All APIs unavailable.")


        # Display Results
        if 'bug_report' in st.session_state:
            report = st.session_state.bug_report
            provider = st.session_state.ai_provider
            
            st.caption(f"Analysis provided by: **{provider}**")
            
            if report.get('issues'):
                st.write("**Issues Found:**")
                for issue in report['issues']:
                    st.error(f"❌ {issue}")
            else:
                st.success("✅ No critical issues found!")
                
            st.write("**Summary of Fixes:**")
            st.info(report.get('summary', 'Code optimized.'))
            
            # Show Fix Code
            with st.expander("View Fixed Code"):
                st.code(report.get('fixed_code'), language=language)
                
            # Actions
            st.write("---")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Apply Fixes"):
                    st.session_state.current_code = report.get('fixed_code')
                    st.session_state.bug_fixed = True
                    st.success("Code updated!")
            with c2:
                if st.button("⏭ Skip / Continue"):
                    st.session_state.current_module = 3
                    st.rerun()
                    
    # Navigation
    st.write("---")
    if st.button("Next: Smart Function Naming ➡"):
        st.session_state.current_module = 3
        st.rerun()
