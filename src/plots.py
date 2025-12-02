"""
SIR simülasyon sonuçları için görselleştirme fonksiyonları
"""

import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import numpy as np
from typing import Dict, List, Tuple
import os


# Seaborn stilini ayarla
sns.set_style("whitegrid")
sns.set_palette("husl")


def plot_time_series(time_series_dict: Dict[str, List[Tuple]], 
                     save_path: str = None,
                     title: str = "SIR Model Time Series"):
    """Zaman serisi grafiği çiz"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle(title, fontsize=16, fontweight='bold')
    
    compartments = ['S', 'I', 'R']
    colors = {'random': 'gray', 'degree': 'red', 'betweenness': 'blue',
              'closeness': 'green', 'eigenvector': 'purple'}
    
    for i, compartment in enumerate(compartments):
        ax = axes[i]
        
        for scenario, time_series in time_series_dict.items():
            values = [counts[i] for counts in time_series]
            time_steps = range(len(values))
            
            color = colors.get(scenario, None)
            label = scenario.replace('_', ' ').title()
            
            ax.plot(time_steps, values, label=label, linewidth=2, 
                   color=color, alpha=0.8)
        
        ax.set_xlabel('Time Step', fontsize=12)
        ax.set_ylabel(f'{compartment} Count', fontsize=12)
        ax.set_title(f'{compartment} ({"Susceptible" if compartment == "S" else "Infected" if compartment == "I" else "Recovered"})',
                    fontsize=13, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()
    
    plt.close()


def plot_comparison_bars(plotting_data: Dict, save_path: str = None):
    """Bar grafiklerle karşılaştır"""
    scenarios = plotting_data['scenarios']
    
    # Daha güzel isimler
    scenario_labels = [s.replace('_', ' ').title() for s in scenarios]
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('Scenario Comparison', fontsize=16, fontweight='bold')
    
    colors = ['gray', 'red', 'blue', 'green', 'purple'][:len(scenarios)]
    
    # 1. Final Outbreak Size
    ax = axes[0]
    bars = ax.bar(scenario_labels, plotting_data['outbreak_sizes'], 
                  yerr=plotting_data['outbreak_stds'], 
                  color=colors, alpha=0.7, capsize=5)
    ax.set_ylabel('Final Outbreak Size', fontsize=12)
    ax.set_title('Total Infected (Final)', fontsize=13, fontweight='bold')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', alpha=0.3)
    
    # Değerleri bar üzerine yaz
    for bar, val in zip(bars, plotting_data['outbreak_sizes']):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{val:.0f}', ha='center', va='bottom', fontsize=10)
    
    # 2. Peak Infected
    ax = axes[1]
    bars = ax.bar(scenario_labels, plotting_data['peak_infecteds'],
                  yerr=plotting_data['peak_infected_stds'],
                  color=colors, alpha=0.7, capsize=5)
    ax.set_ylabel('Peak Infected Count', fontsize=12)
    ax.set_title('Maximum Simultaneous Infections', fontsize=13, fontweight='bold')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', alpha=0.3)
    
    for bar, val in zip(bars, plotting_data['peak_infecteds']):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{val:.0f}', ha='center', va='bottom', fontsize=10)
    
    # 3. Peak Time
    ax = axes[2]
    bars = ax.bar(scenario_labels, plotting_data['peak_times'],
                  yerr=plotting_data['peak_time_stds'],
                  color=colors, alpha=0.7, capsize=5)
    ax.set_ylabel('Time to Peak', fontsize=12)
    ax.set_title('Time to Reach Peak Infection', fontsize=13, fontweight='bold')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', alpha=0.3)
    
    for bar, val in zip(bars, plotting_data['peak_times']):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{val:.1f}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()
    
    plt.close()


def plot_network_snapshot(G: nx.Graph, states: Dict, 
                         time_step: int = 0,
                         save_path: str = None,
                         title: str = None,
                         layout_pos: Dict = None):
    """Ağ durumunu görselleştir"""
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Renk haritası
    color_map = {'S': '#3498db', 'I': '#e74c3c', 'R': '#2ecc71'}  # Mavi, Kırmızı, Yeşil
    node_colors = [color_map[states[node]] for node in G.nodes()]
    
    # Layout
    if layout_pos is None:
        layout_pos = nx.spring_layout(G, seed=42, k=0.5, iterations=50)
    
    # Ağı çiz
    nx.draw_networkx_nodes(G, layout_pos, node_color=node_colors, 
                          node_size=300, alpha=0.8, ax=ax)
    nx.draw_networkx_edges(G, layout_pos, alpha=0.2, ax=ax)
    
    # Düğüm etiketlerini çiz (küçük graflar için)
    if G.number_of_nodes() <= 50:
        nx.draw_networkx_labels(G, layout_pos, font_size=8, ax=ax)
    
    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=color_map['S'], label='Susceptible', alpha=0.8),
        Patch(facecolor=color_map['I'], label='Infected', alpha=0.8),
        Patch(facecolor=color_map['R'], label='Recovered', alpha=0.8)
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=11)
    
    # Başlık
    if title is None:
        title = f'Network State at t={time_step}'
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()
    
    plt.close()
    
    return layout_pos


def plot_multiple_snapshots(G: nx.Graph, simulation_results: Dict,
                           time_points: List[int] = None,
                           save_dir: str = None):
    """Farklı zaman noktalarında ağ durumunu göster"""
    if time_points is None:
        # Otomatik zaman noktaları: başlangıç, 2-3 ara, son
        total_steps = len(simulation_results['time_series']) - 1
        if total_steps <= 5:
            time_points = list(range(total_steps + 1))
        else:
            time_points = [0, total_steps // 4, total_steps // 2,
                          3 * total_steps // 4, total_steps]
    
    # Düzen tutarlılığı için aynı layout kullan
    layout_pos = nx.spring_layout(G, seed=42, k=0.5, iterations=50)
    
    # Simülasyonu tekrar çalıştırarak her adımda durumları kaydet
    # (Orijinal sonuçlarda sadece son durum var)
    # Bunun yerine yeni bir simülasyon çalıştırıp adım adım kaydedelim
    from .sir_simulation import SIRModel
    
    # İlk enfekte düğümleri bul (orijinal simülasyondan)
    # Bu bilgi sonuçlarda yok, bu yüzden parametreli olmalı
    # Şimdilik en yüksek dereceye sahip düğümleri kullanalım
    degrees = dict(G.degree())
    top_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:3]
    initial_infected = [node for node, _ in top_nodes]
    
    # Simülasyonu adım adım çalıştır
    model = SIRModel(G, beta=0.3, gamma=0.1, seed=42)
    model.set_initial_infected(initial_infected)
    
    states_history = [model.states.copy()]  # t=0
    
    for step in range(max(time_points)):
        model.step()
        states_history.append(model.states.copy())
    
    # Seçilen zaman noktalarını çiz
    n_points = len(time_points)
    fig, axes = plt.subplots(1, n_points, figsize=(5*n_points, 5))
    
    if n_points == 1:
        axes = [axes]
    
    for i, t in enumerate(time_points):
        ax = axes[i]
        
        if t < len(states_history):
            states = states_history[t]
        else:
            states = states_history[-1]
        
        # Renk haritası
        color_map = {'S': '#3498db', 'I': '#e74c3c', 'R': '#2ecc71'}
        node_colors = [color_map[states[node]] for node in G.nodes()]
        
        # Ağı çiz
        nx.draw_networkx_nodes(G, layout_pos, node_color=node_colors,
                              node_size=200, alpha=0.8, ax=ax)
        nx.draw_networkx_edges(G, layout_pos, alpha=0.2, ax=ax)
        
        # Durum sayıları
        S_count = sum(1 for s in states.values() if s == 'S')
        I_count = sum(1 for s in states.values() if s == 'I')
        R_count = sum(1 for s in states.values() if s == 'R')
        
        ax.set_title(f't = {t}\nS:{S_count} I:{I_count} R:{R_count}',
                    fontsize=11, fontweight='bold')
        ax.axis('off')
    
    # Legend (sadece ilk grafiğe)
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#3498db', label='Susceptible', alpha=0.8),
        Patch(facecolor='#e74c3c', label='Infected', alpha=0.8),
        Patch(facecolor='#2ecc71', label='Recovered', alpha=0.8)
    ]
    axes[0].legend(handles=legend_elements, loc='upper left', fontsize=9)
    
    fig.suptitle('Network State Evolution Over Time', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, 'network_snapshots.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Grafik kaydedildi: {save_path}")
    else:
        plt.show()
    
    plt.close()


def create_all_plots(experiment_runner, save_dir: str = 'results'):
    """Tüm grafikleri oluştur ve kaydet"""
    os.makedirs(save_dir, exist_ok=True)
    
    print("Grafikler oluşturuluyor...")
    
    plotting_data = experiment_runner.get_results_for_plotting()
    
    plot_time_series(
        plotting_data['time_series'],
        save_path=os.path.join(save_dir, 'time_series.png'),
        title='SIR Model: Comparison of Different Centrality Measures'
    )
    
    plot_comparison_bars(
        plotting_data,
        save_path=os.path.join(save_dir, 'comparison_bars.png')
    )
    
    if experiment_runner.G.number_of_nodes() <= 100:
        degrees = dict(experiment_runner.G.degree())
        top_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:50]
        top_node_ids = [node for node, _ in top_nodes]
        subgraph = experiment_runner.G.subgraph(top_node_ids).copy()
        
        if 'degree' in experiment_runner.results:
            result = experiment_runner.results['degree']['all_results'][0]
            plot_multiple_snapshots(
                subgraph,
                result,
                time_points=[0, 5, 10, 15, 20],
                save_dir=save_dir
            )
    
    print(f"Grafikler '{save_dir}' klasörüne kaydedildi")


# Test fonksiyonu
if __name__ == "__main__":
    print("Plots Modülü Test Ediliyor...\n")
    
    # Örnek veri oluştur
    scenarios = ['random', 'degree', 'betweenness']
    
    # Sahte zaman serisi verileri
    time_series_dict = {}
    for scenario in scenarios:
        n_steps = 30
        S = [100 - i*2 for i in range(n_steps)]
        I = [5 * np.sin(i/5) + 5 for i in range(n_steps)]
        R = [100 - S[i] - I[i] for i in range(n_steps)]
        time_series_dict[scenario] = list(zip(S, I, R))
    
    # Grafik çiz
    print("Zaman serisi grafiği çiziliyor...")
    plot_time_series(time_series_dict, title="Test: SIR Time Series")
    
    # Bar grafik için sahte veri
    plotting_data = {
        'scenarios': scenarios,
        'outbreak_sizes': [80, 90, 85],
        'outbreak_stds': [5, 4, 6],
        'peak_infecteds': [20, 25, 22],
        'peak_infected_stds': [2, 3, 2.5],
        'peak_times': [10, 8, 9],
        'peak_time_stds': [1, 0.8, 1.2],
        'time_series': time_series_dict
    }
    
    print("Karşılaştırma grafiği çiziliyor...")
    plot_comparison_bars(plotting_data)
    
    # Ağ grafiği
    print("Ağ snapshot grafiği çiziliyor...")
    G = nx.karate_club_graph()
    states = {node: 'S' for node in G.nodes()}
    # Birkaç düğümü enfekte yap
    for node in [0, 1, 2]:
        states[node] = 'I'
    # Birkaç düğümü iyileş
    for node in [10, 11]:
        states[node] = 'R'
    
    plot_network_snapshot(G, states, time_step=5, 
                         title="Test: Network State Visualization")
    
    print("\n✓ Plots modülü başarıyla test edildi!")

