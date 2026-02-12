from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import numpy as np
import re
from app.services.ai_service import AIService

class ClusteringService:
    @staticmethod
    def group_services(functions):
        func_names = [f['name'] for f in functions]
        
        # 1. Feature Extraction
        try:
            vectorizer = TfidfVectorizer(analyzer='word', token_pattern=r'[a-zA-Z_][a-zA-Z0-9_]*')
            features = vectorizer.fit_transform(func_names).toarray()
        except:
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
        
        # 3. Name Services
        # Convert clusters_map to dict for AI
        ai_clusters = {str(k): v for k, v in clusters_map.items()}
        ai_names, provider = AIService.suggest_service_names(ai_clusters)
        
        # Normalize AI names
        normalized_names = {}
        if ai_names:
            for k, v in ai_names.items():
                # extract digit from key
                d = re.search(r'\d+', str(k))
                if d:
                    normalized_names[int(d.group(0))] = v
                    
        # Construct final services dict
        services = {}
        for cid, fnames in clusters_map.items():
            # Get name from AI or Fallback
            svc_name = normalized_names.get(cid, f"Service_{cid+1}")
            
            # Clean name
            svc_name = re.sub(r'[^a-zA-Z0-9]', '', svc_name)
            if not svc_name.endswith("Service"):
                svc_name += "Service"
            
            if svc_name in services:
                services[svc_name].extend(fnames)
            else:
                services[svc_name] = fnames
                
        return {
            "services": services,
            "count": len(services),
            "provider": provider
        }
