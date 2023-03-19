from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests


app = FastAPI()
@app.post("/search/{keyword}")
async def search(keyword):
              l=[]#+ads(keyword)
              o={}
              headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

              target_url="https://www.bing.com/search?q="+keyword+"&rdr=1&first={}".format(1)
                  #print(target_url)
              resp=requests.get(target_url,headers=headers)
              soup = BeautifulSoup(resp.text, 'html.parser')
              completeData = soup.find_all("li",{"class":"b_algo"})
              for data in completeData:

                       o["Title"]=data.find("a").text
                       o["link"]=data.find("a").get("href")
                       discrip = data.find("div", {"class":"b_caption"}).text.split("·")[-1]
                       o["Description"] = discrip.split(" ",1)[-1]

                       if len(discrip)>50:
                          l.append(o)
                       o={}

                     
              return {"results":l}
# for run the api uvicorn search_result_api:app
