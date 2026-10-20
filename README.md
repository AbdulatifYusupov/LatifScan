# LatifScan

Веб-сканер подозрительных ссылок, APK, QR-кодов, паролей и скриншотов.

Использует **VirusTotal API**, **Have I Been Pwned** и **Google Gemini** для анализа.

> Pet / portfolio project. Не замена VirusTotal.

## Возможности

- Проверка **URL** через VirusTotal (70+ движков)
- Проверка **APK** (по SHA256 или загрузка файла)
- Распознавание **QR** → если внутри ссылка, сканируется через VT
- Проверка **пароля** через Have I Been Pwned (k-anonymity)
- **AI-анализ скриншотов** (фишинг / скам) через Google Gemini
- Кеширование результатов (24 часа)
- Rate-limit на эндпоинтах
- История сканов

## Стек

| Слой | Технологии |
|------|------------|
| Backend | Python 3.11+, Django 6 |
| БД | SQLite (для разработки) |
| Внешние API | VirusTotal, Have I Been Pwned, Google Gemini |
| Frontend | HTML + CSS + vanilla JS |
| Деплой | Gunicorn + WhiteNoise |

## Быстрый старт

```bash
git clone https://github.com/AbdulatifYusupov/LatifScan.git
cd LatifScan

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example api.env    # заполни ключи
python manage.py migrate
python manage.py runserver
```

Открой http://127.0.0.1:8000/

## Переменные окружения

Файл `api.env`:

```env
VIRUSTOTAL_API_KEY=your_vt_api_key
GEMINI_API_KEY=your_gemini_api_key
HIBP_API_KEY=          # опционально
```

Ключи:
- VirusTotal: https://www.virustotal.com/gui/my-apikey
- Gemini: https://aistudio.google.com/apikey

## Структура

```
main/
  views.py          # HTTP-слой
  services.py       # Бизнес-логика сканирования
  virustotal.py     # Клиент VirusTotal API
  exceptions.py
  helpers.py
  rate_limit.py     # IP rate-limit
  utils.py          # QR decode, HIBP
  ai_screenshot.py  # Gemini
  models.py
```

## Ограничения

- Бесплатный VT: ~4 req/min
- Сканирование синхронное (polling до ~50 сек)
- SQLite не для прода
- Смени `SECRET_KEY` перед деплоем

## Roadmap

- [ ] Фоновые задачи (Celery / django-q)
- [ ] Локальный ClamAV / YARA
- [ ] Docker Compose
- [ ] Rate-limit через Redis
- [ ] Экспорт отчётов JSON/PDF
- [ ] Переименование Django package (сейчас legacy `MultiAvaScaner`)

## License

MIT (можно добавить LICENSE файл)
