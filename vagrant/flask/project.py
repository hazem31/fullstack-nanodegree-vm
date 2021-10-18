
from flask import Flask , render_template , redirect , url_for , flash , jsonify
from flask.globals import request
app = Flask(__name__)

from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine

DBsession = sessionmaker(bind=engine)
session = DBsession()


@property
def serialize(self):
    return {'name' : self.name , 'description' : self.description , 'id' : self.id , 'price' : self.price , 'course' : self.course}

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def RestaurantMenu(restaurant_id) :
    restaurant = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return render_template('menu.html' , restaurant = restaurant , items = items)



@app.route('/restaurants/<int:restaurant_id>/new',methods = ['GET',"POST"])
def newMenuItem(restaurant_id):
    if request.method == "POST":
        item = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
        session.add(item)
        session.commit()
        flash("New Item added")
        return redirect(url_for('RestaurantMenu',restaurant_id = restaurant_id))
    else:
        return render_template('newmenu.html',restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash('Item is updated')
        return redirect(url_for('RestaurantMenu', restaurant_id=restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)


# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete' , methods=['GET' ,'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == "POST":
        session.delete(menuItem)
        session.commit()
        flash("item is deleted")
        return redirect(url_for('RestaurantMenu',restaurant_id = restaurant_id))
    else:
        return render_template('deletemenuitem.html',item = menuItem)


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def RestaurantMenuJSON(restaurant_id) :
    restaurant = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def RestaurantMenuItemJSON(restaurant_id,menu_id) :
    restaurant = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItems=[items.serialize ])



if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host= '0.0.0.0' , port=5000)
