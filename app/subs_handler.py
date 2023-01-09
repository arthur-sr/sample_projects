import traceback
import os
from datetime import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

from .models import Subscriber, Base
from .utils import write_log, write_error


class SubsHandler:
    '''Subscribers database handler'''
    def __init__(self):
        engine = create_engine(os.environ.get('DATABASE'))  
        Base.metadata.create_all(engine)
        self.db_sess = sessionmaker(engine)


    def add_sub(self, sub_info):
        '''Tries to insert new subsciber into a database'''
        
        with self.db_sess() as sess:
            try:
                new_sub = Subscriber(
                    user_id = sub_info['user_id'],
                    username = sub_info['username']
                )
                sess.add(new_sub)
                sess.commit()
                write_log(f'Added sub {sub_info["user_id"]}')
            except IntegrityError as err:
                msg = f'User {sub_info["user_id"]} already in database'
                print(msg)
                write_error(msg)
                sess.rollback()
            except Exception as err:
                print('Unexpected errors has occured. See Logs/errors.log')
                write_error(f"{10*'*'}")
                write_error(err)
                write_error(traceback.format_exc())
                sess.rollback()

    def get_subs(self): 
        '''Returns subs one by one'''
        with self.db_sess() as sess:
            for sub in sess.query(Subscriber).order_by(Subscriber.added).yield_per(1):
                yield sub
    
    def get_sub_by_username(self, username: int)->Subscriber:
        if username:
            with self.db_sess() as sess:
                return sess.query(Subscriber).where(Subscriber.username==username).one()
    


