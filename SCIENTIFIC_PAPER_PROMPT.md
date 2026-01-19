# Scientific Paper Writing Prompt - SIR Network Epidemic Simulation

## GÖREV: Bilimsel Makale Yazımı

Bu prompt, SIR Network Epidemic Simulation projesi hakkında akademik dergi kalitesinde, bilimsel bir makale yazmak için tasarlanmıştır. Makale, graf algoritmaları, ağ teorisi ve epidemiyoloji disiplinlerini birleştiren çok disiplinli bir çalışma olmalıdır.

---

## MAKALE YAPISI VE GEREKSİNİMLERİ

### 1. TITLE (Başlık)
**Gereksinimler:**
- Kısa, öz ve açıklayıcı (maksimum 15 kelime)
- Anahtar kelimeleri içermeli
- Çalışmanın özünü yansıtmalı

**Örnek Format:**
"Impact of Centrality Measures on Epidemic Spread: A Comparative Analysis of SIR Model on Social Networks"

**İçermesi Gerekenler:**
- Ana konu (Centrality Measures)
- Metodoloji (SIR Model)
- Bağlam (Social Networks)
- Yaklaşım (Comparative Analysis)

### 2. ABSTRACT (Özet)
**Uzunluk:** 200-300 kelime

**Bölümler:**
1. **Background (Arka Plan):** 2-3 cümle
   - Epidemik yayılımın önemi
   - Ağ teorisi bağlamı
   - Merkeziyet ölçülerinin rolü

2. **Objective (Amaç):** 1-2 cümle
   - Araştırma sorusu
   - Çalışmanın amacı

3. **Methods (Metodoloji):** 3-4 cümle
   - SIR modeli kullanımı
   - Test edilen merkeziyet ölçüleri
   - Deney tasarımı
   - Veri setleri

4. **Results (Sonuçlar):** 2-3 cümle
   - Ana bulgular
   - En etkili stratejiler
   - İstatistiksel sonuçlar

5. **Conclusion (Sonuç):** 1-2 cümle
   - Çalışmanın katkısı
   - Pratik çıkarımlar
   - Gelecek çalışmalar

**Anahtar Kelimeler:** 5-7 anahtar kelime
- Network analysis
- Epidemic modeling
- Centrality measures
- SIR model
- Social networks
- Graph algorithms

### 3. INTRODUCTION (Giriş)
**Uzunluk:** 800-1200 kelime

**Yapı:**

**3.1. Background and Motivation (Arka Plan ve Motivasyon)**
- Epidemik hastalıkların sosyal ve ekonomik etkileri
- Ağ teorisi ve epidemiyoloji kesişimi
- Salgın kontrolünde stratejik node seçiminin önemi
- Gerçek dünya uygulamaları (aşı kampanyaları, bilgi yayılımı)

**3.2. Problem Statement (Problem Tanımı)**
- Mevcut çalışmalardaki boşluklar
- Merkeziyet ölçülerinin karşılaştırmalı analizinin eksikliği
- Pratik uygulamalarda hangi stratejinin en etkili olduğu sorusu

**3.3. Research Questions (Araştırma Soruları)**
1. Farklı merkeziyet ölçülerine göre seçilen başlangıç enfekte node'ları, salgının yayılımını nasıl etkiler?
2. Hangi merkeziyet ölçüsü en geniş ve en hızlı salgını üretir?
3. Ağ topolojisinin (scale-free, small-world, modular) sonuçlara etkisi nedir?
4. Stratejik node seçimi, rastgele seçime göre ne kadar daha etkilidir?

**3.4. Contributions (Katkılar)**
- Dört farklı merkeziyet ölçüsünün sistematik karşılaştırması
- Farklı ağ topolojilerinde kapsamlı deneysel analiz
- Açık kaynak kodlu, tekrarlanabilir simülasyon platformu
- Pratik uygulamalar için öneriler

**3.5. Paper Organization (Makale Organizasyonu)**
- Bölümlerin kısa özeti

### 4. RELATED WORK (İlgili Çalışmalar)
**Uzunluk:** 1000-1500 kelime

**Alt Bölümler:**

**4.1. Epidemic Models on Networks**
- Kermack-McKendrick SIR modeli (klasik)
- Ağ üzerinde SIR modelleri
- Compartmental modeller (SEIR, SIS, vb.)
- Stokastik vs deterministik modeller

**4.2. Centrality Measures in Network Analysis**
- Degree centrality (Freeman, 1979)
- Betweenness centrality (Freeman, 1977)
- Closeness centrality (Sabidussi, 1966)
- Eigenvector centrality (Bonacich, 1972)
- PageRank ve modern ölçüler

**4.3. Influence Maximization and Seed Selection**
- Influence maximization problem (Kempe et al., 2003)
- Greedy algoritmalar
- Heuristic yaklaşımlar
- Merkeziyet tabanlı seed seçimi

**4.4. Network Topology and Epidemic Spread**
- Scale-free ağlar ve hub node'ların rolü
- Small-world ağlar ve küçük mesafe etkisi
- Modüler ağlar ve köprü node'lar
- Topoloji-epidemik ilişkisi

**4.5. Gap Analysis (Boşluk Analizi)**
- Mevcut çalışmalardaki eksiklikler
- Bu çalışmanın nasıl katkı sağladığı

**Referans Formatı:**
- En az 30-40 referans
- Son 10 yılın çalışmalarına ağırlık
- Klasik ve temel çalışmalar dahil
- Dergi makaleleri, konferans bildirileri, kitaplar

### 5. METHODOLOGY (Metodoloji)
**Uzunluk:** 1500-2000 kelime

**Alt Bölümler:**

**5.1. SIR Model Formulation (SIR Modeli Formülasyonu)**

**5.1.1. Model Description**
- Discrete-time SIR modeli
- Durum geçişleri: S → I → R
- Stokastik dinamikler
- Matematiksel formülasyon:
  ```
  P(S→I) = β * (number of infected neighbors)
  P(I→R) = γ
  ```

**5.1.2. Parameters**
- β (beta): Bulaşma olasılığı [0,1]
- γ (gamma): İyileşme olasılığı [0,1]
- R₀ = β/γ: Temel üreme sayısı
- k_initial: Başlangıç enfekte node sayısı

**5.1.3. Simulation Dynamics**
- Her zaman adımında:
  1. Infection phase: Enfekte node'lar komşularını enfekte eder
  2. Recovery phase: Enfekte node'lar iyileşir
- Simülasyon sonu: I = 0 veya max_steps

**5.2. Centrality Measures (Merkeziyet Ölçüleri)**

**5.2.1. Degree Centrality**
- Tanım ve formül
- Hesaplama karmaşıklığı: O(n)
- Mantık: Yerel bağlantı sayısı

**5.2.2. Betweenness Centrality**
- Tanım ve formül (Brandes algoritması)
- Hesaplama karmaşıklığı: O(nm) veya O(n²)
- Yaklaşık hesaplama (k-sample) büyük ağlar için
- Mantık: Köprü node'ları belirleme

**5.2.3. Closeness Centrality**
- Tanım ve formül
- Hesaplama karmaşıklığı: O(n²)
- Mantık: Merkeze yakınlık

**5.2.4. Eigenvector Centrality**
- Tanım ve formül (Power iteration)
- Hesaplama karmaşıklığı: O(n²) iteratif
- Yakınsama sorunları ve fallback mekanizması
- Mantık: Önemli node'lara bağlılık

**5.2.5. Random Selection (Baseline)**
- Rastgele k node seçimi
- Her simülasyon için farklı seed

**5.3. Experimental Design (Deneysel Tasarım)**

**5.3.1. Network Datasets**
- Watts-Strogatz (Small World): n=200, k=6, p=0.1
- Barabási-Albert (Scale Free): n=200, m=3
- Erdős-Rényi (Random): n=200, p=0.05
- Karate Club: 34 nodes (gerçek veri)
- Les Misérables: 77 nodes (gerçek veri)

**5.3.2. Parameter Settings**
- β ∈ {0.2, 0.3, 0.4, 0.5}
- γ ∈ {0.05, 0.1, 0.15, 0.2}
- k_initial ∈ {3, 5, 7, 10}
- n_runs = 30 (her senaryo için)

**5.3.3. Evaluation Metrics**
1. **Final Outbreak Size**: Toplam enfekte node sayısı (I + R)
2. **Peak Infected**: Maksimum eşzamanlı enfekte node sayısı
3. **Peak Time**: Peak infected'e ulaşılan zaman adımı
4. **Time to Extinction**: Son enfekte node'un iyileşme zamanı
5. **Infection Rate**: Ortalama enfeksiyon hızı

**5.3.4. Statistical Analysis**
- Ortalama ve standart sapma (30 tekrar)
- Güven aralıkları (95% CI)
- İstatistiksel testler:
  - ANOVA (scenario comparison)
  - Post-hoc tests (Tukey HSD)
  - Effect size (Cohen's d)
- Normallik testleri (Shapiro-Wilk)
- Varyans homojenliği (Levene's test)

**5.4. Implementation Details (İmplementasyon Detayları)**
- Programlama dili: Python 3.11
- Ana kütüphaneler: NetworkX, NumPy, Streamlit, Plotly
- Modüler mimari
- Reproducibility: Seed değerleri (42)
- Kod erişilebilirliği: GitHub repository

### 6. RESULTS (Sonuçlar)
**Uzunluk:** 2000-2500 kelime

**Alt Bölümler:**

**6.1. Overall Performance Comparison (Genel Performans Karşılaştırması)**

**6.1.1. Final Outbreak Size**
- Senaryolar arası karşılaştırma tablosu
- Bar grafikleri (hata çubukları ile)
- İstatistiksel anlamlılık testleri
- Bulgular:
  - Degree ve Betweenness en yüksek salgınları üretir
  - Random en düşük salgınları üretir
  - Closeness ve Eigenvector orta düzeyde

**6.1.2. Peak Infected**
- Senaryolar arası karşılaştırma
- Zaman serisi grafikleri
- Peak zamanları
- Bulgular:
  - Degree stratejisi en yüksek peak'i üretir
  - Hızlı yayılım gözlemlenir

**6.1.3. Peak Time**
- Senaryolar arası karşılaştırma
- Hız analizi
- Bulgular:
  - Degree ve Betweenness en hızlı yayılım
  - Random en yavaş yayılım

**6.2. Network Topology Effects (Ağ Topolojisi Etkileri)**

**6.2.1. Scale-free Networks**
- Degree stratejisi çok etkili
- Hub node'ların kritik rolü
- Power-law dağılımının etkisi

**6.2.2. Small-world Networks**
- Tüm stratejiler benzer sonuçlar
- Küçük ortalama mesafe
- Yüksek kümeleme katsayısı

**6.2.3. Modular Networks**
- Betweenness stratejisi köprü node'ları yakalar
- Topluluklar arası geçişler kritik
- Modülerlik skorunun etkisi

**6.3. Parameter Sensitivity Analysis (Parametre Duyarlılık Analizi)**

**6.3.1. Beta (β) Effects**
- Yüksek β: Daha geniş yayılım
- Düşük β: Sınırlı yayılım veya sönme
- R₀ > 1 kritik eşik

**6.3.2. Gamma (γ) Effects**
- Yüksek γ: Hızlı iyileşme, kısa süreli salgın
- Düşük γ: Yavaş iyileşme, uzun süreli salgın

**6.3.3. Initial Infected Count (k_initial)**
- Daha fazla başlangıç enfekte = daha geniş salgın
- Ancak stratejik seçim daha önemli
- Diminishing returns gözlemlenir

**6.4. Statistical Significance (İstatistiksel Anlamlılık)**

**6.4.1. ANOVA Results**
- Senaryolar arası fark anlamlı mı?
- F-statistic ve p-value
- Effect size

**6.4.2. Post-hoc Tests**
- Hangi senaryolar arasında anlamlı fark var?
- Tukey HSD sonuçları
- Çoklu karşılaştırma düzeltmesi

**6.5. Case Studies (Vaka Çalışmaları)**

**6.5.1. Karate Club Network**
- Küçük gerçek dünya ağı
- Senaryoların detaylı analizi
- Enfeksiyon yolu görselleştirmesi

**6.5.2. Large Synthetic Network**
- 200 node'lu Watts-Strogatz ağı
- Ölçeklenebilirlik analizi
- Performans metrikleri

**6.6. Visualization Results (Görselleştirme Sonuçları)**
- Zaman serisi grafikleri
- Ağ görselleştirmeleri
- Enfeksiyon yolu animasyonları
- Karşılaştırma grafikleri

### 7. DISCUSSION (Tartışma)
**Uzunluk:** 1500-2000 kelime

**Alt Bölümler:**

**7.1. Interpretation of Results (Sonuçların Yorumlanması)**
- Ana bulguların anlamı
- Neden Degree ve Betweenness en etkili?
- Hub node'ların kritik rolü
- Köprü node'ların önemi

**7.2. Comparison with Related Work (İlgili Çalışmalarla Karşılaştırma)**
- Literatürdeki benzer çalışmalarla karşılaştırma
- Tutarlılık ve farklılıklar
- Bu çalışmanın katkısı

**7.3. Practical Implications (Pratik Çıkarımlar)**
- Aşı kampanyaları için öneriler
- Bilgi yayılımı stratejileri
- Virüs koruma politikaları
- Influence maximization uygulamaları

**7.4. Limitations (Sınırlamalar)**
- Model sınırlamaları (SIR modeli basitleştirmeleri)
- Ağ veri setleri (sentetik vs gerçek)
- Hesaplama karmaşıklığı (büyük ağlar)
- Parametre seçimi (β, γ değerleri)

**7.5. Future Work (Gelecek Çalışmalar)**
- SEIR, SIS gibi diğer modeller
- Yeni merkeziyet ölçüleri (PageRank, Katz)
- Gerçek dünya veri setleri ile çalışma
- Machine learning ile strateji optimizasyonu
- Temporal ağlar (zamanla değişen ağlar)
- Age-structured modeller

### 8. CONCLUSION (Sonuç)
**Uzunluk:** 300-500 kelime

**İçerik:**
- Çalışmanın özeti
- Ana bulguların vurgulanması
- Çalışmanın katkısı
- Pratik öneriler
- Gelecek çalışmalar için yönlendirme

### 9. REFERENCES (Referanslar)
**Format:** IEEE veya ACM formatı (dergiye göre)

**Örnek Formatlar:**

**IEEE:**
```
[1] D. J. Watts and S. H. Strogatz, "Collective dynamics of 'small-world' networks," Nature, vol. 393, no. 6684, pp. 440-442, 1998.
```

**ACM:**
```
[1] Watts, D. J. and Strogatz, S. H. 1998. Collective dynamics of 'small-world' networks. Nature 393, 6684 (1998), 440-442.
```

**Gerekli Referans Kategorileri:**
- Klasik SIR modeli çalışmaları (Kermack-McKendrick)
- Merkeziyet ölçüleri temel çalışmaları (Freeman, Bonacich)
- Ağ teorisi temel çalışmaları (Watts-Strogatz, Barabási-Albert)
- Influence maximization çalışmaları (Kempe et al.)
- Son 10 yılın epidemik modelleme çalışmaları
- Network epidemiology çalışmaları

**Minimum Referans Sayısı:** 30-40

### 10. APPENDICES (Ekler) - Opsiyonel
- Detaylı algoritma pseudocode'ları
- Ek grafikler ve tablolar
- Kod snippet'leri
- Ek istatistiksel analizler

---

## BİLİMSEL YAZIM KURALLARI

### Dil ve Stil
- **Dil:** İngilizce (veya Türkçe, dergiye göre)
- **Ton:** Objektif, akademik, formal
- **Kişi:** Üçüncü tekil şahıs ("we", "our study" kabul edilebilir)
- **Zaman:** Geniş zaman (present tense) metodoloji ve sonuçlar için
- **Pasif/aktif:** Dengeli kullanım

### Terminoloji
- Teknik terimler ilk kullanımda açıklanmalı
- Kısaltmalar ilk kullanımda açılmalı (örn: SIR (Susceptible-Infected-Recovered))
- Tutarlı terminoloji kullanımı
- Standart notasyon (β, γ, R₀)

### Grafikler ve Tablolar
- **Grafikler:**
  - Yüksek çözünürlük (300 DPI minimum)
  - Açıklayıcı başlıklar
  - Eksen etiketleri ve birimler
  - Legend'ler
  - Hata çubukları (standart sapma veya güven aralığı)
  - Caption'lar (alt yazılar)

- **Tablolar:**
  - Açıklayıcı başlıklar
  - Sütun ve satır başlıkları
  - İstatistiksel değerler (ortalama ± standart sapma)
  - Caption'lar
  - Notlar (gerekirse)

### İstatistiksel Sunum
- Ortalama ± Standart Sapma formatı
- Güven aralıkları: [lower, upper] veya mean (95% CI: lower-upper)
- P-değerleri: p < 0.001, p = 0.023, vb.
- Effect size: Cohen's d, η², vb.
- İstatistiksel testler açıkça belirtilmeli

### Referans Stili
- Tutarlı referans formatı (IEEE, ACM, APA, vb.)
- In-text citations: (Author, Year) veya [1]
- Referans listesi alfabetik veya numaralı
- DOI'ler dahil edilmeli

---

## DENEY TASARIMI DETAYLARI

### Kontrol Değişkenleri
- Ağ boyutu (n)
- Ağ topolojisi
- Seed değerleri (reproducibility)

### Bağımsız Değişkenler
- Merkeziyet ölçüsü stratejisi (5 seviye)
- β değeri (4 seviye)
- γ değeri (4 seviye)
- k_initial (4 seviye)

### Bağımlı Değişkenler
- Final Outbreak Size
- Peak Infected
- Peak Time
- Time to Extinction
- Infection Rate

### Deneysel Tasarım
- Factorial design (tüm kombinasyonlar)
- Her kombinasyon için 30 tekrar
- Toplam simülasyon sayısı: 5 × 4 × 4 × 4 × 30 = 9,600 simülasyon

### İstatistiksel Analiz Planı
1. **Descriptive Statistics:**
   - Ortalama, medyan, standart sapma
   - Min, max, quartiles
   - Box plots

2. **Inferential Statistics:**
   - Normallik testleri (Shapiro-Wilk)
   - Varyans homojenliği (Levene's test)
   - ANOVA (scenario comparison)
   - Post-hoc tests (Tukey HSD)
   - Effect size hesaplamaları

3. **Effect Size:**
   - Cohen's d (iki grup karşılaştırması)
   - η² (ANOVA için)
   - Practical significance

### Reproducibility (Tekrarlanabilirlik)
- Seed değerleri: 42 (base seed)
- Her simülasyon için farklı seed: base_seed + run_number
- Kod ve veri erişilebilirliği
- Detaylı metodoloji açıklaması

---

## HİPOTEZLER

### Ana Hipotezler

**H1:** Degree ve Betweenness merkeziyet ölçülerine göre seçilen başlangıç enfekte node'ları, rastgele seçime göre daha geniş salgınlar üretir.

**H2:** Scale-free ağlarda Degree stratejisi, diğer stratejilere göre daha etkilidir.

**H3:** Modüler ağlarda Betweenness stratejisi, köprü node'ları yakaladığı için daha etkilidir.

**H4:** Stratejik node seçimi, β/γ oranı yüksek olduğunda daha belirgin bir avantaj sağlar.

### Null Hipotezler

**H0:** Senaryolar arasında final outbreak size açısından anlamlı bir fark yoktur.

**H0:** Ağ topolojisi, merkeziyet ölçülerinin etkinliğini etkilemez.

---

## SONUÇ SUNUMU FORMATI

### Tablolar

**Tablo 1: Senaryo Karşılaştırması (Final Outbreak Size)**
```
| Strategy      | Mean ± SD    | 95% CI          | p-value |
|---------------|--------------|-----------------|---------|
| Random        | 45.2 ± 8.3   | [42.1, 48.3]    | -       |
| Degree        | 78.5 ± 5.2   | [76.6, 80.4]    | <0.001  |
| Betweenness   | 75.1 ± 6.1   | [72.9, 77.3]    | <0.001  |
| Closeness     | 65.3 ± 7.2   | [62.7, 67.9]    | <0.001  |
| Eigenvector   | 72.4 ± 5.8   | [70.3, 74.5]    | <0.001  |
```

### Grafikler

**Figure 1: Zaman Serisi Karşılaştırması**
- X-axis: Time steps
- Y-axis: Node count
- Multiple lines: Her senaryo için
- Legend: Senaryo isimleri
- Caption: "Comparison of S, I, R counts over time for different centrality-based seed selection strategies on a Watts-Strogatz network (n=200, β=0.3, γ=0.1)."

**Figure 2: Senaryo Karşılaştırma Bar Grafikleri**
- Three subplots: Final Outbreak Size, Peak Infected, Peak Time
- Error bars: Standard deviation
- Caption: "Comparison of epidemic metrics across different seed selection strategies. Error bars represent standard deviation over 30 simulation runs."

**Figure 3: Ağ Topolojisi Etkisi**
- Multiple panels: Farklı ağ tipleri
- Heatmap veya grouped bar chart
- Caption: "Effect of network topology on strategy effectiveness. Results shown for scale-free, small-world, and modular networks."

---

## LİTERATÜR TARAMASI YÖNLENDİRMESİ

### Önemli Dergiler
- **Network Science:** Network analysis ve epidemik modeller
- **Journal of Complex Networks:** Ağ teorisi ve uygulamaları
- **PLOS ONE:** Epidemiyoloji ve ağ modelleri
- **Physical Review E:** Fiziksel ağlar ve epidemik süreçler
- **IEEE Transactions on Network Science and Engineering:** Network science

### Önemli Konferanslar
- **NetSci:** Network Science Conference
- **ASONAM:** Advances in Social Networks Analysis and Mining
- **WWW:** World Wide Web Conference

### Temel Kitaplar
- "Networks: An Introduction" - Mark Newman
- "Network Science" - Albert-László Barabási
- "Epidemic Modelling" - D. J. Daley & J. Gani

### Önemli Çalışmalar
- Kermack & McKendrick (1927): Klasik SIR modeli
- Watts & Strogatz (1998): Small-world networks
- Barabási & Albert (1999): Scale-free networks
- Kempe et al. (2003): Influence maximization
- Pastor-Satorras & Vespignani (2001): Epidemics on scale-free networks

---

## MAKALE YAZIMI İÇİN EK TALİMATLAR

### 1. Giriş Bölümü
- Hook: İlgi çekici bir açılış
- Problem tanımı: Net ve açık
- Araştırma soruları: Spesifik ve ölçülebilir
- Katkılar: Net ve belirgin

### 2. Metodoloji Bölümü
- Detaylı: Başka biri tekrarlayabilmeli
- Matematiksel formüller: Doğru ve tutarlı
- Algoritmalar: Pseudocode veya açıklama
- Parametreler: Tüm değerler belirtilmeli

### 3. Sonuçlar Bölümü
- Objektif: Yorum yapmadan sun
- İstatistiksel: Sayısal sonuçlar
- Görsel: Grafikler ve tablolar
- Kapsamlı: Tüm deneyler dahil

### 4. Tartışma Bölümü
- Yorum: Sonuçların anlamı
- Karşılaştırma: Literatürle ilişki
- Sınırlamalar: Dürüst ve açık
- Gelecek çalışmalar: Spesifik ve uygulanabilir

### 5. Genel Notlar
- Tutarlılık: Terminoloji ve notasyon
- Netlik: Açık ve anlaşılır
- Kısalık: Gereksiz tekrarlardan kaçın
- Doğruluk: Tüm bilgiler doğru olmalı

---

## KALİTE KONTROL KONTROL LİSTESİ

### İçerik
- [ ] Tüm bölümler mevcut ve tamamlanmış
- [ ] Araştırma soruları net ve ölçülebilir
- [ ] Metodoloji detaylı ve tekrarlanabilir
- [ ] Sonuçlar objektif ve kapsamlı
- [ ] Tartışma derinlemesine ve dengeli
- [ ] Referanslar yeterli ve güncel

### Format
- [ ] Tutarlı referans formatı
- [ ] Grafikler ve tablolar profesyonel
- [ ] Caption'lar mevcut ve açıklayıcı
- [ ] İstatistiksel sunum doğru
- [ ] Terminoloji tutarlı

### Dil
- [ ] Akademik İngilizce (veya Türkçe)
- [ ] Gramer hataları yok
- [ ] Akıcı ve okunabilir
- [ ] Teknik terimler doğru kullanılmış

### Bilimsel Rigor
- [ ] İstatistiksel testler uygun
- [ ] Effect size hesaplanmış
- [ ] Sınırlamalar açıkça belirtilmiş
- [ ] Reproducibility sağlanmış
- [ ] Etik kurallara uygun

---

## SONUÇ

Bu prompt, SIR Network Epidemic Simulation projesi hakkında akademik dergi kalitesinde bir makale yazmak için gerekli tüm yönlendirmeleri içermektedir. Prompt'u kullanarak:

1. **Yapılandırılmış bir makale** yazabilirsiniz
2. **Bilimsel standartlara uygun** içerik üretebilirsiniz
3. **İstatistiksel analiz** gereksinimlerini karşılayabilirsiniz
4. **Literatür taraması** yapabilirsiniz
5. **Profesyonel görselleştirmeler** oluşturabilirsiniz

**Önemli:** Bu prompt, teknik proje bilgilerini (`PROJECT_COMPLETE_PROMPT.md`) bilimsel makale yazım gereksinimleriyle birleştirir. Her iki prompt'u birlikte kullanarak en iyi sonucu alabilirsiniz.

**Kullanım Önerisi:**
1. `PROJECT_COMPLETE_PROMPT.md` - Teknik detaylar için
2. `SCIENTIFIC_PAPER_PROMPT.md` - Makale yapısı ve yazım kuralları için
3. İkisini birlikte AI'a vererek kapsamlı bir makale yazdırın
