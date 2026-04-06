#!/usr/bin/env python3
"""
🔍 SELF-DIAGNOSTIC — Max (VL Medical)
Auto-audit complet de toutes les capacités de Max.
Vérifie : exec, email, Notion, recherche juridique, fichiers, mémoire, gateway.

Usage:
  python3 tools/self_diagnostic.py              # Audit complet
  python3 tools/self_diagnostic.py quick         # Check rapide (exec + email + notion)
  python3 tools/self_diagnostic.py fix           # Audit + tentative d'auto-correction
  python3 tools/self_diagnostic.py report        # Génère un rapport dans diagnostic_report.md

Codes retour:
  0 = tout OK
  1 = problèmes détectés (voir rapport)
  2 = problèmes critiques (Max ne peut pas travailler)
"""

import sys
import os
import json
import subprocess
import time
from datetime import datetime

# === CONFIG ===
WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(WORKSPACE, "tools")
CONFIG_DIR = os.path.join(WORKSPACE, "config")
MEMORY_FILE = os.path.join(WORKSPACE, "MEMORY.md")
PENDING_FILE = os.path.join(WORKSPACE, "PENDING_TASKS.md")
REPORT_FILE = os.path.join(WORKSPACE, "diagnostic_report.md")
MEDIA_OUTBOUND = "/home/gilles/.openclaw-vlmedical/media/outbound"
VLMEDICAL_STATE = "/home/gilles/.openclaw-vlmedical"
EXEC_APPROVALS = "/home/gilles/.openclaw/exec-approvals.json"

# === RESULTS ===
results = []
critical_count = 0
warning_count = 0
ok_count = 0


def check(name, status, detail="", fix_hint=""):
    """Enregistre un résultat de check."""
    global critical_count, warning_count, ok_count
    entry = {"name": name, "status": status, "detail": detail, "fix_hint": fix_hint}
    results.append(entry)
    if status == "CRITICAL":
        critical_count += 1
        icon = "🔴"
    elif status == "WARNING":
        warning_count += 1
        icon = "🟡"
    else:
        ok_count += 1
        icon = "✅"
    print(f"{icon} {name}: {status}" + (f" — {detail}" if detail else ""))
    if fix_hint and status != "OK":
        print(f"   💡 Fix: {fix_hint}")


def run_cmd(cmd, timeout=15):
    """Exécute une commande et retourne (ok, stdout, stderr)."""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", "TIMEOUT"
    except Exception as e:
        return False, "", str(e)


# ======================================================
# CHECKS
# ======================================================

def check_exec_permissions():
    """Vérifie que exec fonctionne (le problème fondamental)."""
    # Test 1: exec-approvals.json existe
    if not os.path.exists(EXEC_APPROVALS):
        check("exec-approvals.json", "CRITICAL",
              f"Fichier absent: {EXEC_APPROVALS}",
              "Jacques doit monter le fichier dans docker-compose.yml")
        return False

    # Test 2: on peut lire le fichier
    try:
        with open(EXEC_APPROVALS, "r") as f:
            data = json.load(f)
        check("exec-approvals.json", "OK", f"version={data.get('version')}")
    except Exception as e:
        check("exec-approvals.json", "CRITICAL",
              f"Lecture impossible: {e}",
              "Vérifier permissions fichier")
        return False

    # Test 3: exec fonctionne réellement
    ok, out, err = run_cmd("echo 'exec_test_ok'")
    if ok and "exec_test_ok" in out:
        check("exec (commandes)", "OK", "Exécution de commandes opérationnelle")
        return True
    else:
        check("exec (commandes)", "CRITICAL",
              f"Commande echo échoue: {err}",
              "Vérifier sandbox.mode=off dans openclaw.json")
        return False


def check_email():
    """Vérifie que l'outil email fonctionne."""
    # Config existe
    config_path = os.path.join(CONFIG_DIR, "email.json")
    if not os.path.exists(config_path):
        check("email — config", "CRITICAL",
              f"Fichier absent: {config_path}",
              "Créer config/email.json avec les credentials Migadu")
        return

    try:
        with open(config_path) as f:
            cfg = json.load(f)
        addr = cfg.get("address", "")
        if not addr:
            check("email — config", "CRITICAL", "Adresse email vide dans config")
            return
        check("email — config", "OK", f"Adresse: {addr}")
    except Exception as e:
        check("email — config", "CRITICAL", f"Config illisible: {e}")
        return

    # Test connexion IMAP
    ok, out, err = run_cmd(f"cd {WORKSPACE} && python3 tools/email_tool.py check 2>&1")
    if ok and ("non lu" in out.lower() or "inbox" in out.lower() or "mail" in out.lower() or "aucun" in out.lower()):
        check("email — IMAP", "OK", out[:100])
    elif "error" in (out + err).lower() or "fail" in (out + err).lower():
        check("email — IMAP", "CRITICAL",
              (out + err)[:150],
              "Vérifier credentials Migadu dans config/email.json")
    else:
        check("email — IMAP", "WARNING",
              f"Réponse inattendue: {(out + err)[:100]}",
              "Tester manuellement: python3 tools/email_tool.py check")


def check_notion():
    """Vérifie la connexion Notion."""
    ok, out, err = run_cmd(f"cd {WORKSPACE} && python3 tools/notion_tool.py check 2>&1")
    combined = out + err
    if ok and ("connect" in combined.lower() or "ok" in combined.lower() or "notion" in combined.lower()):
        check("Notion — connexion", "OK", combined[:100])
    else:
        check("Notion — connexion", "WARNING",
              combined[:150],
              "Vérifier token Notion dans notion_tool.py + partage des pages avec l'intégration Max")


def check_legal_search():
    """Vérifie la recherche juridique."""
    ok, out, err = run_cmd(f"cd {WORKSPACE} && python3 tools/legal_search.py status 2>&1", timeout=30)
    combined = out + err
    if "judilibre" in combined.lower() or "légifrance" in combined.lower() or "ok" in combined.lower():
        check("Recherche juridique", "OK", "APIs juridiques accessibles")
    else:
        check("Recherche juridique", "WARNING",
              combined[:150],
              "Vérifier credentials PISTE dans legal_search.py")


def check_files_and_memory():
    """Vérifie la structure des fichiers essentiels."""
    essential_files = {
        "SOUL.md": os.path.join(WORKSPACE, "SOUL.md"),
        "IDENTITY.md": os.path.join(WORKSPACE, "IDENTITY.md"),
        "AGENTS.md": os.path.join(WORKSPACE, "AGENTS.md"),
        "USER.md": os.path.join(WORKSPACE, "USER.md"),
        "MEMORY.md": MEMORY_FILE,
        "PENDING_TASKS.md": PENDING_FILE,
        "TOOLS.md": os.path.join(WORKSPACE, "TOOLS.md"),
    }

    missing = []
    empty = []
    for name, path in essential_files.items():
        if not os.path.exists(path):
            missing.append(name)
        elif os.path.getsize(path) < 10:
            empty.append(name)

    if missing:
        check("Fichiers essentiels", "CRITICAL",
              f"Manquants: {', '.join(missing)}",
              "Recréer les fichiers manquants dans le workspace")
    elif empty:
        check("Fichiers essentiels", "WARNING",
              f"Quasi-vides: {', '.join(empty)}",
              "Vérifier le contenu de ces fichiers")
    else:
        check("Fichiers essentiels", "OK", f"{len(essential_files)} fichiers présents")

    # MEMORY.md : vérifier qu'elle est à jour
    if os.path.exists(MEMORY_FILE):
        mtime = os.path.getmtime(MEMORY_FILE)
        age_hours = (time.time() - mtime) / 3600
        if age_hours > 72:
            check("MEMORY.md fraîcheur", "WARNING",
                  f"Dernière modif il y a {age_hours:.0f}h",
                  "Mettre à jour MEMORY.md avec les infos récentes")
        else:
            check("MEMORY.md fraîcheur", "OK", f"Modifié il y a {age_hours:.0f}h")

    # PENDING_TASKS.md : vérifier contenu
    if os.path.exists(PENDING_FILE):
        with open(PENDING_FILE) as f:
            content = f.read().strip()
        if len(content) < 20 or "aucune" in content.lower():
            check("PENDING_TASKS.md", "WARNING",
                  "Vide ou presque — est-ce normal ?",
                  "Si des tâches sont en cours, les documenter ici")
        else:
            lines = [l for l in content.split('\n') if l.strip().startswith('- ')]
            check("PENDING_TASKS.md", "OK", f"{len(lines)} tâche(s) listée(s)")


def check_tools_scripts():
    """Vérifie que les scripts outils sont présents et syntaxiquement valides."""
    tools = {
        "email_tool.py": "Email Migadu",
        "notion_tool.py": "Notion API",
        "legal_search.py": "Recherche juridique",
        "create_proforma_lch_pdf.py": "Proforma PDF",
        "gen_proforma_medicov.py": "Proforma Medicov",
    }

    broken = []
    for script, desc in tools.items():
        path = os.path.join(TOOLS_DIR, script)
        if not os.path.exists(path):
            broken.append(f"{script} (ABSENT)")
            continue
        # Vérifier syntaxe Python
        ok, out, err = run_cmd(f"python3 -c \"import ast; ast.parse(open('{path}').read())\" 2>&1")
        if not ok:
            broken.append(f"{script} (ERREUR SYNTAXE: {err[:50]})")

    if broken:
        check("Scripts outils", "WARNING",
              f"Problèmes: {', '.join(broken)}",
              "Corriger les scripts cassés")
    else:
        check("Scripts outils", "OK", f"{len(tools)} scripts valides")


def check_media_dirs():
    """Vérifie les dossiers media pour l'envoi de fichiers WhatsApp."""
    if os.path.exists(MEDIA_OUTBOUND):
        check("Media outbound", "OK", MEDIA_OUTBOUND)
    else:
        check("Media outbound", "WARNING",
              f"Dossier absent: {MEDIA_OUTBOUND}",
              f"mkdir -p {MEDIA_OUTBOUND}")


def check_gateway_health():
    """Vérifie la santé de la gateway VL Medical."""
    ok, out, err = run_cmd("curl -sf http://127.0.0.1:18790/health?t=fbbb3632c613522dba34c9065f757a8fa57ab3073d326a49 2>&1", timeout=10)
    if ok and out:
        try:
            health = json.loads(out)
            status = health.get("status", "unknown")
            if status == "ok" or status == "healthy":
                check("Gateway santé", "OK", f"status={status}")
            else:
                check("Gateway santé", "WARNING", f"status={status}")
        except json.JSONDecodeError:
            check("Gateway santé", "OK" if "ok" in out.lower() else "WARNING", out[:100])
    else:
        check("Gateway santé", "CRITICAL",
              "Gateway ne répond pas sur :18790",
              "docker restart vlmedical-gateway")


def check_whatsapp():
    """Vérifie l'état WhatsApp via le health endpoint."""
    ok, out, err = run_cmd("curl -sf http://127.0.0.1:18790/health?t=fbbb3632c613522dba34c9065f757a8fa57ab3073d326a49 2>&1", timeout=10)
    if ok and out:
        try:
            health = json.loads(out)
            channels = health.get("channels", {})
            wa = channels.get("whatsapp", {})
            if isinstance(wa, dict):
                connected = wa.get("connected", False) or wa.get("status") == "connected"
                if connected:
                    check("WhatsApp", "OK", f"+33756928403 connecté")
                else:
                    check("WhatsApp", "WARNING",
                          f"État: {wa.get('status', 'inconnu')}",
                          "Vérifier connexion WhatsApp — possible re-pairing nécessaire")
            else:
                check("WhatsApp", "WARNING", "Format health inattendu")
        except:
            check("WhatsApp", "WARNING", "Impossible de parser le health")
    else:
        check("WhatsApp", "WARNING", "Health endpoint inaccessible")


def check_disk_space():
    """Vérifie l'espace disque disponible."""
    ok, out, err = run_cmd("df -h /home/gilles | tail -1 | awk '{print $4, $5}'")
    if ok and out:
        parts = out.split()
        if len(parts) >= 2:
            usage_pct = parts[1].replace('%', '')
            try:
                if int(usage_pct) > 90:
                    check("Espace disque", "CRITICAL", f"Restant: {parts[0]} ({parts[1]} utilisé)")
                elif int(usage_pct) > 80:
                    check("Espace disque", "WARNING", f"Restant: {parts[0]} ({parts[1]} utilisé)")
                else:
                    check("Espace disque", "OK", f"Restant: {parts[0]} ({parts[1]} utilisé)")
            except:
                check("Espace disque", "OK", out)


# ======================================================
# AUTO-FIX
# ======================================================

def auto_fix():
    """Tente de corriger les problèmes détectés."""
    fixes_applied = []

    for r in results:
        if r["status"] == "OK":
            continue

        # Fix: media outbound manquant
        if "media outbound" in r["name"].lower() and "absent" in r["detail"].lower():
            os.makedirs(MEDIA_OUTBOUND, exist_ok=True)
            fixes_applied.append(f"Créé {MEDIA_OUTBOUND}")

        # Fix: PENDING_TASKS.md vide
        if "pending_tasks" in r["name"].lower() and not os.path.exists(PENDING_FILE):
            with open(PENDING_FILE, "w") as f:
                f.write(f"# Tâches en attente — Max\n\nDernier check: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n_Aucune tâche en attente._\n")
            fixes_applied.append("Créé PENDING_TASKS.md")

    return fixes_applied


# ======================================================
# RAPPORT
# ======================================================

def generate_report():
    """Génère un rapport markdown."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# 🔍 Rapport Auto-Diagnostic Max — {now}\n",
        f"| Métrique | Valeur |",
        f"|----------|--------|",
        f"| Checks OK | {ok_count} |",
        f"| Warnings | {warning_count} |",
        f"| Critiques | {critical_count} |",
        f"| Score santé | {ok_count}/{ok_count + warning_count + critical_count} |",
        "",
    ]

    if critical_count > 0:
        lines.append("## 🔴 Problèmes critiques\n")
        for r in results:
            if r["status"] == "CRITICAL":
                lines.append(f"- **{r['name']}** : {r['detail']}")
                if r["fix_hint"]:
                    lines.append(f"  - 💡 Fix : {r['fix_hint']}")
        lines.append("")

    if warning_count > 0:
        lines.append("## 🟡 Avertissements\n")
        for r in results:
            if r["status"] == "WARNING":
                lines.append(f"- **{r['name']}** : {r['detail']}")
                if r["fix_hint"]:
                    lines.append(f"  - 💡 Fix : {r['fix_hint']}")
        lines.append("")

    lines.append("## ✅ OK\n")
    for r in results:
        if r["status"] == "OK":
            lines.append(f"- **{r['name']}** : {r['detail']}")

    report = "\n".join(lines)
    with open(REPORT_FILE, "w") as f:
        f.write(report)
    print(f"\n📄 Rapport sauvegardé: {REPORT_FILE}")
    return report


# ======================================================
# MAIN
# ======================================================

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"

    print(f"🔍 AUTO-DIAGNOSTIC MAX — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"   Mode: {mode}")
    print("=" * 60)

    # TOUJOURS vérifier exec en premier
    exec_ok = check_exec_permissions()

    if mode == "quick":
        if exec_ok:
            check_email()
            check_notion()
            check_gateway_health()
    else:
        # Full audit
        check_gateway_health()
        check_whatsapp()
        if exec_ok:
            check_email()
            check_notion()
            check_legal_search()
        check_files_and_memory()
        check_tools_scripts()
        check_media_dirs()
        check_disk_space()

    # Résumé
    print("\n" + "=" * 60)
    total = ok_count + warning_count + critical_count
    print(f"📊 RÉSULTAT: {ok_count}/{total} OK | {warning_count} warnings | {critical_count} critiques")

    if critical_count > 0:
        print("🔴 ÉTAT: DÉGRADÉ — Max ne peut pas travailler correctement")
        print("   → Appeler Jacques pour correction immédiate")
    elif warning_count > 0:
        print("🟡 ÉTAT: OPÉRATIONNEL AVEC RÉSERVES")
    else:
        print("✅ ÉTAT: PLEINEMENT OPÉRATIONNEL")

    # Auto-fix si demandé
    if mode == "fix":
        print("\n🔧 TENTATIVE AUTO-FIX...")
        fixes = auto_fix()
        if fixes:
            for f in fixes:
                print(f"   ✅ {f}")
        else:
            print("   Aucun fix automatique applicable (corrections manuelles requises)")

    # Rapport si demandé
    if mode == "report" or mode == "full":
        generate_report()

    # Code retour
    if critical_count > 0:
        sys.exit(2)
    elif warning_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
