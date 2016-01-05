from sqlalchemy.orm import sessionmaker
from models import Cafes, db_connect, create_cafes_table

class ISnobPipeline(object):
    """Islamabadsnob pipeline for storing scraped data in database"""
    def __init__(self):
	
	engine = db_connect()
	create_cafes_table(engine)
	self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):

	session = self.Session()
	cafe = Cafes(**item)

	try:
	    session.add(cafe)
	    session.commit()
	except:
	    session.rollback()
	    raise
	finally:
	    session.close()

	return item


