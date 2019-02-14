import json
import tempfile
import requests
import bs4
from random import randint


class ImageScraper:
    
    def __init__(self, text):
        self.text = text
        self.header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                     "Chrome/43.0.2357.134 "
                                     "Safari/537.36 ",
                       }

    def _get_images(self, query):
        if query == "":
            raise ValueError("No empty string allowed")
        query = query.replace(" ", "+")
        random_start = randint(0, 10) * 100
        resp = requests.get(
            "https://www.google.com/search?yv=3&tbm=isch&q=" + query + "&start=" + str(random_start) +
            "&asearch=ichunk&async=_id:rg_s,_pms:s,_fmt:pc",
            headers=self.header)
        if resp.status_code == 200:
            soup = bs4.BeautifulSoup(resp.content, "html.parser")
            rs = soup.find_all("div", {"class": "rg_meta"})
            self.text.append("Found All Images Link")
            return rs
        self.text.append("Response was " + str(resp.status_code) + str(resp.text))
        return None

    def _request_image(self, image_link):
        return requests.get(image_link, headers=self.header)

    def get_random_image_of(self, query):
        if query == "":
            raise ValueError("No empty string allowed")
        result = self._get_images(query)
        div_value = result[randint(0, (len(result) - 1))].text

        random_img_link, extension = json.loads(div_value)["ou"], json.loads(div_value)["ity"]
        tmp_img = tempfile.TemporaryFile(delete=False, suffix="." + extension)
        resp = self._request_image(random_img_link)
        for chunk in resp:
            tmp_img.write(chunk)
        return tmp_img
