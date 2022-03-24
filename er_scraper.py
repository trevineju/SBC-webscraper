import requests
from bs4 import BeautifulSoup
import pandas  

WES_LIST = pandas.DataFrame()

def crawler(pagecontent):    
    section = pagecontent.find_all(id="customers")[0]
    index = 0
    for item in list(section.find_all("td")):
        list_text = item.get_text().split(":")
        WES_LIST.loc[index, "sigla"] = list_text[0]
        WES_LIST.loc[index, "titulo"] = list_text[1]
        link = item.find_all('a')[0].get('href')
        WES_LIST.loc[index, "link"] = get_internal_link(link) 
        index += 1
            
        
def get_internal_link(link):
    page = requests.get(link)
    if online_check(page):
        pagecontent = BeautifulSoup(page.content, "html.parser")
        internal_link = (pagecontent.find_all("ul")[0]).find_all("a")[3].get('href')
        return internal_link
    

def online_check(request):
    if request.status_code == 200: return True
    return False
        

def main():
    page = requests.get("https://sol.sbc.org.br/index.php/anais/escolas")
    if online_check(page):  
        pagecontent = BeautifulSoup(page.content, "html.parser")
        crawler(pagecontent)
        

if __name__ == '__main__':
    main()