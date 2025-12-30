#!/usr/bin/env python
"""Run the Sandbox Runner server."""
import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("SANDBOX_PORT", 3001))
    uvicorn.run(
        "sandbox.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,  # Auto-reload during development
    )

