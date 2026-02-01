# ============================================
# FILE: module5_service_grouping.py
# PURPOSE: Module 5 - Smart Service Grouping
# ============================================

import streamlit as st
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict

def render_module5():
    st.header("5️⃣ Smart Service Grouping")
    
    if 'functions_data' not in st.session_state:
        st.warning("No data found.")
        return
        
    functions = st.session_state.functions_data
    func_names = [f['name'] for f in functions]
    
    st.markdown("Grouping functions into logical microservices based on semantic similarity and metrics.")
    
    if 'services' not in st.session_state:
        with st.spinner("AI is architecting your microservices..."):
            # 1. Feature Extraction
            try:
                vectorizer = TfidfVectorizer(analyzer='word', token_pattern=r'[a-zA-Z_][a-zA-Z0-9_]*')
                features = vectorizer.fit_transform(func_names).toarray()
            except:
                # Fallback for small datasets
                features = np.eye(len(func_names))
            
            # 2. Clustering (KMeans)
            n_samples = len(func_names)
            n_clusters = max(2, min(5, n_samples // 3))
            
            if n_samples < 2:
                clusters_map = {0: func_names}
            else:
                kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                labels = kmeans.fit_predict(features)
                
                clusters_map = defaultdict(list)
                for name, label in zip(func_names, labels):
                    clusters_map[int(label)].append(name)
            
            # 3. Name Services (AI Powered)
            from api_manager import api_client
            
            # Prepare cluster data for AI
            cluster_desc = ""
            for cid, fnames in clusters_map.items():
                cluster_desc += f"Cluster {cid}: {', '.join(fnames)}\n"
            
            prompt = f"""
            I have grouped function names into clusters. Suggest a CamelCase specific microservice name for each cluster.
            Examples: UserService, PaymentService, InventoryService.
            
            Clusters:
            {cluster_desc}
            
            Return ONLY a JSON object mapping Cluster ID to Name:
            {{ "0": "NameService", "1": "AnotherService" }}
            """
            
            try:
                response, _ = api_client.generate_content(prompt)
                import json
                import re
                
                # Robust JSON extraction
                json_str = response.strip()
                match = re.search(r'\{[\s\S]*\}', json_str)
                if match:
                    json_str = match.group(0)
                
                # Clean potential bad keys (AI might use "Cluster 0" instead of "0")
                ai_names = json.loads(json_str)
                # Normalize keys to int
                normalized_names = {}
                for k, v in ai_names.items():
                    # extract digit
                    d = re.search(r'\d+', str(k))
                    if d:
                        normalized_names[int(d.group(0))] = v
                        
            except Exception as e:
                # Fallback if AI fails
                normalized_names = {}

            services = {}
            for cid, fnames in clusters_map.items():
                # Get name from AI or Fallback
                svc_name = normalized_names.get(cid, f"Service_{cid+1}")
                
                # Clean name (ensure it looks like a class name)
                # Remove spaces, special chars
                svc_name = re.sub(r'[^a-zA-Z0-9]', '', svc_name)
                if not svc_name.endswith("Service"):
                    svc_name += "Service"
                
                # Merge checks
                if svc_name in services:
                    services[svc_name].extend(fnames)
                else:
                    services[svc_name] = fnames
                
            st.session_state.services = services
            
    # Display Services
    services = st.session_state.services
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        for svc_name, svc_funcs in services.items():
            with st.expander(f"📦 {svc_name}", expanded=True):
                st.write("**Functions:**")
                # Fancy chips
                html = "".join([f"<span style='background:#334155; color:white; padding:2px 8px; border-radius:12px; margin:2px; display:inline-block; font-size:0.8em'>{f}</span>" for f in svc_funcs])
                st.markdown(html, unsafe_allow_html=True)
                
    with col2:
        st.info(f"Created {len(services)} Microservices")
        if st.button("Regenerate Grouping"):
            del st.session_state.services
            st.rerun()

    # Navigation
    st.write("---")
    if st.button("Next: Code Generation ➡"):
        st.session_state.current_module = 6
        st.rerun()
