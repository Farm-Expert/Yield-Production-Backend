from fastapi import FastAPI
from pydantic import BaseModel
import requests
from PIL import Image
import google.generativeai as genai

app=FastAPI()
genai.configure(api_key="AIzaSyCzdI-Itcf8eSbrg8IHeNTfOhzeqkDKTg4")


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
vision=genai.GenerativeModel("gemini-pro-vision")

def read(text):
    res=""
    for chunks in text:
        chunks.text.replace('*','')
        res=res+ chunks.text
    return res
def viewmodel(text,img):
    try:
        res=vision.generate_content([text,img])
        res.resolve()
        return {"Success":read(res)}
    except Exception as e:
        print(e)
        return {"Error": "Harmfull words found in chat"}

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
    res=viewmodel(infor,imgurl)
    return res


