import random # Thêm dòng này ở đầu file
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime
import requests
from dotenv import load_dotenv
import uvicorn
from pathlib import Path # <<<--- 1. THÊM DÒNG IMPORT NÀY

load_dotenv()
from pathlib import Path # <<<--- 1. THÊM DÒNG IMPORT NÀY
BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI()

# --- 1. Mount the 'static' directory ---
# This tells FastAPI that any URL starting with /static should serve a file from the 'static' folder.
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# --- 2. Configure the 'templates' directory ---
# This tells FastAPI where to find HTML files to render.
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# --- CORS Middleware (still good to have for APIs) ---
origins = ["*"] # Allow all for simplicity
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models (remains the same) ---
class UserInput(BaseModel):
    birthdate: str

# --- Helper Functions (remains the same) ---
def calculate_life_path(birthdate: str):
    total = sum(int(digit) for digit in birthdate.replace("-", ""))
    while total > 9 and total not in [11, 22]:
        total = sum(int(digit) for digit in str(total))
    return total

# In main.py

def get_astro_data():
    """
    Fetches astronomical data.
    This version handles videos from APOD and uses a default key for safety.
    """
    # Use os.getenv to safely get the key. If it's not found, use NASA's DEMO_KEY.
    api_key = os.getenv("NASA_API_KEY", "DEMO_KEY")
# A new, stable fallback image from NASA's Webb Telescope gallery
    fallback_image_url = "https://trek.nasa.gov/tiles/Moon/EQ/LRO_WAC_Mosaic_Global_303ppd_v02/1.0.0/default/default028mm/0/0/0.jpg"   
    apod_url = fallback_image_url
    try:
        print(f"Fetching APOD with key: {api_key[:4]}...") # Debug print
        apod_response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={api_key}")

        # Check if the request was successful
        if apod_response.status_code == 200:
            apod_data = apod_response.json()
            
            # IMPORTANT: Check if the media type is an image
            if apod_data.get("media_type") == "image":
                apod_url = apod_data.get("url", fallback_image_url)
            else:
                # If it's a video, we can try to use its thumbnail
                print("Today's APOD is a video. Using thumbnail or fallback.")
                apod_url = apod_data.get("thumbnail_url", fallback_image_url)
        else:
            # The request failed (e.g., bad API key)
            print(f"Error fetching APOD: Status {apod_response.status_code}")
            print(f"Response: {apod_response.text}")

    except requests.RequestException as e:
        print(f"Could not connect to NASA API: {e}")

    # --- The rest of the function is the same ---
    moon_phases = ["New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous", "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent"]
    today = datetime.date.today()
    moon_phase = moon_phases[today.day % len(moon_phases)]
    
    planets = {
        "Mercury": "Gemini",
        "Venus": "Cancer",
        "Mars": "Leo"
    }
    
    return {
        "moon_phase": moon_phase,
        "apod_url": apod_url, # This will now be the correct image URL or a fallback
        "planets": planets
    }


# Trong file app.py hoặc main.py

# Trong file app.py hoặc main.py

def generate_prediction(life_path: int, astro_data: dict):
    # === BƯỚC 1: TẠO DICTIONARY RIÊNG CHO TÍNH CÁCH (CHARACTER) ===
    # Đây là dữ liệu tĩnh, mô tả bản chất của con số
    characters = {
       1: "You are a pioneer, a leader, independent, and full of personality.",
2: "You are a collaborator and a mediator, always seeking balance and harmony.",
3: "You are a creative person, with the ability to inspire and spread joy.",
4: "You are systematic and practical, the solid foundation for any plan.",
5: "You are a freedom lover who enjoys experiences and is not afraid of change.",
6: "You are a nurturer, full of love and responsible towards your family.",
7: "You are an intellectual, introspective person, always seeking truth and deep meaning.",
8: "You have leadership qualities, are skilled at financial management, and are full of ambition.",
9: "You are a humanitarian, compassionate, and always think for the benefit of the community.",
11: "You are a spiritual master, possessing sharp intuition and the ability to inspire.",
22: "You are a master builder, capable of turning grand dreams into reality."  }

    # === BƯỚC 2: TẠO DICTIONARY RIÊNG CHO DỰ ĐOÁN HÀNG NGÀY (PREDICTION) ===
    # Đây là dữ liệu động, là lời khuyên cho "hôm nay"
    daily_predictions = {
       1: "Today, be bold and start a new project or make an important decision.",
    2: "Take time to listen and connect with those around you. Collaboration will bring good results.",
    3: "Don't hesitate to express your creative ideas. Communication is the key to success today.",
    4: "Focus on organizing your work. Attention to detail will help you avoid mistakes.",
    5: "An unexpected opportunity may arise. Be open to it and be ready for a short trip.",
    6: "Pay attention to your family and loved ones. A small act of care can make a big difference.",
    7: "Spend some quiet time reading or reflecting. You will find the answers from within.",
    8: "This is a good time to review your financial or career plans. Be confident in your abilities.",
    9: "Finish any pending tasks. Giving or helping others will bring you joy.",
    11: "Trust your intuition; it will guide you today. Your words carry great influence.",
    22: "Take the first step to realize a big plan. Don't shy away from tasks that require persistence."   }
    
    # Các phần khác của hàm vẫn giữ nguyên
    moon_phase_advice = {
        "New Moon": "This is a time for new beginnings. Set your intentions for the cycle ahead.",
        "Waxing Crescent": "Nurture your budding ideas. The first steps are crucial for growth.",
        "First Quarter": "Challenges may arise, pushing you to take decisive action. Stay focused.",
        "Waxing Gibbous": "Refine your plans and adjust your course. Momentum is building.",
        "Full Moon": "Emotions may be high. It's a time for illumination, completion, and celebrating progress.",
        "Waning Gibbous": "Share your wisdom or express gratitude. It's a good time for giving back.",
        "Last Quarter": "Release what no longer serves you. Let go of old habits to make space for the new.",
        "Waning Crescent": "It's time to rest and recharge. Surrender and prepare for the new cycle."
    }
    
    current_phase = astro_data['moon_phase']
    advice_for_phase = moon_phase_advice.get(current_phase, "Pay attention to the natural cycles around you.")
    moon_advice = f"With the Moon in its {current_phase} phase, {advice_for_phase}"
    colors = {1: "Wine Red", 2: "Orange", 3: "Butter Yellow", 4: "Green gotu kola", 5: "Sky Blue", 6: " indigo blue", 7: "Violet", 8: "Baby Pink", 9: "Golden", 11: "Sliver", 22: "Pure White"}
    keywords_map = {
        1: ["Sun", "Solar Flare"], 2: ["Moon", "Earthrise"], 3: ["Jupiter", "Gas Giant"], 4: ["Earth", "Terra"],
        5: ["Mercury", "Solar System"], 6: ["Venus", "Morning Star"], 7: ["Neptune", "Deep Space"], 8: ["Saturn", "Planet Rings"],
        9: ["Galaxy", "Milky Way"], 11: ["Nebula", "Pillars of Creation"], 22: ["Andromeda Galaxy", "Cosmos"]
    }
    keyword_list = keywords_map.get(life_path, ["star", "space", "hubble"])
    prediction_keyword = random.choice(keyword_list)

    # === BƯỚC 3: TẠO DỮ LIỆU TRẢ VỀ VỚI 2 KEY RIÊNG BIỆT ===
    prediction_data = {
        "life_path_number": life_path,
        "character_description": characters.get(life_path, "A soft-lonely soul"), # Key mới
        "daily_advice": daily_predictions.get(life_path, "Will you all the best luck!"), # Key cũ với nội dung mới
        "lucky_color": colors.get(life_path, "Rainbow"),
        "astronomical_insight": moon_advice
    }
    
    return prediction_data, prediction_keyword
def search_nasa_image(keyword: str):
    """
    Tìm kiếm hình ảnh trên NASA Image Library và trả về một URL ngẫu nhiên.
    """
    fallback_image_url = "https://trek.nasa.gov/tiles/Moon/EQ/LRO_WAC_Mosaic_Global_303ppd_v02/1.0.0/default/default028mm/0/0/0.jpg"
    
    try:
        # media_type=image để đảm bảo chỉ tìm kiếm hình ảnh
        search_url = f"https://images-api.nasa.gov/search?q={keyword}&media_type=image"
        response = requests.get(search_url)

        if response.status_code == 200:
            data = response.json()
            # Lấy danh sách các kết quả tìm thấy
            image_items = data.get("collection", {}).get("items", [])
            
            if not image_items:
                print(f"Không tìm thấy ảnh nào cho từ khóa: '{keyword}'. Dùng ảnh mặc định.")
                return fallback_image_url

            # Chọn một ảnh ngẫu nhiên từ danh sách
            random_item = random.choice(image_items)
            
            # Lấy URL của ảnh (thường là link đầu tiên)
            image_url = random_item.get("links", [{}])[0].get("href", fallback_image_url)
            return image_url
        else:
            print(f"Lỗi khi gọi NASA Image API: {response.status_code}")
            return fallback_image_url
            
    except requests.RequestException as e:
        print(f"Lỗi kết nối tới NASA Image API: {e}")
        return fallback_image_url
    


# --- 3. Create an endpoint to serve the HTML page ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # The 'request' object is required by TemplateResponse
    return templates.TemplateResponse("index.html", {"request": request})


# --- 4. API endpoint for predictions (the URL is now relative) ---
@app.post("/predict")
def predict_day(user_input: UserInput):
    life_path_number = calculate_life_path(user_input.birthdate)
    astro_data = get_astro_data() # Hàm này giờ chỉ cần lấy dữ liệu thiên văn, không cần APOD
    
    # Lấy dữ liệu và từ khóa từ hàm generate_prediction
    prediction_data, keyword = generate_prediction(life_path_number, astro_data)
    
    # Dùng từ khóa để tìm ảnh mới
    image_url = search_nasa_image(keyword)
    
    # Tạo phản hồi cuối cùng
    final_response = {
        **prediction_data,
        "prediction_image_url": image_url # Gửi URL ảnh mới về frontend
    }
    
    return final_response

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
# A new, stable fallback image from NASA's Webb Telescope gallery
