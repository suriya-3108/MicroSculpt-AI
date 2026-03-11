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
            # Scale figure size based on node count for readability
            n = len(G.nodes)
            fig_w = max(14, min(24, n * 0.8))
            fig_h = max(10, min(18, n * 0.6))
            fig, ax = plt.subplots(figsize=(fig_w, fig_h))
            
            # Layout — use spring_layout with spacing scaled to node count
            k_spacing = max(1.5, n * 0.15)  # More space between nodes for larger graphs
            if n < 10:
                pos = nx.spring_layout(G, k=k_spacing, iterations=100, seed=42)
            else:
                # spring_layout with high k gives better spread than kamada_kawai for dense graphs
                pos = nx.spring_layout(G, k=k_spacing, iterations=200, seed=42, scale=2.0)
            
            # Scale node size: smaller nodes for larger graphs, but always readable
            node_size = max(800, min(2500, 4000 - n * 80))
            font_size = max(6, min(9, 12 - n * 0.15))
            
            # Draw nodes
            nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color='#234C6A', 
                                 alpha=0.9, node_shape='o', edgecolors='#1a3a52',
                                 linewidths=1.5)
            
            # Draw edges with curved arrows to reduce overlap
            nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.4, 
                                 edge_color='#456882', arrows=True, 
                                 arrowsize=15, arrowstyle='-|>',
                                 connectionstyle='arc3,rad=0.1',
                                 min_source_margin=15, min_target_margin=15)
            
            # Labels — wrap long names
            labels = {node: node for node in G.nodes()}
            wrapped_labels = {}
            for node, label in labels.items():
                if len(label) > 20:
                    # Split at underscores and wrap into 2-3 lines
                    parts = label.split('_')
                    lines = []
                    current_line = ''
                    for part in parts:
                        if len(current_line) + len(part) + 1 > 12:
                            lines.append(current_line)
                            current_line = part
                        else:
                            current_line = current_line + '_' + part if current_line else part
                    if current_line:
                        lines.append(current_line)
                    wrapped_labels[node] = '\n'.join(lines[:3])
                elif len(label) > 12:
                    mid = len(label) // 2
                    # Find nearest underscore to middle
                    under_pos = label.find('_', mid - 3)
                    if under_pos > 0:
                        wrapped_labels[node] = label[:under_pos] + '\n' + label[under_pos+1:]
                    else:
                        wrapped_labels[node] = label
                else:
                    wrapped_labels[node] = label
            
            nx.draw_networkx_labels(G, pos, wrapped_labels, 
                                  font_size=font_size, font_color='white', 
                                  font_weight='bold', font_family='sans-serif')
            
            plt.axis('off')
            plt.margins(0.1)  # Add padding around graph
            plt.tight_layout(pad=1.5)
            
            # Save to buffer at high DPI for clarity
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', 
                       facecolor='white', edgecolor='none', pad_inches=0.5)
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
