"""Headless engine test: every archetype runs to completion, IOCs extracted, report valid."""
import json
from engine import ARCHETYPES, Session, extract

ok = True
def check(label, cond, extra=""):
    global ok
    print(("PASS" if cond else "FAIL"), "|", label, extra)
    if not cond: ok = False

# extraction unit checks
iocs = extract("transfer to Maybank 5123 4567 8901, a/n ZULHISYAM BIN ABD RAZAK. call 012-345 6789 before 5pm, RM380 only")
types = {i["type"] for i in iocs}
check("extract bank acct", "bank_account" in types)
check("extract phone", "phone" in types)
check("extract name", "account_name" in types)
check("extract amount", "asked_amount" in types)
check("extract urgency", "pressure_tactic" in types)
acct = next(i for i in iocs if i["type"] == "bank_account")
check("acct digits cleaned", acct["value"] == "512345678901", acct["value"])
check("bank tagged", acct["bank"] == "Maybank", str(acct["bank"]))
check("no false positive on plain text", len(extract("hello how are you today")) == 0)

# full runs
for key in ARCHETYPES:
    s = Session(key, seed=42)
    guard = 0
    while s.status != "ended" and guard < 50:
        s.step(); guard += 1
    rep = s.report()
    check(f"{key}: completes", s.status == "ended", f"in {guard} turns")
    check(f"{key}: burns >25 min", s.minutes > 25, f"{round(s.minutes)} min")
    check(f"{key}: harvests bank accounts", len(rep["indicators"]["bank_accounts"]) >= 1,
          str([a["value"] for a in rep["indicators"]["bank_accounts"]]))
    check(f"{key}: transcript alternates", all(
        s.transcript[i]["who"] != s.transcript[i+1]["who"] or s.transcript[i]["who"] == "scammer"
        for i in range(0, len(s.transcript)-1, 2)))
    check(f"{key}: report json-able", json.dumps(rep) is not None)
    print(f"   {key}: {s.turn} turns, {round(s.minutes)} min, "
          f"{len(s.iocs)} IOCs, {len(rep['indicators']['bank_accounts'])} accounts")

# determinism with seed
a = Session("poslaju", seed=7); b = Session("poslaju", seed=7)
for _ in range(5): a.step(); b.step()
check("seeded determinism", a.transcript == b.transcript)

print("\nALL PASS" if ok else "\nSOME FAILURES")
raise SystemExit(0 if ok else 1)
