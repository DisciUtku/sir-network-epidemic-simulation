# SIR Network Epidemic Simulation - Tam Proje Açıklama Promptu

## PROJE GENEL BAKIŞI

### Proje Adı
**SIR Model Simülasyonu - Merkeziyet Ölçüleri ile Hastalık Yayılımı Analizi**

### Proje Türü ve Seviyesi
Yüksek lisans düzeyinde Graf Algoritmaları dersi projesi. Python tabanlı, modüler mimaride geliştirilmiş bir epidemik hastalık yayılım simülasyonu ve analiz platformu.

### Temel Araştırma Sorusu
"Bir sosyal ağda salgını başlatmak için hangi node'ları seçmeliyiz ki salgın mümkün olduğunca geniş ve hızlı yayılsın?"

Bu soru, ağ teorisi, epidemiyoloji ve algoritma optimizasyonu disiplinlerini birleştiren çok disiplinli bir araştırma sorusudur.

### Proje Amacı
Farklı merkeziyet (centrality) ölçülerine göre seçilen başlangıç enfekte node'larının salgının yayılımı üzerindeki etkisini karşılaştırmak ve hangi stratejinin en etkili olduğunu deneysel olarak belirlemek. Proje, teorik bilgiyi pratik uygulamalarla birleştirerek hem eğitim hem de araştırma amaçlı kullanılabilir.

---

## SIR MODELİ - DETAYLI TEORİK AÇIKLAMA

### SIR Modeli Nedir?
SIR (Susceptible-Infected-Recovered) modeli, epidemik hastalık yayılımını modellemek için kullanılan klasik bir matematiksel modeldir. Proje, bu modeli ağ teorisi bağlamında uygular.

### Durumlar ve Geçişler

**1. S (Susceptible) - Duyarlı:**
- Tanım: Hastalığa duyarlı, henüz enfekte olmamış bireyler/node'lar
- Özellikler: Enfekte olabilirler, ancak henüz hastalığı taşımazlar
- Başlangıç durumu: Tüm node'lar varsayılan olarak S durumundadır

**2. I (Infected) - Enfekte:**
- Tanım: Enfekte olmuş, hastalığı yayabilen bireyler/node'lar
- Özellikler: Komşu node'ları enfekte edebilirler, hastalığı taşırlar
- Bulaşma: Her zaman adımında komşularını enfekte etme potansiyeline sahiptirler

**3. R (Recovered) - İyileşmiş:**
- Tanım: İyileşmiş, artık enfekte olamaz veya enfekte edemez bireyler/node'lar
- Özellikler: Bağışıklık kazanmışlardır, salgından etkilenmezler
- Kalıcılık: R durumuna geçen node'lar simülasyon sonuna kadar R kalır

### Simülasyon Dinamiği

**Discrete Time Steps (Ayrık Zaman Adımları):**
Simülasyon, ayrık zaman adımlarında çalışır. Her adımda iki işlem sırayla gerçekleşir:

**1. Bulaşma Fazı (Infection Phase):**
- Her enfekte node (I durumunda), tüm komşu node'larını kontrol eder
- Komşu node S durumundaysa, β (beta) olasılığı ile enfekte edilir
- Bulaşma stokastiktir: `random.random() < beta` kontrolü yapılır
- Enfeksiyon başarılı olursa:
  - Komşu node'un durumu S'den I'ye değişir
  - Enfeksiyon geçmişi kaydedilir: `infection_history[neighbor] = (infected_node, time_step)`

**2. İyileşme Fazı (Recovery Phase):**
- Her enfekte node (I durumunda), γ (gamma) olasılığı ile iyileşir
- İyileşme stokastiktir: `random.random() < gamma` kontrolü yapılır
- İyileşme başarılı olursa:
  - Node'un durumu I'den R'ye değişir
  - Node artık enfekte edemez ve enfekte olamaz

**Simülasyon Sonu:**
- Simülasyon, enfekte node kalmadığında (I = 0) sona erer
- Alternatif olarak, maksimum adım sayısına (max_steps, varsayılan 1000) ulaşıldığında durur

### Parametreler

**β (Beta) - Bulaşma Olasılığı:**
- Aralık: [0, 1]
- Anlamı: Bir enfekte node'un, bir zaman adımında komşu bir duyarlı node'u enfekte etme olasılığı
- Yüksek β: Hızlı yayılım, agresif salgın
- Düşük β: Yavaş yayılım, kontrollü salgın
- Varsayılan değer: 0.3

**γ (Gamma) - İyileşme Olasılığı:**
- Aralık: [0, 1]
- Anlamı: Bir enfekte node'un, bir zaman adımında iyileşme olasılığı
- Yüksek γ: Hızlı iyileşme, kısa süreli salgın
- Düşük γ: Yavaş iyileşme, uzun süreli salgın
- Varsayılan değer: 0.1

**R₀ (Temel Üreme Sayısı):**
- Formül: R₀ = β / γ
- Anlamı: Bir enfekte bireyin, iyileşmeden önce ortalama kaç kişiyi enfekte edeceği
- R₀ > 1: Salgın yayılır (epidemik)
- R₀ < 1: Salgın söner (endemik)
- R₀ = 1: Kritik eşik (endemik denge)

**k_initial - Başlangıç Enfekte Node Sayısı:**
- Anlamı: Simülasyonun başında enfekte olan node sayısı
- Etkisi: Daha fazla başlangıç enfekte = daha geniş salgın potansiyeli
- Varsayılan değer: 5

**n_runs - Tekrar Sayısı:**
- Anlamı: Aynı parametrelerle kaç kez simülasyon çalıştırılacağı
- Neden: Stokastik süreç olduğu için istatistiksel güvenilirlik için çoklu tekrar gerekir
- Varsayılan değer: 30

### Enfeksiyon Takibi Özelliği

Proje, hangi node'un hangi node'dan enfekte olduğunu takip eder:

**infection_history Dictionary:**
- Format: `{node: (source_node, time_step)}`
- source_node: Enfeksiyonun kaynağı (None ise başlangıç enfekte)
- time_step: Enfeksiyonun gerçekleştiği zaman adımı

**Kullanım Alanları:**
- Enfeksiyon yolu görselleştirmesi
- Salgının yayılım dinamiklerini anlama
- Patient Zero (ilk enfekte) analizi
- Ağ üzerinde kritik yolların belirlenmesi

---

## MERKEZİYET ÖLÇÜLERİ - DETAYLI AÇIKLAMA

### Merkeziyet Nedir?
Merkeziyet (centrality), bir ağda node'ların önemini veya etkisini ölçen metriklerdir. Proje, dört farklı merkeziyet ölçüsünü kullanarak başlangıç enfekte node'larını seçer.

### 1. Degree Centrality (Derece Merkeziyeti)

**Tanım:**
Bir node'un sahip olduğu bağlantı (edge) sayısı. En basit ve en hızlı hesaplanan merkeziyet ölçüsüdür.

**Matematiksel Formül:**
```
degree_centrality(v) = degree(v) / (n - 1)
```
- degree(v): Node v'nin derecesi (bağlantı sayısı)
- n: Toplam node sayısı
- Normalizasyon: [0, 1] aralığına normalize edilir

**Hesaplama Karmaşıklığı:**
- O(n) - Çok hızlı
- NetworkX: `nx.degree_centrality(G)`

**Mantık:**
- Daha fazla bağlantı = daha fazla yayılma fırsatı
- Hub node'lar (yüksek dereceli) kritik öneme sahiptir
- Scale-free ağlarda çok etkilidir

**En İyi Olduğu Durumlar:**
- Scale-free ağlar (sosyal medya, web)
- Hub node'ların belirgin olduğu ağlar
- Hızlı hesaplama gerektiğinde

**Avantajlar:**
- Çok hızlı hesaplama
- Basit ve anlaşılır
- Büyük ağlarda bile etkili

**Dezavantajlar:**
- Sadece yerel bilgi kullanır (komşular)
- Ağın global yapısını göz ardı eder

### 2. Betweenness Centrality (Arasındalık Merkeziyeti)

**Tanım:**
Bir node'un, tüm node çiftleri arasındaki en kısa yollar üzerinde kaç kez bulunduğu. Köprü node'ları belirler.

**Matematiksel Formül:**
```
betweenness_centrality(v) = Σ(σ_st(v) / σ_st)
```
- σ_st: Node s ve t arasındaki en kısa yolların sayısı
- σ_st(v): Bu yollardan v'den geçenlerin sayısı
- Toplam: Tüm node çiftleri (s, t) üzerinden

**Hesaplama Karmaşıklığı:**
- Tam hesaplama: O(nm) veya O(n²) - Yavaş
- Yaklaşık hesaplama (k-sample): O(km) - Orta hız
- NetworkX: `nx.betweenness_centrality(G, k=k_sample)`

**Mantık:**
- Köprü node'lar kritik geçiş noktalarıdır
- Bu node'ları enfekte etmek, farklı topluluklar arasında köprü kurar
- Modüler ağlarda çok etkilidir

**En İyi Olduğu Durumlar:**
- Modüler ağlar (topluluklar arası köprüler)
- Küçük dünya ağları
- Kritik geçiş noktalarının önemli olduğu durumlar

**Avantajlar:**
- Global ağ yapısını dikkate alır
- Köprü node'ları yakalar
- Modüler ağlarda çok etkili

**Dezavantajlar:**
- Yavaş hesaplama (büyük ağlarda yaklaşık hesaplama gerekir)
- Karmaşık algoritma

**Optimizasyon:**
- Büyük ağlarda (1000+ node) k-sample yaklaşımı kullanılır
- k_sample = min(100, n/10) - performans/doğruluk dengesi

### 3. Closeness Centrality (Yakınlık Merkeziyeti)

**Tanım:**
Bir node'un, diğer tüm node'lara ortalama en kısa mesafesi. Merkeze yakın node'ları belirler.

**Matematiksel Formül:**
```
closeness_centrality(v) = (n - 1) / Σ d(v, u)
```
- d(v, u): Node v ve u arasındaki en kısa mesafe
- Toplam: Tüm diğer node'lar üzerinden
- Normalizasyon: [0, 1] aralığına normalize edilir

**Hesaplama Karmaşıklığı:**
- O(n²) - Orta hız
- NetworkX: `nx.closeness_centrality(G)`
- Her node için BFS veya Dijkstra algoritması

**Mantık:**
- Merkeze yakın node'lar hızlı erişim sağlar
- Bu node'ları enfekte etmek, tüm ağa hızlı yayılım sağlar
- Küçük dünya ağlarında etkilidir

**En İyi Olduğu Durumlar:**
- Merkezi ağ yapıları
- Küçük dünya ağları
- Hızlı yayılım gerektiğinde

**Avantajlar:**
- Global ağ yapısını dikkate alır
- Merkezi node'ları yakalar
- Hızlı yayılım sağlar

**Dezavantajlar:**
- Orta hızlı hesaplama
- Bağlı olmayan bileşenlerde sorunlu

### 4. Eigenvector Centrality (Özdeğer Merkeziyeti)

**Tanım:**
Bir node'un önemi, bağlı olduğu node'ların önemine bağlıdır. Önemli node'lara bağlı olan node'lar daha yüksek skor alır.

**Matematiksel Formül:**
```
Ax = λx
```
- A: Komşuluk matrisi
- x: Eigenvector (merkeziyet skorları)
- λ: En büyük eigenvalue

**Hesaplama Karmaşıklığı:**
- O(n²) iteratif - Orta hız
- NetworkX: `nx.eigenvector_centrality(G, max_iter=1000)`
- Power iteration metodu kullanılır

**Mantık:**
- Sadece bağlantı sayısı değil, bağlantıların kalitesi önemli
- Hiyerarşik ağlarda etkilidir
- PageRank algoritmasına benzer

**En İyi Olduğu Durumlar:**
- Hiyerarşik ağlar
- Önemli node'ların belirgin olduğu ağlar
- Influence yayılımı

**Avantajlar:**
- Bağlantı kalitesini dikkate alır
- Hiyerarşik yapıları yakalar
- Influence ölçümü

**Dezavantajlar:**
- Yakınsama sorunları olabilir
- Yavaş hesaplama (iteratif)
- Bağlı olmayan bileşenlerde sorunlu

**Fallback Mekanizması:**
- Yakınsama başarısız olursa, otomatik olarak degree centrality'ye geçer
- Kullanıcıya bilgi verilir: "Eigenvector yakınsamadı, degree kullanılıyor"

### 5. Random (Rastgele) - Baseline

**Tanım:**
Rastgele k node seçimi. Diğer stratejilerle karşılaştırma için baseline olarak kullanılır.

**Mantık:**
- Stratejik seçim yapmadan rastgele node'ları enfekte eder
- Diğer stratejilerin etkinliğini ölçmek için referans noktası
- Her simülasyon için farklı rastgele node'lar seçilir

**Kullanım:**
- Baseline karşılaştırma
- Stratejik seçimin değerini ölçme
- Kontrol grubu

---

## PROJE MİMARİSİ VE MODÜLLER

### Genel Mimari
Proje, modüler ve genişletilebilir bir yapıda organize edilmiştir. Her modül tek bir sorumluluğa sahiptir (Single Responsibility Principle).

### Modül Yapısı

```
sir-network-epidemic-simulation/
├── src/
│   ├── __init__.py              # Paket başlatma
│   ├── data_loading.py          # Graf yükleme ve oluşturma
│   ├── centrality.py             # Merkeziyet hesaplamaları
│   ├── sir_simulation.py         # SIR modeli implementasyonu
│   ├── experiments.py             # Deney senaryoları ve çalıştırma
│   └── plots.py                  # Statik grafik oluşturma
├── main.py                       # Komut satırı arayüzü (CLI)
├── gui.py                        # Streamlit web arayüzü (GUI)
├── requirements.txt              # Python bağımlılıkları
├── README.md                     # Proje dokümantasyonu
└── start_gui.bat                 # Windows için GUI başlatma scripti
```

### Modül Detayları

#### 1. src/data_loading.py

**Sorumluluk:** Graf veri setlerini yükleme ve hazırlama

**Ana Fonksiyonlar:**

**`load_edge_list(file_path, delimiter, comments, has_header)`**
- Edge list formatında dosyaları okur
- Format: `node1 node2` (boşluk, tab veya virgül ile ayrılmış)
- Yorum satırları (# ile başlayan) göz ardı edilir
- Self-loop'ları atlar
- Hata toleranslı: Geçersiz satırları atlar ve devam eder

**`get_largest_component(G)`**
- En büyük bağlı bileşeni çıkarır
- Bağlı olmayan ağlar için kritik
- SIR modeli bağlı ağlar gerektirir

**`prepare_graph(file_path, use_largest_component, ...)`**
- Grafı yükler ve hazırlar
- En büyük bileşeni çıkarır (opsiyonel)
- Kullanıma hazır graf döndürür

**`create_sample_network(n, k, p)`**
- Watts-Strogatz modeli ile örnek ağ oluşturur
- Parametreler:
  - n: Node sayısı
  - k: Her node'un komşu sayısı
  - p: Rewiring olasılığı
- Seed: 42 (reproducible)

**Desteklenen Ağ Modelleri:**
- Watts-Strogatz (Small World)
- Barabási-Albert (Scale Free) - GUI'da
- Erdős-Rényi (Random) - GUI'da

**Önerilen Veri Setleri:**
- Facebook Social Network
- Email Network
- Collaboration Network (ca-GrQc)

#### 2. src/centrality.py

**Sorumluluk:** Merkeziyet ölçülerini hesaplama ve node seçimi

**Ana Fonksiyonlar:**

**`calculate_degree_centrality(G)`**
- Degree centrality hesaplar
- NetworkX kullanır
- O(n) karmaşıklık

**`calculate_betweenness_centrality(G, k)`**
- Betweenness centrality hesaplar
- k=None: Tam hesaplama
- k belirtilirse: Yaklaşık hesaplama (k-sample)
- Büyük ağlar için optimizasyon

**`calculate_closeness_centrality(G)`**
- Closeness centrality hesaplar
- O(n²) karmaşıklık

**`calculate_eigenvector_centrality(G, max_iter)`**
- Eigenvector centrality hesaplar
- Power iteration metodu
- Yakınsama başarısız olursa degree'ye fallback

**`calculate_all_centralities(G, use_approximation, k_sample)`**
- Tüm merkeziyet ölçülerini hesaplar
- Dictionary döndürür: `{measure: {node: score}}`
- Optimizasyon seçenekleri

**`get_top_k_nodes_by_measure(centralities, measure, k)`**
- Belirtilen ölçüye göre en yüksek k node'u döndürür
- Sıralama: Yüksekten düşüğe
- Liste döndürür: `[node1, node2, ..., nodek]`

**Yardımcı Fonksiyonlar:**
- `get_top_k_nodes(centrality, k)`: Genel top-k seçimi
- `print_centrality_stats(...)`: İstatistikleri yazdırma
- `compare_centralities(...)`: Ölçüleri karşılaştırma

#### 3. src/sir_simulation.py

**Sorumluluk:** SIR modeli simülasyonu

**SIRModel Sınıfı:**

**Özellikler:**
- `G`: NetworkX graf
- `beta`: Bulaşma olasılığı
- `gamma`: İyileşme olasılığı
- `seed`: Rastgelelik seed'i (reproducible)
- `states`: Node durumları dictionary `{node: 'S'|'I'|'R'}`
- `time_step`: Mevcut zaman adımı
- `infection_history`: Enfeksiyon geçmişi `{node: (source, time)}`
- `initial_infected`: Başlangıç enfekte node'ları

**Ana Metodlar:**

**`reset()`**
- Simülasyonu sıfırlar
- Tüm node'ları S durumuna getirir
- Zaman adımını 0'a ayarlar
- Geçmişi temizler

**`set_initial_infected(nodes)`**
- Başlangıç enfekte node'larını ayarlar
- Bu node'ları I durumuna getirir
- infection_history'ye kaydeder: `(None, 0)`

**`get_state_counts()`**
- S, I, R sayılarını döndürür
- Tuple: `(S_count, I_count, R_count)`

**`get_infected_nodes()`**
- Enfekte node'ları liste olarak döndürür

**`get_susceptible_nodes()`**
- Duyarlı node'ları liste olarak döndürür

**`step()`**
- Bir zaman adımı simüle eder
- Önce bulaşma, sonra iyileşme
- True dönerse devam ediyor, False dönerse bitti
- Enfeksiyon geçmişini günceller

**`run(initial_infected, max_steps)`**
- Tam simülasyonu çalıştırır
- Zaman serisi verilerini toplar
- Sonuçları hesaplar ve döndürür
- Dönen dictionary:
  - `time_series`: `[(S, I, R), ...]`
  - `final_outbreak_size`: Toplam enfekte
  - `peak_infected`: Maksimum eşzamanlı enfekte
  - `peak_time`: Peak zamanı
  - `total_steps`: Toplam adım sayısı
  - `final_states`: Final durumları

**Yardımcı Fonksiyonlar:**

**`run_sir_simulation(...)`**
- Tek simülasyon çalıştırır
- SIRModel wrapper'ı

**`run_multiple_simulations(...)`**
- Birden fazla simülasyon çalıştırır
- Her simülasyon için farklı seed
- Liste döndürür: `[result1, result2, ...]`

**`aggregate_simulation_results(results)`**
- Çoklu simülasyon sonuçlarını birleştirir
- İstatistikleri hesaplar:
  - Ortalama ve standart sapma
  - Ortalama zaman serisi
- Dönen dictionary:
  - `mean_outbreak_size`, `std_outbreak_size`
  - `mean_peak_infected`, `std_peak_infected`
  - `mean_peak_time`, `std_peak_time`
  - `mean_time_series`: Ortalama zaman serisi

#### 4. src/experiments.py

**Sorumluluk:** Deney senaryolarını yönetme ve karşılaştırma

**ExperimentRunner Sınıfı:**

**Özellikler:**
- `G`: NetworkX graf
- `beta`, `gamma`: SIR parametreleri
- `k_initial`: Başlangıç enfekte sayısı
- `n_runs`: Tekrar sayısı
- `seed`: Base seed
- `centralities`: Hesaplanan merkeziyet ölçüleri
- `results`: Senaryo sonuçları `{scenario: aggregated_results}`

**Ana Metodlar:**

**`run_random_scenario()`**
- Rastgele seçim senaryosu
- Her run için farklı rastgele node'lar
- n_runs kez simülasyon çalıştırır
- Sonuçları birleştirir ve kaydeder

**`run_centrality_scenario(measure)`**
- Belirtilen merkeziyet ölçüsüne göre simülasyon
- En yüksek k node'u seçer
- n_runs kez simülasyon çalıştırır
- Sonuçları birleştirir ve kaydeder

**`run_all_scenarios()`**
- Tüm senaryoları çalıştırır:
  1. Random
  2. Degree
  3. Betweenness
  4. Closeness
  5. Eigenvector
- Sonuçları `results` dictionary'sine kaydeder

**`compare_scenarios()`**
- Senaryoları karşılaştırır
- Tablo formatında yazdırır
- En iyi stratejileri belirler:
  - En büyük salgın
  - En yüksek peak
  - En hızlı yayılım

**`get_results_for_plotting()`**
- Grafik için sonuçları düzenler
- Dictionary döndürür:
  - `scenarios`: Senaryo isimleri listesi
  - `outbreak_sizes`: Final salgın büyüklükleri
  - `outbreak_stds`: Standart sapmalar
  - `peak_infecteds`: Peak enfekte sayıları
  - `peak_infected_stds`: Standart sapmalar
  - `peak_times`: Peak zamanları
  - `peak_time_stds`: Standart sapmalar
  - `time_series`: Zaman serileri dictionary'si

#### 5. src/plots.py

**Sorumluluk:** Statik grafik oluşturma (matplotlib/seaborn)

**Ana Fonksiyonlar:**

**`plot_time_series(time_series_dict, save_path, title)`**
- Zaman serisi grafikleri çizer
- 3 alt grafik: S, I, R
- Her senaryo için farklı renk
- Legend ve grid

**`plot_comparison_bars(plotting_data, save_path)`**
- Karşılaştırma bar grafikleri
- 3 alt grafik:
  1. Final Outbreak Size
  2. Peak Infected
  3. Peak Time
- Hata çubukları (standart sapma)
- Değerler bar üzerinde

**`plot_network_snapshot(G, states, time_step, save_path, title, layout_pos)`**
- Ağ durumunu görselleştirir
- Renk kodlaması: S (mavi), I (kırmızı), R (yeşil)
- Spring layout kullanır
- Küçük ağlar için node etiketleri

**`plot_multiple_snapshots(G, simulation_results, time_points, save_dir)`**
- Farklı zaman noktalarında ağ durumu
- Zaman serisi görselleştirmesi
- Otomatik zaman noktası seçimi

**`create_all_plots(experiment_runner, save_dir)`**
- Tüm grafikleri oluşturur ve kaydeder
- Zaman serileri, karşılaştırma, snapshot'lar
- Küçük ağlar için snapshot'lar

**Stil:**
- Seaborn whitegrid stili
- Husl renk paleti
- Yüksek çözünürlük (300 DPI)
- Tight layout

#### 6. main.py

**Sorumluluk:** Komut satırı arayüzü (CLI)

**Modlar:**

**1. Etkileşimli Mod (Varsayılan):**
- Kullanıcıya adım adım sorular sorar
- Veri seti seçimi
- Parametre girişi
- Onay mekanizması

**2. Batch Mod (Komut Satırı Argümanları):**
- Parametreleri doğrudan belirtme
- Otomatik çalıştırma
- Script'lerde kullanım için uygun

**3. Demo Mod:**
- Hızlı test için
- Karate Club grafiği
- Önceden ayarlanmış parametreler

**Komut Satırı Argümanları:**
- `--demo`: Demo modu
- `--list-datasets`: Önerilen veri setlerini listele
- `--sample N`: N node'lu örnek ağ oluştur
- `--input FILE`: Graf dosyası yükle
- `--beta`: Bulaşma olasılığı (varsayılan: 0.3)
- `--gamma`: İyileşme olasılığı (varsayılan: 0.1)
- `--k-initial`: Başlangıç enfekte sayısı (varsayılan: 5)
- `--n-runs`: Tekrar sayısı (varsayılan: 30)
- `--output DIR`: Çıktı klasörü

**Özellikler:**
- Windows console encoding sorunu çözümü
- Kullanıcı dostu mesajlar
- Hata yönetimi
- İlerleme göstergeleri

#### 7. gui.py

**Sorumluluk:** Streamlit web arayüzü (GUI)

**Genel Yapı:**
- Streamlit framework kullanır
- Wide layout
- Sidebar'da parametreler
- 5 sekme (tab)

**Sekmeler:**

**1. Ağ Analizi:**
- 2D ve 3D ağ görselleştirme (Plotly)
- Merkeziyet skorları tablosu
- Node dereceleri histogramı
- Ağ istatistikleri:
  - Düğüm sayısı
  - Kenar sayısı
  - Ortalama derece
  - Kümeleme katsayısı
  - Çap (diameter)
- Merkeziyet görselleştirme seçimi
- En yüksek merkeziyete sahip düğümler listesi

**2. Simülasyon:**
- Parametre ayarları (slider'lar):
  - Beta (bulaşma olasılığı)
  - Gamma (iyileşme olasılığı)
  - Başlangıç enfekte sayısı
  - Tekrar sayısı
- R₀ (Temel Üreme Sayısı) gösterimi
- "Tüm Senaryoları Çalıştır" butonu
- İlerleme çubuğu
- Sonuç özeti tablosu

**3. Sonuçlar:**
- Özet metrikler (kartlar)
- İnteraktif zaman serileri (Plotly)
- Karşılaştırma bar grafikleri
- En etkili stratejiler vurgulaması:
  - En büyük salgın
  - En yüksek peak
  - En hızlı yayılım

**4. Animasyon:**
- Gerçek zamanlı simülasyon animasyonu
- Strateji seçimi
- Parametre ayarları
- Hız kontrolü (slider)
- Maksimum adım sayısı
- 2D/3D görünüm seçimi
- Kenar gösterimi kontrolü
- Canlı metrikler (S, I, R sayıları)
- Durum mesajları

**5. Enfeksiyon Yolu:**
- Enfeksiyon yayılım yolunu görselleştirme
- 2D ve 3D görünümler
- Renk kodlaması:
  - Koyu kırmızı: Başlangıç enfekte (Patient Zero)
  - Sarı: Sonradan enfekte olanlar
  - Mavi: Enfekte olmayanlar
  - Kalın kırmızı çizgiler: Enfeksiyon yolu
- Patient Zero annotation'ları
- İstatistikler:
  - Toplam enfekte
  - Başlangıç enfekte
  - En geç enfeksiyon adımı
- Başlangıç enfekte node'lar listesi

**Veri Seti Seçimi:**
- Örnek ağ oluştur:
  - Watts-Strogatz (Small World)
  - Barabási-Albert (Scale Free)
  - Erdős-Rényi (Random)
- Hazır modeller:
  - Karate Club (34 düğüm)
  - Les Misérables (77 düğüm)
  - Örnek Ağ (100 düğüm)

**Session State Yönetimi:**
- Graf
- Merkeziyet ölçüleri
- Deney sonuçları
- Simülasyon durumu
- 3D layout
- Enfeksiyon geçmişi
- Son başlangıç enfekte node'ları

**CSS Animasyonları:**
- Fade in/out efektleri
- Slide animasyonları
- Hover efektleri
- Pulse animasyonları
- Shimmer efektleri

**Performans Optimizasyonları:**
- Büyük ağlar için 3D animasyon devre dışı
- Layout cache'leme
- Gereksiz hesaplamaların önlenmesi
- Streamlit session state kullanımı

---

## ALGORİTMA VE İMPLEMENTASYON DETAYLARI

### SIR Simülasyon Algoritması

**Pseudocode:**
```
1. Initialize:
   - states[node] = 'S' for all nodes
   - time_step = 0
   - infection_history = {}
   - Set initial_infected nodes to 'I'

2. While infected_nodes exist and time_step < max_steps:
   a. Infection Phase:
      For each infected_node:
         For each neighbor of infected_node:
            If neighbor is 'S' and random() < beta:
               neighbor.state = 'I'
               infection_history[neighbor] = (infected_node, time_step + 1)
   
   b. Recovery Phase:
      For each infected_node:
         If random() < gamma:
            infected_node.state = 'R'
   
   c. Update:
      time_step += 1
      Record (S_count, I_count, R_count)

3. Calculate Results:
   - final_outbreak_size = R_count
   - peak_infected = max(I_counts)
   - peak_time = index of peak_infected
```

### Merkeziyet Hesaplama Algoritmaları

**Degree Centrality:**
```
For each node v:
   degree_centrality[v] = degree(v) / (n - 1)
```

**Betweenness Centrality (Brandes Algorithm):**
```
For each node s:
   Run BFS from s
   Calculate shortest paths
   For each node v on paths:
      betweenness[v] += paths_through_v / total_paths
```

**Closeness Centrality:**
```
For each node v:
   distances = BFS_distances(v)
   closeness[v] = (n - 1) / sum(distances)
```

**Eigenvector Centrality (Power Iteration):**
```
x = [1/n] * n  # Initial guess
For iteration in range(max_iter):
   x_new = A * x
   x_new = x_new / ||x_new||
   If converged:
      break
   x = x_new
```

### Deney Çalıştırma Algoritması

**Pseudocode:**
```
1. Load/Create Graph G
2. Calculate all centralities
3. For each scenario:
   a. Select initial_infected nodes:
      - Random: random.sample(nodes, k)
      - Centrality: top_k_nodes_by_measure(centrality, k)
   
   b. Run n_runs simulations:
      For run in range(n_runs):
         result = run_sir_simulation(G, initial_infected, beta, gamma, seed)
         results.append(result)
   
   c. Aggregate results:
      aggregated = aggregate_simulation_results(results)
      scenario_results[scenario] = aggregated

4. Compare scenarios
5. Generate plots
```

---

## GÖRSELLEŞTİRME ÖZELLİKLERİ

### 2D Ağ Görselleştirme

**Layout:**
- Spring layout (force-directed)
- Seed: 42 (reproducible)
- k: 0.5 (node spacing)
- Iterations: 50

**Node Görselleştirme:**
- Renk: Duruma göre (S: mavi, I: kırmızı, R: yeşil) veya merkeziyet skoruna göre
- Boyut: Degree'ye göre veya sabit
- Hover: Node bilgileri (isim, durum, derece, merkeziyet)

**Edge Görselleştirme:**
- Normal kenarlar: Gri, ince
- Enfeksiyon yolu: Kırmızı, kalın

### 3D Ağ Görselleştirme

**Layout:**
- 2D spring layout + Z ekseni
- Z koordinatı: Node derecesine göre normalize edilmiş
- Camera: Eye (1.5, 1.5, 1.2), Center (0, 0, 0)

**Özellikler:**
- İnteraktif rotasyon
- Zoom ve pan
- 3D hover bilgileri
- Grid ve eksenler

**Performans:**
- Büyük ağlar (200+ node) için otomatik devre dışı
- Layout cache'leme
- Optimize edilmiş rendering

### Zaman Serisi Görselleştirme

**Grafik Türü:**
- Çizgi grafikleri (line plots)
- Her senaryo için farklı renk
- Çizgi stilleri: S (solid), I (dash), R (dot)

**İnteraktif Özellikler:**
- Zoom
- Pan
- Hover (değer gösterimi)
- Legend (göster/gizle)

### Karşılaştırma Grafikleri

**Grafik Türü:**
- Bar grafikleri (bar charts)
- Hata çubukları (standart sapma)
- Değerler bar üzerinde

**Metrikler:**
- Final Outbreak Size
- Peak Infected
- Peak Time

### Animasyon

**Özellikler:**
- Gerçek zamanlı frame-by-frame gösterim
- Hız kontrolü (slider)
- Play/Pause (manuel kontrol)
- Canlı metrikler
- Durum mesajları

**Performans:**
- Streamlit rerun mekanizması
- Time.sleep() ile hız kontrolü
- Optimize edilmiş rendering

---

## KULLANIM SENARYOLARI

### 1. Araştırma Senaryosu

**Amaç:** Farklı merkeziyet ölçülerinin etkinliğini karşılaştırmak

**Adımlar:**
1. Veri seti yükle veya oluştur
2. Merkeziyet ölçülerini hesapla
3. Tüm senaryoları çalıştır
4. Sonuçları karşılaştır
5. Grafikleri analiz et

**Çıktılar:**
- Hangi strateji en etkili?
- Ağ yapısının etkisi nedir?
- Parametrelerin etkisi nedir?

### 2. Eğitim Senaryosu

**Amaç:** SIR modeli ve merkeziyet ölçülerini öğretmek

**Adımlar:**
1. Küçük bir ağ seç (örn: Karate Club)
2. Animasyon sekmesinde simülasyon izle
3. Farklı parametrelerle deney yap
4. Enfeksiyon yolu sekmesinde yayılımı görselleştir
5. Sonuçları yorumla

**Çıktılar:**
- SIR modeli dinamikleri
- Merkeziyet ölçülerinin anlamı
- Ağ yapısının önemi

### 3. Karşılaştırma Senaryosu

**Amaç:** Farklı ağ yapılarında salgın davranışını karşılaştırmak

**Adımlar:**
1. Farklı ağ modelleri oluştur
2. Aynı parametrelerle simülasyon çalıştır
3. Sonuçları karşılaştır
4. Ağ yapısının etkisini analiz et

**Çıktılar:**
- Scale-free vs Small World
- Modüler ağların davranışı
- Topoloji etkisi

### 4. Görselleştirme Senaryosu

**Amaç:** Karmaşık ağ yapılarını ve dinamik süreçleri görselleştirmek

**Adımlar:**
1. İlginç bir ağ seç
2. 3D görselleştirme kullan
3. Animasyon izle
4. Enfeksiyon yolu takip et
5. Screenshot'lar al

**Çıktılar:**
- Görsel materyaller
- Sunum için grafikler
- Eğitim materyalleri

---

## TEKNİK DETAYLAR

### Teknoloji Stack'i

**Python Sürümü:**
- Python 3.8+ (önerilen: 3.11)

**Ana Kütüphaneler:**
- **networkx (3.4+)**: Graf işlemleri ve merkeziyet hesaplamaları
- **numpy (1.26+)**: Sayısal hesaplamalar
- **pandas (2.2+)**: Veri işleme
- **matplotlib (3.10+)**: Statik grafikler
- **seaborn (0.13+)**: Gelişmiş görselleştirme
- **streamlit (1.51+)**: Web arayüzü framework'ü
- **plotly (6.5+)**: İnteraktif görselleştirmeler
- **requests (2.32+)**: Veri seti indirme

### Performans Optimizasyonları

**Büyük Ağlar İçin:**
- Betweenness centrality: k-sample yaklaşımı
- Eigenvector centrality: Fallback mekanizması
- 3D animasyon: Otomatik devre dışı (200+ node)
- Layout cache'leme
- Gereksiz hesaplamaların önlenmesi

**Hesaplama Karmaşıklıkları:**
- Degree: O(n)
- Closeness: O(n²)
- Betweenness (tam): O(nm) veya O(n²)
- Betweenness (yaklaşık): O(km)
- Eigenvector: O(n²) iteratif
- SIR simülasyon: O(m * steps)

### Veri Formatı

**Edge List Format:**
```
node1 node2
node3 node4
...
```

**Desteklenen Ayırıcılar:**
- Boşluk
- Tab
- Virgül

**Yorum Satırları:**
- # ile başlayan satırlar göz ardı edilir

**Header:**
- Opsiyonel header satırı desteklenir

### Hata Yönetimi

**Try-Except Blokları:**
- Dosya okuma hataları
- Graf yükleme hataları
- Merkeziyet hesaplama hataları
- Simülasyon hataları

**Fallback Mekanizmaları:**
- Eigenvector yakınsamazsa → Degree
- Bağlı olmayan ağ → En büyük bileşen
- Geçersiz satırlar → Atla ve devam et

**Kullanıcı Bildirimleri:**
- Başarı mesajları
- Hata mesajları
- Uyarı mesajları
- İlerleme göstergeleri

---

## SONUÇLAR VE BULGULAR

### Genel Bulgular

**1. Degree ve Betweenness Stratejileri:**
- En büyük salgınları üretir
- Hub node'ları hedef alır
- Scale-free ağlarda çok etkili

**2. Random Stratejisi:**
- Baseline olarak kullanılır
- En küçük etkiler
- Stratejik seçimin değerini gösterir

**3. Closeness Stratejisi:**
- Orta düzeyde etkili
- Merkezi node'ları hedef alır
- Küçük dünya ağlarında etkili

**4. Eigenvector Stratejisi:**
- Hiyerarşik ağlarda etkili
- Influence yayılımı sağlar
- Yakınsama sorunları olabilir

### Ağ Yapısına Göre Değişkenlik

**Scale-free Ağlar:**
- Degree stratejisi çok etkili
- Hub node'lar kritik
- Power-law dağılımı

**Small World Ağlar:**
- Tüm stratejiler benzer sonuçlar verebilir
- Küçük ortalama mesafe
- Yüksek kümeleme

**Modüler Ağlar:**
- Betweenness stratejisi köprü node'ları yakalar
- Topluluklar arası geçişler kritik
- Modülerlik yüksek

**Düzenli Ağlar:**
- Tüm stratejiler benzer sonuçlar
- Homojen yapı
- Stratejik seçimin etkisi az

### Parametre Etkileri

**Yüksek β/γ Oranı:**
- Daha geniş yayılım
- Daha yüksek peak
- Daha hızlı yayılım

**Düşük β/γ Oranı:**
- Sınırlı yayılım
- Düşük peak
- Yavaş yayılım veya sönme

**Başlangıç Enfekte Sayısı:**
- Daha fazla başlangıç enfekte = daha geniş salgın
- Ancak stratejik seçim daha önemli

---

## ÖZEL ÖZELLİKLER VE YETENEKLER

### 1. Enfeksiyon Yolu Takibi

**Özellik:**
- Her node için enfeksiyon kaynağı ve zamanı kaydedilir
- Görselleştirme: Enfeksiyon yolu kenarları
- Patient Zero işaretleme

**Kullanım:**
- Salgının yayılım dinamiklerini anlama
- Kritik yolların belirlenmesi
- Eğitim amaçlı görselleştirme

### 2. Patient Zero İşaretleme

**Özellik:**
- Başlangıç enfekte node'lar özel olarak işaretlenir
- Koyu kırmızı renk
- Büyük boyut
- Annotation'lar

**Kullanım:**
- İlk enfekte node'ları vurgulama
- Eğitim amaçlı
- Analiz amaçlı

### 3. 3D Görselleştirme

**Özellik:**
- Node derecelerine göre Z ekseni
- İnteraktif rotasyon
- Zoom ve pan
- 3D hover bilgileri

**Kullanım:**
- Karmaşık ağ yapılarını görselleştirme
- Sunumlar için
- Eğitim amaçlı

### 4. İnteraktif Animasyon

**Özellik:**
- Gerçek zamanlı simülasyon izleme
- Hız kontrolü
- Play/Pause
- Frame-by-frame ilerleme
- Canlı metrikler

**Kullanım:**
- SIR modeli dinamiklerini anlama
- Eğitim amaçlı
- Sunumlar için

### 5. Multi-run Analizi

**Özellik:**
- Stokastik süreç için çoklu tekrar
- İstatistiksel güvenilirlik
- Ortalama ve standart sapma
- Güven aralıkları

**Kullanım:**
- Araştırma amaçlı
- Sonuçların güvenilirliği
- Karşılaştırma analizi

### 6. Çoklu Arayüz Desteği

**CLI:**
- Script'lerde kullanım
- Otomasyon
- Batch işlemler

**GUI:**
- İnteraktif kullanım
- Görselleştirme
- Eğitim amaçlı

---

## PROJE SINIRLAMALARI VE NOTLAR

### Sınırlamalar

**1. Büyük Ağlar:**
- 200+ node'da 3D animasyon yavaş olabilir
- Betweenness yaklaşık hesaplama gerekir
- Memory kullanımı artar

**2. Bağlı Olmayan Ağlar:**
- SIR modeli bağlı ağlar gerektirir
- En büyük bileşen otomatik çıkarılır
- Diğer bileşenler göz ardı edilir

**3. Eigenvector Yakınsama:**
- Bazı ağlarda yakınsamayabilir
- Otomatik fallback mekanizması
- Kullanıcıya bilgi verilir

**4. Stokastik Süreç:**
- Sonuçlar rastgelelik içerir
- Çoklu tekrar gerekir
- Seed kontrolü ile reproducible

### Notlar

**1. Reproducibility:**
- Seed değerleri kullanılır (42)
- Aynı parametrelerle aynı sonuçlar
- Bilimsel çalışmalar için önemli

**2. Performans:**
- Küçük ağlar (<100 node): Tüm özellikler aktif
- Orta ağlar (100-500 node): Bazı optimizasyonlar
- Büyük ağlar (500+ node): Yaklaşık hesaplamalar

**3. Kullanım:**
- Eğitim amaçlı: Küçük ağlar, animasyonlar
- Araştırma amaçlı: Büyük ağlar, çoklu tekrar
- Görselleştirme: Orta boy ağlar, 3D görünüm

---

## SONUÇ

Bu proje, SIR epidemik hastalık yayılım modelini ağ teorisi bağlamında uygulayan, kapsamlı bir simülasyon ve analiz platformudur. Farklı merkeziyet ölçülerinin salgın yayılımına etkisini karşılaştırarak, hem teorik bilgiyi pratik uygulamalarla birleştirir hem de eğitim ve araştırma amaçlı kullanılabilir.

**Güçlü Yönler:**
- Modüler ve genişletilebilir mimari
- İki farklı kullanıcı arayüzü (CLI ve GUI)
- Kapsamlı görselleştirmeler
- Performans optimizasyonları
- Kullanıcı dostu arayüz

**Kullanım Alanları:**
- Eğitim: SIR modeli, merkeziyet ölçüleri, ağ teorisi
- Araştırma: Epidemiyoloji, ağ analizi, algoritma karşılaştırması
- Görselleştirme: Karmaşık ağ yapıları ve dinamik süreçler
- Pratik: Aşı kampanyaları, bilgi yayılımı, virüs koruması

Bu prompt, projenin tüm yönlerini kapsamlı bir şekilde açıklamaktadır ve projeyi anlamak, geliştirmek veya kullanmak isteyen herkes için detaylı bir rehber niteliğindedir.
