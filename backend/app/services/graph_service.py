import networkx as nx
import matplotlib
matplotlib.use('Agg') # Non-interactive backend
import matplotlib.pyplot as plt
import io
import base64

class GraphService:
    @staticmethod
    def generate_graph(functions):
        # Build Graph
        G = nx.DiGraph()
        
        known_funcs = set(f['name'] for f in functions)
        
        for func in functions:
            G.add_node(func['name'], type='function')
            
            # Add edges (calls)
            if 'calls' in func:
                for called in func['calls']:
                    # Only add if called function is essentially part of our code/graph
                    if called in known_funcs:
                        G.add_edge(func['name'], called)
        
        # Metrics
        isolated = [n for n in G.nodes if G.degree(n) == 0]
        metrics = {
            "total_functions": len(G.nodes),
            "connections": len(G.edges),
            "isolated": len(isolated)
        }
        
        # Visualize
        if len(G.nodes) > 0:
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Layout
            if len(G.nodes) < 10:
                pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
            else:
                try:
                    pos = nx.kamada_kawai_layout(G)
                except:
                    pos = nx.spring_layout(G)
            
            # Draw
            nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='#234C6A', 
                                 alpha=0.9, node_shape='o')
            
            nx.draw_networkx_edges(G, pos, width=2, alpha=0.5, 
                                 edge_color='#456882', arrows=True, 
                                 arrowsize=20, arrowstyle='->')
            
            # Labels
            labels = {node: node for node in G.nodes()}
            wrapped_labels = {}
            for node, label in labels.items():
                if len(label) > 15:
                    parts = label.replace('_', '_\n').split('\n')
                    wrapped_labels[node] = '\n'.join(parts[:2])
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
            
            return {
                "image": img_b64,
                "metrics": metrics
            }
        else:
            return {
                "image": None,
                "metrics": metrics,
                "message": "No nodes to visualize"
            }
