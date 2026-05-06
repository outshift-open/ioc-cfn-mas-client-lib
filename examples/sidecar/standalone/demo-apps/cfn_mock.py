#!/usr/bin/env python3
"""
Mock CFN Service - Receives L9 validation requests from sidecars
Displays dual-boundary interception logs
"""
import os
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "cfn-mock"})

@app.route("/")
def index():
    return jsonify({
        "service": "cfn-mock",
        "message": "Mock CFN L9 validation endpoint"
    })

@app.route("/v1/l9/validate", methods=["POST"])
def validate_l9():
    """Mock L9 validation endpoint"""
    data = request.get_json()

    # Extract L9 fields (correct format from l9_converter.py)
    header = data.get("header", {})
    payload = data.get("payload", {})

    direction = header.get("direction", "UNKNOWN").upper()
    mas_id = header.get("sidecar_id", "unknown")
    actor_id = header.get("actor_id", "unknown")
    source = header.get("source", "?")
    dest = header.get("destination", "?")

    # Extract A2A message details
    a2a_msg = payload.get("a2a", {})

    # JSON-RPC 2.0 format
    msg_id = a2a_msg.get("id", "?")
    method = a2a_msg.get("method", "?")
    params = a2a_msg.get("params", {})

    # Display log
    arrow = "→" if direction == "OUTBOUND" else "←"
    timestamp = datetime.now().strftime("%H:%M:%S")

    print(f"\n{'='*60}", flush=True)
    print(f"[{timestamp}] Direction: {direction} {arrow}", flush=True)
    print(f"{'='*60}", flush=True)
    print(f"Intercepted by: {mas_id}", flush=True)
    print(f"Actor: {actor_id}", flush=True)
    print(f"Network: {source} → {dest}", flush=True)
    print(f"A2A Message (JSON-RPC):", flush=True)
    print(f"  - ID: {msg_id}", flush=True)
    print(f"  - Method: {method}", flush=True)
    print(f"  - Params: {params}", flush=True)
    print(f"{'='*60}\n", flush=True)

    # Return validation result
    return jsonify({
        "valid": True,
        "direction": direction,
        "timestamp": timestamp
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", "9002"))
    print(f"Mock CFN Service starting on port {port}...")
    print(f"L9 validation endpoint: http://0.0.0.0:{port}/v1/l9/validate")
    print("")
    app.run(host="0.0.0.0", port=port)
