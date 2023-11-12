import scrapy


class wcgeSpider(scrapy.Spider):
    name = "wcge"
    start_urls = ["https://sol.sbc.org.br/index.php/wcge/issue/archive"]

    def parse(self, response):
        edicoes = response.xpath('//*[@class="obj_issue_summary"]')

        for edicao in edicoes:
            data_publicacao = edicao.xpath("/div/span[2]").get()
            evento_url = edicao.xpath(href)
            