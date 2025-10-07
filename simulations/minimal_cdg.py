"""
CDG Minimal Simulation: 2D Emotion Space
Demonstrates core geometric principles of the Curved Dynamic Geometry framework

This simulation implements:
1. Meaning-space manifold with emotional curvature
2. Geodesic thought trajectories
3. Consciousness threshold detection
4. Concept relationships in curved space
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from typing import Dict, List, Tuple, Optional

class MinimalCDG:
    """
    Minimal implementation of CDG framework in 2D emotion space.
    Demonstrates how geometric curvature shapes cognitive processes.
    """
    
    def __init__(self, consciousness_threshold: float = 2.5):
        """
        Initialize the CDG emotion space with fundamental concepts.
        
        Parameters:
        consciousness_threshold: Minimum integrated curvature for conscious experience
        """
        # 2D emotion space coordinates: valence (x) and arousal (y)
        self.concepts: Dict[str, List[float]] = {
            'joy': [0.8, 0.7],        # High valence, high arousal
            'sadness': [-0.8, -0.6],   # Low valence, low arousal  
            'anger': [-0.6, 0.9],      # Low valence, high arousal
            'fear': [-0.7, 0.8],       # Low valence, high arousal
            'calm': [0.6, -0.5],       # High valence, low arousal
            'excitement': [0.7, 0.8],  # High valence, high arousal
            'contentment': [0.6, 0.2], # High valence, medium arousal
            'anxiety': [-0.5, 0.7],    # Low valence, high arousal
            'serenity': [0.7, -0.3]    # High valence, low arousal
        }
        
        self.R_critical = consciousness_threshold
        self.trajectory_history = []
        
    def compute_metric_tensor(self, x: float, y: float) -> np.ndarray:
        """
        Compute Riemannian metric tensor at point (x,y).
        
        The metric defines conceptual distances and relationships:
        - g11: Valence curvature (stronger near emotional extremes)
        - g22: Arousal curvature 
        - g12: Valence-arousal coupling
        
        Parameters:
        x: Valence coordinate (-1 to 1)
        y: Arousal coordinate (-1 to 1)
        
        Returns:
        2x2 metric tensor [[g11, g12], [g12, g22]]
        """
        # Enhanced metric with emotional dynamics
        g11 = 1.0 + 0.8 * np.exp(-0.5 * x**2)  # Curvature peaks at valence extremes
        g22 = 1.0 + 0.6 * np.exp(-0.5 * y**2)  # Curvature peaks at arousal extremes
        g12 = 0.3 * x * y * np.exp(-0.3 * (x**2 + y**2))  # Coupling strongest near origin
        
        return np.array([[g11, g12], [g12, g22]])
    
    def compute_christoffel_symbols(self, x: float, y: float) -> np.ndarray:
        """
        Compute Christoffel symbols for parallel transport.
        
        Parameters:
        x, y: Coordinates in emotion space
        
        Returns:
        2x2x2 array of Christoffel symbols Γ^k_ij
        """
        g = self.compute_metric_tensor(x, y)
        g_inv = np.linalg.inv(g)
        
        # Numerical derivatives of metric components
        eps = 1e-6
        dx_g = (self.compute_metric_tensor(x + eps, y) - self.compute_metric_tensor(x - eps, y)) / (2 * eps)
        dy_g = (self.compute_metric_tensor(x, y + eps) - self.compute_metric_tensor(x, y - eps)) / (2 * eps)
        
        # Compute Christoffel symbols: Γ^k_ij = 0.5 * g^kl (∂_i g_jl + ∂_j g_il - ∂_l g_ij)
        gamma = np.zeros((2, 2, 2))
        for k in range(2):
            for i in range(2):
                for j in range(2):
                    total = 0.0
                    for l in range(2):
                        # ∂_i g_jl + ∂_j g_il - ∂_l g_ij
                        derivative_term = 0.0
                        if i == 0:  # ∂_x
                            derivative_term += dx_g[j, l]
                        else:  # ∂_y  
                            derivative_term += dy_g[j, l]
                            
                        if j == 0:  # ∂_x
                            derivative_term += dx_g[i, l]
                        else:  # ∂_y
                            derivative_term += dy_g[i, l]
                            
                        if l == 0:  # ∂_x
                            derivative_term -= dx_g[i, j]
                        else:  # ∂_y
                            derivative_term -= dy_g[i, j]
                        
                        total += g_inv[k, l] * derivative_term
                    
                    gamma[k, i, j] = 0.5 * total
        
        return gamma
    
    def compute_scalar_curvature(self, x: float, y: float) -> float:
        """
        Compute scalar curvature R at point (x,y) using Ricci curvature.
        
        Parameters:
        x, y: Coordinates in emotion space
        
        Returns:
        Scalar curvature R (positive = attractive, negative = repulsive)
        """
        try:
            g = self.compute_metric_tensor(x, y)
            g_inv = np.linalg.inv(g)
            gamma = self.compute_christoffel_symbols(x, y)
            
            # Compute Riemann curvature tensor components
            R_1212 = 0.0
            eps = 1e-6
            
            # Numerical computation of Riemann tensor
            for m in range(2):
                # ∂Γ^m_22/∂x - ∂Γ^m_21/∂y + Γ^m_1p Γ^p_22 - Γ^m_2p Γ^p_21
                dx_gamma_m22 = (self.compute_christoffel_symbols(x + eps, y)[m, 1, 1] - 
                              self.compute_christoffel_symbols(x - eps, y)[m, 1, 1]) / (2 * eps)
                dy_gamma_m21 = (self.compute_christoffel_symbols(x, y + eps)[m, 1, 0] - 
                              self.compute_christoffel_symbols(x, y - eps)[m, 1, 0]) / (2 * eps)
                
                christoffel_terms = 0.0
                for p in range(2):
                    christoffel_terms += (gamma[m, 0, p] * gamma[p, 1, 1] - 
                                        gamma[m, 1, p] * gamma[p, 1, 0])
                
                R_m212 = dx_gamma_m22 - dy_gamma_m21 + christoffel_terms
                R_1212 += g[0, m] * R_m212
            
            # Scalar curvature R = g^ij R_ij = g^ij R^k_ikj
            det_g = np.linalg.det(g)
            if abs(det_g) > 1e-10:
                R = R_1212 / det_g
            else:
                R = 0.0
                
            return R
            
        except (np.linalg.LinAlgError, ZeroDivisionError):
            return 0.0
    
    def geodesic_equation(self, state: List[float], t: float) -> List[float]:
        """
        Geodesic equation defining thought trajectories in curved space.
        
        Parameters:
        state: [x, y, vx, vy] - position and velocity
        t: Time parameter
        
        Returns:
        Derivatives [vx, vy, ax, ay]
        """
        x, y, vx, vy = state
        
        try:
            gamma = self.compute_christoffel_symbols(x, y)
            
            # Geodesic acceleration: a^k = -Γ^k_ij v^i v^j
            ax = -(gamma[0, 0, 0] * vx * vx + 
                   2 * gamma[0, 0, 1] * vx * vy + 
                   gamma[0, 1, 1] * vy * vy)
            
            ay = -(gamma[1, 0, 0] * vx * vx + 
                   2 * gamma[1, 0, 1] * vx * vy + 
                   gamma[1, 1, 1] * vy * vy)
            
            return [vx, vy, ax, ay]
            
        except (np.linalg.LinAlgError, ValueError):
            return [vx, vy, 0.0, 0.0]
    
    def simulate_thought_trajectory(self, start_concept: str, end_concept: str, 
                                  duration: float = 15.0, steps: int = 200) -> np.ndarray:
        """
        Simulate optimal thought path between concepts.
        
        Parameters:
        start_concept: Starting emotional concept
        end_concept: Target emotional concept  
        duration: Simulation time
        steps: Number of integration steps
        
        Returns:
        Array of [x, y] positions along geodesic
        """
        if start_concept not in self.concepts or end_concept not in self.concepts:
            available = list(self.concepts.keys())
            raise ValueError(f"Unknown concept. Available: {available}")
        
        start_pos = self.concepts[start_concept]
        end_pos = self.concepts[end_concept]
        
        # Initial velocity toward target (geodesic initial condition)
        direction = np.array(end_pos) - np.array(start_pos)
        distance = np.linalg.norm(direction)
        
        if distance > 0:
            # Normalize and scale by estimated geodesic length
            initial_velocity = direction / distance * 0.15
        else:
            initial_velocity = [0.1, 0.1]
        
        initial_state = start_pos + initial_velocity.tolist()
        time_points = np.linspace(0, duration, steps)
        
        try:
            trajectory = odeint(self.geodesic_equation, initial_state, time_points)
            self.trajectory_history.append({
                'start': start_concept,
                'end': end_concept,
                'path': trajectory[:, :2],
                'curvature': [self.compute_scalar_curvature(x, y) for x, y in trajectory[:, :2]]
            })
            return trajectory[:, :2]
            
        except Exception as e:
            print(f"Geodesic integration failed: {e}")
            # Fallback: straight line interpolation
            t_vals = np.linspace(0, 1, steps)
            trajectory = np.array([(1-t)*np.array(start_pos) + t*np.array(end_pos) for t in t_vals])
            return trajectory
    
    def assess_consciousness_region(self, bounds: Tuple[float, float, float, float], 
                                  resolution: int = 20) -> Tuple[float, bool]:
        """
        Assess consciousness potential in a region using integrated curvature.
        
        Parameters:
        bounds: (x_min, x_max, y_min, y_max) region boundaries
        resolution: Grid resolution for curvature sampling
        
        Returns:
        (integrated_curvature, is_conscious)
        """
        x_min, x_max, y_min, y_max = bounds
        x_vals = np.linspace(x_min, x_max, resolution)
        y_vals = np.linspace(y_min, y_max, resolution)
        
        total_curvature = 0.0
        valid_points = 0
        
        for x in x_vals:
            for y in y_vals:
                curvature = self.compute_scalar_curvature(x, y)
                if not np.isnan(curvature):
                    total_curvature += abs(curvature)
                    valid_points += 1
        
        if valid_points > 0:
            area = (x_max - x_min) * (y_max - y_min)
            integrated_curvature = total_curvature * area / valid_points
        else:
            integrated_curvature = 0.0
        
        is_conscious = integrated_curvature > self.R_critical
        return integrated_curvature, is_conscious
    
    def compute_geodesic_distance(self, concept1: str, concept2: str, 
                                samples: int = 50) -> float:
        """
        Estimate geodesic distance between concepts.
        
        Parameters:
        concept1, concept2: Concepts to measure distance between
        samples: Number of points along trajectory for distance calculation
        
        Returns:
        Estimated geodesic distance
        """
        trajectory = self.simulate_thought_trajectory(concept1, concept2, steps=samples)
        
        # Riemannian distance along geodesic
        distance = 0.0
        for i in range(len(trajectory) - 1):
            x1, y1 = trajectory[i]
            x2, y2 = trajectory[i + 1]
            
            # Midpoint metric
            x_mid, y_mid = (x1 + x2) / 2, (y1 + y2) / 2
            g = self.compute_metric_tensor(x_mid, y_mid)
            
            dx, dy = x2 - x1, y2 - y1
            ds2 = g[0, 0] * dx * dx + 2 * g[0, 1] * dx * dy + g[1, 1] * dy * dy
            distance += np.sqrt(max(0, ds2))
        
        return distance
    
    def analyze_conceptual_relationships(self) -> Dict[str, Dict[str, float]]:
        """
        Analyze geometric relationships between all concept pairs.
        
        Returns:
        Dictionary of geodesic distances between concepts
        """
        concepts = list(self.concepts.keys())
        relationships = {}
        
        for i, concept1 in enumerate(concepts):
            relationships[concept1] = {}
            for j, concept2 in enumerate(concepts):
                if i != j:
                    distance = self.compute_geodesic_distance(concept1, concept2)
                    relationships[concept1][concept2] = distance
        
        return relationships
    
    def visualize_emotion_space(self, trajectory: Optional[np.ndarray] = None, 
                              show_curvature: bool = True) -> plt.Figure:
        """
        Create comprehensive visualization of CDG emotion space.
        
        Parameters:
        trajectory: Optional thought trajectory to plot
        show_curvature: Whether to display curvature heatmap
        
        Returns:
        matplotlib Figure object
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
        
        # Plot 1: Emotion space with concepts and trajectories
        if show_curvature:
            # Create curvature heatmap
            x_vals = np.linspace(-1, 1, 30)
            y_vals = np.linspace(-1, 1, 30)
            curvature_grid = np.zeros((len(y_vals), len(x_vals)))
            
            for i, x in enumerate(x_vals):
                for j, y in enumerate(y_vals):
                    curvature_grid[j, i] = self.compute_scalar_curvature(x, y)
            
            im = ax1.contourf(x_vals, y_vals, curvature_grid, levels=20, alpha=0.6, cmap='RdBu_r')
            plt.colorbar(im, ax=ax1, label='Scalar Curvature R')
        
        # Plot concepts
        colors = plt.cm.Set3(np.linspace(0, 1, len(self.concepts)))
        for (concept, (x, y)), color in zip(self.concepts.items(), colors):
            ax1.scatter(x, y, s=120, color=color, edgecolors='black', linewidth=1.5, alpha=0.8)
            ax1.annotate(concept, (x + 0.03, y + 0.03), fontsize=9, fontweight='bold',
                        bbox=dict(boxstyle="round,pad=0.3", fc='white', alpha=0.7))
        
        # Plot trajectory if provided
        if trajectory is not None:
            ax1.plot(trajectory[:, 0], trajectory[:, 1], 'r-', linewidth=3, alpha=0.8, 
                    label='Geodesic Thought Path')
            ax1.plot(trajectory[0, 0], trajectory[0, 1], 'go', markersize=10, 
                    markeredgecolor='black', label='Start')
            ax1.plot(trajectory[-1, 0], trajectory[-1, 1], 'bo', markersize=10, 
                    markeredgecolor='black', label='End')
        
        ax1.set_xlabel('Valence (Negative ↔ Positive)', fontsize=12)
        ax1.set_ylabel('Arousal (Low ↔ High)', fontsize=12)
        ax1.set_title('CDG Emotion Space: Curved Geometry of Emotional Concepts', fontsize=14)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        ax1.axis([-1, 1, -1, 1])
        ax1.set_aspect('equal')
        
        # Plot 2: Consciousness assessment
        regions = {
            "High Positive": [0.3, 1.0, 0.3, 1.0],
            "High Negative": [-1.0, -0.3, -1.0, -0.3], 
            "High Arousal": [-1.0, 1.0, 0.5, 1.0],
            "Low Arousal": [-1.0, 1.0, -1.0, -0.5],
            "Mixed Valence": [-0.7, 0.7, -0.7, 0.7]
        }
        
        consciousness_data = []
        for name, bounds in regions.items():
            curv, conscious = self.assess_consciousness_region(bounds)
            consciousness_data.append((name, curv, conscious))
        
        # Bar plot of consciousness potential
        names = [data[0] for data in consciousness_data]
        curvatures = [data[1] for data in consciousness_data]
        colors = ['green' if data[2] else 'red' for data in consciousness_data]
        
        bars = ax2.bar(names, curvatures, color=colors, alpha=0.7)
        ax2.axhline(y=self.R_critical, color='red', linestyle='--', 
                   label=f'Consciousness Threshold (R_c = {self.R_critical})')
        
        ax2.set_ylabel('Integrated Curvature ∫|R| dV', fontsize=12)
        ax2.set_title('Consciousness Potential by Emotional Region', fontsize=14)
        ax2.tick_params(axis='x', rotation=45)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, curv in zip(bars, curvatures):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                    f'{curv:.2f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        return fig


def run_comprehensive_demo():
    """Run comprehensive demonstration of CDG framework."""
    print("=" * 60)
    print("CURVED DYNAMIC GEOMETRY OF MEANING - MINIMAL SIMULATION")
    print("=" * 60)
    
    # Initialize CDG system
    cdg = MinimalCDG(consciousness_threshold=2.5)
    
    print("\n1. EMOTION SPACE CONCEPTS:")
    for concept, (x, y) in cdg.concepts.items():
        curvature = cdg.compute_scalar_curvature(x, y)
        conscious = curvature > cdg.R_critical
        status = "CONSCIOUS" if conscious else "sub-conscious"
        print(f"  {concept:12} : ({x:5.2f}, {y:5.2f}) | R = {curvature:6.3f} | {status}")
    
    # Simulate key thought trajectories
    print("\n2. THOUGHT TRAJECTORIES (Geodesic Paths):")
    transitions = [
        ('sadness', 'joy', "Depression to Happiness"),
        ('fear', 'calm', "Anxiety to Serenity"), 
        ('anger', 'contentment', "Anger to Contentment")
    ]
    
    for start, end, description in transitions:
        trajectory = cdg.simulate_thought_trajectory(start, end)
        distance = cdg.compute_geodesic_distance(start, end)
        print(f"  {start:10} → {end:12} : {description:25} | Distance = {distance:.3f}")
    
    # Consciousness analysis
    print("\n3. CONSCIOUSNESS ASSESSMENT:")
    regions = {
        "Positive Emotions": [0.3, 1.0, -1.0, 1.0],
        "Negative Emotions": [-1.0, -0.3, -1.0, 1.0],
        "High Arousal Zone": [-1.0, 1.0, 0.5, 1.0],
        "Core Emotional Space": [-0.8, 0.8, -0.8, 0.8]
    }
    
    for name, bounds in regions.items():
        curv, conscious = cdg.assess_consciousness_region(bounds, resolution=15)
        status = "✓ CONSCIOUS" if conscious else "✗ sub-conscious"
        print(f"  {name:20} : R_total = {curv:6.3f} | {status}")
    
    # Conceptual relationships
    print("\n4. CONCEPTUAL RELATIONSHIPS (Geodesic Distances):")
    relationships = cdg.analyze_conceptual_relationships()
    
    sample_concepts = ['joy', 'sadness', 'anger', 'calm']
    for concept in sample_concepts:
        closest = sorted(relationships[concept].items(), key=lambda x: x[1])[:3]
        print(f"  {concept:10} closest to: ", end="")
        for other, dist in closest:
            print(f"{other}({dist:.3f}) ", end="")
        print()
    
    print("\n5. CDG PREDICTIONS:")
    print("  • Thought paths curve due to emotional geometry")
    print("  • Consciousness emerges in high-curvature regions") 
    print("  • Conceptual distances reflect emotional similarity")
    print("  • Metric tensor encodes emotional relationships")
    
    # Generate visualization
    print("\n6. GENERATING VISUALIZATION...")
    trajectory = cdg.simulate_thought_trajectory('sadness', 'joy')
    fig = cdg.visualize_emotion_space(trajectory, show_curvature=True)
    
    # Save and display
    plt.savefig('cdg_emotion_space_demo.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print("  Visualization saved as 'cdg_emotion_space_demo.png'")
    
    plt.show()
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    run_comprehensive_demo()
