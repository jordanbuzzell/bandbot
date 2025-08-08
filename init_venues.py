#!/usr/bin/env python3

import sys
import os
sys.path.append('backend')

from backend.app.services.rag import rag_service

def main():
    venues_file = "data/nyc_venues.json"
    
    if not os.path.exists(venues_file):
        print(f"Error: {venues_file} not found!")
        return
    
    print("Initializing venue database...")
    try:
        rag_service.embed_venues_from_file(venues_file)
        print("✅ Venue database initialized successfully!")
        print("You can now start the server with: uvicorn backend.app.main:app --reload")
    except Exception as e:
        print(f"❌ Error initializing venue database: {e}")

if __name__ == "__main__":
    main()
