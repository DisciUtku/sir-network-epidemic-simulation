# SIR Model Simülasyonu - Merkeziyet Ölçüleri ile Hastalık Yayılımı

Bu proje, sosyal ağlarda SIR (Susceptible-Infected-Recovered) modeli kullanarak hastalık yayılımını simüle ediyor. Farklı merkeziyet ölçülerine göre seçilen başlangıç node'larının salgın üzerindeki etkisini karşılaştırıyor.

## Ne Yapıyor?

Temel soru şu: Bir ağda hastalığı ilk başta hangi node'lara bulaştırırsak daha geniş yayılır? Rastgele mi, yoksa en çok bağlantıya sahip olanlara mı?

Proje şu merkeziyet ölçülerini test ediyor:
- **Degree**: En çok bağlantıya sahip node'lar
- **Betweenness**: Ağda köprü görevi gören node'lar
- **Closeness**: Diğer node'lara en yakın olanlar
- **Eigenvector**: Önemli node'lara bağlı olanlar

Her stratejiyi birkaç kez çalıştırıp sonuçları karşılaştırıyor.

## Kurulum

Python 3.8+ gerekiyor. Bağımlılıkları yüklemek için:

```bash
pip install -r requirements.txt
```

Gerekli paketler: networkx, matplotlib, seaborn, numpy, pandas, streamlit, plotly

## Kullanım

### GUI ile (Önerilen)

```bash
streamlit run gui.py
```

Windows'ta `start_gui.bat` dosyasını çalıştırabilirsiniz.

GUI'da şunlar var:
- Ağ görselleştirme (2D ve 3D)
- Merkeziyet analizi
- Simülasyon çalıştırma
- Sonuçları görüntüleme
- Animasyon izleme
- Enfeksiyon yolu takibi

Tarayıcıda `http://localhost:8501` adresinde açılır.

### Komut Satırı ile

Hızlı test için:
```bash
python main.py --demo
```

Kendi parametrelerinizle:
```bash
python main.py --sample 200 --beta 0.3 --gamma 0.1 --k-initial 5 --n-runs 30 --output results
```

Kendi veri setinizle:
```bash
python main.py --input data/network.edges --beta 0.3 --gamma 0.1 --k-initial 10 --n-runs 30 --output results
```

## SIR Modeli

SIR modeli her node'u üç durumdan birine koyar:
- **S (Susceptible)**: Henüz enfekte değil, enfekte olabilir
- **I (Infected)**: Enfekte, hastalığı yayabilir
- **R (Recovered)**: İyileşmiş, artık enfekte olamaz

Her adımda:
1. Enfekte bir node, komşularını `beta` olasılığı ile enfekte eder
2. Enfekte bir node, `gamma` olasılığı ile iyileşir

**Beta**: Bulaşma olasılığı (0-1 arası, yüksek = hızlı yayılma)
**Gamma**: İyileşme olasılığı (0-1 arası, yüksek = hızlı iyileşme)

R₀ = beta/gamma değeri 1'den büyükse salgın yayılır, küçükse söner.

## Senaryolar

Program şu stratejileri test eder:
1. **Random**: Rastgele k node seçimi (baseline)
2. **Degree**: En yüksek dereceye sahip k node
3. **Betweenness**: En yüksek betweenness'e sahip k node
4. **Closeness**: En yüksek closeness'e sahip k node
5. **Eigenvector**: En yüksek eigenvector centrality'ye sahip k node

Her senaryo varsayılan olarak 30 kez tekrarlanır ve ortalama sonuçlar alınır.

## Çıktılar

CLI modunda üç tür grafik oluşturulur:
- Zaman serileri (S, I, R sayılarının değişimi)
- Karşılaştırma grafikleri (final enfekte sayısı, peak enfekte, peak zamanı)
- Ağ snapshot'ları (küçük ağlar için)

GUI'da bunlar interaktif olarak görüntülenir. Ayrıca 3D görselleştirme ve enfeksiyon yolu takibi var.

## Veri Formatı

Program edge list formatında dosyaları okur:
```
node1 node2
node3 node4
...
```

Boşluk, tab veya virgül ile ayrılmış olabilir. Yorumlar # ile başlar.

## Proje Yapısı

```
sir-network-epidemic-simulation/
├── src/
│   ├── data_loading.py      # Graf yükleme
│   ├── centrality.py         # Merkeziyet hesaplamaları
│   ├── sir_simulation.py     # SIR modeli
│   ├── experiments.py        # Senaryo çalıştırma
│   └── plots.py              # Grafik oluşturma
├── main.py                   # CLI arayüzü
├── gui.py                    # Streamlit GUI
├── requirements.txt
└── README.md
```

## Özellikler

- 2D ve 3D ağ görselleştirme
- İnteraktif simülasyon animasyonu
- Enfeksiyon yolu takibi (hangi node'un hangi node'dan enfekte olduğu)
- Patient Zero işaretleme
- Farklı merkeziyet ölçülerinin karşılaştırılması

## Deployment

### Streamlit Cloud (Önerilen)

Uygulamayı ücretsiz olarak Streamlit Cloud'a deploy edebilirsiniz:

1. **GitHub'a yükleyin:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/KULLANICI_ADI/REPO_ADI.git
git push -u origin main
```

2. **Streamlit Cloud'a kayıt olun:**
   - [share.streamlit.io](https://share.streamlit.io) adresine gidin
   - GitHub hesabınızla giriş yapın

3. **Deploy edin:**
   - "New app" > Repository seçin > Branch: `main` > Main file: `gui.py` > Deploy!

**Detaylı deployment rehberi için:** `DEPLOY_README.md` dosyasına bakın.

### Diğer Platformlar

- **Railway**: `railway.json` dosyası ile otomatik deploy
- **Render**: `render.yaml` dosyası ile otomatik deploy
- **Docker**: `Dockerfile` ile herhangi bir platforma deploy

## Notlar

- Büyük ağlarda (200+ node) 3D animasyon yavaş olabilir, bu yüzden devre dışı bırakılmıştır
- Betweenness centrality büyük ağlarda yaklaşık hesaplama kullanır
- Eigenvector centrality yakınsamazsa otomatik olarak degree centrality'ye geçer

## Lisans

MIT License - Detaylar için LICENSE dosyasına bakın.
