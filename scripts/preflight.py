#!/usr/bin/env python3
"""Diagnostic local en lecture seule, sans réseau ni lecture de secrets."""
import json,os,platform,shutil,subprocess
from pathlib import Path

def version(command):
    exe=shutil.which(command)
    if not exe:return None
    try:
        result=subprocess.run([exe,"--version"],capture_output=True,text=True,timeout=8,check=False)
        return result.stdout.strip() or "détection sans version disponible"
    except (OSError,subprocess.TimeoutExpired):return "version non déterminée"

mem=None
if Path("/proc/meminfo").exists():
    for line in Path("/proc/meminfo").read_text().splitlines():
        if line.startswith("MemTotal:"):mem=round(int(line.split()[1])/1024/1024,2)
disk=shutil.disk_usage(Path.cwd())
report={"system":platform.system(),"architecture":platform.machine(),
        "cpu_logical":os.cpu_count(),"ram_gib":mem,
        "disk_free_gib":round(disk.free/1024**3,2),
        "tools":{name:version(name) for name in ["git","docker","python3"]},
        "scope":"Diagnostic seulement. Aucun service installé ou démarré.",
        "resource_note":"Les valeurs peuvent décrire un conteneur ; confirmer les ressources contractuelles du serveur."}
print(json.dumps(report,ensure_ascii=False,indent=2))
