import scrapy

from sbcscraper.items import SBCitem


class SBCSpider(scrapy.Spider):
    name = "sbc_spider"
    base_url = "https://sol.sbc.org.br/index.php/-event-acronym-placeholder-/issue/archive"

    target_events = {
        # congressos
        "latinoware":"Congresso Latino-Americano de Software Livre e Tecnologias Abertas",
        "wit": "Mulheres em Tecnologia da Informação (WIT)",
        # encontros
        "eniac": "Encontro Nacional de Inteligência Artificial e Computacional",
        # trilhas
        "courb": "Workshop de Computação Urbana",      
        "vem": "Workshop de Visualização, Evolução e Manutenção de Software",
        "wcge": "Workshop de Computação Aplicada em Governo Eletrônico",
        "wics": "Workshop sobre as Implicações da Computação na Sociedade",
        "wide": "Workshop Investigações em Interação Humano-Dados",
        "wpci": "Workshop de Pensamento Computacional e Inclusão",
        "wtf": "Workshop de Testes e Tolerância a Falhas",
        "wtrans": "Workshop de Transparência em Sistemas",
        #simpósios
        "educomp":"Simpósio Brasileiro de Educação em Computação",
        "educomp_estendido":"Simpósio Brasileiro de Educação em Computação (estendido)",
        "sbqs":"Simpósio Brasileiro de Qualidade de Software",
        "sbqs_estendido":"Simpósio Brasileiro de Qualidade de Software (estendido)",
        "sbsi":"Simpósio Brasileiro de Sistemas de Informação",
        "sbsi_estendido":"Simpósio Brasileiro de Sistemas de Informação (estendido)",
        "sbsc":"Simpósio Brasileiro de Sistemas Colaborativos",
        "sbsc_estendido":"Simpósio Brasileiro de Sistemas Colaborativos (estendido)",
        "sbbd":"Simpósio Brasileiro de Bancos de Dados",
        "sbbd_estendido":"Simpósio Brasileiro de Bancos de Dados (estendido)",
        "stil":"Simpósio Brasileiro de Tecnologia da Informação e da Linguagem Humana",
    }
   
    def start_requests(self):
        for acronym in self.target_events.keys():
            event_url = self.base_url.replace("-event-acronym-placeholder-", acronym)
            yield scrapy.Request(event_url, cb_kwargs = dict(event=self.target_events[acronym]))

    def parse(self, response, event):
        editions_url = response.xpath('//*[@class="obj_issue_summary"]/a/@href').getall()

        for edition_url in editions_url:
            yield scrapy.Request(edition_url, callback=self.parsepage, cb_kwargs = dict(event=event))
    
    def parsepage(self, response, event):
        date = ''.join(response.xpath('//*[@class="published"]/span[2]/text()').get().split())
        
        titles = response.xpath('//*[@class="obj_article_summary"]//*[@class="title"]/a/text()').getall()
        authors = response.xpath('//*[@class="authors"]/text()').getall()
        file_urls = response.xpath('//*[@class="obj_galley_link pdf"]/@href').getall()

        for i in range(len(file_urls)):
            yield SBCitem(
                    evento = event,
                    titulo = titles[i].replace("\t", "").replace("\n", ""),
                    data = date,
                    autoria = authors[i].replace("\t", "").replace("\n", ""),
                    url = file_urls[i]
            )