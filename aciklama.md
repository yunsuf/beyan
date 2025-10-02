# Beyan Belge Sayısallaştırma Sistemi — Açıklama ve Kullanım (TR)

> n8n ile görsel iş akışı + Kimi‑VL belge anlama + OpenAI tabanlı sınıflandırma/çıkarma/doğrulama

---

## 🎯 Bu Proje Ne Yapar?

Beyan; fatura, çeki listesi (packing list), sertifika gibi iş belgelerini otomatik olarak işleyip yapılandırılmış veriye dönüştüren bir yapay zekâ sistemidir. Süreç şu şekilde işler:
- Belge yüklenir (n8n Webhook)
- Kimi‑VL servisinde görsel/metin içerik çözümlemesi yapılır
- OpenAI ajanları ile belge türü sınıflandırılır, alanlar çıkarılır ve doğrulanır
- Güven düşükse insan incelemesi istenir
- Sonuçlar saklanır ve geri bildirim olarak döner

Özet mimari: Webhook → Kimi‑VL → OpenAI Sınıflandırma → OpenAI Çıkarma → OpenAI Doğrulama → (Gerekirse) İnsan İncelemesi → PostgreSQL.

---

## 📁 Depo Yapısı (Kısaca)

- `docker-compose.yml`: Tüm servislerin orkestrasyonu (n8n, Postgres, Redis, Kimi‑VL, opsiyonel Nginx/Monitoring)
- `services/kimi-vl/`: Kimi‑VL API servisi (FastAPI) — `main.py`, `Dockerfile`, `requirements.txt`
- `n8n/workflows/document-processing-pipeline.json`: n8n akışı (webhook → Kimi‑VL → OpenAI ajanları → saklama/yanıt)
- `system_docs/`: Sistem tasarımı ve teknik kılavuzlar (`Quick_Start_Guide.md`, tasarım dokümanları)
- `ai-docs/`: AI/LLM/multi‑agent entegrasyon rehberleri
- `help-docs/`: Dökümantasyon geliştirme yardımcıları
- `sample_docs/`: Örnek belgeler (test için PDF/JPEG)
- `scripts/setup.sh`: İlk kurulum/yardımcı komutlar
- `preprompts/`, `rule/`: Ön-yönlendirmeler ve kısıtlar
- `README.md`: İngilizce genel bakış ve hızlı başlatma özetleri

Not: README’de bazı linkler `docs/` altını işaret ediyor olabilir; bu depoda karşılığı `ai-docs/` ve `system_docs/` dizinleridir.

---

## ⚡ Hızlı Başlangıç

Ön Koşullar:
- Docker & Docker Compose
- 8GB+ RAM (öneri: 16GB+), GPU varsa 8GB+ VRAM (opsiyonel)

Kurulum ve Çalıştırma:
```bash
# Depoya geçin
cd beyan

# (Varsa) temel kurulum
./scripts/setup.sh

# Servisleri başlatın
docker-compose up -d

# n8n arayüzü
open http://localhost:5678
```

İlk Akış (n8n):
1) n8n arayüzüne girin (`http://localhost:5678`).
2) `n8n/workflows/document-processing-pipeline.json` dosyasını içe aktarın.
3) Webhook yolu: `process-document`.
4) Örnek belgeyi webhook’a gönderin:
```bash
curl -X POST \
  -F "file=@sample_docs/2640316788_Commercial Invoice_1.pdf" \
  http://localhost:5678/webhook/process-document
```
5) Çalıştırmaları n8n Execution History’den izleyin.

Kimi‑VL API’yi Doğrudan Test:
```bash
curl -X POST http://localhost:8001/process \
  -F "file=@sample_docs/2640316788_Commercial Invoice_1.pdf"
```
Beklenen: `success`, `data.text_content`, `data.confidence`, `extracted_fields` vb. içeren JSON.

---

## 🧩 Bileşenler

- **n8n (5678)**: Görsel iş akışı, webhook, yönlendirme ve insan‑döngüsü formları
- **Kimi‑VL Servisi (8001)**: Belge anlama/çıkarma için FastAPI servisi (`services/kimi-vl/main.py`)
- **OpenAI Ajanları**: n8n üzerindeki OpenAI düğümleri (sınıflandırma, alan çıkarımı, doğrulama)
- **PostgreSQL (5432)**: Süreç çıktılarının saklanması (akışta `processed_documents` tablosu örneklenmiş)
- **Redis (6379)**: Önbellek/işlem sırası (Docker Compose ile gelir)

---

## 🔧 Yapılandırma

Değişkenler `docker-compose.yml` içinde tanımlıdır ve `.env` dosyasıyla geçersiz kılınabilir:
- `N8N_USER`, `N8N_PASSWORD`, `N8N_ENCRYPTION_KEY`
- `POSTGRES_USER`, `POSTGRES_PASSWORD`
- `OPENAI_API_KEY`
- `DEVICE` (auto/cpu/cuda)

Servis Portları:
- n8n: `http://localhost:5678`
- Kimi‑VL: `http://localhost:8001` (Swagger: `/docs`)

---

## 🛠️ Bu Belgeyi Nasıl Kullanırsınız?

- **Kurulum/Çalıştırma**: “Hızlı Başlangıç” ile tüm sistemi ayağa kaldırın.
- **Akış Mantığını Anlama**: `n8n/workflows/document-processing-pipeline.json` içindeki düğümlere bakın.
- **API Testleri**: Kimi‑VL `/process` uç noktasını `curl` ile deneyin.
- **Derinlemesine**: Ayrıntılar ve sorun giderme için `system_docs/Quick_Start_Guide.md` ve diğer `system_docs/`/`ai-docs/` belgelerine geçin.

---

## 🚀 Bundan Sonra Ne Yapmalıyım?

1) Kendi belgelerinizi işleyin: `sample_docs/` yerine gerçek belgelerinizle test edin.
2) Şema özelleştirme: n8n’de OpenAI çıkarım düğümündeki JSON şemayı ihtiyaçlarınıza göre düzenleyin.
3) Doğrulama kuralları: İş kurallarınızı “Validation” ajanına ekleyin (tarih/format/tutarlılık kontrolleri).
4) Veritabanı: `processed_documents` şemasını tanımlayın ve kalıcılığı netleştirin.
5) Performans: GPU kullanımı (`DEVICE=cuda`), `MAX_BATCH_SIZE`, toplu işleme stratejileri.
6) Güvenlik/Prod: Varsayılan parolaları değiştirin, TLS/Proxy (Nginx), erişim kontrolleri, yedekleme/izleme.

---

## 🩺 Sorun Giderme

- Tipik hatalar, sağlık kontrolleri ve test komutları için: `system_docs/Quick_Start_Guide.md` → Troubleshooting
- GPU bellek, model yükleme, port çakışmaları vb. için kılavuzdaki hazır komutları kullanın

---

## 📚 Ek Kaynaklar

- Genel bakış: `README.md`
- Hızlı Kılavuz ve ayrıntılı adımlar: `system_docs/Quick_Start_Guide.md`
- Teknik tasarım: `system_docs/system_design.md` ve `system_docs/Kimi-VL_Technical_Implementation_Guide.md`
- n8n entegrasyonu ve çok‑ajan yapısı: `ai-docs/`

Lisans: MIT (bkz. `README.md`).

---

## ✅ Kısa Kontrol Listesi

- Docker ile servisleri başlattınız mı?
- n8n akışını içe aktarıp webhook’u çalıştırdınız mı?
- Kimi‑VL `/process` ile tek belge test ettiniz mi?
- Çıkan JSON’dan alanlar sizin şemanıza uyuyor mu?
- Gerekirse insan incelemesi adımı çalışıyor mu?

Hazırsınız. Artık gerçek belgelerinizle süreci devreye alabilir, şemaları ve doğrulama kurallarını işinize göre rafine edebilirsiniz.
