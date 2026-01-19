"""
Farklı merkeziyet ölçüleri ile SIR simülasyon deneyleri
"""

import networkx as nx
import numpy as np
import random
import json
from datetime import datetime
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
    
    def get_initial_infected_nodes(self, scenario: str) -> List:
        """Senaryo için başlangıç enfekte node'ları döndür"""
        if scenario == 'random':
            # Random için ilk run'un node'larını kullan
            nodes = list(self.G.nodes())
            random.seed(self.seed)
            return random.sample(nodes, self.k_initial)
        else:
            return get_top_k_nodes_by_measure(
                self.centralities, scenario, self.k_initial
            )
    
    def export_to_json(self, include_individual_runs: bool = True) -> str:
        """
        Tüm deney sonuçlarını akademik makale için detaylı JSON formatında döndür
        
        Args:
            include_individual_runs: Her run'un detaylı sonuçlarını dahil et
            
        Returns:
            JSON string
        """
        # Ağ topolojisi bilgileri
        network_info = {
            'num_nodes': self.G.number_of_nodes(),
            'num_edges': self.G.number_of_edges(),
            'is_connected': nx.is_connected(self.G),
            'average_degree': sum(dict(self.G.degree()).values()) / self.G.number_of_nodes() if self.G.number_of_nodes() > 0 else 0,
            'average_clustering': nx.average_clustering(self.G),
            'diameter': nx.diameter(self.G) if nx.is_connected(self.G) else None,
            'density': nx.density(self.G)
        }
        
        # Merkeziyet ölçüleri özeti (en yüksek 10 node)
        centrality_summary = {}
        for measure, scores in self.centralities.items():
            sorted_nodes = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]
            centrality_summary[measure] = {
                'top_nodes': [{'node': int(node), 'score': float(score)} for node, score in sorted_nodes],
                'mean_score': float(np.mean(list(scores.values()))),
                'std_score': float(np.std(list(scores.values()))),
                'max_score': float(max(scores.values())),
                'min_score': float(min(scores.values()))
            }
        
        # Senaryo sonuçları
        scenarios_data = {}
        for scenario_name, aggregated_results in self.results.items():
            # Başlangıç enfekte node'ları
            initial_infected = self.get_initial_infected_nodes(scenario_name)
            
            # İstatistiksel metrikler
            outbreak_sizes = [r['final_outbreak_size'] for r in aggregated_results['all_results']]
            peak_infecteds = [r['peak_infected'] for r in aggregated_results['all_results']]
            peak_times = [r['peak_time'] for r in aggregated_results['all_results']]
            total_steps = [r['total_steps'] for r in aggregated_results['all_results']]
            
            # Güven aralıkları (95% CI)
            def confidence_interval(data, confidence=0.95):
                n = len(data)
                if n < 2:
                    return {'lower': float(np.mean(data)), 'upper': float(np.mean(data)), 'margin': 0.0}
                
                mean = np.mean(data)
                std = np.std(data, ddof=1)
                se = std / np.sqrt(n)
                
                # scipy ile t-dağılımı kullan
                try:
                    from scipy import stats
                    t_critical = stats.t.ppf((1 + confidence) / 2, n - 1)
                except ImportError:
                    # scipy yoksa z-score yaklaşımı (n > 30 için yaklaşık)
                    # Normal dağılım için z-score
                    z_critical = 1.96 if confidence == 0.95 else 2.576 if confidence == 0.99 else 2.0
                    t_critical = z_critical
                
                margin = t_critical * se
                return {
                    'lower': float(mean - margin),
                    'upper': float(mean + margin),
                    'margin': float(margin)
                }
            
            scenario_data = {
                'scenario_name': scenario_name,
                'initial_infected_nodes': [int(node) for node in initial_infected],
                'num_initial_infected': len(initial_infected),
                
                # İstatistiksel özet
                'statistics': {
                    'final_outbreak_size': {
                        'mean': float(aggregated_results['mean_outbreak_size']),
                        'std': float(aggregated_results['std_outbreak_size']),
                        'min': float(np.min(outbreak_sizes)),
                        'max': float(np.max(outbreak_sizes)),
                        'median': float(np.median(outbreak_sizes)),
                        'q1': float(np.percentile(outbreak_sizes, 25)),
                        'q3': float(np.percentile(outbreak_sizes, 75)),
                        'ci_95': confidence_interval(outbreak_sizes)
                    },
                    'peak_infected': {
                        'mean': float(aggregated_results['mean_peak_infected']),
                        'std': float(aggregated_results['std_peak_infected']),
                        'min': float(np.min(peak_infecteds)),
                        'max': float(np.max(peak_infecteds)),
                        'median': float(np.median(peak_infecteds)),
                        'q1': float(np.percentile(peak_infecteds, 25)),
                        'q3': float(np.percentile(peak_infecteds, 75)),
                        'ci_95': confidence_interval(peak_infecteds)
                    },
                    'peak_time': {
                        'mean': float(aggregated_results['mean_peak_time']),
                        'std': float(aggregated_results['std_peak_time']),
                        'min': float(np.min(peak_times)),
                        'max': float(np.max(peak_times)),
                        'median': float(np.median(peak_times)),
                        'q1': float(np.percentile(peak_times, 25)),
                        'q3': float(np.percentile(peak_times, 75)),
                        'ci_95': confidence_interval(peak_times)
                    },
                    'total_steps': {
                        'mean': float(np.mean(total_steps)),
                        'std': float(np.std(total_steps)),
                        'min': float(np.min(total_steps)),
                        'max': float(np.max(total_steps)),
                        'median': float(np.median(total_steps))
                    }
                },
                
                # Ortalama zaman serisi
                'mean_time_series': [
                    {
                        'time_step': int(t),
                        'susceptible': float(S),
                        'infected': float(I),
                        'recovered': float(R),
                        'total_infected': float(I + R)
                    }
                    for t, (S, I, R) in enumerate(aggregated_results['mean_time_series'])
                ],
                
                # R₀ ve epidemik durum
                'epidemic_metrics': {
                    'r0': float(self.beta / self.gamma) if self.gamma > 0 else float('inf'),
                    'is_epidemic': self.beta / self.gamma > 1 if self.gamma > 0 else True,
                    'infection_rate': float(self.beta),
                    'recovery_rate': float(self.gamma)
                }
            }
            
            # Bireysel run sonuçları (opsiyonel)
            if include_individual_runs:
                scenario_data['individual_runs'] = []
                for run_idx, result in enumerate(aggregated_results['all_results']):
                    run_data = {
                        'run_number': run_idx + 1,
                        'seed': self.seed + run_idx if self.seed is not None else None,
                        'final_outbreak_size': int(result['final_outbreak_size']),
                        'peak_infected': int(result['peak_infected']),
                        'peak_time': int(result['peak_time']),
                        'total_steps': int(result['total_steps']),
                        'time_series': [
                            {
                                'time_step': int(t),
                                'susceptible': int(S),
                                'infected': int(I),
                                'recovered': int(R)
                            }
                            for t, (S, I, R) in enumerate(result['time_series'])
                        ]
                    }
                    scenario_data['individual_runs'].append(run_data)
            
            scenarios_data[scenario_name] = scenario_data
        
        # Karşılaştırma metrikleri
        comparison_metrics = {}
        if len(self.results) > 1:
            outbreak_sizes_all = {s: self.results[s]['mean_outbreak_size'] for s in self.results.keys()}
            peak_infecteds_all = {s: self.results[s]['mean_peak_infected'] for s in self.results.keys()}
            peak_times_all = {s: self.results[s]['mean_peak_time'] for s in self.results.keys()}
            
            comparison_metrics = {
                'best_outbreak_size': {
                    'scenario': max(outbreak_sizes_all.items(), key=lambda x: x[1])[0],
                    'value': float(max(outbreak_sizes_all.values()))
                },
                'best_peak_infected': {
                    'scenario': max(peak_infecteds_all.items(), key=lambda x: x[1])[0],
                    'value': float(max(peak_infecteds_all.values()))
                },
                'fastest_spread': {
                    'scenario': min(peak_times_all.items(), key=lambda x: x[1])[0],
                    'value': float(min(peak_times_all.values()))
                },
                'relative_improvement_over_random': {
                    scenario: {
                        'outbreak_size_improvement': float((self.results[scenario]['mean_outbreak_size'] - 
                                                           self.results['random']['mean_outbreak_size']) / 
                                                          self.results['random']['mean_outbreak_size'] * 100)
                        if 'random' in self.results else None,
                        'peak_infected_improvement': float((self.results[scenario]['mean_peak_infected'] - 
                                                           self.results['random']['mean_peak_infected']) / 
                                                          self.results['random']['mean_peak_infected'] * 100)
                        if 'random' in self.results else None
                    }
                    for scenario in self.results.keys()
                    if scenario != 'random'
                }
            }
        
        # Ana JSON yapısı
        export_data = {
            'metadata': {
                'experiment_id': f"sir_experiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'export_timestamp': datetime.now().isoformat(),
                'experiment_date': datetime.now().strftime('%Y-%m-%d'),
                'software_version': '1.0.0',
                'description': 'SIR Model Simulation - Centrality Measures Comparison'
            },
            
            'experiment_parameters': {
                'beta': float(self.beta),
                'gamma': float(self.gamma),
                'r0': float(self.beta / self.gamma) if self.gamma > 0 else float('inf'),
                'k_initial': int(self.k_initial),
                'n_runs': int(self.n_runs),
                'base_seed': int(self.seed) if self.seed is not None else None,
                'max_steps': 1000  # Varsayılan
            },
            
            'network_topology': network_info,
            
            'centrality_measures': {
                'summary': centrality_summary,
                'note': 'Top 10 nodes for each centrality measure are shown'
            },
            
            'scenarios': scenarios_data,
            
            'comparison_metrics': comparison_metrics,
            
            'notes': {
                'statistical_analysis': {
                    'confidence_level': '95%',
                    'ci_method': 't-distribution',
                    'n_runs_per_scenario': self.n_runs
                },
                'data_quality': {
                    'includes_individual_runs': include_individual_runs,
                    'reproducibility': f'Seed-based (base_seed={self.seed})' if self.seed else 'Non-reproducible'
                }
            }
        }
        
        return json.dumps(export_data, indent=2, ensure_ascii=False)


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

