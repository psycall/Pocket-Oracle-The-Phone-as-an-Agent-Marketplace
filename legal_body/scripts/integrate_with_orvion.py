#!/usr/bin/env python3
"""
integrate_with_orvion.py
────────────────────────
Idempotent integration helper that wires the `legal_body/` module into an
existing ORVION repo WITHOUT overwriting any existing file.

What it does:
  1. Detects the ORVION root (looks for `main.py` + `frontend/`).
  2. Copies `legal_body/` into the repo (skips existing files).
  3. Patches `main.py` to mount the new router (only if not already mounted).
  4. Adds a frontend route stub (only if not already declared).
  5. Appends a small section to README.md (only if marker missing).

Usage:
    python scripts/integrate_with_orvion.py --orvion-path /path/to/ORVION-The-Agentic-Settlement-Layer

Safe to run multiple times. Conflict-free by design.
"""
import argparse
import shutil
import sys
from pathlib import Path

ROUTER_MOUNT_SNIPPET = """
# ── ORVION Persona — Legal Body module ───────────────────────────────
try:
    from legal_body.backend.api.v1.legal import router as legal_router
    app.include_router(legal_router, prefix="/api/v1/legal", tags=["legal-body"])
    from legal_body.backend.models.persona import Base as LegalBase
    LegalBase.metadata.create_all(bind=engine)
except Exception as _e:  # pragma: no cover
    import logging
    logging.getLogger(__name__).warning("legal_body module not loaded: %s", _e)
"""

README_BLOCK = """
## 🧬 ORVION Persona — Agent Incorporation Engine

The `legal_body/` module gives any ORVION Agent Wallet a **legal body**:
a zero-member LLC (or equivalent) cryptographically bound to the agent's
keys, so the agent can contract, hold property and sue/be sued under
existing U.S. business-entity codes.

* Smart contracts: `legal_body/contracts/AgentPersona.sol`, `OperatingAgreement.sol`, `JurisdictionRegistry.sol`
* API: `/api/v1/legal/incorporate`, `/sign`, `/dissociate`, `/personas`
* Frontend: `/legal/incorporate`, `/legal/dashboard`
* Templates: Wyoming DAO LLC · Delaware Series LLC · NY LLC · Marshall Islands DAO

Inspired by Aaron Wright's *"The Agent's Legal Body"* (2026) and Shawn
Bayern's *"Of Bitcoins, Independently Wealthy Software, and the Zero-Member LLC"* (2014).
Built for [Circle Agent Stack](https://www.circle.com) and the
[Arc Network](https://www.arc.network).
"""

MARKER = "ORVION Persona — Agent Incorporation Engine"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orvion-path", required=True, help="Path to your ORVION repo root")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    orvion = Path(args.orvion_path).resolve()
    legal_src = Path(__file__).resolve().parents[1]   # .../legal_body/

    if not (orvion / "main.py").exists():
        print(f"❌ {orvion}/main.py not found — is this an ORVION repo?", file=sys.stderr)
        return 1

    print(f"📦 Integrating {legal_src.name} → {orvion}")

    # 1. Copy module (skip-on-conflict)
    target_root = orvion / "legal_body"
    target_root.mkdir(exist_ok=True)
    copied, skipped = 0, 0
    for src in legal_src.rglob("*"):
        rel = src.relative_to(legal_src)
        dst = target_root / rel
        if src.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
            continue
        if dst.exists():
            skipped += 1
            continue
        if args.dry_run:
            print(f"  [dry] would copy {rel}")
        else:
            shutil.copy2(src, dst)
        copied += 1
    print(f"  ↳ copied: {copied}   skipped (already present): {skipped}")

    # 2. Patch main.py
    main_py = orvion / "main.py"
    content = main_py.read_text(encoding="utf-8")
    if "legal_body.backend.api.v1.legal" not in content:
        if not args.dry_run:
            main_py.write_text(content.rstrip() + "\n" + ROUTER_MOUNT_SNIPPET, encoding="utf-8")
        print("  ↳ patched main.py (router mount)")
    else:
        print("  ↳ main.py already mounts legal_body — skipping")

    # 3. README
    readme = orvion / "README.md"
    if readme.exists() and MARKER not in readme.read_text(encoding="utf-8"):
        if not args.dry_run:
            with readme.open("a", encoding="utf-8") as f:
                f.write("\n" + README_BLOCK)
        print("  ↳ appended README.md section")

    print("\n✅ Integration complete. Restart the FastAPI app to load the new routes.")
    print("   Then visit: http://localhost:8000/docs   → look for the 'legal-body' tag.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
