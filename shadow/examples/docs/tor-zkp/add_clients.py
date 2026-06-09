from pathlib import Path
import shutil

base = Path("shadow.data.template/hosts/torclient")
for name in ["torclient2", "torclient3"]:
    dst = Path(f"shadow.data.template/hosts/{name}")
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(base, dst)

extra = """
  torclient2:
    network_node_id: 0
    processes:
    - path: /home/asusms/tor_project/tor/src/app/tor
      args: --Address torclient2 --Nickname torclient2
            --defaults-torrc torrc-defaults -f torrc
      start_time: 900
      expected_final_state: running
    - path: tgen
      environment: { OPENBLAS_NUM_THREADS: "1" }
      args: ../../../conf/tgen.torclient.graphml.xml
      start_time: 1500

  torclient3:
    network_node_id: 0
    processes:
    - path: /home/asusms/tor_project/tor/src/app/tor
      args: --Address torclient3 --Nickname torclient3
            --defaults-torrc torrc-defaults -f torrc
      start_time: 900
      expected_final_state: running
    - path: tgen
      environment: { OPENBLAS_NUM_THREADS: "1" }
      args: ../../../conf/tgen.torclient.graphml.xml
      start_time: 1500
"""

p = Path("shadow.yaml")
text = p.read_text()
if "torclient2:" not in text:
    p.write_text(text.rstrip() + "\n" + extra)
print("done")
