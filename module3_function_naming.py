# ============================================
# FILE: module3_function_naming.py
# PURPOSE: Module 3 - Smart AI Function Naming
# ============================================

import streamlit as st
from api_manager import api_client
import json
import re

# Helper to update code (moved to global scope)
def update_code_with_names(original_code, name_map):
    new_code = original_code
    # Sort by length desc to avoid partial matches
    for old, new in sorted(name_map.items(), key=lambda x: len(x[0]), reverse=True):
        # Python def with word boundary
        new_code = re.sub(rf'def\s+{old}\b', f'def {new}', new_code)
        # Calls with word boundary
        new_code = re.sub(rf'\b{old}\s*\(', f'{new}(', new_code)
    return new_code

def render_module3():
    st.header("3️⃣ Smart Function Naming")
    
    if 'current_code' not in st.session_state:
        st.warning("Please start from Module 1.")
        return
    
    code = st.session_state.current_code
    language = st.session_state.current_language
    functions = st.session_state.functions_data
    
    # Check if already done
    if st.session_state.get('renaming_done', False):
        st.success("✅ Function names have been updated!")
        
        with st.expander("📄 View Updated Code"):
            st.code(st.session_state.current_code, language=language)
            
        if st.button("Reset & Rename Again"):
            st.session_state.renaming_done = False
            del st.session_state.naming_suggestions
            st.rerun()
            
        st.write("---")
        if st.button("Next: Dependency Graph ➡", type="primary"):
            st.session_state.current_module = 4
            st.rerun()
        return

    st.markdown("AI will analyze your functions and suggest more meaningful business-logic names.")
    
    # 1. Analyze and Suggest
    if 'naming_suggestions' not in st.session_state:
        if st.button("🧠 Analyze Function Names", type="primary"):
            with st.spinner("AI is brainstorming better names..."):
                # Extract function names
                func_names = [f['name'] for f in functions]
                
                prompt = f"""
                Analyze the following {language} function names and suggest better, more descriptive names.
                
                Current Functions: {func_names}
                
                Code Context (first 2000 chars):
                {code[:2000]}
                
                Return ONLY a valid JSON object.
                CRITICAL rules for JSON:
                1. Use double quotes for all keys and strings.
                2. Escape all newlines in strings with \\n.
                3. No markdown formatting.
                
                Structure:
                {{
                    "suggestions": [
                        {{"current": "old_name", "suggested": "new_name", "reason": "why this is better"}}
                    ]
                }}
                
                If all names are good, return: {{"suggestions": []}}
                """
                
                response, provider = api_client.generate_content(prompt)
                
                if response:
                    # json and re are already imported globally
                    try:
                        # Robust extraction: Find first { and last }
                        # This handles code blocks, plain text with json, etc.
                        json_str = response.strip()
                        match = re.search(r'\{[\s\S]*\}', json_str)
                        
                        if match:
                            json_str = match.group(0)
                        
                        data = json.loads(json_str)
                        st.session_state.naming_suggestions = data.get('suggestions', [])
                        st.session_state.naming_provider = provider
                        st.rerun()
                    except json.JSONDecodeError as e:
                        st.error(f"❌ Failed to parse AI response")
                        st.warning("AI returned invalid JSON.")
                        with st.expander("🔍 View Raw Response"):
                            st.code(response)
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
                        with st.expander("🔍 View Raw Response"):
                            st.code(response)
                else:
                    st.error("❌ AI Analysis failed. All APIs unavailable.")
    
    # 2. Review Suggestions
    if 'naming_suggestions' in st.session_state:
        suggestions = st.session_state.naming_suggestions
        
        if not suggestions:
            st.info("✅ All function names look good! No changes needed.")
            if st.button("Continue"):
                 st.session_state.renaming_done = True
                 st.rerun()
        else:
            st.subheader("💡 Renaming Suggestions")
            
            # Form for capturing input ONLY
            with st.form("renaming_form"):
                current_renames = {}
                for item in suggestions:
                    c1, c2, c3 = st.columns([1, 1, 2])
                    with c1:
                        st.code(item['current'], language='text')
                    with c2:
                        new_name = st.text_input("New Name", value=item['suggested'], key=f"name_{item['current']}", label_visibility="collapsed")
                        current_renames[item['current']] = new_name
                    with c3:
                        st.caption(item['reason'])
                    st.divider()
                
                # The button must be the LAST thing in the form
                submitted = st.form_submit_button("✅ Apply Checked Renames")

            # Logic OUTSIDE the form
            if submitted:
                # Update code
                new_code = update_code_with_names(code, current_renames)
                st.session_state.current_code = new_code
                
                # Update functions data
                for f in st.session_state.functions_data:
                    if f['name'] in current_renames:
                        f['name'] = current_renames[f['name']]
                        
                st.success("Function names updated successfully!")
                st.session_state.renaming_done = True
                
                # Wait a moment for user to see success message before rerun
                import time
                time.sleep(1)
                st.rerun()


    # Navigation (Only show if not done, otherwise handled at top)
    st.write("---")
    if st.button("Skip Renaming ➡"):
        st.session_state.current_module = 4
        st.rerun()
