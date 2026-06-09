from pathlib import Path
import shutil

# --- CONFIGURATION ---
yaml_path = Path("shadow.yaml")
template_hosts = Path("shadow.data.template/hosts")
text = yaml_path.read_text()

def add_node(name, template_source, yaml_block):
    global text
    # 1. Clone the directory sandbox
    dst = template_hosts / name
    if dst.exists(): shutil.rmtree(dst)
    shutil.copytree(template_hosts / template_source, dst)
    
    # 2. Append to YAML if not already present
    if f"  {name}:" not in text:
        text = text.rstrip() + "\n" + yaml_block
        return True
    return False

# --- ADD NODES ---

# # Add Exits (exit3 to exit4)
# for i in range(3, 5):
#     name = f"exit{i}"
#     block = f"""  {name}:
#     network_node_id: 0
#     processes:
#     - path: /home/asusms/tor_project/tor/src/app/tor
#       args: --Address {name} --Nickname {name}
#             --defaults-torrc torrc-defaults -f torrc
#       start_time: 60
#       expected_final_state: running
# """
#     if add_node(name, "exit1", block): print(f"Added {name}")

# Add Relays (relay5 to relay15)
for i in range(16, 21):
    name = f"relay{i}"
    block = f"""  {name}:
    network_node_id: 0
    processes:
    - path: /home/asusms/tor_project/tor/src/app/tor
      args: --Address {name} --Nickname {name}
            --defaults-torrc torrc-defaults -f torrc
      start_time: 60
      expected_final_state: running
"""
    if add_node(name, "relay1", block): print(f"Added {name}")

# Add Clients (torclient101 to torclient150)
for i in range(151, 201):
    name = f"torclient{i}"
    block = f"""  {name}:
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
    if add_node(name, "torclient", block): print(f"Added {name}")

# Save the final file
yaml_path.write_text(text + "\n")
print("Done: All nodes added and sandboxes cloned.")