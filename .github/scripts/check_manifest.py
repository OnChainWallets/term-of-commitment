"""Valida o versions.json contra os arquivos do repo e contra a branch base.

Uso: python check_manifest.py [<base_ref>]
Sem base_ref (push na main) roda so as checagens que nao comparam com a base.
"""

import json
import os
import re
import subprocess
import sys

MANIFEST = "versions.json"
REQUIRED = {"version", "file", "effective_date"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
HASH_RE = re.compile(r"^[0-9a-f]{7}$")

errors: list[str] = []
warnings: list[str] = []


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], capture_output=True, text=True)


def check_structure(manifest: dict) -> None:
    if not isinstance(manifest, dict) or not manifest:
        errors.append(f"{MANIFEST} precisa ser um objeto com pelo menos um documento")
        return
    for doc, entry in manifest.items():
        if not isinstance(entry, dict):
            errors.append(f"{doc}: entrada precisa ser um objeto")
            continue
        missing = REQUIRED - entry.keys()
        if missing:
            errors.append(f"{doc}: faltam os campos {sorted(missing)}")
            continue
        version = entry["version"]
        # bool e subclasse de int em Python
        if not isinstance(version, int) or isinstance(version, bool) or version < 1:
            errors.append(f"{doc}: version deve ser inteiro >= 1, veio {version!r}")
        if not os.path.isfile(entry["file"]):
            errors.append(f"{doc}: file '{entry['file']}' nao existe no repo")
        if not DATE_RE.match(str(entry["effective_date"])):
            errors.append(f"{doc}: effective_date deve ser AAAA-MM-DD, veio {entry['effective_date']!r}")
        legacy = entry.get("v1_legacy_hash")
        if legacy is not None and not HASH_RE.match(str(legacy)):
            errors.append(f"{doc}: v1_legacy_hash deve ter 7 caracteres hex, veio {legacy!r}")


def check_against_base(manifest: dict, base_ref: str) -> None:
    shown = git("show", f"{base_ref}:{MANIFEST}")
    if shown.returncode != 0:
        if git("rev-parse", "--verify", base_ref).returncode != 0:
            errors.append(f"base '{base_ref}' nao encontrada: rode o checkout com fetch-depth: 0")
            return
        print(f"::notice::{MANIFEST} nao existe em {base_ref}; comparacao de versao pulada")
        base = {}
    else:
        base = json.loads(shown.stdout)

    for doc, old in base.items():
        if doc not in manifest:
            errors.append(f"{doc}: documento saiu do manifesto (existe em {base_ref})")
            continue
        new_v, old_v = manifest[doc].get("version"), old.get("version")
        if isinstance(new_v, int) and isinstance(old_v, int) and new_v < old_v:
            errors.append(f"{doc}: version voltou de {old_v} para {new_v}")
        if old.get("v1_legacy_hash") != manifest[doc].get("v1_legacy_hash"):
            errors.append(f"{doc}: v1_legacy_hash nao pode mudar (aceites antigos dependem dele)")

    diff = git("diff", "--name-only", f"{base_ref}...HEAD")
    if diff.returncode != 0:
        errors.append(f"git diff contra {base_ref} falhou: {diff.stderr.strip()}")
        return
    changed = set(diff.stdout.split())
    for doc, entry in manifest.items():
        if entry.get("file") not in changed:
            continue
        old_v = base.get(doc, {}).get("version")
        if old_v is not None and entry.get("version") == old_v:
            warnings.append(
                f"{doc}: {entry['file']} mudou e a version continua {old_v}. "
                "Se a mudanca e material, suba a version; se e typo ou formatacao, ignore."
            )


def main() -> int:
    try:
        with open(MANIFEST, encoding="utf-8") as f:
            manifest = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"::error file={MANIFEST}::{exc}")
        return 1

    check_structure(manifest)
    if len(sys.argv) > 1 and sys.argv[1]:
        check_against_base(manifest, sys.argv[1])

    for msg in warnings:
        print(f"::warning file={MANIFEST}::{msg}")
    for msg in errors:
        print(f"::error file={MANIFEST}::{msg}")
    print(f"{len(manifest)} documento(s), {len(errors)} erro(s), {len(warnings)} aviso(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
