#!/bin/bash

# Configuration variables
PROXY="127.0.0.1:9008"
TARGET="http://127.0.0.1:8888/project-test"
TOTAL_CIRCUITS=5

echo "========================================================"
echo " Starting FFS-ZKP Validation Harness"
echo " Target: $TARGET"
echo " Testing $TOTAL_CIRCUITS Independent Tor Circuits..."
echo "========================================================"
echo ""

for ((i=1; i<=TOTAL_CIRCUITS; i++)); do
    echo -n "[*] Initiating Circuit $i/5... "

    # We use circuit$i:pass as SOCKS5 credentials. 
    # Tor isolates streams with different credentials into completely different circuits.
    OUTPUT=$(curl -s --socks5-hostname "circuit$i:pass@$PROXY" "$TARGET")

    # [FIXED] Now looking for the exact string your Python script outputs
    if echo "$OUTPUT" | grep -q "Multi-Round FFS-ZKP Authenticated!"; then
        echo -e "\e[32m[SUCCESS]\e[0m ZKP Handshake Passed and Payload Received."
    else
        echo -e "\e[31m[FAILED]\e[0m Connection Dropped or Math Mismatch."
        # Print the output for debugging if it failed
        if [ ! -z "$OUTPUT" ]; then
            echo "    -> Output: $OUTPUT"
        fi
    fi

    sleep 1
done

echo ""
echo "========================================================"
echo " Validation Harness Complete."
echo "========================================================"
