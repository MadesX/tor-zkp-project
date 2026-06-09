import base64
import re
import binascii
import traceback
from torpy.guard import TorGuard

# --- CONFIGURATION ---
# Path to the Guard node's cached descriptors
CACHE_PATH = "/home/asusms/tor_project/chutney/net/nodes/000a/cached-descriptors"

# Starting Setup
INITIAL_PORT = 5000  # Port of the first node (test000a)
NUM_HOPS = 5         # Number of nodes in the circuit (max 3 for 'basic' network, 9 for lab10)
# ---------------------

class NetworkParser:
    """Parses the Chutney cache file to extract routing keys."""
    def __init__(self, cache_path):
        self.nodes = {}
        try:
            with open(cache_path, 'rb') as f:
                content = f.read().decode('utf-8', errors='ignore')
                self._parse(content)
        except FileNotFoundError:
            print(f"CRITICAL ERROR: Could not find cache file at: {cache_path}")

    def _parse(self, content):
        blocks = content.split("router ")
        for block in blocks:
            if not block.strip(): continue
            
            lines = block.splitlines()
            nickname = lines[0].split()[0]
            
            # Extract Fingerprint
            fingerprint = None
            fp_match = re.search(r'^fingerprint\s+(.*)$', block, re.MULTILINE)
            if fp_match:
                fingerprint = fp_match.group(1).replace(" ", "")

            # Extract Curve25519 NTOR Key
            ntor = None
            ntor_match = re.search(r'^ntor-onion-key\s+(.*)$', block, re.MULTILINE)
            if ntor_match:
                key_b64 = ntor_match.group(1).strip()
                key_b64 += "=" * ((4 - len(key_b64) % 4) % 4)
                ntor = base64.b64decode(key_b64)

            # Store node data if all parts were found
            if nickname and fingerprint and ntor:
                self.nodes[nickname] = {
                    'fingerprint': fingerprint,
                    'ntor': ntor
                }

    def get_node_data(self, nickname):
        if nickname not in self.nodes:
            raise ValueError(f"Could not find node '{nickname}'. Wait for network gossip.")
        return self.nodes[nickname]

class LocalRouter:
    """Represents a specific Chutney relay and holds its cryptographic keys."""
    def __init__(self, ip, port, nickname, parser):
        self.ip = ip
        self.or_port = port
        self.nickname = nickname
        self.flags = ["Guard", "Exit"]
        
        data = parser.get_node_data(nickname)
        
        # Convert hex string to raw bytes for cryptographic handshake
        self.fingerprint = binascii.unhexlify(data['fingerprint'])

        # Mock descriptor object required by torpy
        self.descriptor = type('obj', (object,), {
            'ntor_onion_key': data['ntor'], 
            'ntor_key': data['ntor'],
            'fingerprint': self.fingerprint
        })

    def __str__(self):
        return f"{self.nickname} ({self.ip}:{self.or_port})"

class DummyConsensus:
    """Bypasses torpy's automatic node selection."""
    def get_router(self, fingerprint):
        return None 

def main():
    try:
        print(f"Reading network cache from {CACHE_PATH}...")
        parser = NetworkParser(CACHE_PATH)

        # 1. Generate the list of Node objects dynamically based on NUM_HOPS
        nodes = []
        for i in range(NUM_HOPS):
            nickname = f"test{i:03d}a" 
            port = INITIAL_PORT + i
            print(f" - Preparing config for node {i+1}: {nickname} on port {port}")
            node = LocalRouter("127.0.0.1", port, nickname, parser)
            nodes.append(node)

        # 2. Connect to the Guard (Index 0)
        guard_node = nodes[0]
        print(f"\nConnecting to Entry Node: {guard_node.nickname}")
        
        guard = TorGuard(guard_node, DummyConsensus())
        circuit = guard.create_circuit(1)
        print(" -> Hop 1 (Guard) built.")

        # 3. Loop through remaining nodes to extend the circuit
        for i in range(1, NUM_HOPS):
            next_node = nodes[i]
            print(f"Extending to Hop {i+1}: {next_node.nickname}...")
            circuit.extend(next_node)
            print(f" -> Hop {i+1} built.")

        print(f"\nFULL {NUM_HOPS}-HOP CIRCUIT READY.")

        # 4. Open a stream and send the HTTP request
        print("Sending HTTP request...")
        stream = circuit.create_stream(("127.0.0.1", 8080))
        stream.send(b"GET / HTTP/1.0\r\n\r\n")
        
        # Read the incoming response from the server
        recv = stream.recv(1024)
        print(f"\n--- RESPONSE ---\n{recv.decode()}")
        
        guard.close()

    except Exception:
        print("\n--- DETAILED ERROR REPORT ---")
        traceback.print_exc()

if __name__ == "__main__":
    main()