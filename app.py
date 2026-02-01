# ============================================
# FILE: app.py
# PURPOSE: Main Application Entry Point (Premium UI)
# ============================================

import streamlit as st

# Must be first
st.set_page_config(
    page_title="MicroSculpt AI 2.0",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
with open('styles.css', 'r') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Import Modules
from module1_input import render_module1
from module2_bug_detection import render_module2
from module3_function_naming import render_module3
from module4_dependency_graph import render_module4
from module5_service_grouping import render_module5
from module6_code_generation import render_module6

# Initialize Session State
if 'current_module' not in st.session_state:
    st.session_state.current_module = 1

# Sidebar Navigation
with st.sidebar:
    st.title("🧬 MicroSculpt AI")
    st.caption("v2.0 | Multi-Language & AI-Powered")
    st.divider()
    
    steps = {
        1: "📥 Input & Analysis",
        2: "🐛 Bug Detection",
        3: "🏷️ Smart Naming",
        4: "🕸️ Dependency Graph",
        5: "📦 Service Grouping",
        6: "🚀 Code Generation"
    }
    
    current = st.session_state.current_module
    
    for step, name in steps.items():
        status = "🟢" if current > step else "🔵" if current == step else "⚪"
        style = "font-weight:bold; color:#3b82f6;" if current == step else "color:#94a3b8;"
        if st.button(f"{status} {name}", key=f"nav_{step}", use_container_width=True):
            if step <= current + 1: # Only allow going forward one step or back
                st.session_state.current_module = step
                st.rerun()

    st.divider()
    st.info("💡 **Pro Tip:** Use the AI suggestions in Module 2 & 3 for best results!")

# Main Content Routing
module_map = {
    1: render_module1,
    2: render_module2,
    3: render_module3,
    4: render_module4,
    5: render_module5,
    6: render_module6
}

# Render Current Module
render_func = module_map.get(st.session_state.current_module)
if render_func:
    render_func()
else:
    st.error("Module not found!")
