from fastapi import FastAPI
from typing import List
import uvicorn
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.pipelines.prediction_pipeline import PredictData,Matchstat
from fastapi import Request,Form


# Initialize the FastAPI app
app = FastAPI()

templates = Jinja2Templates(directory="templates")
@app.get("/predict", response_class=HTMLResponse)
async def get_predict(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def post_predict(
    request: Request,
    currentscore: int = Form(...),
    battingteam: str = Form(...),
    bowlingteam: str = Form(...),
    remainingovers: float = Form(...),
    remainingwickets: int = Form(...),
    runrate: float = Form(...),
    requiredrunrate: float = Form(...)
):
   stat = Matchstat(
        currentscore=currentscore,
        battingteam=battingteam,
        bowlingteam=bowlingteam,
        remainingovers=remainingovers,
        remainingwickets=remainingwickets,
        runrate=runrate,
        requiredrunrate=requiredrunrate
    )
   pred_df=stat.get_data_as_dataframe()

   model=PredictData()
   result=model.predict(pred_df)
   if result==1:
       result=battingteam
   else:
       result=bowlingteam

    
   return templates.TemplateResponse("home.html", {"request": request, "result": result})
       

teams = [
    'Kolkata Knight Riders', 'Chennai Super Kings', 'Delhi Capitals',
    'Royal Challengers Bangalore', 'Rajasthan Royals', 'Punjab Kings',
    'Sunrisers Hyderabad', 'Mumbai Indians', 'Gujarat Titans',
    'Lucknow Super Giants'
]
@app.get("/get_teams",response_model=List[str])
def get_teams():
     return teams




if __name__=='__main__':

     uvicorn.run(app, host="0.0.0.0", port=8000)
  