from fastapi import FastAPI, Query
import requests
import random

app = FastAPI()

# Branding
OWNER_INFO = "@narutocodex8"

# List of common Free Proxies (Aap apni paid proxy bhi yahan add kar sakte hain)
PROXIES = [
    "http://45.77.56.114:8080",
    "http://167.172.189.199:80",
    "http://159.203.87.130:3128"
]

@app.get("/")
def home():
    return {
        "Owner": OWNER_INFO,
        "Status": "API is Active with Proxy Rotation",
        "Endpoint": "/convert?eat=TOKEN"
    }

@app.get("/convert")
def convert_token(eat: str = Query(..., description="Enter EAT Token")):
    # Current Working Garena Endpoint
    GARENA_URL = "https://account.garena.com/api/v1/login"
    
    # Random User-Agent for Anti-Detection
    user_agents = [
        "FreeFire/1.103.1 (Android; 13; SM-G998B)",
        "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36",
        "Dalvik/2.1.0 (Linux; U; Android 11; M2007J20CG)"
    ]

    headers = {
        "Content-Type": "application/json",
        "User-Agent": random.choice(user_agents),
        "X-GA-Region": "IND",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    payload = {
        "eat_token": eat,
        "region": "IND",
        "client_type": 1,
        "app_id": 100067,
        "version": "1.103.1"
    }

    # Proxy Configuration (Optional: Remove 'proxies' if it causes slow speed)
    proxy = {"http": random.choice(PROXIES), "https": random.choice(PROXIES)}

    try:
        # Request with Proxy and Timeout
        response = requests.post(
            GARENA_URL, 
            json=payload, 
            headers=headers, 
            # proxies=proxy, # Agar proxy slow ho toh ise comment (#) kar dein
            timeout=25
        )
        
        if response.status_code == 200:
            data = response.json()
            if "access_token" in data:
                return {
                    "Owner": OWNER_INFO,
                    "success": True,
                    "access_token": data["access_token"],
                    "account_id": data.get("account_id"),
                    "nickname": data.get("nickname", "Unknown"),
                    "status": "Success"
                }
            else:
                return {
                    "Owner": OWNER_INFO,
                    "success": False,
                    "message": "Invalid Token",
                    "details": data
                }
        else:
            return {
                "Owner": OWNER_INFO,
                "success": False,
                "error": f"Server Error {response.status_code}",
                "tip": "Check if Garena domain is alive"
            }

    except Exception as e:
        return {
            "Owner": OWNER_INFO,
            "success": False,
            "error": "Connection Failed",
            "reason": str(e)
        }
        