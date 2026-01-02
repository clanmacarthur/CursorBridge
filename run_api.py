#!/usr/bin/env python
"""Run the Core API server."""
import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("API_PORT", 3000))
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,  # Auto-reload during development
    )






