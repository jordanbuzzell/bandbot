import chromadb
import json
import os
from typing import List, Dict
from chromadb.utils import embedding_functions
from .llm_client import anthropic_client

class RAGService:
    def __init__(self):
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.environ["OPENAI_API_KEY"],
            model_name=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
        )
        
        self.chroma_client = chromadb.PersistentClient(path="./data/chroma")
        self.collection = self.chroma_client.get_or_create_collection(
            name="nyc_venues",
            embedding_function=openai_ef
        )

    def embed_venues_from_file(self, file_path: str):
        with open(file_path, 'r') as f:
            venues = json.load(f)

        documents = []
        metadatas = []
        ids = []

        for i, venue in enumerate(venues):
            doc_text = f"{venue['name']} in {venue['neighborhood']}. Capacity: {venue['capacity']}. Genres: {venue['genres']}. {venue['description']}"
            documents.append(doc_text)
            metadatas.append(venue)
            ids.append(str(i))

        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def retrieve_venues(self, query: str, k: int = 5) -> List[Dict]:
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )
        
        venues = []
        if results['metadatas'] and results['metadatas'][0]:
            for metadata in results['metadatas'][0]:
                venues.append(metadata)
        
        return venues
    
    def get_venue_recommendations(self, band_style: str, expected_audience: int) -> List[Dict]:
        query = f"Music venue for {band_style} band with {expected_audience} person audience"
        retrieved_venues = self.retrieve_venues(query, k=5)
        
        if not retrieved_venues:
            return []
        
        venue_context = "\n".join([
            f"- {v['name']} ({v['neighborhood']}): {v['capacity']} capacity, genres: {v['genres']}, {v['description']}"
            for v in retrieved_venues
        ])
        
        prompt = f"""You are BandBot, a music industry assistant helping bands find suitable NYC venues.

Based on this band information:
- Style: {band_style}
- Expected audience size: {expected_audience}

Here are some relevant NYC venues:
{venue_context}

Recommend the top 3 most suitable venues from this list. For each venue, explain why it's a good match.

Return your response as a JSON array with this format:
[
  {{
    "name": "Venue Name",
    "neighborhood": "Neighborhood",
    "capacity": "Capacity info",
    "genres": "Genre info",
    "description": "Venue description",
    "why_recommended": "Explanation of why this venue fits the band"
  }}
]"""
        
        response = anthropic_client.complete(prompt)
        
        try:
            recommendations = json.loads(response)
            return recommendations[:3]
        except json.JSONDecodeError:
            return [{
                "name": venue['name'],
                "neighborhood": venue['neighborhood'],
                "capacity": venue['capacity'],
                "genres": venue['genres'],
                "description": venue['description'],
                "why_recommended": f"Good match for {band_style} with {expected_audience} expected audience"
            } for venue in retrieved_venues[:3]]

rag_service = RAGService()
