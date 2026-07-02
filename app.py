from flask import Flask, render_template, request, jsonify
import requests
import re

app = Flask(__name__)

# URL سے یوٹیوب کی ID نکالنے کا فنکشن
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
        
    # سمارٹ کوالٹی چیک:
    if '/shorts/' in url:
        # شارٹس چھوٹی ہوتی ہیں، اس لیے ان کے لیے 720p (quality=22) بالکل محفوظ ہے
        api_url = f"https://youtube-video-fast-downloader-24-7.p.rapidapi.com/download_short/{video_id}?quality=22"
    else:
        # لمبی ویڈیوز کے لیے 360p (quality=18) سیٹ کیا ہے تاکہ سرور کبھی ٹائم آؤٹ نہ ہو
        api_url = f"https://youtube-video-fast-downloader-24-7.p.rapidapi.com/download_video/{video_id}?quality=18"
    
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "youtube-video-fast-downloader-24-7.p.rapidapi.com",
        "x-rapidapi-key": "495f4beb3fmsh51fcb0c00e174c4p1c51b4jsnd552714ea005"
    }

    try:
        response = requests.get(api_url, headers=headers)
        
        try:
            data = response.json()
        except Exception:
            return jsonify({"success": False, "error": "API Bad Response: Data format galat hai."})
            
        if response.status_code == 200:
            download_url = data.get('file') or data.get('reserved_file') or data.get('url')
            
            if download_url:
                # تھمب نیل اور ٹائٹل کا خودکار جگاڑ
                thumbnail_url = data.get('thumb') or data.get('thumbnail') or f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                video_title = data.get('title') or "YouTube Video Ready!"

                return jsonify({
                    "success": True, 
                    "download_url": download_url,
                    "thumbnail": thumbnail_url,
                    "title": video_title
                })
            else:
                return jsonify({"success": False, "error": "Link missing in data. Video aur choti karke try karein."})
        else:
            return jsonify({"success": False, "error": f"API Error (Code {response.status_code}): Please try again."})

    except Exception as e:
        return jsonify({"success": False, "error": f"Connection Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
