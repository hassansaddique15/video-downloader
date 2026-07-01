
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# آپ کی API Key اور Host
API_KEY = "495f4beb3fmsh51fcb0c00e174c4p1c51b4jsnd552714ea005"
API_HOST = "youtube-video-fast-downloader-24-7.p.rapidapi.com"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_video', methods=['POST'])
def get_video():
    url = request.form.get('url')
    
    # API کو ریکویسٹ بھیجنا (ویڈیو ڈاؤن لوڈ لنک کے لیے)
    # نوٹ: ہم 'Get Video Download URL' والا اینڈ پوائنٹ استعمال کر رہے ہیں
    querystring = {"url": url}
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    
    try:
        # یہاں ہم ویڈیو لنک والا اینڈ پوائنٹ کال کریں گے
        response = requests.get("https://youtube-video-fast-downloader-24-7.p.rapidapi.com/dl", 
                                headers=headers, params=querystring)
        data = response.json()
        
        if "link" in data:
            return jsonify({"success": True, "download_url": data["link"]})
        else:
            return jsonify({"success": False, "error": "ویڈیو نہیں ملی، لنک دوبارہ چیک کریں"})
    except Exception:
        return jsonify({"success": False, "error": "سرور پر غلطی ہوئی"})

if __name__ == '__main__':
    app.run(debug=True)
