from fastapi import FastAPI, Query
import requests

app = FastAPI(title="Free Fire Token Converter")

# Global Credits
OWNER_INFO = "@narutocodex8"

@app.get("/")
def home():
    return {
        "Owner": OWNER_INFO,
        "Project": "Free Fire EAT to Access Token API",
        "Status": "Running",
        "Endpoint": "/convert?eat=YOUR_TOKEN"
    }

@app.get("/convert")
def convert_token(eat: str = Query(..., description="Enter your Free Fire EAT Token")):
    # Header logic with your ownership
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "FreeFire/1.103.1 (Android)", # Updated User-Agent
        "Connection": "keep-alive"
    }
    
    payload = {
        "eat_token": eat,
        "region": "IND",
        "version": "1.103.1" 
    }

    # API Endpoint of Garena (Reverse Engineered)
    GARENA_URL = "https://auth.freefiremobile.com/api/v1/login"

    try:
        response = requests.post(GARENA_URL, json=payload, headers=headers, timeout=12)
        data = response.json()
        
        if "access_token" in data:
            return {
                "Owner": OWNER_INFO,
                "success": True,
                "access_token": data["access_token"],
                "account_id": data.get("account_id"),
                "nickname": data.get("nickname", "Unknown"),
                "region": data.get("region")
            }
        else:
            return {
                "Owner": OWNER_INFO,
                "success": False,
                "message": "Token Invalid ya Expire ho gaya hai",
                "garena_error": data
            }

    except Exception as e:
        return {
            "Owner": OWNER_INFO,
            "success": False,
            "error": str(e)
        }

# For Local Testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    