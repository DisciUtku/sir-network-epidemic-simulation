# Deployment Rehberi - SIR Network Epidemic Simulation

## ⚠️ ÖNEMLİ NOT: Vercel ve Streamlit

**Vercel Streamlit uygulamalarını doğrudan desteklemez.** Vercel, Next.js, React gibi frontend framework'leri için optimize edilmiştir ve Streamlit gibi Python web framework'lerini desteklemez.

### Alternatif Çözümler:

1. **Streamlit Cloud** (Önerilen - En Kolay) ✅
2. **Heroku** (Ücretli planlar mevcut)
3. **Railway** (Kolay ve ücretsiz tier)
4. **Render** (Ücretsiz tier mevcut)
5. **Docker + Herhangi bir Cloud Provider**

---

## Seçenek 1: Streamlit Cloud'a Deploy (ÖNERİLEN)

Streamlit Cloud, Streamlit uygulamaları için özel olarak tasarlanmış ve **tamamen ücretsiz** bir platformdur.

### Adım 1: GitHub Repository Hazırlığı

1. Projenizi GitHub'a yükleyin:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/KULLANICI_ADI/REPO_ADI.git
git push -u origin main
```

### Adım 2: Streamlit Cloud'a Kayıt

1. [streamlit.io](https://streamlit.io) adresine gidin
2. "Sign up" butonuna tıklayın
3. GitHub hesabınızla giriş yapın

### Adım 3: Uygulamayı Deploy Etme

1. [share.streamlit.io](https://share.streamlit.io) adresine gidin
2. "New app" butonuna tıklayın
3. GitHub repository'nizi seçin
4. Branch: `main`
5. Main file path: `gui.py`
6. "Deploy!" butonuna tıklayın

### Adım 4: Deploy Sonrası

- Uygulama birkaç dakika içinde deploy edilecek
- URL formatı: `https://KULLANICI_ADI-REPO-ADİ.streamlit.app`
- Her GitHub push'unda otomatik olarak yeniden deploy edilir

---

## Seçenek 2: Railway'a Deploy

Railway, Python uygulamalarını kolayca deploy etmenizi sağlar.

### Adım 1: Railway Hesabı Oluşturma

1. [railway.app](https://railway.app) adresine gidin
2. GitHub hesabınızla giriş yapın

### Adım 2: Proje Oluşturma

1. "New Project" butonuna tıklayın
2. "Deploy from GitHub repo" seçeneğini seçin
3. Repository'nizi seçin

### Adım 3: Railway Configuration

Railway otomatik olarak Python uygulamalarını algılar, ancak manuel ayar için:

1. Settings > Environment Variables:
   - `PORT`: Railway otomatik ayarlar
   
2. Settings > Deploy:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run gui.py --server.port $PORT --server.address 0.0.0.0`

### Adım 4: Deploy

Railway otomatik olarak deploy edecektir. URL'yi almak için:
1. Settings > Domains
2. "Generate Domain" butonuna tıklayın

---

## Seçenek 3: Render'a Deploy

Render, ücretsiz tier sunan bir platformdur.

### Adım 1: Render Hesabı Oluşturma

1. [render.com](https://render.com) adresine gidin
2. GitHub hesabınızla giriş yapın

### Adım 2: Web Service Oluşturma

1. "New +" > "Web Service" seçin
2. GitHub repository'nizi bağlayın

### Adım 3: Ayarlar

- **Name**: `sir-epidemic-simulation` (veya istediğiniz isim)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run gui.py --server.port $PORT --server.address 0.0.0.0`

### Adım 4: Deploy

Render otomatik olarak deploy edecektir. URL formatı:
`https://sir-epidemic-simulation.onrender.com`

---

## Seçenek 4: Docker ile Deploy

Docker kullanarak herhangi bir platforma deploy edebilirsiniz.

### Dockerfile Oluşturma

Proje kök dizininde `Dockerfile` oluşturun (zaten oluşturuldu, aşağıda kontrol edin).

### Docker Image Oluşturma

```bash
docker build -t sir-epidemic-simulation .
```

### Docker Container Çalıştırma

```bash
docker run -p 8501:8501 sir-epidemic-simulation
```

### Docker ile Deploy Platformları

- **Google Cloud Run**
- **AWS ECS/Fargate**
- **Azure Container Instances**
- **DigitalOcean App Platform**

---

## Gerekli Dosyalar

Deployment için gerekli dosyalar projeye eklendi:

1. ✅ `Dockerfile` - Docker container için
2. ✅ `Procfile` - Heroku/Railway için
3. ✅ `runtime.txt` - Python versiyonu için
4. ✅ `.dockerignore` - Docker build optimizasyonu
5. ✅ `setup.sh` - Render için setup script

---

## Environment Variables (Opsiyonel)

Bazı platformlarda environment variables ayarlayabilirsiniz:

- `STREAMLIT_SERVER_PORT`: Port numarası (genellikle otomatik)
- `STREAMLIT_SERVER_ADDRESS`: `0.0.0.0` (tüm arayüzlerden erişim için)

---

## Troubleshooting

### Port Sorunları

Eğer port hatası alırsanız, `gui.py` dosyasında port ayarını kontrol edin:
```python
# Streamlit otomatik port kullanır, ancak bazı platformlarda:
# streamlit run gui.py --server.port $PORT --server.address 0.0.0.0
```

### Bağımlılık Sorunları

`requirements.txt` dosyasının güncel olduğundan emin olun:
```bash
pip freeze > requirements.txt
```

### Memory Sorunları

Büyük ağlar için memory limitleri olabilir. Platform ayarlarından memory'i artırın.

---

## Önerilen Platform: Streamlit Cloud

**Neden Streamlit Cloud?**
- ✅ Tamamen ücretsiz
- ✅ Streamlit için özel optimize edilmiş
- ✅ Otomatik CI/CD (GitHub push = auto deploy)
- ✅ Kolay kullanım
- ✅ Hızlı deploy
- ✅ Özel domain desteği (ücretsiz)

---

## Sonraki Adımlar

1. GitHub repository'nizi hazırlayın
2. Streamlit Cloud'a kayıt olun
3. Uygulamayı deploy edin
4. URL'nizi paylaşın!

Herhangi bir sorunla karşılaşırsanız, platform'un dokümantasyonuna bakın veya GitHub Issues'da sorun bildirin.

