# SIR Model Simülasyonu - Proje Açıklama Promptu

Bu proje, sosyal ağ grafikleri üzerinde SIR (Susceptible-Infected-Recovered) epidemik hastalık yayılım modelini simüle eden bir Python uygulamasıdır. Proje, farklı merkeziyet (centrality) ölçülerine göre seçilen başlangıç enfekte node'larının salgının yayılımı üzerindeki etkisini karşılaştırmayı amaçlar.

## Proje Amacı ve Konsepti

Temel araştırma sorusu: "Bir sosyal ağda salgını başlatmak için hangi node'ları seçmeliyiz ki salgın mümkün olduğunca geniş ve hızlı yayılsın?"

Proje, bu soruyu cevaplamak için dört farklı merkeziyet ölçüsü kullanarak başlangıç enfekte node'larını seçer ve her stratejinin salgın üzerindeki etkisini karşılaştırır:

1. **Degree Centrality**: En çok bağlantıya (edge) sahip node'lar
2. **Betweenness Centrality**: Ağda en çok "köprü" görevi gören, en kısa yollar üzerinde bulunan node'lar
3. **Closeness Centrality**: Diğer tüm node'lara ortalama en kısa mesafede olan node'lar
4. **Eigenvector Centrality**: Önemli node'lara bağlı olan node'lar

Ayrıca rastgele seçim (Random) stratejisi baseline olarak kullanılır.

## Teknik Detaylar

### SIR Modeli

SIR modeli, popülasyonu üç duruma ayırır:
- **S (Susceptible)**: Hastalığa duyarlı, henüz enfekte olmamış
- **I (Infected)**: Enfekte, hastalığı yayabilir
- **R (Recovered)**: İyileşmiş, artık enfekte olamaz veya enfekte edemez

**Simülasyon Dinamiği:**
Her zaman adımında (discrete time steps):
1. **Bulaşma (Infection)**: Her enfekte node, komşularını `beta` (bulaşma olasılığı) parametresi ile enfekte eder
2. **İyileşme (Recovery)**: Her enfekte node, `gamma` (iyileşme olasılığı) parametresi ile iyileşerek R durumuna geçer

**Temel Üreme Sayısı (R₀)**: beta/gamma
- R₀ > 1: Salgın yayılır
- R₀ < 1: Salgın söner

### Proje Yapısı

Proje modüler bir yapıda organize edilmiştir:

```
sir-network-epidemic-simulation/
├── src/
│   ├── data_loading.py          # Graf yükleme ve oluşturma
│   ├── centrality.py            # Merkeziyet ölçüleri hesaplama
│   ├── sir_simulation.py        # SIR modeli implementasyonu
│   ├── experiments.py           # Deney senaryoları ve çalıştırma
│   └── plots.py                 # Statik grafik oluşturma (matplotlib)
├── main.py                      # Komut satırı arayüzü (CLI)
├── gui.py                       # Streamlit web arayüzü (GUI)
├── requirements.txt             # Python bağımlılıkları
└── README.md                    # Proje dokümantasyonu
```

### Modüller ve İşlevleri

#### 1. `src/data_loading.py`
- Edge list formatında graf dosyalarını yükler
- En büyük bağlı bileşeni (largest connected component) çıkarır
- Watts-Strogatz modeli kullanarak örnek ağlar oluşturur
- Önerilen sosyal ağ veri setlerini listeler

#### 2. `src/centrality.py`
- Dört farklı merkeziyet ölçüsünü hesaplar (NetworkX kütüphanesi kullanarak)
- Her merkeziyet ölçüsüne göre en yüksek skorlu k node seçer
- Büyük ağlar için yaklaşık hesaplama seçenekleri sunar (örneğin, betweenness için k-sample)

#### 3. `src/sir_simulation.py`
- `SIRModel` sınıfı: Tek bir simülasyon çalıştırır
  - Node durumlarını yönetir (S, I, R)
  - Enfeksiyon geçmişini takip eder (hangi node'un hangi node'dan enfekte olduğu)
  - Her adımda bulaşma ve iyileşme işlemlerini gerçekleştirir
- `run_multiple_simulations`: Aynı parametrelerle birden fazla simülasyon çalıştırır (stokastik süreç için)
- `aggregate_simulation_results`: Çoklu simülasyon sonuçlarını birleştirir ve istatistikler hesaplar

**Önemli Özellik: Enfeksiyon Takibi**
- Her node için, hangi node'dan enfekte olduğu ve hangi zaman adımında enfekte olduğu kaydedilir
- `infection_history` dictionary'si: `{node: (source_node, time_step)}`
- `initial_infected` listesi: Başlangıç enfekte node'ları (Patient Zero'lar)

#### 4. `src/experiments.py`
- `ExperimentRunner` sınıfı: Tüm deney senaryolarını yönetir
- Her merkeziyet ölçüsü için simülasyon çalıştırır
- Rastgele baseline senaryosu çalıştırır
- Sonuçları karşılaştırır ve özetler
- Her senaryo için `n_runs` (varsayılan 30) kez tekrar eder

#### 5. `src/plots.py`
- Statik matplotlib grafikleri oluşturur:
  - Zaman serileri (S, I, R sayılarının zamanla değişimi)
  - Karşılaştırma bar grafikleri (final outbreak size, peak infected, peak time)
  - Ağ snapshot'ları (farklı zaman noktalarında ağ durumu)

### Kullanıcı Arayüzleri

#### 1. Komut Satırı Arayüzü (`main.py`)
- Etkileşimli mod: Kullanıcıya adım adım sorular sorar
- Komut satırı argümanları: Parametreleri doğrudan belirtme
- Demo modu: Hızlı test için önceden ayarlanmış parametreler
- Veri seti listeleme: Önerilen sosyal ağ veri setlerini gösterir

**Parametreler:**
- `--demo`: Hızlı demo çalıştır
- `--sample N`: N node'lu örnek ağ oluştur
- `--input FILE`: Graf dosyası yükle (edge list)
- `--beta`: Bulaşma olasılığı (0-1, varsayılan: 0.3)
- `--gamma`: İyileşme olasılığı (0-1, varsayılan: 0.1)
- `--k-initial`: Başlangıç enfekte node sayısı (varsayılan: 5)
- `--n-runs`: Her senaryo için tekrar sayısı (varsayılan: 30)
- `--output DIR`: Çıktı klasörü

#### 2. Streamlit Web Arayüzü (`gui.py`)
Modern, interaktif web tabanlı arayüz. Özellikleri:

**Sekmeler (Tabs):**
1. **Ağ Analizi**: 
   - 2D ve 3D ağ görselleştirme (Plotly)
   - Merkeziyet skorları tablosu
   - Node dereceleri histogramı
   - Ağ istatistikleri

2. **Simülasyon**:
   - Parametre ayarları (slider'lar)
   - Senaryo seçimi
   - Simülasyon çalıştırma butonu
   - Sonuç özeti tablosu

3. **Sonuçlar**:
   - İnteraktif zaman serileri (Plotly)
   - Karşılaştırma bar grafikleri
   - İstatistiksel özetler

4. **Animasyon**:
   - Gerçek zamanlı 2D simülasyon animasyonu
   - Hız kontrolü (slider)
   - Play/Pause butonları
   - Frame-by-frame ilerleme
   - Büyük ağlar için 3D animasyon (opsiyonel, performans nedeniyle devre dışı)

5. **Enfeksiyon Yolu**:
   - Enfeksiyon yayılım yolunu görselleştirme
   - 2D ve 3D görünümler
   - Renk kodlaması:
     - Koyu kırmızı: Başlangıç enfekte node'lar (Patient Zero)
     - Sarı: Sonradan enfekte olan node'lar
     - Mavi: Enfekte olmayan node'lar
     - Kırmızı kalın çizgiler: Enfeksiyon yolu kenarları (hangi node'un hangi node'u enfekte ettiği)
   - "Patient Zero" annotation'ları

**GUI Özellikleri:**
- Streamlit session state yönetimi
- Sidebar'da parametre ayarları
- Responsive layout (wide mode)
- CSS animasyonları (fade-in, slide-in efektleri)
- Plotly interaktif grafikleri (zoom, pan, hover)
- Büyük ağlar için performans optimizasyonları

### Teknoloji Stack'i

**Python Kütüphaneleri:**
- `networkx` (3.4+): Graf işlemleri ve merkeziyet hesaplamaları
- `numpy` (1.26+): Sayısal hesaplamalar
- `pandas` (2.2+): Veri işleme
- `matplotlib` (3.10+): Statik grafikler
- `seaborn` (0.13+): Gelişmiş görselleştirme
- `streamlit` (1.51+): Web arayüzü
- `plotly` (6.5+): İnteraktif görselleştirmeler
- `requests` (2.32+): Veri seti indirme

### Veri Formatı

Proje, edge list formatında graf dosyalarını okur:
```
node1 node2
node3 node4
...
```

Ayırıcılar: boşluk, tab veya virgül
Yorumlar: # ile başlayan satırlar göz ardı edilir

### Simülasyon Çıktıları

Her senaryo için hesaplanan metrikler:
- **Final Outbreak Size**: Toplam enfekte olmuş node sayısı (I + R durumunda)
- **Peak Infected**: Maksimum aynı anda enfekte node sayısı
- **Peak Time**: Peak infected'e ulaşılan zaman adımı
- **Time Series**: Her zaman adımında S, I, R sayıları

### Kullanım Senaryoları

1. **Araştırma**: Farklı merkeziyet ölçülerinin salgın yayılımına etkisini incelemek
2. **Eğitim**: SIR modeli, merkeziyet ölçüleri ve ağ teorisi kavramlarını öğretmek
3. **Karşılaştırma**: Farklı ağ yapılarında (sosyal, biyolojik, teknolojik) salgın davranışını karşılaştırmak
4. **Görselleştirme**: Karmaşık ağ yapılarını ve dinamik süreçleri görselleştirmek

### Performans Optimizasyonları

- Büyük ağlar (1000+ node) için betweenness centrality yaklaşık hesaplama (k-sample)
- Eigenvector centrality yakınsamazsa otomatik olarak degree centrality'ye fallback
- 3D animasyon büyük ağlar için otomatik devre dışı bırakılır
- Streamlit session state ile gereksiz hesaplamalar önlenir
- Plotly için optimize edilmiş node ve edge çizimi

### Özel Özellikler

1. **Enfeksiyon Yolu Takibi**: Hangi node'un hangi node'dan enfekte olduğunu görselleştirme
2. **Patient Zero İşaretleme**: Başlangıç enfekte node'ları özel annotation ile işaretleme
3. **3D Görselleştirme**: Node derecelerine göre Z ekseni yüksekliği
4. **İnteraktif Animasyon**: Gerçek zamanlı simülasyon izleme
5. **Renk Kodlaması**: Farklı enfeksiyon durumları için sezgisel renkler
6. **Multi-run Analizi**: Stokastik süreç için istatistiksel güvenilirlik

### Beklenen Sonuçlar

Genel olarak:
- **Degree ve Betweenness** stratejileri → Daha büyük salgınlar
- **Random** stratejisi → Baseline, en küçük etkiler
- **Yüksek β/γ oranı** → Daha geniş yayılım
- **Hub node'lardan başlamak** → Daha hızlı ve geniş yayılım

Ancak sonuçlar ağ yapısına (topolojiye) göre değişebilir. Örneğin:
- Scale-free ağlarda (sosyal ağlar): Degree stratejisi çok etkili
- Düzenli ağlarda: Tüm stratejiler benzer sonuçlar verebilir
- Modüler ağlarda: Betweenness stratejisi köprü node'ları yakalayabilir

Bu proje, yüksek lisans düzeyinde bir graf algoritmaları dersi projesidir ve hem teorik hem de pratik bilgileri birleştirir.


