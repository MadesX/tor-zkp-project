import socket
import random
import threading

# Configuration
HOST = '127.0.0.1'
PORT = 8888
K_SECRETS = 4
VAR_SIZE = 128
T_ROUNDS = 20

def verify_ffs_zkp(conn, addr):
    print(f"[*] Connection received from {addr}.\nStarting {T_ROUNDS}-Round FFS-ZKP Verification...")
    
    # Set a timeout so Tor background circuits do not lock up a thread forever
    conn.settimeout(15.0) 
    
    try:
        # Receive Modulus and Public Keys
        n = int.from_bytes(conn.recv(VAR_SIZE), byteorder='big')
        v_array = [int.from_bytes(conn.recv(VAR_SIZE), byteorder='big') for _ in range(K_SECRETS)]
            
        # Receive 20 Commitments (x)
        x_array = [int.from_bytes(conn.recv(VAR_SIZE), byteorder='big') for _ in range(T_ROUNDS)]
        
        # Generate and send 20 challenge arrays
        a_matrix = []
        challenge_bytes = bytearray()
        
        for _ in range(T_ROUNDS):
            a_array = [random.choice([1, 0]) for _ in range(K_SECRETS)]
            a_matrix.append(a_array)
            challenge_bytes.extend(a_array)
            
        conn.sendall(challenge_bytes)
        
        # Receive 20 Responses (y)
        y_array = [int.from_bytes(conn.recv(VAR_SIZE), byteorder='big') for _ in range(T_ROUNDS)]
        
        # Verify all 20 rounds
        all_passed = True
        for j in range(T_ROUNDS):
            y_sq = pow(y_array[j], 2, n)
            
            rhs = x_array[j]
            for i in range(K_SECRETS):
                if a_matrix[j][i] == 1:
                    rhs = (rhs * v_array[i]) % n

            if not (y_sq == rhs or y_sq == (n - rhs) % n):
                all_passed = False
                break

        # Final Verdict
        if all_passed:
            print(f"[SUCCESS] All rounds verified!\nExit Node {addr} is mathematically trusted.")
            conn.sendall(b"ZKP_OK")
            
            try:
                # Forward the web request
                http_request = conn.recv(4096)
                success_message = (
                    "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\n"
                    "=================================================\n"
                    "Multi-Round FFS-ZKP Authenticated!\n"
                    "=================================================\n"
                )
                conn.sendall(success_message.encode('utf-8'))
            except socket.timeout:
                print(f"[*] {addr} did not send HTTP data (Likely a Tor network health check). Dropping cleanly.")
        else:
            print(f"[FAILED] Cheating detected on {addr}. Terminating connection.")
            conn.sendall(b"ZKP_FAIL")
            
    except Exception as e:
        print(f"[ERROR] ZKP Handshake failed on {addr}: {e}")
    finally:
        conn.close()

# Start the Multi-Threaded TCP Server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"[*] Secure Service Provider listening on {HOST}:{PORT}")
    
    while True:
        conn, addr = s.accept()
        # Spawn a completely independent thread for every incoming Tor circuit
        threading.Thread(target=verify_ffs_zkp, args=(conn, addr), daemon=True).start()