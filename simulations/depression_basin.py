"""
Depression Basin Simulation
Demonstrates Principle 6: Healing Geometry - Therapeutic smoothing of pathological curvature

This simulation models:
1. Depression as negative curvature basins in emotion space
2. Therapeutic interventions as geometric smoothing processes
3. Recovery as curvature normalization and basin lifting
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from typing import List, Tuple, Dict, Optional
import seaborn as sns

class DepressionBasinSimulation:
    """
    Simulates depression as geometric pathology and therapy as curvature healing.
    
    Implements CDG Principle 6: Healing Geometry
    "Psychological healing involves smoothing pathological curvature gradients"
    """
    
    def __init__(self, depression_strength: float = 0.8, therapy_efficacy: float = 0.12):
        """
        Initialize depression geometry simulation.
        
        Parameters:
        depression_strength: Depth of depression curvature basin (0-1)
        therapy_efficacy: Rate of therapeutic curvature smoothing (0-1)
        """
        # Depression parameters
        self.depression_centers = [
            [-0.7, -0.6],  # Primary depression basin
            [-0.5, -0.8],  # Secondary basin (anhedonia)
            [-0.9, -0.4]   # Tertiary basin (hopelessness)
        ]
        self.depression_strength = depression_strength
        self.depression_width = 0.4  # Spatial extent of depression influence
        
        # Therapy parameters
        self.therapy_efficacy = therapy_efficacy
        self.behavioral_activation_strength = 0.15
        self.cognitive_restructuring_strength = 0.10
        self.mindfulness_strength = 0.08
        
        # Healthy state parameters
        self.healthy_baseline_curvature = 0.25
        self.recovery_threshold = 0.3  # Minimum curvature improvement for success
        
        # Patient state
        self.patient_trajectory = []
        self.therapy_sessions = []
        
    def depression_potential(self, x: float, y: float, therapy_sessions: int = 0) -> float:
        """
        Compute depression-induced negative curvature at position (x,y).
        
        Parameters:
        x, y: Coordinates in emotion space
        therapy_sessions: Number of completed therapy sessions
        
        Returns:
        Total curvature (negative = depression, positive = healthy)
        """
        # Therapy reduces depression strength exponentially
        therapy_factor = np.exp(-therapy_sessions * self.therapy_efficacy)
        current_strength = self.depression_strength * therapy_factor
        
        depression_curvature = 0.0
        
        # Sum contributions from all depression centers
        for center in self.depression_centers:
            dx = x - center[0]
            dy = y - center[1]
            distance_sq = dx**2 + dy**2
            
            # Gaussian depression basin
            basin_contribution = -current_strength * np.exp(-distance_sq / (2 * self.depression_width**2))
            depression_curvature += basin_contribution
        
        # Healthy baseline increases with therapy
        healthy_component = self.healthy_baseline_curvature * (1 - np.exp(-therapy_sessions * 0.08))
        
        # Therapeutic interventions create positive curvature regions
        therapy_benefit = self._compute_therapy_benefits(x, y, therapy_sessions)
        
        total_curvature = depression_curvature + healthy_component + therapy_benefit
        return total_curvature
    
    def _compute_therapy_benefits(self, x: float, y: float, sessions: int) -> float:
        """
        Compute positive curvature contributions from therapeutic interventions.
        
        Parameters:
        x, y: Emotion space coordinates
        sessions: Therapy sessions completed
        
        Returns:
        Positive curvature from therapeutic effects
        """
        if sessions == 0:
            return 0.0
        
        benefit = 0.0
        
        # Behavioral Activation: Creates positive curvature near activity regions
        activity_centers = [[0.6, 0.3], [0.4, 0.5], [0.7, 0.2]]  # Positive engagement areas
        for center in activity_centers:
            dx = x - center[0]
            dy = y - center[1]
            distance_sq = dx**2 + dy**2
            activity_benefit = (self.behavioral_activation_strength * 
                              np.exp(-distance_sq / 0.5) * 
                              (1 - np.exp(-sessions * 0.1)))
            benefit += activity_benefit
        
        # Cognitive Restructuring: Reduces negative thought patterns
        negative_centers = [[-0.6, -0.5], [-0.7, -0.4]]  # Cognitive distortion areas
        for center in negative_centers:
            dx = x - center[0]
            dy = y - center[1]
            distance_sq = dx**2 + dy**2
            if distance_sq < 0.3:  # Only affects nearby negative regions
                restructuring_benefit = (self.cognitive_restructuring_strength *
                                       np.exp(-distance_sq / 0.2) *
                                       (1 - np.exp(-sessions * 0.08)))
                benefit += restructuring_benefit
        
        # Mindfulness: General curvature smoothing
        mindfulness_benefit = (self.mindfulness_strength * 
                             (1 - np.exp(-sessions * 0.06)) *
                             np.exp(-(x**2 + y**2) / 2))
        benefit += mindfulness_benefit
        
        return benefit
    
    def therapeutic_force_field(self, x: float, y: float, sessions: int) -> Tuple[float, float]:
        """
        Compute therapeutic forces guiding patient toward healthier regions.
        
        Parameters:
        x, y: Current position
        sessions: Therapy sessions completed
        
        Returns:
        (force_x, force_y): Therapeutic force vector
        """
        # Force toward positive valence regions
        force_x = 0.0
        force_y = 0.0
        
        # Attraction to positive emotional states
        positive_targets = [[0.6, 0.4], [0.5, 0.3], [0.7, 0.5]]
        for target in positive_targets:
            dx = target[0] - x
            dy = target[1] - y
            distance = np.sqrt(dx**2 + dy**2)
            if distance > 0:
                strength = (self.therapy_efficacy * 
                          np.exp(-sessions * 0.05) / (1 + distance))
                force_x += strength * dx / distance
                force_y += strength * dy / distance
        
        # Repulsion from depression centers (weakened by therapy)
        therapy_factor = np.exp(-sessions * self.therapy_efficacy)
        for center in self.depression_centers:
            dx = x - center[0]
            dy = y - center[1]
            distance = np.sqrt(dx**2 + dy**2)
            if distance > 0:
                repulsion_strength = (0.2 * therapy_factor * 
                                    np.exp(-distance**2 / 0.5))
                force_x += repulsion_strength * dx / distance
                force_y += repulsion_strength * dy / distance
        
        return force_x, force_y
    
    def simulate_therapy_course(self, initial_state: List[float], 
                              total_sessions: int = 16,
                              session_duration: float = 1.0) -> Dict:
        """
        Simulate complete therapeutic course for a depressed patient.
        
        Parameters:
        initial_state: Starting [x,y] position in emotion space
        total_sessions: Number of therapy sessions to simulate
        session_duration: Time per session in arbitrary units
        
        Returns:
        Dictionary containing therapy trajectory and metrics
        """
        current_state = np.array(initial_state, dtype=float)
        trajectory = [current_state.copy()]
        curvature_history = []
        depression_strength_history = []
        therapeutic_forces = []
        
        print(f"Starting therapy simulation from {initial_state}")
        print(f"Target: {total_sessions} sessions")
        
        for session in range(total_sessions):
            # Store pre-session state
            pre_curvature = self.depression_potential(current_state[0], current_state[1], session)
            curvature_history.append(pre_curvature)
            
            # Current depression strength
            current_depression = self.depression_strength * np.exp(-session * self.therapy_efficacy)
            depression_strength_history.append(current_depression)
            
            # Compute therapeutic forces for this session
            force_x, force_y = self.therapeutic_force_field(current_state[0], current_state[1], session)
            therapeutic_forces.append((force_x, force_y))
            
            # Apply therapeutic movement (with some randomness for realism)
            movement_scale = session_duration * (1 + 0.1 * np.random.normal())
            new_x = current_state[0] + force_x * movement_scale
            new_y = current_state[1] + force_y * movement_scale
            
            # Boundary constraints
            new_x = np.clip(new_x, -1.0, 1.0)
            new_y = np.clip(new_y, -1.0, 1.0)
            
            current_state = np.array([new_x, new_y])
            trajectory.append(current_state.copy())
            
            # Session progress report
            if session % 4 == 0 or session == total_sessions - 1:
                curvature_change = pre_curvature - curvature_history[0] if session > 0 else 0
                print(f"  Session {session:2d}: Position ({new_x:6.3f}, {new_y:6.3f}), "
                      f"Curvature: {pre_curvature:7.3f}, Δ: {curvature_change:7.3f}")
        
        # Post-therapy assessment
        final_curvature = self.depression_potential(current_state[0], current_state[1], total_sessions)
        curvature_improvement = final_curvature - curvature_history[0]
        therapy_successful = curvature_improvement > self.recovery_threshold
        
        results = {
            'trajectory': np.array(trajectory),
            'curvature_history': curvature_history,
            'depression_strength_history': depression_strength_history,
            'therapeutic_forces': therapeutic_forces,
            'final_state': current_state,
            'curvature_improvement': curvature_improvement,
            'successful': therapy_successful,
            'recovery_percentage': min(100, max(0, (curvature_improvement / self.recovery_threshold) * 100))
        }
        
        self.patient_trajectory = trajectory
        self.therapy_sessions = list(range(total_sessions))
        
        return results
    
    def create_comprehensive_visualization(self, therapy_results: Dict) -> plt.Figure:
        """
        Create multi-panel visualization of depression therapy simulation.
        
        Parameters:
        therapy_results: Output from simulate_therapy_course
        
        Returns:
        matplotlib Figure object
        """
        fig = plt.figure(figsize=(20, 12))
        
        # 1. 3D Depression Geometry Evolution
        ax1 = fig.add_subplot(231, projection='3d')
        self._plot_3d_geometry_evolution(ax1, therapy_results)
        
        # 2. Therapy Trajectory in Emotion Space
        ax2 = fig.add_subplot(232)
        self._plot_therapy_trajectory(ax2, therapy_results)
        
        # 3. Curvature Improvement Over Time
        ax3 = fig.add_subplot(233)
        self._plot_curvature_progress(ax3, therapy_results)
        
        # 4. Therapeutic Force Analysis
        ax4 = fig.add_subplot(234)
        self._plot_therapeutic_forces(ax4, therapy_results)
        
        # 5. Depression Basin Reduction
        ax5 = fig.add_subplot(235)
        self._plot_basin_reduction(ax5, therapy_results)
        
        # 6. Recovery Metrics
        ax6 = fig.add_subplot(236)
        self._plot_recovery_metrics(ax6, therapy_results)
        
        plt.suptitle('CDG Principle 6: Healing Geometry - Depression Therapy Simulation', 
                    fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()
        
        return fig
    
    def _plot_3d_geometry_evolution(self, ax, results: Dict):
        """Plot 3D visualization of curvature evolution."""
        x = np.linspace(-1, 1, 40)
        y = np.linspace(-1, 1, 40)
        X, Y = np.meshgrid(x, y)
        
        # Pre-therapy geometry
        Z_pre = np.zeros_like(X)
        for i in range(len(x)):
            for j in range(len(y)):
                Z_pre[i, j] = self.depression_potential(X[i, j], Y[i, j], 0)
        
        # Post-therapy geometry
        Z_post = np.zeros_like(X)
        for i in range(len(x)):
            for j in range(len(y)):
                Z_post[i, j] = self.depression_potential(X[i, j], Y[i, j], 
                                                        len(results['curvature_history']))
        
        # Plot pre-therapy
        ax.plot_surface(X, Y, Z_pre, cmap='coolwarm', alpha=0.7, 
                       linewidth=0, antialiased=True, label='Pre-therapy')
        ax.set_title('A. Depression Geometry Evolution', fontsize=12, pad=10)
        ax.set_xlabel('Valence')
        ax.set_ylabel('Arousal')
        ax.set_zlabel('Curvature')
        ax.view_init(elev=25, azim=45)
    
    def _plot_therapy_trajectory(self, ax, results: Dict):
        """Plot patient trajectory through emotion space."""
        trajectory = results['trajectory']
        
        # Create curvature background
        x = np.linspace(-1, 1, 50)
        y = np.linspace(-1, 1, 50)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        
        for i in range(len(x)):
            for j in range(len(y)):
                Z[i, j] = self.depression_potential(X[i, j], Y[i, j], 0)
        
        # Plot curvature contour
        contour = ax.contourf(X, Y, Z, levels=20, alpha=0.6, cmap='RdBu_r')
        plt.colorbar(contour, ax=ax, label='Curvature')
        
        # Plot trajectory
        colors = plt.cm.viridis(np.linspace(0, 1, len(trajectory)))
        for i in range(len(trajectory)-1):
            ax.plot(trajectory[i:i+2, 0], trajectory[i:i+2, 1], 
                   color=colors[i], linewidth=2, alpha=0.8)
        
        # Mark key points
        ax.plot(trajectory[0, 0], trajectory[0, 1], 'ro', markersize=10, 
               label='Start (Depressed)')
        ax.plot(trajectory[-1, 0], trajectory[-1, 1], 'go', markersize=10, 
               label='End (Recovered)')
        
        # Mark depression centers
        for center in self.depression_centers:
            ax.plot(center[0], center[1], 'kx', markersize=8, markeredgewidth=2)
        
        ax.set_xlabel('Valence')
        ax.set_ylabel('Arousal')
        ax.set_title('B. Therapeutic Trajectory in Emotion Space')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
    
    def _plot_curvature_progress(self, ax, results: Dict):
        """Plot curvature improvement over therapy sessions."""
        sessions = self.therapy_sessions
        curvature = results['curvature_history']
        
        ax.plot(sessions, curvature, 'b-', linewidth=3, label='Current Curvature')
        ax.axhline(y=0, color='red', linestyle='--', alpha=0.7, label='Healthy Baseline')
        
        # Fill area under curve for visual emphasis
        ax.fill_between(sessions, curvature, alpha=0.3, color='blue')
        
        # Mark recovery threshold
        recovery_level = results['curvature_history'][0] + self.recovery_threshold
        ax.axhline(y=recovery_level, color='green', linestyle=':', 
                  label=f'Recovery Threshold (Δ={self.recovery_threshold})')
        
        ax.set_xlabel('Therapy Session')
        ax.set_ylabel('Curvature')
        ax.set_title('C. Curvature Improvement Over Time')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_therapeutic_forces(self, ax, results: Dict):
        """Plot therapeutic forces guiding recovery."""
        forces = np.array(results['therapeutic_forces'])
        force_magnitudes = np.sqrt(forces[:, 0]**2 + forces[:, 1]**2)
        
        sessions = self.therapy_sessions
        
        ax.plot(sessions, force_magnitudes, 'orange', linewidth=2, label='Force Magnitude')
        ax.plot(sessions, forces[:, 0], 'r--', alpha=0.7, label='Valence Force (X)')
        ax.plot(sessions, forces[:, 1], 'b--', alpha=0.7, label='Arousal Force (Y)')
        
        ax.set_xlabel('Therapy Session')
        ax.set_ylabel('Therapeutic Force')
        ax.set_title('D. Therapeutic Forces During Recovery')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_basin_reduction(self, ax, results: Dict):
        """Plot reduction in depression basin strength."""
        depression_strength = results['depression_strength_history']
        sessions = self.therapy_sessions
        
        ax.plot(sessions, depression_strength, 'purple', linewidth=3, 
               label='Depression Basin Strength')
        
        # Exponential fit to show decay pattern
        if len(sessions) > 1:
            from scipy.optimize import curve_fit
            def exp_decay(x, a, b):
                return a * np.exp(-b * x)
            
            try:
                popt, _ = curve_fit(exp_decay, sessions, depression_strength, 
                                  p0=[depression_strength[0], self.therapy_efficacy])
                ax.plot(sessions, exp_decay(sessions, *popt), 'r--', 
                       label=f'Exponential Decay (τ={1/popt[1]:.2f})')
            except:
                pass
        
        ax.set_xlabel('Therapy Session')
        ax.set_ylabel('Depression Strength')
        ax.set_title('E. Depression Basin Reduction')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_recovery_metrics(self, ax, results: Dict):
        """Plot final recovery metrics and success indicators."""
        metrics = {
            'Curvature Improvement': results['curvature_improvement'],
            'Recovery Percentage': results['recovery_percentage'],
            'Final Valence': results['final_state'][0],
            'Final Arousal': results['final_state'][1],
            'Sessions Required': len(self.therapy_sessions)
        }
        
        colors = ['green' if results['successful'] else 'red', 
                 'lightgreen', 'lightblue', 'lightblue', 'orange']
        
        bars = ax.bar(range(len(metrics)), list(metrics.values()), color=colors, alpha=0.7)
        
        ax.set_xticks(range(len(metrics)))
        ax.set_xticklabels(list(metrics.keys()), rotation=45, ha='right')
        ax.set_ylabel('Metric Value')
        ax.set_title('F. Final Recovery Metrics')
        
        # Add value labels on bars
        for bar, value in zip(bars, metrics.values()):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                   f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # Success indicator
        status = "SUCCESSFUL RECOVERY" if results['successful'] else "INCOMPLETE RECOVERY"
        status_color = "green" if results['successful'] else "red"
        ax.text(0.5, 0.95, status, transform=ax.transAxes, ha='center', 
               fontsize=12, fontweight='bold', color=status_color,
               bbox=dict(boxstyle="round,pad=0.3", facecolor=status_color, alpha=0.2))


def run_depression_therapy_demo():
    """Run comprehensive depression therapy simulation demonstration."""
    print("=" * 70)
    print("CDG PRINCIPLE 6: HEALING GEOMETRY - DEPRESSION THERAPY SIMULATION")
    print("=" * 70)
    
    # Initialize simulation
    sim = DepressionBasinSimulation(depression_strength=0.85, therapy_efficacy=0.15)
    
    # Simulate therapy for severely depressed patient
    print("\n1. PATIENT PROFILE:")
    print("   Initial State: Severe Depression (Deep curvature basin)")
    print("   Depression Centers:", sim.depression_centers)
    print("   Therapy Plan: 16-session CBT + Behavioral Activation")
    
    initial_state = [-0.65, -0.55]  # Starting in depression basin
    therapy_results = sim.simulate_therapy_course(initial_state, total_sessions=16)
    
    print(f"\n2. THERAPY OUTCOMES:")
    print(f"   Initial Curvature: {therapy_results['curvature_history'][0]:.3f}")
    print(f"   Final Curvature: {therapy_results['curvature_history'][-1]:.3f}")
    print(f"   Curvature Improvement: {therapy_results['curvature_improvement']:.3f}")
    print(f"   Recovery Threshold: {sim.recovery_threshold:.3f}")
    print(f"   Therapy Successful: {therapy_results['successful']}")
    print(f"   Recovery Percentage: {therapy_results['recovery_percentage']:.1f}%")
    
    print(f"\n3. FINAL POSITION:")
    final_pos = therapy_results['final_state']
    print(f"   Valence: {final_pos[0]:.3f} (Initial: {initial_state[0]:.3f})")
    print(f"   Arousal: {final_pos[1]:.3f} (Initial: {initial_state[1]:.3f})")
    
    distance_from_depression = min(np.linalg.norm(final_pos - center) 
                                 for center in sim.depression_centers)
    print(f"   Distance from Nearest Depression Center: {distance_from_depression:.3f}")
    
    print("\n4. CDG INSIGHTS:")
    print("   • Depression manifests as negative curvature basins")
    print("   • Therapy creates positive curvature through multiple mechanisms")
    print("   • Recovery involves geometric smoothing and basin lifting")
    print("   • Successful treatment requires ΔR > recovery threshold")
    
    # Generate comprehensive visualization
    print("\n5. GENERATING VISUALIZATION...")
    fig = sim.create_comprehensive_visualization(therapy_results)
    
    # Save high-quality figure
    plt.savefig('cdg_depression_therapy_simulation.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("   Visualization saved as 'cdg_depression_therapy_simulation.png'")
    
    plt.show()
    
    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
    
    return therapy_results


if __name__ == "__main__":
    # Run the comprehensive demonstration
    results = run_depression_therapy_demo()
    
    # Additional analysis for research purposes
    print("\nADDITIONAL ANALYSIS:")
    print(f"Final therapeutic force magnitude: {np.linalg.norm(results['therapeutic_forces'][-1]):.4f}")
    print(f"Average curvature improvement per session: {results['curvature_improvement']/len(results['curvature_history']):.4f}")
    
    # Check if recovery follows CDG predictions
    cdg_prediction_5 = results['curvature_improvement'] > 0.3
    print(f"CDG Prediction 5 (ΔR > 0.3): {cdg_prediction_5}")
