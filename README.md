# LatifScan

Сканер подозрительных ссылок, APK, QR, паролей и фишинг-скриншотов.

**VirusTotal** + **Have I Been Pwned** + **Google Gemini**.

> Portfolio project by Abdulatif Yusupov. Inspired by MultiAvaScanner, evolved separately.

## Что умеет

- URL / APK / QR → VirusTotal (70+ движков)
- **Детальный отчёт по движкам** + экспорт JSON
- Пароли → HIBP (k-anonymity, без платного ключа)
- Скриншоты → Gemini (фишинг / скам)
- Rate-limit, кеш результатов 24ч
- Docker / docker-compose

## Стек

Python 3.12 · Django 6 · VT API · Gemini · WhiteNoise · Gunicorn

## Быстрый старт

```bash
git clone https://github.com/AbdulatifYusupov/LatifScan.git
cd LatifScan
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example api.env   # VT + Gemini keys
python manage.py migrate
python manage.py runserver
```

http://127.0.0.1:8000/

### Docker

```bash
cp .env.example api.env   # заполни ключи
docker compose up --build
```

## Env

```env
VIRUSTOTAL_API_KEY=
GEMINI_API_KEY=
HIBP_API_KEY=          # optional
DEBUG=True             # local
```

## API

| Method | Path | Description |
|--------|------|-------------|
| POST | `/scan/url/` | URL scan |
| POST | `/scan/file/` | APK scan |
| POST | `/scan/qr/` | QR scan |
| POST | `/scan/password/` | Password check |
| POST | `/scan/screenshot/` | AI screenshot |
| GET | `/scan/<id>/` | Scan JSON |
| GET | `/scan/<id>/export/` | Download full JSON report |

## Roadmap

- [ ] ClamAV / YARA local engines
- [ ] Background jobs (Celery/Redis)
- [ ] Auth + private history
- [ ] Rename Django package `MultiAvaScaner` → `latifscan`

## License

MIT
