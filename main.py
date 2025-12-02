"""
SIR Model Simulasyonu - Ana Calistirma Dosyasi

Farkli merkeziyet olcülerinin hastalik yayilimina etkisini analiz eder.
"""

import os
import sys
import argparse
import networkx as nx

# Windows console encoding sorununu çöz
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Modülleri import et
from src.data_loading import (
    create_sample_network,
    prepare_graph,
    print_recommended_datasets
)
from src.experiments import ExperimentRunner
from src.plots import create_all_plots

def print_header():
    """Program başlığını yazdırır."""
    print("\n" + "="*70)
    print(" "*15 + "SIR MODEL SİMÜLASYONU")
    print(" "*10 + "Merkeziyet Ölçüleri ve Hastalık Yayılımı")
    print("="*70 + "\n")


def interactive_mode():
    """Etkileşimli menü modunda çalışır."""
    print_header()
    
    print("Veri Seti Seçimi:")
    print("  1. Örnek ağ oluştur (Watts-Strogatz model)")
    print("  2. Kendi veri setimi yükle")
    print("  3. Önerilen veri setlerini göster")
    
    choice = input("\nSeçiminiz (1-3): ").strip()
    
    G = None
    
    if choice == '1':
        # Örnek ağ parametreleri
        print("\nÖrnek Ağ Parametreleri:")
        n = int(input("  Düğüm sayısı (n) [varsayılan: 200]: ") or "200")
        k = int(input("  Komşu sayısı (k) [varsayılan: 6]: ") or "6")
        p = float(input("  Rewiring olasılığı (p) [varsayılan: 0.1]: ") or "0.1")
        
        print(f"\nÖrnek ağ oluşturuluyor (n={n}, k={k}, p={p})...")
        G = create_sample_network(n=n, k=k, p=p)
        
    elif choice == '2':
        file_path = input("\nDosya yolu: ").strip()
        
        if not os.path.exists(file_path):
            print(f"❌ Dosya bulunamadı: {file_path}")
            return
        
        use_largest = input("En büyük bağlı bileşeni kullan? (E/h) [E]: ").strip().lower()
        use_largest = use_largest != 'h'
        
        print(f"\nGraf yükleniyor: {file_path}")
        G = prepare_graph(file_path, use_largest_component=use_largest)
        
    elif choice == '3':
        print_recommended_datasets()
        print("\nLütfen veri setini indirip seçenek 2 ile yükleyin.")
        return
    
    else:
        print("❌ Geçersiz seçim!")
        return
    
    if G is None:
        print("❌ Graf yüklenemedi!")
        return
    
    # Simülasyon parametreleri
    print("\n" + "-"*70)
    print("Simülasyon Parametreleri:")
    print("-"*70)
    
    beta = float(input("  Bulaşma olasılığı (beta) [0-1, varsayılan: 0.3]: ") or "0.3")
    gamma = float(input("  İyileşme olasılığı (gamma) [0-1, varsayılan: 0.1]: ") or "0.1")
    k_initial = int(input(f"  Başlangıçta enfekte düğüm sayısı [varsayılan: 5]: ") or "5")
    n_runs = int(input("  Her senaryo için tekrar sayısı [varsayılan: 30]: ") or "30")
    
    print(f"\n{'='*70}")
    print("PARAMETRELERİN ÖZETİ")
    print(f"{'='*70}")
    print(f"Graf: {G.number_of_nodes()} düğüm, {G.number_of_edges()} kenar")
    print(f"Beta (bulaşma): {beta}")
    print(f"Gamma (iyileşme): {gamma}")
    print(f"Başlangıç enfekte: {k_initial} düğüm")
    print(f"Tekrar sayısı: {n_runs}")
    print(f"{'='*70}\n")
    
    confirm = input("Simülasyonu başlat? (E/h) [E]: ").strip().lower()
    if confirm == 'h':
        print("İptal edildi.")
        return
    
    # Deney çalıştır
    print("\n" + "#"*70)
    print("SİMÜLASYONLAR ÇALIŞTIRILIYOR...")
    print("#"*70)
    
    runner = ExperimentRunner(G, beta, gamma, k_initial, n_runs)
    runner.run_all_scenarios()
    runner.compare_scenarios()
    
    # Grafikleri oluştur
    save_plots = input("\nGrafikleri kaydet? (E/h) [E]: ").strip().lower()
    if save_plots != 'h':
        save_dir = input("  Kayıt klasörü [varsayılan: results]: ").strip() or "results"
        create_all_plots(runner, save_dir=save_dir)
    
    print("\n" + "="*70)
    print("✓ PROGRAM TAMAMLANDI")
    print("="*70 + "\n")


def batch_mode(args):
    """Komut satırı parametreleri ile çalışır."""
    print_header()
    
    # Graf yükle
    if args.sample:
        print(f"Örnek ağ oluşturuluyor (n={args.sample})...")
        G = create_sample_network(n=args.sample, k=6, p=0.1)
    elif args.input:
        print(f"Graf yükleniyor: {args.input}")
        if not os.path.exists(args.input):
            print(f"❌ Dosya bulunamadı: {args.input}")
            return
        G = prepare_graph(args.input, use_largest_component=True)
    else:
        print("❌ --sample veya --input parametresi gerekli!")
        return
    
    print(f"\n{'='*70}")
    print("PARAMETRELERİN ÖZETİ")
    print(f"{'='*70}")
    print(f"Graf: {G.number_of_nodes()} düğüm, {G.number_of_edges()} kenar")
    print(f"Beta (bulaşma): {args.beta}")
    print(f"Gamma (iyileşme): {args.gamma}")
    print(f"Başlangıç enfekte: {args.k_initial} düğüm")
    print(f"Tekrar sayısı: {args.n_runs}")
    print(f"{'='*70}\n")
    
    # Deney çalıştır
    print("#"*70)
    print("SİMÜLASYONLAR ÇALIŞTIRILIYOR...")
    print("#"*70)
    
    runner = ExperimentRunner(G, args.beta, args.gamma, args.k_initial, args.n_runs)
    runner.run_all_scenarios()
    runner.compare_scenarios()
    
    # Grafikleri oluştur
    if args.output:
        create_all_plots(runner, save_dir=args.output)
    
    print("\n" + "="*70)
    print("✓ PROGRAM TAMAMLANDI")
    print("="*70 + "\n")


def quick_demo():
    """Hızlı demo çalıştırır."""
    print_header()
    print("HIZLI DEMO MODU")
    print("Karate Club grafiği ile hızlı bir demo çalıştırılıyor...\n")
    
    # Karate Club grafiği
    G = nx.karate_club_graph()
    print(f"Graf: {G.number_of_nodes()} düğüm, {G.number_of_edges()} kenar")
    
    # Parametreler
    beta = 0.3
    gamma = 0.1
    k_initial = 3
    n_runs = 10  # Demo için az
    
    print(f"Beta: {beta}, Gamma: {gamma}")
    print(f"Başlangıç enfekte: {k_initial} düğüm")
    print(f"Tekrar sayısı: {n_runs}\n")
    
    # Deney çalıştır
    runner = ExperimentRunner(G, beta, gamma, k_initial, n_runs)
    runner.run_all_scenarios()
    runner.compare_scenarios()
    
    # Grafikleri oluştur
    create_all_plots(runner, save_dir='results_demo')
    
    print("\n" + "="*70)
    print("✓ DEMO TAMAMLANDI")
    print("Demo grafikleri 'results_demo' klasörüne kaydedildi.")
    print("="*70 + "\n")


def main():
    """Ana fonksiyon."""
    parser = argparse.ArgumentParser(
        description='SIR Model Simülasyonu - Merkeziyet Ölçüleri Analizi',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Kullanım Örnekleri:
  # Etkileşimli mod
  python main.py
  
  # Hızlı demo
  python main.py --demo
  
  # Örnek ağ ile
  python main.py --sample 200 --beta 0.3 --gamma 0.1 --k-initial 5 --n-runs 30 --output results
  
  # Kendi veri setinle
  python main.py --input data/network.edges --beta 0.3 --gamma 0.1 --k-initial 10 --n-runs 30 --output results
  
  # Önerilen veri setlerini göster
  python main.py --list-datasets
        """
    )
    
    parser.add_argument('--demo', action='store_true',
                       help='Hızlı demo çalıştır (Karate Club grafiği)')
    
    parser.add_argument('--list-datasets', action='store_true',
                       help='Önerilen veri setlerini listele')
    
    parser.add_argument('--sample', type=int, metavar='N',
                       help='Örnek ağ oluştur (N düğüm)')
    
    parser.add_argument('--input', '-i', type=str, metavar='FILE',
                       help='Graf dosyası (edge list formatı)')
    
    parser.add_argument('--beta', type=float, default=0.3,
                       help='Bulaşma olasılığı (varsayılan: 0.3)')
    
    parser.add_argument('--gamma', type=float, default=0.1,
                       help='İyileşme olasılığı (varsayılan: 0.1)')
    
    parser.add_argument('--k-initial', type=int, default=5,
                       help='Başlangıçta enfekte düğüm sayısı (varsayılan: 5)')
    
    parser.add_argument('--n-runs', type=int, default=30,
                       help='Her senaryo için tekrar sayısı (varsayılan: 30)')
    
    parser.add_argument('--output', '-o', type=str, metavar='DIR',
                       help='Çıktı klasörü (grafiklerin kaydedileceği)')
    
    args = parser.parse_args()
    
    # Komut satırı modları
    if args.demo:
        quick_demo()
    elif args.list_datasets:
        print_recommended_datasets()
    elif args.sample or args.input:
        batch_mode(args)
    else:
        # Etkileşimli mod (varsayılan)
        try:
            interactive_mode()
        except KeyboardInterrupt:
            print("\n\nProgram kullanıcı tarafından durduruldu.")
            sys.exit(0)


if __name__ == "__main__":
    main()

