from pathlib import Path
import shutil

base = Path("shadow.data.template/hosts/torclient")
hosts = Path("shadow.data.template/hosts")

for i in range(2, 11):
    dst = hosts / f"torclient{i}"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(base, dst)

p = Path("shadow.yaml")
text = p.read_text()

marker = "\n  torclient2:"
if marker in text:
    text = text[:text.index(marker)].rstrip() + "\n"

extra = ""
for i in range(2, 11):
    name = f"torclient{i}"
    extra += f"""
  {name}:
    network_node_id: 0
    processes:
    - path: /home/asusms/tor_project/tor/src/app/tor
      args: --Address {name} --Nickname {name}
            --defaults-torrc torrc-defaults -f torrc
      start_time: 900
      expected_final_state: running
    - path: tgen
      environment: {{ OPENBLAS_NUM_THREADS: "1" }}
      args: ../../../conf/tgen.torclient.graphml.xml
      start_time: 1500
"""

p.write_text(text.rstrip() + "\n" + extra)
print("done: torclient1 through torclient10 configured")
