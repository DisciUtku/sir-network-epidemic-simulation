"""
Graf veri setlerini yükleme ve hazırlama modülü
"""

import networkx as nx
import requests
import os
from typing import Optional, Tuple


def download_dataset(url: str, save_path: str) -> None:
    """Veri setini indir"""
    response = requests.get(url)
    response.raise_for_status()
    
    with open(save_path, 'wb') as f:
        f.write(response.content)
    print(f"Veri seti kaydedildi: {save_path}")


def load_edge_list(file_path: str, delimiter: str = None, 
                   comments: str = '#', has_header: bool = False) -> nx.Graph:
    """Edge list dosyasından graf yükle"""
    
    # Dosyayı oku
    G = nx.Graph()
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        if has_header:
            next(f)  # Başlık satırını atla
            
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            
            # Boş satır veya yorum satırını atla
            if not line or line.startswith(comments):
                continue
                
            try:
                if delimiter:
                    parts = line.split(delimiter)
                else:
                    parts = line.split()
                    
                if len(parts) >= 2:
                    # İlk iki sütunu düğüm olarak al
                    u, v = parts[0], parts[1]
                    
                    # Sayıya çevirmeyi dene
                    try:
                        u, v = int(u), int(v)
                    except ValueError:
                        pass  # String olarak kalsın
                    
                    # Self-loop'ları atla
                    if u != v:
                        G.add_edge(u, v)
            except Exception as e:
                print(f"Uyarı: Satır {line_num} işlenemedi: {e}")
                continue
    
    return G


def get_largest_component(G: nx.Graph) -> nx.Graph:
    """En büyük bağlı bileşeni döndür"""
    if not nx.is_connected(G):
        largest_cc = max(nx.connected_components(G), key=len)
        G_largest = G.subgraph(largest_cc).copy()
        return G_largest
    else:
        return G


def prepare_graph(file_path: str, use_largest_component: bool = True,
                 delimiter: str = None, comments: str = '#',
                 has_header: bool = False) -> nx.Graph:
    """Grafı yükle ve hazırla"""
    G = load_edge_list(file_path, delimiter, comments, has_header)
    
    if use_largest_component:
        G = get_largest_component(G)
    
    return G


def create_sample_network(n: int = 100, k: int = 4, p: float = 0.1) -> nx.Graph:
    """Örnek ağ oluştur (Watts-Strogatz)"""
    G = nx.watts_strogatz_graph(n, k, p, seed=42)
    return G


# Önerilen veri setleri
RECOMMENDED_DATASETS = {
    'facebook': {
        'name': 'Facebook Social Network (ego-networks)',
        'description': 'Facebook arkadaşlık ağı - 4039 düğüm',
        'url': 'http://networkrepository.com/fb-pages-food.php',
        'note': 'Manuel indirme gerekebilir'
    },
    'email': {
        'name': 'Email Network',
        'description': 'Email iletişim ağı - küçük ve hızlı',
        'url': 'http://networkrepository.com/email-univ.php',
        'note': 'Manuel indirme gerekebilir'
    },
    'ca-GrQc': {
        'name': 'Collaboration Network',
        'description': 'Bilimsel işbirliği ağı - 5242 düğüm',
        'url': 'https://snap.stanford.edu/data/ca-GrQc.txt.gz',
        'note': 'SNAP veri seti'
    }
}


def print_recommended_datasets():
    """Önerilen veri setlerini listele"""
    print("\nÖnerilen veri setleri:")
    for key, info in RECOMMENDED_DATASETS.items():
        print(f"  {key}: {info['name']}")
        print(f"    {info['description']}")


# Test fonksiyonu
if __name__ == "__main__":
    print("Data Loading Modülü Test Ediliyor...\n")
    
    # Önerilen veri setlerini listele
    print_recommended_datasets()
    
    # Örnek ağ oluştur ve test et
    print("\n\nÖrnek ağ oluşturuluyor...")
    G = create_sample_network(n=200, k=6, p=0.1)
    
    # Graf bilgilerini göster
    print(f"\nGraf özellikleri:")
    print(f"  Bağlı mı: {nx.is_connected(G)}")
    print(f"  Ortalama kümeleme katsayısı: {nx.average_clustering(G):.4f}")
    print(f"  Çap (diameter): {nx.diameter(G) if nx.is_connected(G) else 'N/A'}")
    
    print("\n✓ Data loading modülü başarıyla test edildi!")

