import os
import traceback
import csv
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Zooshop, Base
from .utils import write_error, write_log


class ZooshopHandler:
    def __init__(self):
        engine = create_engine(os.environ.get('DB'))
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.db_sess = sessionmaker(engine)
        print('ZooshopHandler initiallzed successfully')
    
    def add_shop(self, shop: dict):
        with self.db_sess() as sess:
            try:
                new_shop = Zooshop(
                    on_page_order_number = shop['on_page_order_number'],
                    shop_name = shop['shop_name'],

                    description = shop['description'],
                    phone = shop['phone'],
                    website = shop['website'],
                    address = shop['address'],
                    how_to_get = shop['how_to_get'],

                    page_number = shop['page_number'],
                )
                sess.add(new_shop)
                sess.commit()
            except Exception as err:
                sess.rollback()
                msg = f'{"*"*10}\n'
                msg += f'{err}\n'
                msg += f'{traceback.format_exc()}\n'
                print(msg)
                write_log(msg)

    def add_shops(self, shops: list[dict], url: str):       
        if len(re.split(r'/\d+/', url)) == 1:
            page_number = 1
        else:
            page_number = int(url.rsplit('/', 1)[0].rsplit('/', 1)[1])
        for shop in shops:
            shop['page_number'] = page_number
            self.add_shop(shop)

    
    def load_out_csv(self, file_path):
        with self.db_sess() as sess:
            shops: list[Zooshop] = sess.query(Zooshop)\
                .order_by(Zooshop.page_number, Zooshop.on_page_order_number).all()
        
        header = ['page_number', 'on_page_order_number', 'shop_name', 'phone', 'website', 'address', 'description']
        with open(file_path, 'w', encoding='utf-8') as f:    
            writer = csv.writer(f, delimiter ='\t')
            
            writer.writerow(header) 
            for shop in shops:
                writer.writerow((
                    shop.page_number,
                    shop.on_page_order_number,
                    shop.shop_name,
                    shop.phone,
                    shop.website,
                    shop.address,
                    shop.description
                ))





