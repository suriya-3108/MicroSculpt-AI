# ============================================
# FILE: module4_dependency_graph.py
# PURPOSE: Module 4 - Enhanced Dependency Graph
# ============================================

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import io
import base64

def render_module4():
    st.header("4️⃣ Dependency Visualization")
    
    if 'functions_data' not in st.session_state:
        st.warning("No data found.")
        return
        
    functions = st.session_state.functions_data
    
    # Build Graph
    G = nx.DiGraph()
    
    for func in functions:
        G.add_node(func['name'], type='function')
        
        # Add edges (calls)
        # Note: Parsers need to populate 'calls'
        if 'calls' in func:
            for called in func['calls']:
                # Only add if called function is essentially part of our code/graph
                # Check if called entity exists in our functions list (simple check)
                known_funcs = [f['name'] for f in functions]
                if called in known_funcs:
                    G.add_edge(func['name'], called)
    
    # 2. Visualize
    st.markdown("### Interactive Call Graph")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if len(G.nodes) > 0:
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Better layout for readability
            if len(G.nodes) < 10:
                pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
            else:
                pos = nx.kamada_kawai_layout(G)
            
            # Draw nodes
            nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='#234C6A', 
                                 alpha=0.9, node_shape='o')
            
            # Draw edges
            nx.draw_networkx_edges(G, pos, width=2, alpha=0.5, 
                                 edge_color='#456882', arrows=True, 
                                 arrowsize=20, arrowstyle='->')
            
            # Draw labels with better formatting
            labels = {node: node for node in G.nodes()}
            
            # Wrap long labels
            wrapped_labels = {}
            for node, label in labels.items():
                if len(label) > 15:
                    # Split at underscores or camelCase
                    parts = label.replace('_', '_\n').split('\n')
                    wrapped_labels[node] = '\n'.join(parts[:2])  # Max 2 lines
                else:
                    wrapped_labels[node] = label
            
            nx.draw_networkx_labels(G, pos, wrapped_labels, 
                                  font_size=8, font_color='white', 
                                  font_weight='bold', font_family='sans-serif')
            
            plt.axis('off')
            plt.tight_layout()
            
            # Save to buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            plt.close()
            buf.seek(0)
            img_b64 = base64.b64encode(buf.read()).decode()
            
            st.markdown(
                f'<img src="data:image/png;base64,{img_b64}" style="width:100%; border-radius:10px; border:1px solid #ddd;">',
                unsafe_allow_html=True
            )
        else:
            st.info("No dependencies found to visualize. Single functions detected.")

    with col2:
        st.subheader("Metrics")
        st.metric("Total Functions", len(G.nodes))
        st.metric("Connections", len(G.edges))
        
        # Isolated
        isolated = [n for n in G.nodes if G.degree(n) == 0]
        st.metric("Isolated", len(isolated))
        
    # Navigation
    st.write("---")
    if st.button("Next: Service Grouping ➡"):
        st.session_state.current_module = 5
        st.rerun()
