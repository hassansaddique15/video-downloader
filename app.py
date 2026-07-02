from flask import Flask, render_template, request, jsonify
import requests
import re

app = Flask(__name__)

# یہ فنکشن یوٹیوب کے ہر قسم کے لنک (ویڈیو اور شارٹس) میں سے ID نکالے گا
def get_youtube_id(url):
    match = re.search(r'(?:v=|\/shorts\/|youtu\.be\/)([0-9A-Za-z_-]{11})', url)
    if match:
        return match.group(1)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_video', methods=['POST'])
def get_video():
    url = request.form.get('url')
    video_id = get_youtube_id(url)
    
    if not video_id:
        return jsonify({"success": False, "error": "Invalid YouTube URL! Please enter a valid link."})
        
    # سمارٹ چیک: اگر لنک میں shorts ہے تو شارٹس والی API کال ہوگی، ورنہ عام ویڈیو والی
    if '/shorts/' in url:
        api_url = f"https://youtube-video-fast-downloader-24-7.p.rapidapi.com/download_short/{video_id}?quality=247"
    else:
        api_url = f"https://youtube-video-fast-downloader-24-7.p.rapidapi.com/download_video/{video_id}?quality=247"
    
    # آپ کی جادوئی چابی (API Key)
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "youtube-video-fast-downloader-24-7.p.rapidapi.com",
        "x-rapidapi-key": "495f4beb3fmsh51fcb0c00e174c4p1c51b4jsnd552714ea005"
    }

    try:
        # API کو ریکویسٹ بھیجنا
        response = requests.get(api_url, headers=headers)
        data = response.json()
        
        if response.status_code == 200:
            # API سے ملنے والا ڈاؤن لوڈ لنک
            download_url = data.get('url') or data.get('download_url') or data.get('link')
            if download_url:
                 return jsonify({"success": True, "download_url": download_url})
            else:
                 return jsonify({"success": False, "error": "Could not extract download link. API might be changing response format."})
        else:
            return jsonify({"success": False, "error": "API Error: Please try again later."})

    except Exception as e:
        return jsonify({"success": False, "error": "Server error while contacting API."})

if __name__ == '__main__':
    app.run(debug=True)
