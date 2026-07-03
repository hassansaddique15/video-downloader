
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
        
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "youtube-video-fast-downloader-24-7.p.rapidapi.com",
        "x-rapidapi-key": "495f4beb3fmsh51fcb0c00e174c4p1c51b4jsnd552714ea005"
    }

    # ==========================================
    # SMART QUALITY CONTROL & CRASH PROTECTION
    # ==========================================
    if '/shorts/' in url:
        # شارٹس کے لیے 720p (quality=22)
        api_url = f"https://youtube-video-fast-downloader-24-7.p.rapidapi.com/download_short/{video_id}?quality=22"
        timeout_limit = 12 # شارٹس جلدی پروسیس ہو جاتی ہیں
    else:
        # نارمل ویڈیوز کے لیے 360p (quality=18)
        api_url = f"https://youtube-video-fast-downloader-24-7.p.rapidapi.com/download_video/{video_id}?quality=18"
        timeout_limit = 12 # 12 سیکنڈ تک 360p کا انتظار کریں گے

    try:
        # پہلی کوشش (360p یا 720p)
        response = requests.get(api_url, headers=headers, timeout=timeout_limit)
        
    except requests.exceptions.Timeout:
        # اگر 12 سیکنڈ میں جواب نہ آئے تو سرور پر بوجھ ہے (ویڈیو لمبی ہے)
        if '/shorts/' not in url:
            try:
                # خودکار طریقے سے کوالٹی سب سے کم (144p - quality=17) کر کے دوبارہ ٹرائی کریں
                fallback_url = f"https://youtube-video-fast-downloader-24-7.p.rapidapi.com/download_video/{video_id}?quality=17"
                response = requests.get(fallback_url, headers=headers, timeout=25) # اس بار 25 سیکنڈ کا ٹائم دیں گے
            except requests.exceptions.Timeout:
                # اگر پھر بھی ٹائم آؤٹ ہو تو سرور کو کریش سے بچائیں
                return jsonify({"success": False, "error": "یہ ویڈیو بہت لمبی ہے اور ہمارا فری سرور اسے پروسیس نہیں کر پا رہا۔ براہ کرم کوئی چھوٹی ویڈیو ٹرائی کریں!"})
            except Exception as e:
                return jsonify({"success": False, "error": f"Connection Error: {str(e)}"})
        else:
             return jsonify({"success": False, "error": "سرور اس وقت مصروف ہے۔ براہ کرم دوبارہ کوشش کریں!"})

    except Exception as e:
        return jsonify({"success": False, "error": f"Connection Error: {str(e)}"})

    # ==========================================
    # DATA EXTRACTION
    # ==========================================
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
            return jsonify({"success": False, "error": "لنک نہیں مل سکا۔ شاید یہ ویڈیو پرائیویٹ ہے یا بہت بڑی ہے۔"})
    else:
        return jsonify({"success": False, "error": f"API Error (Code {response.status_code}): Please try again."})

if __name__ == '__main__':
    app.run(debug=True)
