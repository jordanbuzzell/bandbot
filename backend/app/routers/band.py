from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import HTMLResponse
from ..services.schemas import BandNameRequest, BandNameResponse
from ..services.llm_client import anthropic_client

router = APIRouter(prefix="/band-name", tags=["band"])

@router.post("", response_model=BandNameResponse)
async def generate_band_name(request: BandNameRequest):
    try:
        name_options = anthropic_client.generate_band_names(request.description)
        return BandNameResponse(name_options=name_options)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating band names: {str(e)}")

@router.post("/htmx", response_class=HTMLResponse)
async def generate_band_name_htmx(description: str = Form(...)):
    try:
        name_options = anthropic_client.generate_band_names(description)
        
        html = """
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 class="text-lg font-semibold text-blue-800 mb-3">🎵 Your Band Name Ideas:</h3>
            <ul class="space-y-2">
        """
        
        for name in name_options:
            html += f'<li class="bg-white px-3 py-2 rounded border-l-4 border-blue-400 text-gray-800 font-medium">{name}</li>'
        
        html += """
            </ul>
            <p class="text-sm text-blue-600 mt-3">💡 Tip: Try different descriptions to get more name ideas!</p>
        </div>
        """
        
        return html
    except Exception as e:
        return f"""
        <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            <strong>Error:</strong> {str(e)}
        </div>
        """
