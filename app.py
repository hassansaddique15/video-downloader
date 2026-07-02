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
        response = requests.get(api_url, headers=headers)
        
        try:
            data = response.json()
        except Exception as json_err:
            return jsonify({"success": False, "error": f"API Bad Response: {response.text[:150]}"})
            
        if response.status_code == 200:
            # ⬇️ ہم نے یہاں 'file' لکھ دیا ہے تاکہ یہ API سے ڈائریکٹ لنک پکڑ لے ⬇️
            download_url = data.get('file') or data.get('reserved_file')
            
            if download_url:
                 return jsonify({"success": True, "download_url": download_url})
            else:
                 return jsonify({"success": False, "error": f"Link missing in data: {str(data)}"})
        else:
            return jsonify({"success": False, "error": f"API Blocked (Code {response.status_code}): {data.get('message', 'Unknown Error')}"})

    except Exception as e:
        return jsonify({"success": False, "error": f"Connection Crash: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
