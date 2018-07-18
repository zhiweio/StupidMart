# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from StupidMart.extensions import login_manager
from StupidMart.admin.models import User

blueprint = Blueprint('public', __name__, static_folder='../static/assets')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    """Home page."""
    # Handle logging in
    return render_template('/public/index.html')


def _validate_on_submit(user, password):
    # @param user - User type
    if not user:
        messages = 'Unknown username'
        return False, messages

    if not user.verify_password(password):
        messages = 'Invalid password'
        return False, messages

    # if not user.active:
    #     messages = 'User not activated'
    #     return False, messages

    return True, None


@blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    """Home page."""
    # Handle logging in
    if request.method == 'POST':
        username = request.form.get('username', 'null')
        password = request.form.get('password', 'null')
        user = User.query.filter_by(username=username).first()
        validated, messages = _validate_on_submit(user, password)
        if validated:
            login_user(user)
            redirect_url = request.args.get('next') or url_for('user.bills')
            return redirect(redirect_url)
        else:
            msg = {'msg': messages}
    return render_template('public/login.html', messages=msg)


@blueprint.route('/signin/', methods=['GET', 'POST'])
def signin():
    return render_template('public/login.html')


@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    return redirect(url_for('public.index'))


@blueprint.route('/about/')
def about():
    """About page."""
    return render_template('public/about.html')
