import os
import sys
import uvicorn

if __name__ == "__main__":
    # Get the PORT from environment variable, default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    # Print for debugging
    print(f"Starting server on port {port}")
    
    # Run the FastAPI app
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
