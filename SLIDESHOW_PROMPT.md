# SIR Network Epidemic Simulation - Slideshow Hazırlama Promptu

## AI Agent Görevi
Bu proje hakkında akademik sunum kalitesinde, profesyonel ve kapsamlı bir slideshow hazırlamak. Sunum hem teknik hem de görsel açıdan zengin olmalı, projenin tüm yönlerini kapsamalı ve izleyicilere projenin değerini ve önemini net bir şekilde aktarmalıdır.

---

## Proje Genel Bilgileri

### Proje Adı
**SIR Model Simülasyonu - Merkeziyet Ölçüleri ile Hastalık Yayılımı Analizi**

### Proje Türü
Yüksek lisans düzeyinde Graf Algoritmaları dersi projesi

### Temel Araştırma Sorusu
"Bir sosyal ağda salgını başlatmak için hangi node'ları seçmeliyiz ki salgın mümkün olduğunca geniş ve hızlı yayılsın?"

### Proje Amacı
Farklı merkeziyet (centrality) ölçülerine göre seçilen başlangıç enfekte node'larının salgının yayılımı üzerindeki etkisini karşılaştırmak ve hangi stratejinin en etkili olduğunu belirlemek.

---

## Sunum Yapısı ve İçerik Detayları

### SLIDE 1: Kapak Sayfası
**Başlık:** SIR Model Simülasyonu: Merkeziyet Ölçüleri ve Hastalık Yayılımı Analizi
**Alt Başlık:** Graf Algoritmaları Dersi - Yüksek Lisans Projesi
**Görsel:** Ağ görselleştirmesi veya SIR model diyagramı
**Tarih ve İsim:** Sunum tarihi ve proje sahibi bilgileri

### SLIDE 2: İçindekiler / Sunum Akışı
1. Giriş ve Motivasyon
2. SIR Modeli Teorisi
3. Merkeziyet Ölçüleri
4. Proje Mimarisi
5. Uygulama Detayları
6. Sonuçlar ve Bulgular
7. Görselleştirmeler
8. Sonuç ve Gelecek Çalışmalar

### SLIDE 3: Giriş ve Motivasyon
**Başlık:** Neden Bu Proje?
**İçerik:**
- Epidemik hastalıkların sosyal ağlarda nasıl yayıldığını anlamak kritik öneme sahip
- Salgın kontrolü için stratejik node seçimi hayati önem taşır
- Farklı merkeziyet ölçülerinin etkinliğini karşılaştırmak pratik değer sağlar
- Gerçek dünya uygulamaları: Aşı kampanyaları, bilgi yayılımı, virüs koruması

**Görsel:** Gerçek dünya örnekleri (sosyal medya ağları, ulaşım ağları, vb.)

### SLIDE 4: SIR Modeli Teorisi - Genel Bakış
**Başlık:** SIR Modeli Nedir?
**İçerik:**
- **S (Susceptible)**: Hastalığa duyarlı, henüz enfekte olmamış bireyler
- **I (Infected)**: Enfekte olmuş, hastalığı yayabilen bireyler
- **R (Recovered)**: İyileşmiş, artık enfekte olamaz veya enfekte edemez bireyler

**Görsel:** SIR model durum geçiş diyagramı (S → I → R)
**Formül:** R₀ = β/γ (Temel Üreme Sayısı)
- R₀ > 1: Salgın yayılır
- R₀ < 1: Salgın söner

### SLIDE 5: SIR Modeli - Simülasyon Dinamiği
**Başlık:** Nasıl Çalışır?
**İçerik:**
- **Discrete Time Steps**: Her adımda iki işlem gerçekleşir
  1. **Bulaşma (Infection)**: Her enfekte node, komşularını β (beta) olasılığı ile enfekte eder
  2. **İyileşme (Recovery)**: Her enfekte node, γ (gamma) olasılığı ile iyileşir

**Parametreler:**
- β (beta): Bulaşma olasılığı (0-1 arası, yüksek = hızlı yayılma)
- γ (gamma): İyileşme olasılığı (0-1 arası, yüksek = hızlı iyileşme)

**Görsel:** Bir zaman adımında ağ üzerinde enfeksiyon yayılımı animasyonu veya snapshot

### SLIDE 6: Merkeziyet Ölçüleri - Genel Bakış
**Başlık:** Ağda Önemli Node'ları Nasıl Belirleriz?
**İçerik:**
Proje dört farklı merkeziyet ölçüsünü test ediyor:
1. **Degree Centrality**: En çok bağlantıya sahip node'lar
2. **Betweenness Centrality**: Ağda köprü görevi gören node'lar
3. **Closeness Centrality**: Diğer node'lara en yakın olanlar
4. **Eigenvector Centrality**: Önemli node'lara bağlı olanlar

**Baseline:** Random (rastgele seçim)

**Görsel:** Her merkeziyet ölçüsünün farklı node'ları vurguladığını gösteren ağ görselleştirmeleri

### SLIDE 7: Merkeziyet Ölçüleri - Detaylı Açıklamalar
**Başlık:** Her Ölçünün Anlamı

**1. Degree Centrality:**
- Tanım: Bir node'un sahip olduğu bağlantı sayısı
- Mantık: Daha fazla bağlantı = daha fazla yayılma fırsatı
- Hesaplama: O(n) - çok hızlı
- En iyi olduğu durum: Scale-free ağlar (sosyal medya)

**2. Betweenness Centrality:**
- Tanım: Bir node'un tüm en kısa yollar üzerinde kaç kez bulunduğu
- Mantık: Köprü node'lar kritik geçiş noktalarıdır
- Hesaplama: O(n²) veya O(nm) - yavaş, büyük ağlarda yaklaşık hesaplama
- En iyi olduğu durum: Modüler ağlar, topluluklar arası köprüler

**3. Closeness Centrality:**
- Tanım: Bir node'un diğer tüm node'lara ortalama en kısa mesafesi
- Mantık: Merkeze yakın node'lar hızlı erişim sağlar
- Hesaplama: O(n²) - orta hız
- En iyi olduğu durum: Merkezi ağ yapıları

**4. Eigenvector Centrality:**
- Tanım: Önemli node'lara bağlı olan node'lar daha yüksek skor alır
- Mantık: Sadece bağlantı sayısı değil, bağlantıların kalitesi önemli
- Hesaplama: O(n²) iteratif - yakınsama sorunları olabilir
- En iyi olduğu durum: Hiyerarşik ağlar

**Görsel:** Her ölçü için örnek node'ları gösteren karşılaştırmalı görselleştirme

### SLIDE 8: Proje Mimarisi - Genel Yapı
**Başlık:** Proje Nasıl Organize Edildi?
**İçerik:**
Modüler ve genişletilebilir bir yapı:

```
sir-network-epidemic-simulation/
├── src/
│   ├── data_loading.py      # Graf yükleme ve oluşturma
│   ├── centrality.py         # Merkeziyet hesaplamaları
│   ├── sir_simulation.py     # SIR modeli implementasyonu
│   ├── experiments.py        # Deney senaryoları ve çalıştırma
│   └── plots.py              # Statik grafik oluşturma
├── main.py                   # Komut satırı arayüzü (CLI)
├── gui.py                    # Streamlit web arayüzü (GUI)
├── requirements.txt          # Python bağımlılıkları
└── README.md                 # Dokümantasyon
```

**Görsel:** Modül bağımlılık diyagramı veya mimari şema

### SLIDE 9: Proje Mimarisi - Modül Detayları
**Başlık:** Her Modülün Sorumluluğu

**1. data_loading.py:**
- Edge list formatında graf dosyalarını yükler
- En büyük bağlı bileşeni çıkarır
- Watts-Strogatz, Barabási-Albert, Erdős-Rényi modelleri ile örnek ağlar oluşturur
- Önerilen sosyal ağ veri setlerini listeler

**2. centrality.py:**
- Dört farklı merkeziyet ölçüsünü hesaplar (NetworkX kullanarak)
- Her merkeziyet ölçüsüne göre en yüksek skorlu k node seçer
- Büyük ağlar için yaklaşık hesaplama seçenekleri sunar

**3. sir_simulation.py:**
- `SIRModel` sınıfı: Tek bir simülasyon çalıştırır
- Node durumlarını yönetir (S, I, R)
- Enfeksiyon geçmişini takip eder (hangi node'un hangi node'dan enfekte olduğu)
- `run_multiple_simulations`: Çoklu simülasyon çalıştırır
- `aggregate_simulation_results`: Sonuçları birleştirir ve istatistikler hesaplar

**4. experiments.py:**
- `ExperimentRunner` sınıfı: Tüm deney senaryolarını yönetir
- Her merkeziyet ölçüsü için simülasyon çalıştırır
- Rastgele baseline senaryosu çalıştırır
- Sonuçları karşılaştırır ve özetler

**5. plots.py:**
- Statik matplotlib grafikleri oluşturur
- Zaman serileri, karşılaştırma bar grafikleri, ağ snapshot'ları

**Görsel:** Her modülün input/output akışını gösteren diyagram

### SLIDE 10: Kullanıcı Arayüzleri
**Başlık:** İki Farklı Kullanım Yöntemi

**1. Komut Satırı Arayüzü (CLI) - main.py:**
- Etkileşimli mod: Kullanıcıya adım adım sorular sorar
- Komut satırı argümanları: Parametreleri doğrudan belirtme
- Demo modu: Hızlı test için önceden ayarlanmış parametreler
- Veri seti listeleme: Önerilen sosyal ağ veri setlerini gösterir

**Örnek Kullanım:**
```bash
python main.py --sample 200 --beta 0.3 --gamma 0.1 --k-initial 5 --n-runs 30
```

**2. Streamlit Web Arayüzü (GUI) - gui.py:**
Modern, interaktif web tabanlı arayüz:
- **5 Sekme:**
  1. Ağ Analizi: 2D/3D görselleştirme, merkeziyet skorları
  2. Simülasyon: Parametre ayarları, senaryo seçimi
  3. Sonuçlar: İnteraktif zaman serileri, karşılaştırma grafikleri
  4. Animasyon: Gerçek zamanlı simülasyon izleme
  5. Enfeksiyon Yolu: Enfeksiyon yayılım yolunu görselleştirme

**Görsel:** GUI ekran görüntüleri veya mockup'lar

### SLIDE 11: GUI Özellikleri - Detaylı
**Başlık:** İnteraktif Web Arayüzünün Güçlü Özellikleri

**Ağ Analizi Sekmesi:**
- 2D ve 3D ağ görselleştirme (Plotly)
- Merkeziyet skorları tablosu
- Node dereceleri histogramı
- Ağ istatistikleri (düğüm sayısı, kenar sayısı, ortalama derece, kümeleme katsayısı, çap)

**Simülasyon Sekmesi:**
- Parametre ayarları (slider'lar)
- Senaryo seçimi (Random, Degree, Betweenness, Closeness, Eigenvector)
- Simülasyon çalıştırma butonu
- Sonuç özeti tablosu

**Sonuçlar Sekmesi:**
- İnteraktif zaman serileri (Plotly - zoom, pan, hover)
- Karşılaştırma bar grafikleri (final outbreak size, peak infected, peak time)
- İstatistiksel özetler (ortalama, standart sapma)

**Animasyon Sekmesi:**
- Gerçek zamanlı 2D simülasyon animasyonu
- Hız kontrolü (slider)
- Play/Pause butonları
- Frame-by-frame ilerleme
- Büyük ağlar için 3D animasyon (opsiyonel)

**Enfeksiyon Yolu Sekmesi:**
- Enfeksiyon yayılım yolunu görselleştirme
- 2D ve 3D görünümler
- Renk kodlaması:
  - Koyu kırmızı: Başlangıç enfekte node'lar (Patient Zero)
  - Sarı: Sonradan enfekte olan node'lar
  - Mavi: Enfekte olmayan node'lar
  - Kırmızı kalın çizgiler: Enfeksiyon yolu kenarları

**Görsel:** Her sekmenin ekran görüntüleri

### SLIDE 12: Teknoloji Stack'i
**Başlık:** Kullanılan Teknolojiler ve Kütüphaneler

**Python Kütüphaneleri:**
- **networkx (3.4+)**: Graf işlemleri ve merkeziyet hesaplamaları
- **numpy (1.26+)**: Sayısal hesaplamalar
- **pandas (2.2+)**: Veri işleme
- **matplotlib (3.10+)**: Statik grafikler
- **seaborn (0.13+)**: Gelişmiş görselleştirme
- **streamlit (1.51+)**: Web arayüzü framework'ü
- **plotly (6.5+)**: İnteraktif görselleştirmeler
- **requests (2.32+)**: Veri seti indirme

**Görsel:** Teknoloji stack görselleştirmesi veya logo'lar

### SLIDE 13: Simülasyon Metrikleri
**Başlık:** Hangi Metrikleri Ölçüyoruz?

**1. Final Outbreak Size (Final Salgın Büyüklüğü):**
- Tanım: Toplam enfekte olmuş node sayısı (I + R durumunda)
- Önemi: Salgının ne kadar geniş yayıldığını gösterir
- Birim: Node sayısı

**2. Peak Infected (Maksimum Eşzamanlı Enfekte):**
- Tanım: Aynı anda enfekte olan maksimum node sayısı
- Önemi: Sağlık sisteminin karşılaşacağı maksimum yükü gösterir
- Birim: Node sayısı

**3. Peak Time (Peak Zamanı):**
- Tanım: Peak infected'e ulaşılan zaman adımı
- Önemi: Salgının ne kadar hızlı yayıldığını gösterir
- Birim: Zaman adımı

**4. Time Series (Zaman Serisi):**
- Tanım: Her zaman adımında S, I, R sayıları
- Önemi: Salgının dinamik gelişimini gösterir
- Görselleştirme: Çizgi grafikleri

**Görsel:** Her metriğin örnek grafikleri

### SLIDE 14: Deney Tasarımı
**Başlık:** Simülasyonlar Nasıl Çalıştırılıyor?

**Deney Akışı:**
1. Graf yükleme veya oluşturma
2. Merkeziyet ölçülerinin hesaplanması
3. Her strateji için:
   - Başlangıç enfekte node'ların seçilmesi
   - n_runs (varsayılan 30) kez simülasyon çalıştırma
   - Sonuçların birleştirilmesi ve istatistiklerin hesaplanması
4. Senaryoların karşılaştırılması

**Parametreler:**
- β (beta): Bulaşma olasılığı (varsayılan: 0.3)
- γ (gamma): İyileşme olasılığı (varsayılan: 0.1)
- k_initial: Başlangıç enfekte node sayısı (varsayılan: 5)
- n_runs: Her senaryo için tekrar sayısı (varsayılan: 30)

**Stokastik Süreç:**
- Her simülasyon rastgelelik içerir (bulaşma ve iyileşme olasılıkları)
- Çoklu tekrar ile istatistiksel güvenilirlik sağlanır
- Ortalama ve standart sapma hesaplanır

**Görsel:** Deney akış diyagramı

### SLIDE 15: Sonuçlar ve Bulgular - Genel Özet
**Başlık:** Hangi Strateji En Etkili?

**Genel Bulgular:**
- **Degree ve Betweenness** stratejileri → Daha büyük salgınlar üretir
- **Random** stratejisi → Baseline, en küçük etkiler
- **Yüksek β/γ oranı** → Daha geniş yayılım
- **Hub node'lardan başlamak** → Daha hızlı ve geniş yayılım

**Ağ Yapısına Göre Değişkenlik:**
- **Scale-free ağlarda** (sosyal ağlar): Degree stratejisi çok etkili
- **Düzenli ağlarda**: Tüm stratejiler benzer sonuçlar verebilir
- **Modüler ağlarda**: Betweenness stratejisi köprü node'ları yakalayabilir

**Görsel:** Senaryo karşılaştırma bar grafikleri

### SLIDE 16: Sonuçlar - Detaylı Analiz
**Başlık:** Senaryo Karşılaştırması

**Örnek Sonuçlar (200 node'lu Watts-Strogatz ağı, β=0.3, γ=0.1, k=5):**

| Senaryo | Final Outbreak | Peak Infected | Peak Time |
|---------|----------------|---------------|-----------|
| Random | 45.2 ± 8.3 | 12.5 ± 3.1 | 15.2 ± 4.5 |
| Degree | 78.5 ± 5.2 | 25.3 ± 2.8 | 8.5 ± 2.1 |
| Betweenness | 75.1 ± 6.1 | 23.8 ± 3.2 | 9.2 ± 2.5 |
| Closeness | 65.3 ± 7.2 | 18.9 ± 3.5 | 11.3 ± 3.1 |
| Eigenvector | 72.4 ± 5.8 | 22.1 ± 2.9 | 9.8 ± 2.3 |

**Yorumlar:**
- Degree stratejisi en büyük salgını üretir
- Betweenness stratejisi de benzer sonuçlar verir
- Random stratejisi en az etkilidir
- Closeness stratejisi orta düzeyde etkilidir

**Görsel:** Karşılaştırma bar grafikleri ve zaman serisi grafikleri

### SLIDE 17: Görselleştirmeler - Zaman Serileri
**Başlık:** Salgının Zamanla Gelişimi

**Görsel İçeriği:**
- Her senaryo için S, I, R sayılarının zamanla değişimi
- Farklı renkler ve çizgi stilleri ile senaryoların karşılaştırılması
- Peak noktalarının işaretlenmesi
- Ortalama değerler ve güven aralıkları (çoklu simülasyon için)

**Görsel:** Zaman serisi grafikleri (3 alt grafik: S, I, R)

### SLIDE 18: Görselleştirmeler - Ağ Durumu
**Başlık:** Ağ Üzerinde Enfeksiyon Yayılımı

**Görsel İçeriği:**
- Farklı zaman noktalarında ağ durumu snapshot'ları
- Renk kodlaması:
  - Mavi: Susceptible (S)
  - Kırmızı: Infected (I)
  - Yeşil: Recovered (R)
- Node boyutları: Merkeziyet skoruna göre
- Enfeksiyon yolu takibi: Hangi node'un hangi node'dan enfekte olduğu

**Görsel:** Ağ snapshot'ları (zaman serisi) ve enfeksiyon yolu görselleştirmesi

### SLIDE 19: Özel Özellikler
**Başlık:** Projenin Benzersiz Özellikleri

**1. Enfeksiyon Yolu Takibi:**
- Her node için, hangi node'dan enfekte olduğu ve hangi zaman adımında enfekte olduğu kaydedilir
- `infection_history` dictionary'si: `{node: (source_node, time_step)}`
- Görselleştirme: Enfeksiyon yolu kenarları kalın kırmızı çizgilerle gösterilir

**2. Patient Zero İşaretleme:**
- Başlangıç enfekte node'lar özel annotation ile işaretlenir
- Koyu kırmızı renk ve büyük boyut ile vurgulanır

**3. 3D Görselleştirme:**
- Node derecelerine göre Z ekseni yüksekliği
- İnteraktif rotasyon ve zoom
- Büyük ağlar için performans optimizasyonu

**4. İnteraktif Animasyon:**
- Gerçek zamanlı simülasyon izleme
- Hız kontrolü
- Play/Pause butonları
- Frame-by-frame ilerleme

**5. Multi-run Analizi:**
- Stokastik süreç için istatistiksel güvenilirlik
- Ortalama ve standart sapma hesaplamaları
- Güven aralıkları

**Görsel:** Her özelliğin ekran görüntüleri

### SLIDE 20: Performans Optimizasyonları
**Başlık:** Büyük Ağlar İçin Optimizasyonlar

**Yaklaşık Hesaplamalar:**
- Büyük ağlar (1000+ node) için betweenness centrality yaklaşık hesaplama (k-sample)
- Eigenvector centrality yakınsamazsa otomatik olarak degree centrality'ye fallback

**Performans İyileştirmeleri:**
- 3D animasyon büyük ağlar için otomatik devre dışı bırakılır
- Streamlit session state ile gereksiz hesaplamalar önlenir
- Plotly için optimize edilmiş node ve edge çizimi
- Layout hesaplamaları cache'lenir

**Ölçeklenebilirlik:**
- Küçük ağlar (<100 node): Tüm özellikler aktif
- Orta ağlar (100-500 node): Tüm özellikler aktif, bazı optimizasyonlar
- Büyük ağlar (500+ node): Yaklaşık hesaplamalar, bazı görselleştirmeler devre dışı

**Görsel:** Performans karşılaştırma grafikleri

### SLIDE 21: Kullanım Senaryoları
**Başlık:** Proje Nerede Kullanılabilir?

**1. Araştırma:**
- Farklı merkeziyet ölçülerinin salgın yayılımına etkisini incelemek
- Ağ topolojisinin salgın davranışına etkisini analiz etmek
- Yeni stratejiler geliştirmek ve test etmek

**2. Eğitim:**
- SIR modeli, merkeziyet ölçüleri ve ağ teorisi kavramlarını öğretmek
- İnteraktif görselleştirmeler ile öğrenmeyi kolaylaştırmak
- Öğrencilerin kendi deneylerini yapmasına olanak sağlamak

**3. Karşılaştırma:**
- Farklı ağ yapılarında (sosyal, biyolojik, teknolojik) salgın davranışını karşılaştırmak
- Gerçek dünya veri setleri ile çalışmak

**4. Görselleştirme:**
- Karmaşık ağ yapılarını görselleştirmek
- Dinamik süreçleri anlamak ve sunmak

**Görsel:** Her kullanım senaryosu için örnekler

### SLIDE 22: Gerçek Dünya Uygulamaları
**Başlık:** Pratik Değer

**1. Aşı Kampanyaları:**
- Hangi bireyleri öncelikli aşılamalıyız?
- Hub node'ları aşılamak salgını durdurabilir mi?

**2. Bilgi Yayılımı:**
- Viral içeriklerin sosyal medyada nasıl yayıldığını anlamak
- Etkili pazarlama stratejileri geliştirmek

**3. Virüs Koruma:**
- Bilgisayar ağlarında virüs yayılımını önlemek
- Kritik node'ları korumak

**4. Epidemiyoloji:**
- Gerçek salgınları modellemek
- Müdahale stratejilerini test etmek

**Görsel:** Gerçek dünya örnekleri ve uygulamaları

### SLIDE 23: Kod Kalitesi ve Best Practices
**Başlık:** Proje Standartları

**Kod Organizasyonu:**
- Modüler yapı: Her modül tek bir sorumluluğa sahip
- Temiz kod prensipleri: Okunabilir, bakımı kolay
- Dokümantasyon: Her fonksiyon ve sınıf için docstring'ler

**Python Best Practices:**
- Type hints kullanımı
- Error handling ve exception management
- Seed değerleri ile reproducible sonuçlar
- Configurable parametreler

**Görselleştirme Standartları:**
- Tutarlı renk şemaları
- Açıklayıcı başlıklar ve etiketler
- Legend'ler ve açıklamalar
- Yüksek çözünürlük (300 DPI)

**Görsel:** Kod örnekleri ve yapı diyagramları

### SLIDE 24: Sonuç ve Özet
**Başlık:** Proje Özeti

**Başarılar:**
- ✅ Kapsamlı bir SIR simülasyon sistemi geliştirildi
- ✅ Dört farklı merkeziyet ölçüsü karşılaştırıldı
- ✅ İki farklı kullanıcı arayüzü sunuldu (CLI ve GUI)
- ✅ İnteraktif görselleştirmeler eklendi
- ✅ Büyük ağlar için optimizasyonlar yapıldı

**Ana Bulgular:**
- Degree ve Betweenness stratejileri en etkilidir
- Ağ yapısı sonuçları etkiler
- Stratejik node seçimi kritik öneme sahiptir

**Görsel:** Proje özet görselleştirmesi

### SLIDE 25: Gelecek Çalışmalar
**Başlık:** Geliştirilebilecek Yönler

**1. Yeni Modeller:**
- SEIR modeli (Exposed durumu eklemek)
- SIS modeli (tekrar enfeksiyon)
- Age-structured modeller

**2. Yeni Merkeziyet Ölçüleri:**
- PageRank centrality
- Katz centrality
- Load centrality

**3. Gelişmiş Özellikler:**
- Gerçek zamanlı veri entegrasyonu
- Machine learning ile strateji optimizasyonu
- Paralel simülasyon desteği

**4. Arayüz İyileştirmeleri:**
- Daha fazla interaktivite
- Export özellikleri (PDF, CSV)
- Karşılaştırma raporları

**Görsel:** Gelecek çalışmalar roadmap'i

### SLIDE 26: Teşekkür ve Sorular
**Başlık:** Teşekkürler

**İçerik:**
- İzlediğiniz için teşekkürler
- Sorularınız için hazırım
- Proje kaynak koduna erişim bilgileri
- İletişim bilgileri

**Görsel:** Proje logosu veya görsel

---

## Görsel Gereksinimleri

### Grafikler ve Görselleştirmeler
1. **Ağ Görselleştirmeleri:**
   - 2D ve 3D ağ görselleştirmeleri
   - Farklı merkeziyet ölçülerine göre renklendirilmiş node'lar
   - Enfeksiyon yolu görselleştirmeleri
   - Ağ snapshot'ları (zaman serisi)

2. **İstatistiksel Grafikler:**
   - Zaman serisi grafikleri (S, I, R)
   - Karşılaştırma bar grafikleri
   - Scatter plot'lar
   - Histogram'lar

3. **Diyagramlar:**
   - SIR model durum geçiş diyagramı
   - Proje mimarisi diyagramı
   - Modül bağımlılık diyagramı
   - Deney akış diyagramı

4. **Ekran Görüntüleri:**
   - GUI ekran görüntüleri
   - CLI çıktıları
   - Animasyon frame'leri

### Görsel Stil Rehberi
- **Renkler:**
  - S (Susceptible): Mavi (#3498db)
  - I (Infected): Kırmızı (#e74c3c)
  - R (Recovered): Yeşil (#2ecc71)
  - Senaryo renkleri: Random (gri), Degree (kırmızı), Betweenness (mavi), Closeness (yeşil), Eigenvector (mor)

- **Tipografi:**
  - Başlıklar: Bold, büyük font
  - Alt başlıklar: Medium, orta font
  - Metin: Regular, okunabilir font

- **Layout:**
  - Temiz ve düzenli
  - Yeterli boşluk
  - Tutarlı hizalama

---

## Sunum Formatı Önerileri

### Slayt Sayısı
- Toplam: 26 slayt
- Sunum süresi: 15-20 dakika (yaklaşık 1 dakika/slayt)

### Slayt Tasarımı
- Modern ve profesyonel görünüm
- Tutarlı tema ve renk şeması
- Yeterli kontrast (okunabilirlik)
- Görseller ve metin dengesi

### İçerik Dengesi
- Teknik detaylar ve görsel açıklamalar dengeli
- Her slayt tek bir ana konuya odaklanmalı
- Bullet point'ler kısa ve öz olmalı
- Görseller destekleyici olmalı, ana içerik olmamalı

---

## Özel Notlar

1. **Akademik Ton:**
   - Profesyonel ve akademik bir dil kullanılmalı
   - Teknik terimler doğru kullanılmalı
   - Referanslar ve kaynaklar belirtilmeli (eğer varsa)

2. **Görsel Zenginlik:**
   - Her slayt mümkünse en az bir görsel içermeli
   - Görseller açıklayıcı ve ilgi çekici olmalı
   - Animasyonlar ve geçişler dikkatli kullanılmalı

3. **Hikaye Anlatımı:**
   - Sunum bir hikaye gibi akmalı
   - Her slayt bir öncekiyle bağlantılı olmalı
   - Sonuç ve özet net olmalı

4. **İzleyici Odaklı:**
   - Teknik detaylar ve genel bakış dengeli olmalı
   - İzleyicinin seviyesine uygun açıklamalar yapılmalı
   - Pratik değer vurgulanmalı

---

## Ek Talimatlar

- Bu prompt, AI agent'a proje hakkında kapsamlı bilgi sağlamalıdır
- AI agent, bu bilgileri kullanarak profesyonel bir slideshow oluşturmalıdır
- Slaytlar hem teknik hem de görsel açıdan zengin olmalıdır
- Sunum, projenin değerini ve önemini net bir şekilde aktarmalıdır
- Her slayt için önerilen içerik ve görsel türleri belirtilmiştir
- AI agent, bu önerileri takip ederek tutarlı ve profesyonel bir sunum oluşturmalıdır

