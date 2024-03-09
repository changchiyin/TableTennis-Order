import requests
import uvicorn
from bs4 import BeautifulSoup
from fastapi import FastAPI
from pydantic import BaseModel


class Detail(BaseModel):
    url: str


# noinspection PyTypeChecker
def get_information(url):
    web = requests.get(url)
    soup = BeautifulSoup(web.text, 'lxml')
    detail_name = soup.find('td', {'class': 'detail_name'}).getText()
    detail_price = int("".join(filter(str.isdigit, soup.find('td', {'class': 'detail_price'}).getText())))
    # noinspection PyTypeChecker
    detail_option = []
    if soup.select_one('select[name="spcode"]') is not None:
        options = soup.select_one('select[name="spcode"]').select('option')
        if len(options) > 0:
            for i in range(2, len(options)):
                detail_option.append(options[i].string)
    return dict(detail_name=detail_name, detail_price=detail_price, detail_option=detail_option)


app = FastAPI()


@app.post("/")
async def search_detail(detail: Detail):
    return get_information(detail.url)


if __name__ == '__main__':
    uvicorn.run(app)
