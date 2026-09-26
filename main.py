import asyncio
import json
import os
from dotenv import load_dotenv
import httpx

# Load environment variables
load_dotenv()

# Example public endpoints
URLS = [
    "https://jsonplaceholder.typicode.com/todos/1",
    "https://jsonplaceholder.typicode.com/todos/2"
]

async def fetch_data(client: httpx.AsyncClient, url: str) -> dict:
    """Fetch a single URL asynchronously with error handling."""
    try:
        response = await client.get(url, timeout=10.0)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        print(f"Error fetching {url}: {e}")
        return {}

async def main():
    async with httpx.AsyncClient() as client:
        # Run multiple requests concurrently
        tasks = [fetch_data(client, url) for url in URLS]
        results = await asyncio.gather(*tasks)
        
        # Combine results
        combined_data = {
            "status": "success",
            "data": results
        }
        
        # Save results as JSON
        output_file = "combined_results.json"
        with open(output_file, "w") as f:
            json.dump(combined_data, f, indent=4)
            
        print(f"Successfully saved combined results to {output_file}")

if __name__ == "__main__":
    asyncio.run(main())