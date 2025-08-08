from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import HTMLResponse
from ..services.schemas import VenueRequest, VenueResponse, VenueRecommendation
from ..services.rag import rag_service

router = APIRouter(prefix="/venues", tags=["venues"])

@router.post("", response_model=VenueResponse)
async def get_venue_recommendations(request: VenueRequest):
    try:
        recommendations = rag_service.get_venue_recommendations(
            request.band_style, 
            request.expected_audience
        )
        
        venue_recs = [
            VenueRecommendation(**rec) for rec in recommendations
        ]
        
        return VenueResponse(venues=venue_recs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting venue recommendations: {str(e)}")

@router.post("/htmx", response_class=HTMLResponse)
async def get_venue_recommendations_htmx(
    band_style: str = Form(...), 
    expected_audience: int = Form(...)
):
    try:
        recommendations = rag_service.get_venue_recommendations(band_style, expected_audience)
        
        if not recommendations:
            return """
            <div class="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded">
                <strong>No venues found.</strong> Try a different style or audience size.
            </div>
            """
        
        html = """
        <div class="bg-green-50 border border-green-200 rounded-lg p-4">
            <h3 class="text-lg font-semibold text-green-800 mb-4">🏛️ Recommended NYC Venues:</h3>
            <div class="space-y-4">
        """
        
        for venue in recommendations:
            html += f"""
            <div class="bg-white border border-green-200 rounded-lg p-4">
                <div class="flex justify-between items-start mb-2">
                    <h4 class="text-lg font-semibold text-gray-800">{venue['name']}</h4>
                    <span class="text-sm text-gray-500">{venue['neighborhood']}</span>
                </div>
                <div class="text-sm text-gray-600 mb-2">
                    <span class="font-medium">Capacity:</span> {venue['capacity']} | 
                    <span class="font-medium">Genres:</span> {venue['genres']}
                </div>
                <p class="text-gray-700 text-sm mb-2">{venue['description']}</p>
                <div class="bg-green-100 border-l-4 border-green-400 p-2 text-sm">
                    <strong>Why it's perfect for you:</strong> {venue['why_recommended']}
                </div>
            </div>
            """
        
        html += """
            </div>
            <p class="text-sm text-green-600 mt-4">🎤 Ready to reach out? Research their booking process and send a professional inquiry!</p>
        </div>
        """
        
        return html
    except Exception as e:
        return f"""
        <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            <strong>Error:</strong> {str(e)}
        </div>
        """
