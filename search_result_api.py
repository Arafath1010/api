from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests, lxml


app = FastAPI()
@app.post("/search/{keyword}")
async def search(keyword):
       l=[]
       o={}
       headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
       for i in range(1,41,10):
              #print(i)
         try:
              target_url="https://www.bing.com/search?q="+keyword+"&rdr=1&first={}".format(i)
                  #print(target_url)
              resp=requests.get(target_url,headers=headers)
              soup = BeautifulSoup(resp.text, 'html.parser')
              completeData = soup.find_all("li",{"class":"b_algo"})
              for data in completeData:
                       count = 0
                       o["Title"]=data.find("a").text
                       o["link"]=data.find("a").get("href")
                       if "/" == str(data.find("a").get("href"))[-1]:
                            description = (data.find("div", {"class":"b_caption"}).text.replace(str(data.find("a").get("href"))[:-1],"")).split("...",1)
                            #print(len(description))
                            if "https://" in description[0]:
                               o["Description"]= description[1]
                               count = len(description[1])
                            else:
                               o["Description"]= description[0]
                               count = len(description[0])

                       else:
                            
                            description =(data.find("div", {"class":"b_caption"}).text.replace(str(data.find("a").get("href")),"")).split("...",1)
                            #print(len(description))
                            if "https://" in description[0]:
                               o["Description"]= description[1]
                               count = len(description[1])
                            else:
                               o["Description"]= description[0]
                               count = len(description[0])
                       if count>70:
                          l.append(o)
                       o={}
         except:
               continue
                     
       return {"results":l}
# for run the api uvicorn search_result_api:app
