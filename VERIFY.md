# VERIFY: coordination-manager

Use this to confirm the skill is installed and usable on a surface.

**Question to ask the agent after loading the skill:** "Name the six phases of the Coordination Manager protocol, and the file where the ledger lives."

**Expected answer (any wording):** Intake & ACK · Grilling · Diagnosis · Plan · Deliverables · Coordination loop; the ledger is `coord/ledger.json`.

**Scripted check (needs Python 3.9+):** `sh tests/smoke.sh` → ends with `SMOKE PASS`.
