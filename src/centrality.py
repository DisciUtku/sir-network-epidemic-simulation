"""
Merkeziyet (centrality) ölçülerini hesaplama modülü
"""

import networkx as nx
from typing import Dict, List, Tuple


def calculate_degree_centrality(G: nx.Graph) -> Dict:
    """Degree centrality hesapla"""
    centrality = nx.degree_centrality(G)
    return centrality


def calculate_betweenness_centrality(G: nx.Graph, k: int = None) -> Dict:
    """Betweenness centrality hesapla, k=None ise tam hesaplama"""
    if k is not None:
        centrality = nx.betweenness_centrality(G, k=k, seed=42)
    else:
        centrality = nx.betweenness_centrality(G)
    return centrality


def calculate_closeness_centrality(G: nx.Graph) -> Dict:
    """Closeness centrality hesapla"""
    centrality = nx.closeness_centrality(G)
    return centrality


def calculate_eigenvector_centrality(G: nx.Graph, max_iter: int = 1000) -> Dict:
    """Eigenvector centrality hesapla"""
    try:
        centrality = nx.eigenvector_centrality(G, max_iter=max_iter)
    except nx.PowerIterationFailedConvergence:
        print("Eigenvector yakınsamadı, degree kullanılıyor")
        centrality = calculate_degree_centrality(G)
    return centrality


def calculate_all_centralities(G: nx.Graph, 
                               use_approximation: bool = False,
                               k_sample: int = None) -> Dict[str, Dict]:
    """Tüm merkeziyet ölçülerini hesapla"""
    print("Merkeziyet ölçüleri hesaplanıyor...")
    
    centralities = {}
    
    centralities['degree'] = calculate_degree_centrality(G)
    
    if use_approximation and k_sample is None:
        k_sample = min(100, G.number_of_nodes() // 10)
    centralities['betweenness'] = calculate_betweenness_centrality(G, k=k_sample)
    
    centralities['closeness'] = calculate_closeness_centrality(G)
    
    centralities['eigenvector'] = calculate_eigenvector_centrality(G)
    
    return centralities


def get_top_k_nodes(centrality: Dict, k: int) -> List[Tuple]:
    """En yüksek k düğümü döndür"""
    sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
    return sorted_nodes[:k]


def get_top_k_nodes_by_measure(centralities: Dict[str, Dict], 
                               measure: str, 
                               k: int) -> List:
    """Belirtilen ölçüye göre en yüksek k düğümü döndür"""
    if measure not in centralities:
        raise ValueError(f"Geçersiz merkeziyet ölçüsü: {measure}")
    
    top_nodes = get_top_k_nodes(centralities[measure], k)
    return [node for node, score in top_nodes]


def print_centrality_stats(centrality: Dict, name: str, top_k: int = 10):
    """Merkeziyet istatistiklerini yazdır"""
    print(f"\n{name} Centrality İstatistikleri:")
    print("-" * 50)
    
    scores = list(centrality.values())
    print(f"Ortalama: {sum(scores) / len(scores):.6f}")
    print(f"Maksimum: {max(scores):.6f}")
    print(f"Minimum: {min(scores):.6f}")
    
    print(f"\nEn yüksek {top_k} düğüm:")
    top_nodes = get_top_k_nodes(centrality, top_k)
    for i, (node, score) in enumerate(top_nodes, 1):
        print(f"  {i}. Düğüm {node}: {score:.6f}")


def compare_centralities(centralities: Dict[str, Dict], k: int = 10):
    """Farklı ölçülerin en üst k düğümlerini karşılaştır"""
    top_nodes_by_measure = {}
    for measure in centralities:
        top_nodes_by_measure[measure] = set(
            get_top_k_nodes_by_measure(centralities, measure, k)
        )
    
    for measure in centralities:
        print(f"\n{measure.upper()}:")
        nodes = top_nodes_by_measure[measure]
        
        for other_measure in centralities:
            if other_measure != measure:
                intersection = nodes & top_nodes_by_measure[other_measure]
                overlap_pct = len(intersection) / k * 100
                print(f"  {other_measure} ile örtüşme: {len(intersection)}/{k} (%{overlap_pct:.1f})")


# Test fonksiyonu
if __name__ == "__main__":
    G = nx.karate_club_graph()
    
    centralities = calculate_all_centralities(G)
    
    for measure in centralities:
        print_centrality_stats(centralities[measure], measure.upper(), top_k=5)
    
    compare_centralities(centralities, k=5)
    
    print("\nEn üst 5 düğüm:")
    for measure in centralities:
        top_nodes = get_top_k_nodes_by_measure(centralities, measure, 5)
        print(f"{measure.upper()}: {top_nodes}")

