"""
Farklı merkeziyet ölçüleri ile SIR simülasyon deneyleri
"""

import networkx as nx
import numpy as np
import random
from typing import Dict, List
from .centrality import (
    calculate_all_centralities,
    get_top_k_nodes_by_measure
)
from .sir_simulation import (
    run_multiple_simulations,
    aggregate_simulation_results
)


class ExperimentRunner:
    """SIR deneyleri çalıştırır"""
    
    def __init__(self, G: nx.Graph, beta: float, gamma: float,
                 k_initial: int, n_runs: int = 30, seed: int = 42):
        self.G = G
        self.beta = beta
        self.gamma = gamma
        self.k_initial = k_initial
        self.n_runs = n_runs
        self.seed = seed
        
        use_approx = G.number_of_nodes() > 1000
        self.centralities = calculate_all_centralities(G, use_approximation=use_approx)
        
        # Sonuçları sakla
        self.results = {}
    
    def run_random_scenario(self) -> Dict:
        """Rastgele seçim senaryosu"""
        print(f"\nRastgele seçim ({self.k_initial} düğüm)")
        
        # Her run için farklı rastgele düğümler seçilecek
        all_results = []
        nodes = list(self.G.nodes())
        
        for i in range(self.n_runs):
            seed = self.seed + i if self.seed is not None else None
            if seed is not None:
                random.seed(seed)
            
            # Rastgele k düğüm seç
            initial_infected = random.sample(nodes, self.k_initial)
            
            # Simülasyon çalıştır
            from .sir_simulation import run_sir_simulation
            result = run_sir_simulation(
                self.G, initial_infected, self.beta, self.gamma,
                seed=seed
            )
            all_results.append(result)
        
        # Sonuçları birleştir
        aggregated = aggregate_simulation_results(all_results)
        self.results['random'] = aggregated
        
        self._print_results(aggregated, "RASTGELE")
        return aggregated
    
    def run_centrality_scenario(self, measure: str) -> Dict:
        """Merkeziyet ölçüsüne göre simülasyon"""
        print(f"\n{measure.upper()} Centrality ({self.k_initial} düğüm)")
        
        initial_infected = get_top_k_nodes_by_measure(
            self.centralities, measure, self.k_initial
        )
        
        # Çoklu simülasyon çalıştır
        all_results = run_multiple_simulations(
            self.G, initial_infected, self.beta, self.gamma,
            n_runs=self.n_runs, base_seed=self.seed
        )
        
        # Sonuçları birleştir
        aggregated = aggregate_simulation_results(all_results)
        self.results[measure] = aggregated
        
        self._print_results(aggregated, measure.upper())
        return aggregated
    
    def run_all_scenarios(self) -> Dict[str, Dict]:
        """Tüm senaryoları çalıştır"""
        print("\nTüm senaryolar çalıştırılıyor...")
        
        self.run_random_scenario()
        self.run_centrality_scenario('degree')
        self.run_centrality_scenario('betweenness')
        self.run_centrality_scenario('closeness')
        self.run_centrality_scenario('eigenvector')
        
        print("\nTüm senaryolar tamamlandı")
        
        return self.results
    
    def compare_scenarios(self):
        """Senaryoları karşılaştır"""
        if not self.results:
            print("Henüz hiçbir senaryo çalıştırılmadı!")
            return
        
        print("\nSenaryo Karşılaştırması:")
        print(f"{'Senaryo':<15} {'Salgın':<20} {'Maks. Enfekte':<20} {'Peak Zamanı':<15}")
        print("-" * 70)
        
        for scenario, results in self.results.items():
            outbreak = f"{results['mean_outbreak_size']:.1f} ± {results['std_outbreak_size']:.1f}"
            peak_inf = f"{results['mean_peak_infected']:.1f} ± {results['std_peak_infected']:.1f}"
            peak_t = f"{results['mean_peak_time']:.1f} ± {results['std_peak_time']:.1f}"
            
            print(f"{scenario:<15} {outbreak:<20} {peak_inf:<20} {peak_t:<15}")
        
        max_outbreak = max(self.results.items(),
                          key=lambda x: x[1]['mean_outbreak_size'])
        print(f"\nEn büyük salgın: {max_outbreak[0].upper()} ({max_outbreak[1]['mean_outbreak_size']:.1f})")
        
        max_peak = max(self.results.items(),
                      key=lambda x: x[1]['mean_peak_infected'])
        print(f"En yüksek peak: {max_peak[0].upper()} ({max_peak[1]['mean_peak_infected']:.1f})")
        
        min_peak_time = min(self.results.items(),
                           key=lambda x: x[1]['mean_peak_time'])
        print(f"En hızlı yayılım: {min_peak_time[0].upper()} ({min_peak_time[1]['mean_peak_time']:.1f} adım)")
    
    def _print_results(self, results: Dict, name: str):
        """Sonuç özetini yazdırır."""
        print(f"  Salgın: {results['mean_outbreak_size']:.1f} ± {results['std_outbreak_size']:.1f}")
        print(f"  Peak enfekte: {results['mean_peak_infected']:.1f} ± {results['std_peak_infected']:.1f}")
        print(f"  Peak zamanı: {results['mean_peak_time']:.1f} ± {results['std_peak_time']:.1f}")
    
    def get_results_for_plotting(self) -> Dict:
        """Grafik için sonuçları düzenle"""
        scenarios = list(self.results.keys())
        
        plotting_data = {
            'scenarios': scenarios,
            'outbreak_sizes': [self.results[s]['mean_outbreak_size'] for s in scenarios],
            'outbreak_stds': [self.results[s]['std_outbreak_size'] for s in scenarios],
            'peak_infecteds': [self.results[s]['mean_peak_infected'] for s in scenarios],
            'peak_infected_stds': [self.results[s]['std_peak_infected'] for s in scenarios],
            'peak_times': [self.results[s]['mean_peak_time'] for s in scenarios],
            'peak_time_stds': [self.results[s]['std_peak_time'] for s in scenarios],
            'time_series': {s: self.results[s]['mean_time_series'] for s in scenarios}
        }
        
        return plotting_data


def quick_experiment(G: nx.Graph, beta: float = 0.3, gamma: float = 0.1,
                    k_initial: int = 5, n_runs: int = 30) -> ExperimentRunner:
    """Hızlı deney çalıştır"""
    runner = ExperimentRunner(G, beta, gamma, k_initial, n_runs)
    runner.run_all_scenarios()
    runner.compare_scenarios()
    return runner


# Test fonksiyonu
if __name__ == "__main__":
    G = nx.karate_club_graph()
    
    beta = 0.3
    gamma = 0.1
    k_initial = 3
    n_runs = 10
    
    runner = quick_experiment(G, beta, gamma, k_initial, n_runs)
    
    plotting_data = runner.get_results_for_plotting()
    print(f"\nGrafik verisi hazır: {len(plotting_data['scenarios'])} senaryo")

