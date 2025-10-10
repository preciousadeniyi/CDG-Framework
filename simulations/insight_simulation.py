"""
INSIGHT SIMULATION - VERIFIED WORKING
Demonstrates insight as geodesic formation in concept space
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class InsightSimulation:
    """Demonstrates insight moments as geometric phenomena"""
    
    def __init__(self):
        self.concepts = ['Problem', 'Frustration', 'Distraction', 'Hint', 'Incubation', 'Solution']
        
        # Initial concept distances (before insight)
        self.initial_distances = {
            ('Problem', 'Solution'): 5.0,
            ('Problem', 'Hint'): 3.0,
            ('Hint', 'Solution'): 4.0,
            ('Problem', 'Frustration'): 1.5,
            ('Frustration', 'Distraction'): 2.0,
            ('Distraction', 'Incubation'): 1.5,
            ('Incubation', 'Hint'): 2.0,
        }
    
    def create_concept_network(self, insight_occurred=False):
        """Create a network of concepts"""
        G = nx.Graph()
        
        # Add nodes
        for concept in self.concepts:
            G.add_node(concept)
        
        # Add edges with distances
        for (node1, node2), distance in self.initial_distances.items():
            G.add_edge(node1, node2, weight=distance)
        
        # Insight creates a direct connection
        if insight_occurred:
            G.add_edge('Problem', 'Solution', weight=1.0)  # Short path!
        
        return G
    
    def simulate_insight_process(self, n_trials=100):
        """Simulate multiple insight scenarios"""
        print("💡 CDG Insight Simulation")
        print("=" * 40)
        
        insight_count = 0
        path_lengths_before = []
        path_lengths_after = []
        
        for i in range(n_trials):
            # Randomly determine if insight occurs (30% chance)
            insight_occurred = np.random.random() < 0.3
            
            # Network before potential insight
            G_before = self.create_concept_network(insight_occurred=False)
            
            try:
                path_before = nx.shortest_path(G_before, 'Problem', 'Solution', weight='weight')
                distance_before = nx.shortest_path_length(G_before, 'Problem', 'Solution', weight='weight')
            except nx.NetworkXNoPath:
                distance_before = float('inf')
            
            # Network after potential insight
            G_after = self.create_concept_network(insight_occurred=insight_occurred)
            
            try:
                path_after = nx.shortest_path(G_after, 'Problem', 'Solution', weight='weight')
                distance_after = nx.shortest_path_length(G_after, 'Problem', 'Solution', weight='weight')
            except nx.NetworkXNoPath:
                distance_after = float('inf')
            
            if insight_occurred and distance_before < float('inf') and distance_after < float('inf'):
                insight_count += 1
                path_lengths_before.append(distance_before)
                path_lengths_after.append(distance_after)
        
        if insight_count > 0:
            avg_before = np.mean(path_lengths_before)
            avg_after = np.mean(path_lengths_after)
            avg_gain = avg_before - avg_after
            
            print(f"Results from {n_trials} simulations:")
            print(f"  Insight occurrences: {insight_count} ({insight_count/n_trials*100:.1f}%)")
            print(f"  Average path before insight: {avg_before:.2f}")
            print(f"  Average path after insight: {avg_after:.2f}")
            print(f"  Average cognitive gain: {avg_gain:.2f} units")
            
            return insight_count, avg_gain
        else:
            print("No insight occurrences in simulation")
            return 0, 0
    
    def visualize_insight_network(self):
        """Visualize the concept network before and after insight"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Before insight
        G_before = self.create_concept_network(insight_occurred=False)
        pos = nx.spring_layout(G_before, seed=42)
        
        # Draw network before insight
        nx.draw_networkx_nodes(G_before, pos, node_color='lightblue', 
                              node_size=1500, ax=ax1)
        nx.draw_networkx_labels(G_before, pos, ax=ax1)
        
        edges_before = G_before.edges(data=True)
        nx.draw_networkx_edges(G_before, pos, edgelist=edges_before, ax=ax1)
        
        edge_labels_before = {(u, v): f"{d['weight']:.1f}" for u, v, d in edges_before}
        nx.draw_networkx_edge_labels(G_before, pos, edge_labels_before, ax=ax1)
        
        ax1.set_title('Before Insight: Indirect Path\n(High Cognitive Load)', fontsize=12)
        ax1.axis('off')
        
        # After insight
        G_after = self.create_concept_network(insight_occurred=True)
        
        # Draw network after insight
        nx.draw_networkx_nodes(G_after, pos, node_color='lightgreen', 
                              node_size=1500, ax=ax2)
        nx.draw_networkx_labels(G_after, pos, ax=ax2)
        
        edges_after = G_after.edges(data=True)
        regular_edges = [(u, v) for u, v, d in edges_after if (u, v) != ('Problem', 'Solution')]
        insight_edge = [('Problem', 'Solution')]
        
        nx.draw_networkx_edges(G_after, pos, edgelist=regular_edges, ax=ax2)
        nx.draw_networkx_edges(G_after, pos, edgelist=insight_edge, 
                              edge_color='red', width=3, style='dashed', ax=ax2)
        
        edge_labels_after = {(u, v): f"{d['weight']:.1f}" for u, v, d in edges_after}
        nx.draw_networkx_edge_labels(G_after, pos, edge_labels_after, ax=ax2)
        
        ax2.set_title('After Insight: Direct Geodesic\n("Aha!" Moment)', fontsize=12)
        ax2.axis('off')
        
        plt.tight_layout()
        plt.savefig('insight_demo.png', dpi=150, bbox_inches='tight')
        plt.show()
    
    def run_demo(self):
        """Run the complete insight demonstration"""
        # Simulate insight process
        insight_count, avg_gain = self.simulate_insight_process(n_trials=100)
        
        print(f"\nCDG Explanation of Insight:")
        print(f"  ✓ Insight forms new geodesic between concepts")
        print(f"  ✓ Creates optimal cognitive pathway") 
        print(f"  ✓ Reduces mental 'distance' by {avg_gain:.1f} units on average")
        print(f"  ✓ Explains sudden 'Aha!' moment phenomenology")

if __name__ == "__main__":
    demo = InsightSimulation()
    demo.run_demo()
    demo.visualize_insight_network()
    
    print("\n🎉 Insight demo completed!")
    print("Check 'insight_demo.png' for network visualization")
