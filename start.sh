#!/usr/bin/env bash
# Install browser binaries (only needed the first boot ― safe to keep)
playwright install --with-deps

# Start FastAPI via uvicorn on the port Fly expects (8080)
uvicorn main:app --host 0.0.0.0 --port 8080