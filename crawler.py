from bs4 import BeautifulSoup
import requests
import pymongo
client =pymongo.MongoClient('mongodb://localhost:27017')
db = client['HoundHunt']
collection = db['webscraped']


urls = ['https://www.javatpoint.com']

counter = 0




for url in urls:
    counter = counter + 1

    if counter==5:
        break

    r = requests.get(url)
    htmlcontent = r.content
    soup = BeautifulSoup(htmlcontent,'html.parser')



    anchod = soup.find_all('a')
    with open('links.txt','a') as lol:
        for link in anchod:
            if link==None:
                continue
            if (('http' in link.get('href')) or ('https' in link.get('href'))):
                lol.write('\n' + link.get('href'))
                urls.append(link.get('href'))
                # print(link.get('href'))
                r = requests.get(link.get('href'))
                htmlcontent = r.content
                soup = BeautifulSoup(htmlcontent,'html.parser')
                title = soup.find('h1')
                mydict = {'url':link.get('href'),'title':str(title.text),'html':soup}
                collection.insert_one(mydict)
            else:
                a = url +link.get('href')
                r = requests.get(a)
                htmlcontent = r.content
                soup = BeautifulSoup(htmlcontent,'html.parser')
                title = soup.find('h1')
                lol.write('\n' + url +link.get('href'))
                urls.append(url +link.get('href'))
                mydict = {'url':str(a),'title':str(title.text) if title is not None else '', 'html':soup.prettify()}
                collection.insert_one(mydict)    


    urls.remove(url)