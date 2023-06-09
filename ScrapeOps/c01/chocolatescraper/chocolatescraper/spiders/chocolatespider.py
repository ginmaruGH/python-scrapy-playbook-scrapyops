import scrapy

class ChocolatespiderSpider(scrapy.Spider):

    # spiderの名前
    name = 'chocolatespider'

    # the url of the first page that we will start scraping
    # スクレイピングを開始する最初のページのURL
    start_urls = ['https://www.chocolate.co.uk/collections/all']

    def parse(self, response):

        # here we are looping through the products and extracting the name, price & url
        # 商品をループして、名前、価格、URLを抽出
        products = response.css('product-item')
        for product in products:
            # here we put the data returned into the format we want to output for our csv or json file
            # 返されたデータをcsvファイルやjsonファイルに出力したい形式に変換
            yield{
                'name' : product.css('a.product-item-meta__title::text').get(),
                'price' : product.css('span.price').get().replace('<span class="price">\n              <span class="visually-hidden">Sale price</span>','').replace('</span>',''),
                'url' : product.css('div.product-item-meta a').attrib['href'],
            }

        # next pageを取得
        next_page = response.css('[rel="next"] ::attr(href)').get()

        if next_page is not None:
            next_page_url = 'https://www.chocolate.co.uk' + next_page
            yield response.follow(next_page_url, callback=self.parse)
