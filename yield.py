from fastapi import FastAPI
from pydantic import BaseModel
import requests
from PIL import Image
from gemz_api import test

app=FastAPI()

class User(BaseModel):
    imgurl:str
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float
    label:str
@app.get("/")
def index():
    return "welcome in yield production"

# take user input for yield production:


@app.post("/yield")
def yieldprod(data:User):
    data_in = [[
        data.N, data.P, data.K, data.temperature,
        data.humidity, data.ph, data.rainfall,data.label
    ]]
    imgurl=data.imgurl
    print(imgurl)
    if(len(imgurl)>6 and imgurl[:6]=="https:"):
        imgurl=requests.get(imgurl)
        image_blob = imgurl.content

        with open('yieldimg.jpg', 'wb') as f:
            f.write(image_blob)
        imgurl='yieldimg.jpg'
    imgurl = Image.open(imgurl)

    infor=str(data_in)+"'Now you are a expert of soil crops yield production I will provide you data related to crops and you have to analysis it and give me accurate result:'I will provide you image of crops and details of all soil elements like[Nitrogen, Phosphorus, Potassium, Temperature , Humidity, rainfall, ph-value, Crop Name] analysis all the condition and predict the  production of crops in quintles in a specific range."
    # create imgblob
    res=test.viewmodel(infor,imgurl)
    return res


