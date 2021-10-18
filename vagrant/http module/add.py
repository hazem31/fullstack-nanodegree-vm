from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine

DBsession = sessionmaker(bind=engine)
session = DBsession()

Myrestaurant = Restaurant(name = 'Pizza palace')
session.add(Myrestaurant)
session.commit()
cheesepizza = MenuItem(name = 'Chesse Pizza',description = "made with natural ingridents" , course = "Entree" , price = "$9.88" , restaurant = Myrestaurant)

session.add(cheesepizza)
session.commit()