import requests
import lxml.html

base_url = 'https://rabota.ua'


class JobsUa:
    def __init__(self,base_url):
        self.base_url = base_url
    

    def get_info(self):
        page = 1
        flag = True
        cards = []
        while flag:
            url = '{0}/ровно?parentId=1&pg={1}'.format(self.base_url,page)
            rez = requests.get(url)
            if rez.status_code==200:
                dom = lxml.html.fromstring(rez.text)
                divs = dom.xpath("//article[@class='card']")
                flag = len(divs)!=0

                for div in divs:

                    a_s = div.xpath('div[@class="card-body"]//p[@class="card-title"]/a')
                    div_bs = div.xpath('div[@class="card-body"]//span[@class="salary"]')
                    times = div.xpath('div[@class="card-footer"]/div')
                    kompani_divs = div.xpath('div[@class="card-body"]//p[@class="company-name"]')
                    for a,div_b,time,kompani_div in zip(a_s,div_bs,times,kompani_divs):
                        kompani = kompani_div.xpath('a')
                        if kompani:
                            kompani = kompani[0]
                        cards.append(
                                {
                                    'link':self.base_url+a.attrib.get('href'),
                                    'title':a.text_content(),
                                    'kompani':kompani.text_content(),
                                    'sel':div_b.text_content(),
                                    'time':time.text_content()
                                }
                        )
            
            else:
                return('Error', rez.status_code)

            page = page + 1

        return cards

work = JobsUa('https://rabota.ua')
print(work.get_info())
