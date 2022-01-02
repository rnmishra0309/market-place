from com.models import DB, ItemsDB, UsersDB

ITEMS = [
    {'name': 'Phone', 'barcode': '893212299897', 'price': 500, 'description':'a phone'},
    {'name': 'Laptop', 'barcode': '123985473165', 'price': 900, 'description':'a laptop'},
    {'name': 'Keyboard', 'barcode': '231985128446', 'price': 150, 'description':'a keyboard'}
]

USERS = [
    {'username': 'rudra', 'email': '123@g.com', 'password_enc': '12345', 'budget': 1000},
    {'username': 'rudraNM', 'email': '123NM@g.com', 'password_enc': '123456', 'budget': 1000}
]

def drop_db():
    global DB
    DB.drop_all()

def initialize_db():
    global DB
    DB.create_all()

def add_elements_ITEMSDB(item_dict):
    global DB, ItemsDB
    result = ItemsDB(name=item_dict['name'], price=item_dict['price'],
                     barcode=item_dict['barcode'], description=item_dict['description'])
    DB.session.add(result)
    DB.session.commit()

def add_elements_USERSDB(user_dict):
    global DB, UsersDB
    result = UsersDB(username=user_dict['username'], email=user_dict['email'], 
                     password_enc=user_dict['password_enc'], budget=user_dict['budget'])
    DB.session.add(result)
    DB.session.commit()

def show_db_elements():
    global ItemsDB, UsersDB
    item_list = []
    for item in ItemsDB.query.all():
        item_list.append((item.name, item.barcode))
    print(f"The DB Contents Are: \n{item_list}")

    user_list = []
    for item in UsersDB.query.all():
        user_list.append(item.username)
    print(f"The DB Contents Are: \n{user_list}")

if __name__=="__main__":    
    drop = input("Do you want to drop all DB?\n press 1 else press any other key: ")
    if drop == '1':
        drop_db()

    initialize_db()

    for item in ITEMS:
        add_elements_ITEMSDB(item)
    
    for item in USERS:
        add_elements_USERSDB(item)

    show_db_elements()
