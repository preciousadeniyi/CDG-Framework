"""
Insight Moment Simulation
Demonstrates geodesic formation during "Aha!" moments
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class InsightSimulation:
    def __init__(self):
        self.concepts = ['Problem', 'Frustration', 'Incubation', 'Hint', 'Solution']
        self.initial_distances = {
            ('Problem', 'Solution'): 5.0,  # Initially far apart
            ('Problem', 'Hint'): 3.0,
            ('Hint', 'Solution'): 4.0,
            ('Problem', 'Frustration'): 1.0,
            ('Frustration', 'Incubation'): 2.0,
            ('Incubation', 'Hint'): 1.5,
        }
        
        self.insight_probability = 0.3  # Base probability of insight
        
    def create_concept_network(self, insight_occurred=False):
        """Create semantic network with or without insight"""
        G = nx.Graph()
        
        for concept in self.concepts:
            G.add_node(concept)
        
        # Add edges with distances
        for (c1, c2), dist in self.initial_distances.items():
            G.add_edge(c1, c2, weight=dist, distance=dist)
        
        # Insight creates direct connection
        if insight_occurred:
            G.add_edge('Problem', 'Solution', weight=1.0, distance=1.0)  # New geodesic!
            
        return G
    
    def simulate_insight_process(self, n_simulations=1000):
        """Simulate multiple insight scenarios"""
        print("=== Insight Moment Simulation ===\n")
        
        insight_count = 0
        path_lengths_before = []
        path_lengths_after = []
        insight_gains = []
        
        for i in range(n_simulations):
            # Randomly determine if insight occurs
            insight_occurred = np.random.random() < self.insight_probability
            
            # Before insight
            G_before = self.create_concept_network(insight_occurred=False)
            try:
                path_before = nx.shortest_path(G_before, 'Problem', 'Solution', weight='weight')
                distance_before = nx.shortest_path_length(G_before, 'Problem', 'Solution', weight='weight')
            except nx.NetworkXNoPath:
                distance_before = float('inf')
            
            # After insight  
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
                insight_gains.append(distance_before - distance_after)
        
        if insight_count > 0:
            avg_gain = np.mean(insight_gains)
            success_rate = insight_count / n_simulations
            
            print(f"Simulation Results ({n_simulations} trials):")
            print(f"Insight occurrences: {insight_count} ({success_rate*100:.1f}%)")
            print(f"Average path length before insight: {np.mean(path_lengths_before):.2f}")
            print(f"Average path length after insight: {np.mean(path_lengths_after):.2f}")
            print(f"Average insight gain: {avg_gain:.2f} units")
            
            # Statistical significance
            from scipy import stats
            t_stat, p_value = stats.ttest_rel(path_lengths_before, path_lengths_after)
            print(f"Statistical significance: p = {p_value:.4f}")
            
            return {
                'success_rate': success_rate,
                'avg_gain': avg_gain,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
        else:
            print("No insight occurrences in simulation")
            return None
    
    def visualize_insight_network(self):
        """Visualize the concept network before and after insight"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Before insight
        G_before = self.create_concept_network(insight_occurred=False)
        pos = nx.spring_layout(G_before, seed=42)
        
        # Draw network
        nx.draw_networkx_nodes(G_before, pos, node_color='lightblue', 
                              node_size=2000, ax=ax1)
        nx.draw_networkx_labels(G_before, pos, ax=ax1)
        
        # Draw edges with weights
        edges = G_before.edges(data=True)
        nx.draw_networkx_edges(G_before, pos, edgelist=edges, ax=ax1)
        edge_labels = {(u, v): f"{d['weight']:.1f}" for u, v, d in edges}
        nx.draw_networkx_edge_labels(G_before, pos, edge_labels=edge_labels, ax=ax1)
        
        ax1.set_title('Before Insight: Indirect Path\n(Problem → Hint → Solution)', fontsize=14)
        ax1.axis('off')
        
        # After insight
        G_after = self.create_concept_network(insight_occurred=True)
        
        # Draw network
        nx.draw_networkx_nodes(G_after, pos, node_color='lightgreen', 
                              node_size=2000, ax=ax2)
        nx.draw_networkx_labels(G_after, pos, ax=ax2)
        
        # Draw edges with weights
        edges = G_after.edges(data=True)
        regular_edges = [(u, v) for u, v, d in edges if (u, v) != ('Problem', 'Solution')]
        insight_edge = [('Problem', 'Solution')]
        
        nx.draw_networkx_edges(G_after, pos, edgelist=regular_edges, ax=ax2)
        nx.draw_networkx_edges(G_after, pos, edgelist=insight_edge, 
                              edge_color='red', width=3, ax=ax2)
        
        edge_labels = {(u, v): f"{d['weight']:.1f}" for u, v, d in edges}
        nx.draw_networkx_edge_labels(G_after, pos, edge_labels=edge_labels, ax=ax2)
        
        ax2.set_title('After Insight: Direct Geodesic\n(Problem → Solution)', fontsize=14)
        ax2.axis('off')
        
        plt.tight_layout()
        plt.savefig('insight_network.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def calculate_insight_probability(self, current_network):
        """Calculate probability of insight based on network structure"""
        try:
            current_distance = nx.shortest_path_length(current_network, 'Problem', 'Solution', weight='weight')
            
            # Insight more likely when current path is long but not infinite
            if current_distance < float('inf'):
                # Base probability decreases with distance but has random component
                probability = max(0.1, self.insight_probability * (5.0 / current_distance))
                return min(probability, 0.8)  # Cap at 80%
            else:
                return 0.1  # Low probability if no path exists
        except nx.NetworkXNoPath:
            return 0.1

# Run insight simulation
if __name__ == "__main__":
    insight_sim = InsightSimulation()
    
    # Single demonstration
    print("=== Single Insight Demonstration ===")
    
    # Before insight
    G_before = insight_sim.create_concept_network(insight_occurred=False)
    path_before = nx.shortest_path(G_before, 'Problem', 'Solution', weight='weight')
    distance_before = nx.shortest_path_length(G_before, 'Problem', 'Solution', weight='weight')
    
    print("BEFORE INSIGHT:")
    print(f"Path: {' → '.join(path_before)}")
    print(f"Distance: {distance_before:.1f}")
    print(f"Complexity: High (indirect path)\n")
    
    # After insight  
    G_after = insight_sim.create_concept_network(insight_occurred=True)
    path_after = nx.shortest_path(G_after, 'Problem', 'Solution', weight='weight')
    distance_after = nx.shortest_path_length(G_after, 'Problem', 'Solution', weight='weight')
    
    print("AFTER INSIGHT:")
    print(f"Path: {' → '.join(path_after)}")
    print(f"Distance: {distance_after:.1f}") 
    print(f"Complexity: Low (direct geodesic)")
    
    # Calculate insight "gain"
    gain = distance_before - distance_after
    print(f"\nInsight Gain: {gain:.1f} units ({gain/distance_before*100:.1f}% reduction)")
    
    # Probability calculation
    insight_prob = insight_sim.calculate_insight_probability(G_before)
    print(f"Insight Probability: {insight_prob:.2f}")
    
    print("\n" + "="*50)
    
    # Multiple simulations for statistics
    results = insight_sim.simulate_insight_process(n_simulations=1000)
    
    print("\nCDG Explanation:")
    print("• Insight occurs when new geodesic forms between distant concepts")
    print("• Creates optimal cognitive pathway for sudden understanding") 
    print("• Geometric distance reduction correlates with subjective 'Aha!' intensity")
    
    # Create visualization
    insight_sim.visualize_insight_network()
