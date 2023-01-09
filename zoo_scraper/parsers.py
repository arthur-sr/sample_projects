import re

class ItemContainer:
    def __init__(self, container_html: str):
        self.container = container_html
    
    def get_on_page_order_number(self):
        return int(self.container.split('<span class="order-number">', 1)[1].split('.', 1)[0].strip(' \n\r'))

    def get_shop_name(self):
        shop_name = re.split(r'<span class="order-number">\d+. </span>', self.container, 1)[1].split('<', 1)[0].strip(' \n\r')
        return shop_name.replace('&quot;', "'").replace('&#171;','«').replace('&#187;', '»')
        #return shop_name

    def get_description(self):
        try: 
            return self.container.split('<div class="similar-item__description">', 1)[1].split('</div>')[0].strip(' \n\r')
        except:
            return ''
    
    def get_phone(self):
        try:
            return self.container.split('<div class="phone ">')[1].split('</div>', 1)[0].strip(' \n\r')
        except:
            return ''
    
    def get_website(self):
        try:
            return self.container.split('<div class="site">')[1].split('</div>', 1)[0].strip(' \n\r')
        except:
            return ''

    def get_address(self):
        try:
            return self.container.split('<div class="similar-item__adrss-item">')[1].split('</div>', 1)[0].strip(' \n\r')
        except:
            return ''


class Zoopage:
    def __init__(self, page_html: str):
        self.page = page_html   
    
    def get_shops(self):
        rubricator_result = self.page.split('id="rubricator-result"', 1)
        if len(rubricator_result) > 1:
            rubricator_result = rubricator_result[1]
            rubricator_result = rubricator_result.rsplit('class="gradient selected_site"', 1)[0]
        else:
            rubricator_result = self.page
        
        containers = rubricator_result.split('class="similar-item__container"')[1:]

        shops = []
        for container_html in containers:
            container = ItemContainer(container_html)

            shops.append({
                'on_page_order_number': container.get_on_page_order_number(),
                'shop_name': container.get_shop_name(),
                'description': container.get_description(),
                'phone': container.get_phone(),
                'website': container.get_website(),
                'address': container.get_address(),
                'how_to_get': ''
            })
        
        return shops
    



