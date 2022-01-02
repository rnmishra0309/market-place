from flask import render_template, request, redirect, url_for, flash
from com import app
from com.models import ItemsDB, UsersDB, DB
from com.forms import RegisterForm, LoginForm, PurchaseForm
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseForm(request.form)
    if request.method == "POST":
        purchased_item = request.form.get('purchased_item')
        p_item_object = ItemsDB.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category='danger')

        return redirect(url_for('market_page'))
    if request.method == "GET":
        items = ItemsDB.query.filter_by(owner=None)
        field_names = ['id', 'name', 'price', 'barcode']
        return render_template('market.html',field_names=field_names, items_list=items, purchase_form=purchase_form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        attempted_user = UsersDB.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as {attempted_user.username}', category="success")
            return redirect(url_for('market_page'))
        else:
            flash(f'Username and Password is wrong!!', category="danger")
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        new_user = UsersDB(username=form.username.data,
                           email=form.email.data, password=form.password.data)
        DB.session.add(new_user)
        DB.session.commit()
        login_user(new_user)
        flash(f'Success! You are logged in as {new_user.username}', category="success")
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f'Errors: {err}', category='danger')
    return render_template('register.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You are logged out!!", category='info')
    return redirect(url_for('home_page'))