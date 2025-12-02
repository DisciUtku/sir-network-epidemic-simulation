"""
SIR (Susceptible-Infected-Recovered) hastalık yayılım modeli
"""

import networkx as nx
import numpy as np
from typing import List, Tuple, Dict, Set
from collections import defaultdict
import random


class SIRModel:
    """SIR modeli simülasyonu"""
    
    def __init__(self, G: nx.Graph, beta: float, gamma: float, seed: int = None):
        """G: graf, beta: bulaşma olasılığı, gamma: iyileşme olasılığı"""
        self.G = G
        self.beta = beta
        self.gamma = gamma
        self.seed = seed
        
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        # Düğüm durumları
        self.states = {}
        self.reset()
    
    def reset(self):
        """Simülasyonu sıfırla"""
        self.states = {node: 'S' for node in self.G.nodes()}
        self.time_step = 0
        self.infection_history = {}  # {node: (source_node, time_step)}
        self.initial_infected = []
    
    def set_initial_infected(self, nodes: List):
        """Başlangıç enfekte düğümlerini ayarla"""
        self.initial_infected = nodes.copy()
        for node in nodes:
            if node in self.states:
                self.states[node] = 'I'
                self.infection_history[node] = (None, 0)  # None = başlangıç enfekte
    
    def get_state_counts(self) -> Tuple[int, int, int]:
        """S, I, R sayılarını döndür"""
        S_count = sum(1 for state in self.states.values() if state == 'S')
        I_count = sum(1 for state in self.states.values() if state == 'I')
        R_count = sum(1 for state in self.states.values() if state == 'R')
        return S_count, I_count, R_count
    
    def get_infected_nodes(self) -> List:
        return [node for node, state in self.states.items() if state == 'I']
    
    def get_susceptible_nodes(self) -> List:
        return [node for node, state in self.states.items() if state == 'S']
    
    def step(self) -> bool:
        """Bir adım simüle et, True dönerse devam ediyor"""
        infected_nodes = self.get_infected_nodes()
        
        if not infected_nodes:
            return False  # Simülasyon bitti
        
        new_states = self.states.copy()
        
        # 1. Bulaşma (Infection): Enfekte düğümler komşularını enfekte edebilir
        for infected_node in infected_nodes:
            # Enfekte düğümün tüm komşularını kontrol et
            for neighbor in self.G.neighbors(infected_node):
                # Eğer komşu hala duyarlı ise
                if self.states[neighbor] == 'S':
                    # Beta olasılığı ile enfekte et
                    if random.random() < self.beta:
                        new_states[neighbor] = 'I'
                        # Enfeksiyon geçmişini kaydet
                        if neighbor not in self.infection_history:
                            self.infection_history[neighbor] = (infected_node, self.time_step + 1)
        
        # 2. İyileşme (Recovery): Enfekte düğümler iyileşebilir
        for infected_node in infected_nodes:
            # Gamma olasılığı ile iyileş
            if random.random() < self.gamma:
                new_states[infected_node] = 'R'
        
        self.states = new_states
        self.time_step += 1
        
        return True  # Simülasyon devam ediyor
    
    def run(self, initial_infected: List, max_steps: int = 1000) -> Dict:
        """Simülasyonu çalıştır, sonuçları döndür"""
        # Simülasyonu sıfırla
        self.reset()
        
        # Başlangıç enfekte düğümlerini ayarla
        self.set_initial_infected(initial_infected)
        
        # Zaman serisi verileri
        time_series = []
        
        # Başlangıç durumunu kaydet
        S, I, R = self.get_state_counts()
        time_series.append((S, I, R))
        
        # Simülasyonu çalıştır
        for step in range(max_steps):
            continues = self.step()
            
            # Mevcut durumu kaydet
            S, I, R = self.get_state_counts()
            time_series.append((S, I, R))
            
            # Enfekte kalmadıysa dur
            if not continues:
                break
        
        # Sonuçları hesapla
        infected_counts = [I for S, I, R in time_series]
        recovered_counts = [R for S, I, R in time_series]
        
        peak_infected = max(infected_counts)
        peak_time = infected_counts.index(peak_infected)
        final_outbreak_size = recovered_counts[-1]  # Son R sayısı
        
        results = {
            'time_series': time_series,
            'final_outbreak_size': final_outbreak_size,
            'peak_infected': peak_infected,
            'peak_time': peak_time,
            'total_steps': len(time_series) - 1,
            'final_states': self.states.copy()
        }
        
        return results


def run_sir_simulation(G: nx.Graph, 
                      initial_infected: List,
                      beta: float,
                      gamma: float,
                      seed: int = None,
                      max_steps: int = 1000) -> Dict:
    """Tek simülasyon çalıştır"""
    model = SIRModel(G, beta, gamma, seed)
    return model.run(initial_infected, max_steps)


def run_multiple_simulations(G: nx.Graph,
                             initial_infected: List,
                             beta: float,
                             gamma: float,
                             n_runs: int = 30,
                             max_steps: int = 1000,
                             base_seed: int = 42) -> List[Dict]:
    """Birden fazla simülasyon çalıştır"""
    results = []
    
    for i in range(n_runs):
        seed = base_seed + i if base_seed is not None else None
        result = run_sir_simulation(G, initial_infected, beta, gamma, seed, max_steps)
        results.append(result)
    
    return results


def aggregate_simulation_results(results: List[Dict]) -> Dict:
    """Simülasyon sonuçlarını birleştir ve istatistikleri hesapla"""
    outbreak_sizes = [r['final_outbreak_size'] for r in results]
    peak_infecteds = [r['peak_infected'] for r in results]
    peak_times = [r['peak_time'] for r in results]
    
    # Ortalama zaman serisi hesapla (tüm simülasyonlar aynı uzunlukta olmayabilir)
    max_length = max(len(r['time_series']) for r in results)
    
    # Her zaman adımı için ortalama S, I, R
    mean_time_series = []
    for t in range(max_length):
        S_values, I_values, R_values = [], [], []
        
        for result in results:
            if t < len(result['time_series']):
                S, I, R = result['time_series'][t]
                S_values.append(S)
                I_values.append(I)
                R_values.append(R)
            else:
                # Simülasyon bittiyse son değerleri kullan
                S, I, R = result['time_series'][-1]
                S_values.append(S)
                I_values.append(I)
                R_values.append(R)
        
        mean_S = np.mean(S_values)
        mean_I = np.mean(I_values)
        mean_R = np.mean(R_values)
        mean_time_series.append((mean_S, mean_I, mean_R))
    
    aggregated = {
        'mean_outbreak_size': np.mean(outbreak_sizes),
        'std_outbreak_size': np.std(outbreak_sizes),
        'mean_peak_infected': np.mean(peak_infecteds),
        'std_peak_infected': np.std(peak_infecteds),
        'mean_peak_time': np.mean(peak_times),
        'std_peak_time': np.std(peak_times),
        'mean_time_series': mean_time_series,
        'all_results': results
    }
    
    return aggregated


def print_simulation_summary(results: Dict, scenario_name: str = ""):
    """Sonuçları yazdır"""
    if scenario_name:
        print(f"\n{scenario_name}:")
    
    if 'mean_outbreak_size' in results:
        print(f"  Salgın: {results['mean_outbreak_size']:.1f} ± {results['std_outbreak_size']:.1f}")
        print(f"  Peak enfekte: {results['mean_peak_infected']:.1f} ± {results['std_peak_infected']:.1f}")
        print(f"  Peak zamanı: {results['mean_peak_time']:.1f} ± {results['std_peak_time']:.1f}")
    else:
        print(f"  Toplam enfekte: {results['final_outbreak_size']}")
        print(f"  Maksimum enfekte: {results['peak_infected']} (zaman: {results['peak_time']})")
        print(f"  Toplam adım: {results['total_steps']}")


# Test fonksiyonu
if __name__ == "__main__":
    G = nx.karate_club_graph()
    
    beta = 0.3
    gamma = 0.1
    k = 3
    
    degrees = dict(G.degree())
    top_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:k]
    initial_infected = [node for node, degree in top_nodes]
    
    print("Tek simülasyon:")
    result = run_sir_simulation(G, initial_infected, beta, gamma, seed=42)
    print_simulation_summary(result)
    
    print("\nÇoklu simülasyon (10 tekrar):")
    results = run_multiple_simulations(G, initial_infected, beta, gamma, n_runs=10)
    aggregated = aggregate_simulation_results(results)
    print_simulation_summary(aggregated)

