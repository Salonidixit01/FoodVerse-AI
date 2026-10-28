from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from pathlib import Path
import os

app = FastAPI(title="FoodVerse AI API", version="1.0.0", description="Multimodal food intelligence prototype API")
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in origins], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
LIMITS = {"image": 10*1024*1024, "video": 50*1024*1024, "audio": 20*1024*1024}

class CookingRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    ingredients: str = Field(default="", max_length=2000)
class MealPlanRequest(BaseModel):
    goal: str = "Balanced eating"
    dietary_preference: str = "No restrictions"
    daily_calorie_target: int = Field(default=2000, ge=1200, le=3200)

async def read_file(file: UploadFile, kind: str):
    data = await file.read(LIMITS[kind]+1)
    if not data: raise HTTPException(400, "Uploaded file is empty.")
    if len(data)>LIMITS[kind]: raise HTTPException(413, f"File exceeds {LIMITS[kind]//(1024*1024)} MB limit.")
    return data

@app.get("/")
def root(): return {"name":"FoodVerse AI API","status":"ok","docs":"/docs"}
@app.get("/health")
def health(): return {"status":"ok","mode":"demo","note":"Model providers are not configured; outputs are clearly labelled demonstration responses."}
@app.get("/api/capabilities")
def capabilities():
    return {"food_recognition":"demo","nutrition":"illustrative estimates","freshness":"demo","hygiene_video":"demo","audio":"upload acknowledgement","cooking":"template assistant","meal_planning":"rule-based sample"}

@app.post("/api/food/analyze")
async def food(file: UploadFile=File(...)):
    data=await read_file(file,"image")
    try: Image.open(BytesIO(data)).verify()
    except (UnidentifiedImageError,OSError): raise HTTPException(400,"Please upload a valid image.")
    name=Path(file.filename or "").stem.lower()
    options={"pizza":("Pizza",285,12,36,10),"salad":("Mixed salad",180,5,20,9),"apple":("Apple",95,0,25,0),"burger":("Burger",520,26,48,25),"pasta":("Pasta",430,14,62,12)}
    item=next((v for k,v in options.items() if k in name),("Mixed meal",420,18,54,14))
    dish,kcal,protein,carbs,fat=item
    return {"title":"Food recognition & nutrition","summary":f"Generic demonstration estimate for possible {dish.lower()}; the uploaded pixels were not analyzed by an AI model.","detected_items":[dish],"nutrition":{"calories":kcal,"protein_g":protein,"carbohydrates_g":carbs,"fat_g":fat,"health_score":82},"findings":["Portion size, oil, toppings and hidden ingredients can change nutrition."],"recommendations":["Confirm ingredients and serving size.","Aim for a varied plate with vegetables, protein and appropriate portions."],"demo_mode":True}

@app.post("/api/freshness/analyze")
async def freshness(file: UploadFile=File(...)):
    data=await read_file(file,"image")
    try: Image.open(BytesIO(data)).verify()
    except (UnidentifiedImageError,OSError): raise HTTPException(400,"Please upload a valid image.")
    return {"title":"Freshness screening","summary":"Demo response; image pixels were not assessed. Appearance cannot rule out pathogens or toxins.","freshness":{"classification":"Moderately Fresh","confidence":"Demo only — no visual model configured"},"findings":["Check storage temperature, use-by dates, smell, texture and packaging."],"recommendations":["Follow food-specific storage guidance.","When in doubt about food safety, discard suspicious food; do not taste-test it."],"demo_mode":True}

@app.post("/api/hygiene/analyze")
async def hygiene(file: UploadFile=File(...)):
    data=await read_file(file,"video")
    if not ((file.content_type or "").startswith("video/") or (file.filename or "").lower().endswith((".mp4",".mov",".webm",".m4v"))): raise HTTPException(400,"Upload an MP4, MOV, WebM or M4V video.")
    return {"title":"Kitchen hygiene review","summary":"Demo-only report; no video frames were analyzed.","hygiene_indicators":{"glove_usage":"Not assessed — model not configured","hair_covering":"Not assessed — model not configured","food_handling":"Not assessed — model not configured","surface_cleanliness":"Not assessed — model not configured","cross_contamination":"Not assessed — model not configured"},"findings":["Review footage manually and verify context.","Use a documented hygiene checklist and local food safety rules."],"recommendations":["Separate raw and ready-to-eat foods.","Clean food-contact surfaces and ensure handwashing and appropriate hair restraints."],"demo_mode":True,"file_size_bytes":len(data)}

@app.post("/api/audio/analyze")
async def audio(file: UploadFile=File(...)):
    data=await read_file(file,"audio")
    return {"title":"Audio insight","summary":"Audio upload received; speech recognition is not configured.","transcription":None,"findings":["No transcription or acoustic analysis was performed."],"recommendations":["Configure a trusted speech-to-text provider to enable transcript-based assistance."],"demo_mode":True,"file_size_bytes":len(data)}

@app.post("/api/cooking/assistant")
def cooking(body: CookingRequest):
    ingredients=[x.strip() for x in body.ingredients.split(",") if x.strip()]
    if ingredients:
        answer=f"Flexible idea using {', '.join(ingredients[:12])}: cook grains or legumes according to package instructions, wash and chop produce, then sauté or steam until appropriate. Combine and season with herbs, lemon or spices. Avoid cross-contamination and follow food-specific safe cooking guidance. Tell me your time limit and equipment to tailor the steps."
    else: answer="Tell me your ingredients, time limit and dietary preferences and I can suggest a simple recipe."
    return {"answer":answer,"demo_mode":True}

@app.post("/api/meal-plan")
def meal_plan(body: MealPlanRequest):
    target=body.daily_calorie_target; pref=body.dietary_preference.lower()
    if "vegan" in pref:
        dishes=["Oats with plant milk, fruit and seeds","Lentil, grain and vegetable bowl","Fruit and roasted chickpeas","Tofu or bean stir-fry"]
    elif "vegetarian" in pref:
        dishes=["Oats with yoghurt and fruit","Rice, lentils and mixed vegetables","Fruit and nuts","Paneer or chickpea vegetable bowl"]
    else:
        dishes=["Oats with yoghurt and seasonal fruit","Whole grains with lentils, vegetables and protein","Fruit and nuts","Vegetable bowl with beans, tofu, eggs or preferred protein"]
    meals=[{"meal":name,"dish":dish,"calories":round(target*pct)} for name,dish,pct in zip(["Breakfast","Lunch","Snack","Dinner"],dishes,[.25,.35,.1,.3])]
    return {"title":f"{body.goal} · sample day","daily_calories":target,"meals":meals,"note":"Illustrative calorie allocation, not a prescribed diet; actual nutrition depends on recipe and serving size.","demo_mode":True}
