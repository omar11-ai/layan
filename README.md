# LAYAN — Scam Jammer

**Make the scammer waste their own time.**

[Live demo →](https://televisions-travelers-logical-rocks.trycloudflare.com) · [MIT licensed](LICENSE)

---

Most people block scam calls. Blocking is passive — it ends the interaction but
produces nothing. LAYAN *engages* reported scam numbers instead: it stalls,
asks naive questions, and harvests the mule accounts, phone numbers, names, and
script fingerprints — all while burning the scammer's minutes.

The evidence it collects is structured for a real police report.

## Why

Scam calls in Malaysia are not random. They follow a small number of scripted
archetypes, reuse the same payment channels, and leak the same operational
details every time. Those leaks are the only thing that actually helps
enforcement — but only if someone is patient enough to pull them.

LAYAN is that patience, automated.

## How it works

1. A reported number is tagged with an **archetype** (customs fee, tax refund,
   romance, paid task).
2. A **persona** — Puan Rina, 54, retired guru from Kepala Batas — engages the
   caller. She is plausible, patient, and endlessly curious about bank details.
3. The engine **scripts the scammer's escalation** and **extracts IOCs** from
   every exchange: bank accounts, phone numbers, account names, payment
   channels, amounts demanded, and pressure tactics.
4. The session produces an **evidence pack** ready for PDRM / NSRC, with
   recommended next actions.

## Archetypes

| Archetype | Fingerprint | Shape |
|---|---|---|
| Pos Laju Customs Fee | `PARCEL-CUSTOMS` | Parcel held at customs, fee demanded, transfer pressure |
| LHDN Tax Refund | `TAX-REFUND` | Refund claim, then "processing fee" |
| Romance | `ROMANCE-ESCALATE` | Relationship building, then investment request |
| Paid Task | `PAID-TASK` | Fake job, small upfront payment, then larger ask |

## Install

```bash
git clone https://github.com/omar11-ai/layan.git
cd layan
python server.py
# -> http://localhost:8130
```

Pure standard library. Nothing to install, nothing to break.

## Use

```bash
python server.py
```

REST API:

```
GET  /api/archetypes        list available scam archetypes
GET  /api/stats              fleet-wide engagement statistics
GET  /api/sessions           list active sessions
GET  /api/session/<id>       current state of one session
GET  /api/session/<id>/report  the evidence pack
```

Or drive the engine directly:

```python
from engine import Fleet

fleet = Fleet()
sid, session = fleet.new("poslaju", seed=42)

session.step()          # scammer line + jammer reply
session.step()          # keep the scammer busy

print(session.report()) # PDRM-ready evidence pack
```

## Safety

The bundled scammer side is a **scripted simulator** of real Malaysian scam
archetypes. It is fully offline and deterministic under a seed, so demos are
safe and reproducible. Connecting the engine to real telephony is your call and
your responsibility — make sure you have the legal basis to do so in your
jurisdiction.

## License

MIT — see [LICENSE](LICENSE).

---

Built by [Omar Wael](https://github.com/omar11-ai) in Malaysia.
