from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import app 
from app.forms import LogInForm, ReviewForm, SignUpForm
from app.models import User, Reviews

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('form submitted')
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(first_name, last_name, email, username, password)
        check_user = User.query.filter( (User.username == username) | (User.email == email) ).first()
        if check_user is not None:
            flash("User with that username or email already exists!", "danger")
            return redirect(url_for('signup'))
        new_user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        flash(f"{new_user} has successfully signed up!", "success")
        return redirect(url_for('reviews'))

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            flash(f'{user} is now logged in', 'success')
            return redirect(url_for('index'))
        else:
            flash('Incorrect username and/or password. Please try again', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'warning')
    return redirect(url_for('login'))



@app.route('/review', methods=['GET', 'POST'])
@login_required
def review():
    form = ReviewForm()
    if form.validate_on_submit():
        dealership_name = form.dealership_name.data
        dealership_address = form.dealership_address.data
        rating = form.rating.data
        msrp = form.msrp.data
        markup = form.markup.data
        sold = form.sold.data
        comment = form.comment.data
        new_review = Reviews(dealership_name=dealership_name, dealership_address=dealership_address, rating=rating, msrp=msrp, markup=markup, sold=sold, comment=comment, user_id=current_user.id)
        flash(f"Your review of {new_review} has been posted!", 'success')
        return redirect(url_for('reviews'))
    return render_template('review.html', form=form)


@app.route('/reviews')
def reviews():
    reviews = Reviews.query.order_by(Reviews.date_created.desc()).all()
    return render_template('reviews.html', reviews=reviews)


@app.route('/reviews/<review_id>')
def get_review(review_id):
    review = Reviews.query.get(review_id)
    return render_template('view.html', review=review)

@app.route('/reviews/<review_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    review = Reviews.query.get(review_id)
    if review.author != current_user:
        flash('You do not have permission to edit this review', 'danger')
        return redirect(url_for('reviews'))
    form = ReviewForm()
    if form.validate_on_submit():
        new_name = form.dealership_name.data
        new_address = form.dealership_address.data
        new_rating = form.rating.data
        new_msrp = form.msrp.data
        new_markup = form.markup.data
        new_sold = form.sold.data
        new_comment = form.comment.data
        review.update(dealership_name=new_name, dealership_address=new_address, rating=new_rating, msrp=new_msrp, markup=new_markup, sold=new_sold, comment=new_comment)
        flash(f"Your review of {review.dealership_name} has been updated", 'info')
        return redirect(url_for('reviews'))
    return render_template('edit.html', review=review, form=form)


@app.route('/reviews/<review_id>/delete')
@login_required
def delete_review(review_id):
    review = Reviews.query.get(review_id)
    if review.author != current_user:
        flash('You do not have permission to delete this review', 'danger')
        return redirect(url_for('reviews'))
    review.delete()
    flash(f"Your review of {review.dealership_name} has been deleted", 'info')
    return redirect(url_for('reviews'))