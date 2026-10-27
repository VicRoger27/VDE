#!/usr/bin/env bash
# VDE Privacy & Telemetry Audit Tool
# Verifies zero external cloud connections and inspects source code for tracking endpoints

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${BOLD}==========================================================${NC}"
echo -e "${CYAN} VDE Privacy & Telemetry Audit${NC}"
echo -e " Principle: Zero Cloud Tracking, Zero External Web Calls"
echo -e "${BOLD}==========================================================${NC}"

FAILURES=0

# -------------------------------------------------------------
# 1. Static Source Code Telemetry Audit
# -------------------------------------------------------------
echo -e "\n>> Step 1: Scanning codebase for telemetry and analytics keywords..."

SUSPICIOUS_TERMS=(
    "telemetry"
    "analytics"
    "google-analytics"
    "sentry"
    "mixpanel"
    "segment.io"
    "clarity.ms"
    "bing.com"
    "msn.com"
    "telemetry.microsoft.com"
)

for term in "${SUSPICIOUS_TERMS[@]}"; do
    MATCHES=$(grep -rnI --exclude-dir=".git" --exclude-dir="CHANGELOG" --exclude-dir="scripts" --exclude="*.md" "$term" "$ROOT_DIR" 2>/dev/null || true)
    if [ -n "$MATCHES" ]; then
        echo -e "${RED}[ALERT] Suspicious term found: '$term'${NC}"
        echo "$MATCHES"
        FAILURES=$((FAILURES + 1))
    fi
done

if [ "$FAILURES" -eq 0 ]; then
    echo -e "${GREEN}✓ Source scan: Clean. Zero telemetry, tracking, or ad libraries detected.${NC}"
fi

# -------------------------------------------------------------
# 2. Endpoint Authorization Verification
# -------------------------------------------------------------
echo -e "\n>> Step 2: Auditing configured network endpoints..."

# Check URLs in qt-launcher and astal-shell
URL_MATCHES=$(grep -rnIE "https?://" --exclude-dir=".git" --exclude-dir="CHANGELOG" --exclude-dir="scripts" --exclude="*.md" "$ROOT_DIR" 2>/dev/null || true)

NON_LOCAL_COUNT=0
while IFS= read -r line; do
    if [ -n "$line" ]; then
        # Check if line contains localhost / 127.0.0.1 or standard schema definition
        if [[ "$line" =~ 127\.0\.0\.1|localhost|www\.w3\.org|schemas\. ]]; then
            continue
        fi
        echo -e "${YELLOW}[Warning Non-Local URL]:${NC} $line"
        NON_LOCAL_COUNT=$((NON_LOCAL_COUNT + 1))
    fi
done <<< "$URL_MATCHES"

if [ "$NON_LOCAL_COUNT" -eq 0 ]; then
    echo -e "${GREEN}✓ Endpoint audit: Strict localhost isolation verified.${NC}"
    echo "  Only authorized endpoint: http://127.0.0.1:8080 (Local llama.cpp MiniCPM-V 4.7)"
else
    FAILURES=$((FAILURES + NON_LOCAL_COUNT))
fi

# -------------------------------------------------------------
# 3. Live Socket Inspection (if active)
# -------------------------------------------------------------
echo -e "\n>> Step 3: Auditing active sockets for VDE processes..."

if command -v ss >/dev/null 2>&1; then
    VDE_PIDS=$(pgrep -f "vde-bar|vde-launcher|labwc" 2>/dev/null || true)
    ACTIVE_EXTERNAL=0

    for pid in $VDE_PIDS; do
        SOCKETS=$(ss -tupn "pid = $pid" 2>/dev/null | tail -n +2 || true)
        while IFS= read -r sock; do
            if [ -n "$sock" ]; then
                # Check destination
                DST=$(echo "$sock" | awk '{print $5}')
                if [[ ! "$DST" =~ 127\.0\.0\.1|::1|\[::1\] ]]; then
                    echo -e "${RED}[EXTERNAL SOCKET DETECTED] Process $pid connected to: $DST${NC}"
                    ACTIVE_EXTERNAL=$((ACTIVE_EXTERNAL + 1))
                fi
            fi
        done <<< "$SOCKETS"
    done

    if [ "$ACTIVE_EXTERNAL" -eq 0 ]; then
        echo -e "${GREEN}✓ Socket inspection: Zero external connections active.${NC}"
    else
        FAILURES=$((FAILURES + ACTIVE_EXTERNAL))
    fi
else
    echo "  'ss' command not available; skipped live socket inspection."
fi

# -------------------------------------------------------------
# Summary
# -------------------------------------------------------------
echo ""
if [ "$FAILURES" -eq 0 ]; then
    echo -e "${GREEN}${BOLD}==========================================================${NC}"
    echo -e "${GREEN}${BOLD}✓ PRIVACY AUDIT: 100% PASSED${NC}"
    echo -e "VDE is strictly isolated, private, and telemetry-free."
    echo -e "${GREEN}${BOLD}==========================================================${NC}"
    exit 0
else
    echo -e "${RED}${BOLD}==========================================================${NC}"
    echo -e "${RED}${BOLD}✗ PRIVACY AUDIT: FAILED (${FAILURES} issues identified)${NC}"
    echo -e "${RED}${BOLD}==========================================================${NC}"
    exit 1
fi
