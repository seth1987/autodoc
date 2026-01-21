#!/usr/bin/env bash
# Build script for Render

set -o errexit

pip install -r requirements.txt

# Install Playwright browser
playwright install chromium
playwright install-deps chromium || true
