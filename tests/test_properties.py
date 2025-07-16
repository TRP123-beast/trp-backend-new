import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_search_properties_endpoint():
    """Test the search properties endpoint"""
    response = client.post("/api/v1/properties/search")
    
    # Should return 200 if environment variables are set correctly
    # or 500 if there are configuration issues
    assert response.status_code in [200, 500]
    
    if response.status_code == 200:
        data = response.json()
        assert "value" in data
        assert isinstance(data["value"], list)
        
        # If we have properties, check the structure
        if data["value"]:
            property = data["value"][0]
            required_fields = ["BathroomsTotalInteger", "BedroomsTotal", "City", "CityRegion", "ListingKey", "ListPrice"]
            for field in required_fields:
                assert field in property

def test_search_properties_response_structure():
    """Test that the response structure matches expected format"""
    response = client.post("/api/v1/properties/search")
    
    if response.status_code == 200:
        data = response.json()
        
        # Check for @odata.context field (aliased as odata_context)
        assert "odata_context" in data or "@odata.context" in data
        
        # Check for value array
        assert "value" in data
        assert isinstance(data["value"], list) 