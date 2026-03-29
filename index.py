from flask import Flask, request, jsonify
import requests
import uuid

app = Flask(__name__)

def get_ff_jwt(uid, password):
    # Updated Endpoint: Using the global authentication path
    url = "https://client.us.freefiremobile.com/api/v1/login" 
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Dalvik/2.1.0 (Linux; Android 11; Build/RP1A.200720.011)",
        "X-GA-SDK-VERSION": "4.102.1", # Updated to a more recent SDK version
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }

    payload = {
        "device_id": str(uuid.uuid4()), 
        "account": uid,
        "password": password,
        "account_type": 1, 
        "app_id": 100067,
    }

    try:
        # Using a shorter timeout and checking if the URL is reachable
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if "access_token" in data:
                return {
                    "status": "success", 
                    "token": data["access_token"],
                    "region": data.get("region", "unknown")
                }
            else:
                return {"status": "error", "message": data.get("error_msg", "Login failed - Check UID/Pass")}
        else:
            return {"status": "error", "message": f"Server returned status: {response.status_code}"}
            
    except requests.exceptions.ConnectionError:
        # This triggers if Garena is blocking Vercel's IP
        return {"status": "error", "message": "Garena blocked the connection. Try using a Proxy or different region endpoint."}
    except Exception as e:
        return {"status": "error", "message": f"System Error: {str(e)}"}

@app.route('/get_token', methods=['GET'])
def main_api():
    uid = request.args.get('uid')
    password = request.args.get('password')

    response_data = {
        "credit": "@narutocodexofc",
        "developer": "@narutocodex8"
    }

    if not uid or not password:
        response_data.update({
            "status": "error",
            "message": "Usage: /get_token?uid=YOUR_UID&password=YOUR_PASS"
        })
        return jsonify(response_data), 400

    result = get_ff_jwt(uid, password)
    response_data.update(result)
    
    return jsonify(response_data)

def handler(event, context):
    return app(event, context)
    