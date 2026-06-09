from pathlib import Path
import shutil

yaml_path = Path("shadow.yaml")
text = yaml_path.read_text()

base_host = Path("shadow.data.template/hosts/exit1")

new_exits = ["exit3", "exit4"]

for name in new_exits:
    dst = Path(f"shadow.data.template/hosts/{name}")
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(base_host, dst)

extra = ""

for name in new_exits:
    if f"  {name}:" not in text:
        extra += f"""
  {name}:
    network_node_id: 0
    processes:
    - path: /home/asusms/tor_project/tor/src/app/tor
      args: --Address {name} --Nickname {name}
            --defaults-torrc torrc-defaults -f torrc
      start_time: 60
      expected_final_state: running
"""

insert_before = "  relay1:"
if extra and insert_before in text:
    text = text.replace(insert_before, extra + "\n" + insert_before)
    yaml_path.write_text(text)
elif extra:
    yaml_path.write_text(text.rstrip() + "\n" + extra)

print("added exit3 and exit4")
