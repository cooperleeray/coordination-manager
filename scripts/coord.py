#!/usr/bin/env python3
"""coord.py: the Coordination Manager's ledger tool (Python 3.9+, stdlib only).

The ledger (coord/ledger.json) is the machine-readable truth of a coordination
engagement: sessions, phases, gates, relays, decisions, deliverables, conflicts,
risks and terms. This tool keeps it consistent and renders human views.

Commands
  init <slug> [--dir coord] [--no-git]   create a workspace
  add  <kind> <id> key=value ...         add an entry (fails if the id exists)
  set  <kind> <id> key=value ...         update fields of an existing entry
  show <kind> [id]                        print entries as JSON
  log  "message"                          append to the change log
  board                                   write coord/BOARD.md
  next                                    print what can move now / what is blocked
  lint                                    consistency checks (exit 1 on errors)
  glossary                                write deliverables/<PROJECT>-CODES-GLOSSARY.md

Kinds: session phase gate relay decision deliverable conflict risk term
List values use ';' (e.g. expects="hash;fingerprint", depends="P1;P2").
Use --dir PATH (before the command) when the workspace is not ./coord.
"""
import json, os, re, subprocess, sys, datetime

KINDS = {  # kind -> (ledger key, list fields, default fields)
    "session":     ("sessions",     [], {"name": "", "where": "", "owns": "", "not_owns": "", "state": "active"}),
    "phase":       ("phases",       ["depends"], {"title": "", "owner": "", "status": "pending", "gate": "", "depends": []}),
    "gate":        ("gates",        [], {"phase": "", "criteria": "", "status": "open"}),
    "relay":       ("relays",       ["expects"], {"target": "", "phase": "", "purpose": "", "status": "drafted",
                                                   "expects": [], "changes_files": "no", "verdict": "", "supersedes": ""}),
    "decision":    ("decisions",    ["blocks"], {"question": "", "recommendation": "", "status": "open",
                                                  "needed_by": "", "blocks": [], "ruling": ""}),
    "deliverable": ("deliverables", [], {"file": "", "version": "1", "audience": "", "status": "draft"}),
    "conflict":    ("conflicts",    [], {"parties": "", "subject": "", "recommendation": "", "status": "open", "ruling": ""}),
    "risk":        ("risks",        [], {"description": "", "likelihood": "", "impact": "", "mitigation": "", "owner": "", "status": "open"}),
    "term":        ("terms",        [], {"meaning": ""}),
}
STATUS = {
    "phases": {"pending", "in_progress", "waiting", "blocked", "done", "skipped"},
    "gates": {"open", "passed", "waived"},
    "relays": {"drafted", "sent", "returned", "reviewed", "closed", "superseded"},
    "decisions": {"open", "decided", "deferred"},
    "conflicts": {"open", "ruled"},
    "risks": {"open", "mitigated", "closed"},
    "deliverables": {"draft", "delivered", "approved", "superseded"},
}
CODE_RE = re.compile(r"\b(S\d+|P\d+[a-z]?|R\d+[a-z]?|OD-\d+|G-[A-Za-z0-9.]+|C-\d+|RK-\d+|D-\d+)\b")
CODE_KIND = [(re.compile(r"^S\d+$"), "sessions"), (re.compile(r"^P\d+[a-z]?$"), "phases"),
             (re.compile(r"^R\d+[a-z]?$"), "relays"), (re.compile(r"^OD-\d+$"), "decisions"),
             (re.compile(r"^G-"), "gates"), (re.compile(r"^C-\d+$"), "conflicts"),
             (re.compile(r"^RK-\d+$"), "risks"), (re.compile(r"^D-\d+$"), "deliverables")]

def now(): return datetime.datetime.now().astimezone().isoformat(timespec="seconds")
def die(msg): print("error:", msg, file=sys.stderr); sys.exit(2)

def parse_args(argv):
    d = "coord"
    if len(argv) >= 2 and argv[0] == "--dir": d, argv = argv[1], argv[2:]
    return d, argv

def load(d):
    p = os.path.join(d, "ledger.json")
    if not os.path.exists(p): die(f"no ledger at {p} (run: coord.py init <slug>)")
    with open(p) as f: return json.load(f)

def save(d, L):
    L["updated"] = now()
    tmp = os.path.join(d, "ledger.json.tmp")
    with open(tmp, "w") as f: json.dump(L, f, indent=2, ensure_ascii=False); f.write("\n")
    os.replace(tmp, os.path.join(d, "ledger.json"))

def kv(pairs, listf):
    out = {}
    for p in pairs:
        if "=" not in p: die(f"expected key=value, got {p!r}")
        k, v = p.split("=", 1)
        out[k] = [x.strip() for x in v.split(";") if x.strip()] if k in listf else v
    return out

def cmd_init(d, args):
    if not args: die("usage: init <slug> [--no-git]")
    slug = args[0]
    if os.path.exists(os.path.join(d, "ledger.json")): die(f"{d}/ledger.json already exists")
    os.makedirs(os.path.join(d, "deliverables"), exist_ok=True)
    os.makedirs(os.path.join(d, "returns"), exist_ok=True)
    L = {"project": slug, "created": now(), "updated": now(), "log": []}
    for _, (key, _, _) in KINDS.items(): L[key] = {}
    save(d, L); log(d, L, f"workspace initialised for {slug}"); save(d, L)
    with open(os.path.join(d, "CHECKPOINT.md"), "w") as f:
        f.write(f"# CHECKPOINT: {slug} / CM\n\n- **Phase:** Phase 1 intake (not started)\n- **Next action:** collect intake\n")
    if "--no-git" not in args and not os.path.exists(os.path.join(d, ".git")):
        try:
            subprocess.run(["git", "init", "-q", d], check=True)
            subprocess.run(["git", "-C", d, "add", "-A"], check=True)
            subprocess.run(["git", "-C", d, "commit", "-q", "-m", f"coord: init {slug}"], check=False)
        except Exception as e: print("note: git init skipped:", e)
    print(f"initialised {d}/ (ledger.json, CHECKPOINT.md, deliverables/, returns/)")

def log(d, L, msg): L.setdefault("log", []).append({"at": now(), "msg": msg})

def cmd_add_set(d, args, mode):
    if len(args) < 2: die(f"usage: {mode} <kind> <id> key=value ...")
    kind, ident, rest = args[0], args[1], args[2:]
    if kind not in KINDS: die(f"unknown kind {kind!r}; one of {', '.join(KINDS)}")
    key, listf, defaults = KINDS[kind]
    L = load(d); table = L.setdefault(key, {})
    fields = kv(rest, listf)
    if mode == "add":
        if ident in table: die(f"{kind} {ident} already exists (use set)")
        entry = json.loads(json.dumps(defaults)); entry.update(fields); table[ident] = entry
        if kind == "phase" and entry.get("gate") and entry["gate"] not in L["gates"]:
            L["gates"][entry["gate"]] = {"phase": ident, "criteria": "", "status": "open"}
    else:
        if ident not in table: die(f"{kind} {ident} not found")
        table[ident].update(fields)
    if key in STATUS and "status" in table[ident] and table[ident]["status"] not in STATUS[key]:
        die(f"bad status {table[ident]['status']!r} for {kind}; allowed: {sorted(STATUS[key])}")
    log(d, L, f"{mode} {kind} {ident}: " + ", ".join(f"{k}={v}" for k, v in fields.items()))
    save(d, L); print(f"{mode} {kind} {ident} ok")

def cmd_show(d, args):
    L = load(d)
    if not args: die("usage: show <kind> [id]")
    key = KINDS.get(args[0], (args[0],))[0]
    data = L.get(key, {})
    print(json.dumps(data.get(args[1]) if len(args) > 1 else data, indent=2, ensure_ascii=False))

def cmd_log(d, args):
    L = load(d); log(d, L, " ".join(args)); save(d, L); print("logged")

def blockers(L, pid):
    ph = L["phases"][pid]; why = []
    for dep in ph.get("depends", []):
        if L["phases"].get(dep, {}).get("status") not in ("done", "skipped"): why.append(f"depends on {dep}")
    for oid, od in L["decisions"].items():
        if od["status"] == "open" and pid in od.get("blocks", []): why.append(f"decision {oid} open")
    for rid, r in L["relays"].items():
        if r.get("phase") == pid and r["status"] in ("sent",): why.append(f"relay {rid} awaiting return")
    return why

def cmd_next(d, args, quiet=False):
    L = load(d); lines = []
    act = [p for p, v in L["phases"].items() if v["status"] not in ("done", "skipped") and not blockers(L, p)]
    blk = {p: blockers(L, p) for p, v in L["phases"].items() if v["status"] not in ("done", "skipped") and blockers(L, p)}
    lines.append("ACTIONABLE PHASES: " + (", ".join(f"{p} ({L['phases'][p]['title']})" for p in act) or "none"))
    for p, w in blk.items(): lines.append(f"BLOCKED {p}: " + "; ".join(w))
    for rid, r in L["relays"].items():
        if r["status"] == "drafted": lines.append(f"READY TO SEND: {rid} → {r['target']} ({r['purpose']})")
        if r["status"] == "returned": lines.append(f"REVIEW NEEDED: {rid} returned from {r['target']}")
    for oid, od in L["decisions"].items():
        if od["status"] == "open": lines.append(f"DECISION NEEDED: {oid} {od['question']} (by {od.get('needed_by') or '—'})")
    for cid, c in L["conflicts"].items():
        if c["status"] == "open": lines.append(f"RULING NEEDED: {cid} {c['subject']}")
    if not quiet: print("\n".join(lines))
    return lines

def table(rows, head):
    if not rows: return "_none_\n"
    out = "| " + " | ".join(head) + " |\n|" + "---|" * len(head) + "\n"
    for r in rows: out += "| " + " | ".join(str(x).replace("|", "/").replace("\n", " ") for x in r) + " |\n"
    return out

def cmd_board(d, args):
    L = load(d)
    s = f"# BOARD: {L['project']}\n\n_Generated {now()} from ledger.json. Do not edit by hand._\n\n"
    s += "## Next\n" + "\n".join(f"- {x}" for x in cmd_next(d, [], quiet=True)) + "\n\n"
    s += "## Sessions\n" + table([(k, v["name"], v["where"], v["owns"], v["state"]) for k, v in L["sessions"].items()],
                                 ["Code", "Name", "Where", "Owns", "State"]) + "\n"
    s += "## Phases\n" + table([(k, v["title"], v["owner"], v["status"], f"{v.get('gate','')} ({L['gates'].get(v.get('gate',''),{}).get('status','—')})",
                                 "; ".join(blockers(L, k)) or "—") for k, v in L["phases"].items()],
                               ["Phase", "Title", "Owner", "Status", "Gate", "Blocked by"]) + "\n"
    live = [(k, v["target"], v["phase"], v["status"], v["purpose"]) for k, v in L["relays"].items() if v["status"] not in ("closed", "superseded")]
    s += "## Relays (open)\n" + table(live, ["Relay", "Target", "Phase", "Status", "Purpose"]) + "\n"
    s += "## Decisions (open)\n" + table([(k, v["question"], v["recommendation"], v["needed_by"], ", ".join(v.get("blocks", [])))
                                          for k, v in L["decisions"].items() if v["status"] == "open"],
                                         ["ID", "Question", "Recommendation", "Needed by", "Blocks"]) + "\n"
    s += "## Conflicts (open)\n" + table([(k, v["parties"], v["subject"], v["recommendation"]) for k, v in L["conflicts"].items() if v["status"] == "open"],
                                         ["ID", "Parties", "Subject", "Recommendation"]) + "\n"
    s += "## Risks (open)\n" + table([(k, v["description"], v["impact"], v["mitigation"], v["owner"]) for k, v in L["risks"].items() if v["status"] == "open"],
                                     ["ID", "Risk", "Impact", "Mitigation", "Owner"]) + "\n"
    s += "## Deliverables\n" + table([(k, v["file"], v["version"], v["audience"], v["status"]) for k, v in L["deliverables"].items()],
                                    ["ID", "File", "Ver", "Audience", "Status"]) + "\n"
    s += "## Recent log\n" + "\n".join(f"- {e['at']}: {e['msg']}" for e in L.get("log", [])[-10:]) + "\n"
    with open(os.path.join(d, "BOARD.md"), "w") as f: f.write(s)
    print(f"wrote {d}/BOARD.md")

def defined(L, code):
    if code in L.get("terms", {}): return True
    for rx, key in CODE_KIND:
        if rx.match(code): return code in L.get(key, {})
    return True

def cmd_lint(d, args):
    L = load(d); err, warn = [], []
    for key, allowed in STATUS.items():
        for k, v in L.get(key, {}).items():
            if v.get("status") not in allowed: err.append(f"{key}.{k}: bad status {v.get('status')!r}")
    for rid, r in L["relays"].items():
        if r["target"] and r["target"] not in L["sessions"]: err.append(f"relay {rid}: unknown target {r['target']}")
        if r["phase"] and r["phase"] not in L["phases"]: err.append(f"relay {rid}: unknown phase {r['phase']}")
        if not r.get("expects"): warn.append(f"relay {rid}: no 'expects' (return review will be weak)")
        if r["status"] == "returned": warn.append(f"relay {rid}: returned but not reviewed")
    inflight = {}
    for rid, r in L["relays"].items():
        if r["status"] == "sent": inflight.setdefault(r["target"], []).append(rid)
    for t, rs in inflight.items():
        if len(rs) > 1: err.append(f"WIP limit: {len(rs)} relays in flight to {t}: {', '.join(rs)}")
    for pid, p in L["phases"].items():
        for dep in p.get("depends", []):
            if dep not in L["phases"]: err.append(f"phase {pid}: unknown dependency {dep}")
        g = p.get("gate")
        if g and g not in L["gates"]: err.append(f"phase {pid}: unknown gate {g}")
        if p["status"] == "done" and g and L["gates"].get(g, {}).get("status") == "open":
            err.append(f"phase {pid} is done but gate {g} is still open")
        if p.get("owner") and p["owner"] not in L["sessions"] and p["owner"] not in ("Operator", "CM"):
            warn.append(f"phase {pid}: owner {p['owner']} is not a session code")
    for oid, od in L["decisions"].items():
        for b in od.get("blocks", []):
            if b not in L["phases"]: err.append(f"decision {oid}: blocks unknown phase {b}")
        if od["status"] == "decided" and not od.get("ruling"): warn.append(f"decision {oid}: decided without a recorded ruling")
    for cid, c in L["conflicts"].items():
        if c["status"] == "ruled" and not c.get("ruling"): err.append(f"conflict {cid}: ruled without a recorded ruling")
    ddir = os.path.join(d, "deliverables")
    if os.path.isdir(ddir):
        for fn in sorted(os.listdir(ddir)):
            if not fn.endswith(".md") or fn.endswith("CODES-GLOSSARY.md"): continue
            text = open(os.path.join(ddir, fn), encoding="utf-8").read()
            missing = sorted({c for c in CODE_RE.findall(text) if not defined(L, c)})
            if missing: err.append(f"{fn}: codes not in ledger: {', '.join(missing)}")
    for w in warn: print("warn:", w)
    for e in err: print("ERROR:", e)
    print(f"lint: {len(err)} error(s), {len(warn)} warning(s)")
    sys.exit(1 if err else 0)

def cmd_glossary(d, args):
    L = load(d); p = L["project"].upper()
    s = f"# {p}: codes glossary (one page)\n\n_Generated {now()} from ledger.json._\n\n"
    s += "## Sessions\n" + table([(k, v["name"], v["owns"]) for k, v in L["sessions"].items()], ["Code", "Session", "Owns"]) + "\n"
    s += "## Phases\n" + table([(k, v["title"], v["owner"], v["status"]) for k, v in L["phases"].items()], ["Code", "Phase", "Owner", "Status"]) + "\n"
    s += "## Relays\n" + table([(k, v["target"], v["phase"], v["purpose"]) for k, v in L["relays"].items()], ["Code", "To", "Phase", "Purpose"]) + "\n"
    s += "## Decisions\n" + table([(k, v["question"], v["status"]) for k, v in L["decisions"].items()], ["Code", "Decision", "Status"]) + "\n"
    s += "## Gates\n" + table([(k, v["phase"], v["criteria"], v["status"]) for k, v in L["gates"].items()], ["Code", "Phase", "Criteria", "Status"]) + "\n"
    if L["conflicts"]: s += "## Conflicts\n" + table([(k, v["subject"], v["status"]) for k, v in L["conflicts"].items()], ["Code", "Subject", "Status"]) + "\n"
    if L["terms"]: s += "## Terms\n" + table([(k, v["meaning"]) for k, v in L["terms"].items()], ["Term", "Meaning"]) + "\n"
    out = os.path.join(d, "deliverables", f"{p}-CODES-GLOSSARY.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f: f.write(s)
    print(f"wrote {out}")

def main():
    d, argv = parse_args(sys.argv[1:])
    if not argv or argv[0] in ("-h", "--help", "help"): print(__doc__); return
    c, a = argv[0], argv[1:]
    cmds = {"init": cmd_init, "show": cmd_show, "log": cmd_log, "board": cmd_board,
            "lint": cmd_lint, "glossary": cmd_glossary, "next": cmd_next,
            "add": lambda d, a: cmd_add_set(d, a, "add"), "set": lambda d, a: cmd_add_set(d, a, "set")}
    if c not in cmds: die(f"unknown command {c!r} (see --help)")
    cmds[c](d, a)

if __name__ == "__main__":
    main()
