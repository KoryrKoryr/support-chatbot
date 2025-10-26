# 💬 Support Chatbot Backend (MVP)

A modular, production-ready FastAPI backend that powers a customer support chatbot with lead capture, email escalation and logging. This repository provides an MVP backend suitable for integration with a frontend chat widget or for iterative AI enhancements.

---

## Overview

Support Chatbot is a lightweight FastAPI service that:

- Serves FAQ answers from a CSV knowledge base (`faq.csv`).
- Auto-reloads FAQ data when the CSV file changes using a file watcher.
- Captures leads to `leads.csv`.
- Sends escalation emails when the bot cannot answer a question (configurable via environment).
- Provides colorized terminal logs and daily rotating log files.

---

## Features

- Chat endpoint (`POST /api/chat`) — answers user questions from `faq.csv` using keyword matching (AI-ready).
- Lead capture (`POST /api/lead`) — saves leads (name, email, company) into `leads.csv`.
- Email escalation (`POST /api/escalate`) — sends escalation emails via SMTP.
- Logging — `logs/app.log` + console with colorized output and rotation.
- Simple, CSV-based datastore for quick iteration; designed to be replaced with DB/AI components in future iterations.

---

## Tech Stack

| Component | Technology                               |
| --------- | ---------------------------------------- |
| Framework | [FastAPI](https://fastapi.tiangolo.com/) |
| Language  | Python 3.8+                              |
| Email     | `smtplib` + SSL                          |
| Logging   | Python `logging`, `colorama`             |
| Config    | `.env` + `python-dotenv`                 |
| Runtime   | Uvicorn                                  |
| Data      | CSV (for MVP stage)                      |

---

## Project structure

```bash
support-chatbot/
├── app/
│   ├── main.py            # FastAPI entrypoint
│   ├── config.py          # Loads environment variables
│   ├── models.py          # Pydantic request models
│   ├── utils.py           # Core utilities: FAQ, leads, email
│   ├── logger.py          # Centralized logging setup
│   ├── routes/
│   │   ├── chat.py        # Chat endpoint
│   │   ├── lead.py        # Lead capture endpoint
│   │   └── escalate.py    # Email escalation endpoint
│   ├── __init__.py
├── logs/
│   └── app.log            # Rotating daily log file
├── faq.csv                # Sample FAQ data
├── leads.csv              # Generated leads
├── .env                   # Environment variables (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Key files & symbols (quick reference)

- app/main.py — application bootstrap, ensures leads header, starts watcher
- app/config.py — configuration constants: FAQ_PATH, SMTP_SERVER, SMTP_PORT, ALERT_EMAIL, RECEIVER_EMAIL
- app/utils.py — load_faqs(), find_faq_answer(), start_faq_watcher(), save_lead(), send_escalation_email()
- app/models.py — Pydantic request/response models
- app/logger.py — logger setup and named loggers (chat_logger, lead_logger, email_logger)
- app/routes/\* — route implementations for chat, lead, escalate
- app/scripts/check_env.py — checks required env vars and prints status

---

## Quickstart / Installation

1. Clone repo

   ```bash
   git clone https://github.com/KoryrKoryr/support-chatbot.git
   cd support-chatbot
   ```

2. Create and activate a virtual environment

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables

   ```bash
   cp .env.example .env
   # Edit .env and set ALERT_EMAIL, ALERT_PASS, RECEIVER_EMAIL, SMTP_SERVER, SMTP_PORT
   ```

   Option 2:

   Manually create a `.env` file at the project root:

   ```env
    SMTP_SERVER=smtp.gmail.com
    SMTP_PORT=465
    ALERT_EMAIL=your_email@example.com
    ALERT_PASS=CHANGEME
    RECEIVER_EMAIL=your_email@example.com
   ```

5. Optional: verify environment variables

   ```bash
   python app/scripts/check_env.py
   ```

6. Run the server (development)

   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

   OpenAPI docs: <http://127.0.0.1:8000/docs>

---

## API

- POST /api/chat

  - Body: JSON matching app.models.ChatRequest (e.g., { "question": "How do I reset my password?" })
  - Behavior: uses load_faqs() and find_faq_answer() to return the best-matching FAQ answer. If no match, the caller may trigger an escalation.

- POST /api/lead

  - Body: JSON matching app.models.LeadRequest (e.g., { "name": "...", "email": "...", "company": "..." })
  - Behavior: save_lead() appends to `leads.csv`. Leads are logged with lead_logger.

- POST /api/escalate
  - Body: JSON matching app.models.EscalationRequest (e.g., { "question": "...", "name": "...", "email": "..." })
  - Behavior: send_escalation_email() sends SMTP alert to configured receiver and logs the action.

Example requests:

Chat:

```json
POST /api/chat
{ "question": "How do I reset my password?" }
```

Lead:

```json
POST /api/lead
{ "name": "Jane Doe", "email": "jane@example.com", "company": "Acme Inc" }
```

Escalate:

```json
POST /api/escalate
{ "question": "Do you offer enterprise pricing?", "name": "John Smith", "email": "john@business.com" }
```

---

## Behavior notes

- FAQ auto-reload: start_faq_watcher() watches `faq.csv` and reloads FAQs on file modifications.
- Matching: find_faq_answer() performs simple token containment / keyword matching; intended to be replaced or augmented by vector/ML search later.
- Lead storage: leads.csv is appended to by save_lead(); main.py ensures header row exists on startup.
- Escalation email: uses SMTP credentials from .env via app/config.py; check logs on failure.

---

## Logging

All major actions are logged automatically:

| Logger         | Purpose                | Output                   |
| -------------- | ---------------------- | ------------------------ |
| `chat_logger`  | Logs chat interactions | `logs/app.log` + console |
| `lead_logger`  | Logs new leads         | `logs/app.log` + console |
| `email_logger` | Logs escalations       | `logs/app.log` + console |

Example:

```bash
2025-10-23 12:01:55 [INFO] [chat-events] User asked: How do I reset my password?
2025-10-23 12:01:55 [INFO] [lead-events] New lead saved: Jane Doe (jane@example.com)
2025-10-23 12:02:15 [INFO] [email-events] Escalation email sent to support@example.com
```

---

## Troubleshooting

- Emails failing:

  - Verify SMTP settings in `.env`.
  - Use `app/scripts/check_env.py` to confirm required env vars are set.
  - Check logs in `logs/app.log` for traceback.

- FAQ updates not reflected:

  - Ensure the process has read access to `faq.csv`.
  - Confirm the file watcher is running (started by app/main on startup).

- Leads not saved:
  - Confirm `leads.csv` exists or check startup log which creates/initializes it.
  - Inspect permissions for the file.

---

## Testing

- Use the FastAPI interactive docs at /docs for manual testing.
  - Use the built-in Swagger UI to test `/api/chat`, `/api/lead` and `/api/escalate`.
  <!-- - Consider adding pytest-based unit tests for utils (load_faqs, find_faq_answer, save_lead, send_escalation_email) as next steps. -->

---

## Next milestones

- Add frontend floating widget and integrate with this backend.
- Replace CSV FAQ with vector store + embeddings for semantic search.
- Add authentication and rate limiting.
- Add persistent datastore (Postgres) for leads.
- Add unit & integration tests and CI pipeline.

<!-- ---

## Contributing

--- -->

## License

MIT License © 2025 Denis Korir

---

## Maintainer

Author: Denis Korir  
GitHub: [@koryrkoryr](https://github.com/KoryrKoryr)  
Contact: <kibet.d.korir@gmail.com>
