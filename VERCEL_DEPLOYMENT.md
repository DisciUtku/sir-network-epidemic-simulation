# Vercel Deployment Rehberi - Alternatif Çözümler

## ⚠️ ÖNEMLİ: Vercel Streamlit Desteklemez

Vercel, Streamlit gibi Python web framework'lerini doğrudan desteklemez. Vercel, Next.js, React, Vue gibi frontend framework'leri için optimize edilmiştir.

## Çözüm Seçenekleri

### Seçenek 1: Streamlit Cloud (EN ÖNERİLEN) ✅

Streamlit Cloud, Streamlit uygulamaları için özel olarak tasarlanmış ve **tamamen ücretsiz** bir platformdur.

**Avantajlar:**
- ✅ Tamamen ücretsiz
- ✅ Streamlit için optimize edilmiş
- ✅ Otomatik CI/CD (GitHub push = auto deploy)
- ✅ Kolay kullanım
- ✅ Hızlı deploy
- ✅ Özel domain desteği

**Deploy Adımları:**

1. **GitHub Repository Hazırlığı:**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/KULLANICI_ADI/REPO_ADI.git
git push -u origin main
```

2. **Streamlit Cloud'a Kayıt:**
   - [streamlit.io](https://streamlit.io) adresine gidin
   - "Sign up" butonuna tıklayın
   - GitHub hesabınızla giriş yapın

3. **Uygulamayı Deploy Etme:**
   - [share.streamlit.io](https://share.streamlit.io) adresine gidin
   - "New app" butonuna tıklayın
   - GitHub repository'nizi seçin
   - Branch: `main`
   - Main file path: `gui.py`
   - "Deploy!" butonuna tıklayın

4. **Sonuç:**
   - URL formatı: `https://KULLANICI_ADI-REPO-ADİ.streamlit.app`
   - Her GitHub push'unda otomatik olarak yeniden deploy edilir

---

### Seçenek 2: Vercel + Streamlit Proxy (Gelişmiş)

Vercel'de Streamlit'i çalıştırmak için bir proxy çözümü kullanabilirsiniz. Bu yaklaşım karmaşıktır ve önerilmez, ancak mümkündür.

**Yaklaşım:**
1. Streamlit uygulamasını başka bir platformda çalıştırın (Railway, Render, vb.)
2. Vercel'de bir Next.js proxy uygulaması oluşturun
3. Proxy, Streamlit uygulamasına istekleri yönlendirir

**Dezavantajlar:**
- ❌ Karmaşık setup
- ❌ Ekstra maliyet (iki platform)
- ❌ Gecikme sorunları
- ❌ Bakım zorluğu

**Önerilmez!** Bunun yerine Streamlit Cloud kullanın.

---

### Seçenek 3: Railway (Vercel Alternatifi)

Railway, Vercel'e benzer bir deneyim sunar ve Python uygulamalarını destekler.

**Deploy Adımları:**

1. **Railway Hesabı Oluşturma:**
   - [railway.app](https://railway.app) adresine gidin
   - GitHub hesabınızla giriş yapın

2. **Proje Oluşturma:**
   - "New Project" butonuna tıklayın
   - "Deploy from GitHub repo" seçeneğini seçin
   - Repository'nizi seçin

3. **Railway Otomatik Algılama:**
   - Railway otomatik olarak Python uygulamalarını algılar
   - `railway.json` dosyası varsa otomatik kullanılır

4. **Deploy:**
   - Railway otomatik olarak deploy edecektir
   - URL'yi almak için: Settings > Domains > "Generate Domain"

**Avantajlar:**
- ✅ Kolay kullanım
- ✅ Otomatik deploy
- ✅ Ücretsiz tier mevcut
- ✅ Python desteği

---

### Seçenek 4: Render (Vercel Alternatifi)

Render, ücretsiz tier sunan bir platformdur.

**Deploy Adımları:**

1. **Render Hesabı Oluşturma:**
   - [render.com](https://render.com) adresine gidin
   - GitHub hesabınızla giriş yapın

2. **Web Service Oluşturma:**
   - "New +" > "Web Service" seçin
   - GitHub repository'nizi bağlayın

3. **Ayarlar:**
   - **Name**: `sir-epidemic-simulation`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run gui.py --server.port $PORT --server.address 0.0.0.0`

4. **Deploy:**
   - Render otomatik olarak deploy edecektir
   - URL formatı: `https://sir-epidemic-simulation.onrender.com`

**Avantajlar:**
- ✅ Ücretsiz tier
- ✅ Kolay kullanım
- ✅ Otomatik deploy

---

### Seçenek 5: Docker + Cloud Run (Google Cloud)

Google Cloud Run, Docker container'ları çalıştırır.

**Deploy Adımları:**

1. **Google Cloud Setup:**
```bash
# Google Cloud CLI yükleyin
# https://cloud.google.com/sdk/docs/install

# Proje oluşturun
gcloud projects create sir-epidemic-simulation

# Projeyi seçin
gcloud config set project sir-epidemic-simulation

# Container Registry'yi etkinleştirin
gcloud services enable containerregistry.googleapis.com
```

2. **Docker Image Oluşturma ve Push:**
```bash
# Docker image oluştur
docker build -t gcr.io/sir-epidemic-simulation/sir-app .

# Google Container Registry'ye push et
docker push gcr.io/sir-epidemic-simulation/sir-app
```

3. **Cloud Run'a Deploy:**
```bash
gcloud run deploy sir-epidemic-simulation \
  --image gcr.io/sir-epidemic-simulation/sir-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8501
```

**Avantajlar:**
- ✅ Ölçeklenebilir
- ✅ Sadece kullandığınız kadar ödersiniz
- ✅ Ücretsiz tier mevcut

---

## Karşılaştırma Tablosu

| Platform | Ücretsiz Tier | Kolaylık | Otomatik Deploy | Önerilen |
|----------|---------------|----------|-----------------|----------|
| **Streamlit Cloud** | ✅ Evet | ⭐⭐⭐⭐⭐ | ✅ Evet | ✅ **EVET** |
| Railway | ✅ Evet | ⭐⭐⭐⭐ | ✅ Evet | ✅ Evet |
| Render | ✅ Evet | ⭐⭐⭐⭐ | ✅ Evet | ✅ Evet |
| Google Cloud Run | ✅ Evet | ⭐⭐⭐ | ❌ Manuel | ⚠️ Orta |
| Vercel | ✅ Evet | ⭐⭐⭐⭐⭐ | ✅ Evet | ❌ Streamlit desteklemez |

---

## Önerilen Yaklaşım

**Streamlit Cloud kullanın!** 

Neden?
1. Streamlit için özel olarak tasarlanmış
2. Tamamen ücretsiz
3. En kolay deploy süreci
4. Otomatik CI/CD
5. En iyi performans

---

## Hızlı Başlangıç (Streamlit Cloud)

```bash
# 1. GitHub'a push edin
git add .
git commit -m "Ready for deployment"
git push origin main

# 2. Streamlit Cloud'a gidin
# https://share.streamlit.io

# 3. "New app" > Repository seçin > Deploy!

# 4. Hazır! 🎉
```

---

## Sorun Giderme

### Port Sorunları
- Platform otomatik port atar, `$PORT` environment variable'ını kullanın
- `gui.py` dosyasında port ayarı gerekmez (Streamlit otomatik yönetir)

### Bağımlılık Sorunları
- `requirements.txt` dosyasının güncel olduğundan emin olun
- Tüm bağımlılıkların belirtildiğini kontrol edin

### Memory Sorunları
- Büyük ağlar için platform ayarlarından memory'i artırın
- Streamlit Cloud: Settings > Resources

---

## Sonuç

**Vercel Streamlit desteklemediği için, Streamlit Cloud kullanmanızı şiddetle öneririm.**

Streamlit Cloud:
- ✅ Ücretsiz
- ✅ Kolay
- ✅ Hızlı
- ✅ Streamlit için optimize edilmiş

Herhangi bir sorunuz varsa, Streamlit Cloud dokümantasyonuna bakın veya GitHub Issues'da sorun bildirin.

