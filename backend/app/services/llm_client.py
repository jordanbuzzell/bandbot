import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class AnthropicClient:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def complete(self, prompt: str, max_tokens: int = 1000) -> str:
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()

    def generate_band_names(self, description: str) -> list[str]:
        prompt = f"""You are BandBot, a creative assistant that helps musicians name their bands. 
Generate exactly 5 unique, creative band name ideas based on this description: {description}

Return your response as a JSON array of strings, like this:
["Band Name 1", "Band Name 2", "Band Name 3", "Band Name 4", "Band Name 5"]

Make the names creative, memorable, and fitting for the style described."""

        response = self.complete(prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return response.split('\n')[:5]

anthropic_client = AnthropicClient()
