#!/bin/bash
# Init container script to set up iptables for transparent traffic interception
# This must run before the main containers start

set -e

echo "Setting up iptables for A2A traffic interception..."

# Constants
ENVOY_UID="1337"
INBOUND_INTERCEPT_PORT="15001"
OUTBOUND_INTERCEPT_PORT="15002"
APP_PORTS="8000,8001"  # Ports the agent apps listen on

# Create custom chains for organization
iptables -t nat -N ENVOY_INBOUND 2>/dev/null || true
iptables -t nat -N ENVOY_OUTPUT 2>/dev/null || true

# ============================================
# OUTBOUND TRAFFIC (from agent to external)
# ============================================

# Exclude Envoy's own traffic (UID 1337)
# This prevents infinite loops when Envoy forwards traffic
iptables -t nat -A OUTPUT -m owner --uid-owner ${ENVOY_UID} -j RETURN

# Exclude localhost traffic (no need to intercept)
iptables -t nat -A OUTPUT -d 127.0.0.1/8 -j RETURN

# Redirect all other TCP traffic to Envoy outbound listener
iptables -t nat -A OUTPUT -p tcp -j REDIRECT --to-port ${OUTBOUND_INTERCEPT_PORT}

# ============================================
# INBOUND TRAFFIC (from external to agent)
# ============================================

# Redirect incoming traffic on app ports to Envoy inbound listener
iptables -t nat -A PREROUTING -p tcp -m multiport --dports ${APP_PORTS} -j REDIRECT --to-port ${INBOUND_INTERCEPT_PORT}

echo "iptables rules configured successfully"
echo ""
echo "Rules summary:"
iptables -t nat -L OUTPUT -n -v --line-numbers | head -20
echo ""
iptables -t nat -L PREROUTING -n -v --line-numbers | head -20
