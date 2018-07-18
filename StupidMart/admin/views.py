# -*- coding: utf-8 -*-

# import json
from datetime import date, datetime

from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from flask_login import login_required

from StupidMart.admin.models import User, Role
from StupidMart.database import db
from StupidMart.decorators import admin_required

blueprint = Blueprint('admin', __name__, url_prefix='/admin',
                      static_folder='../static/assets')


# Add page
@blueprint.route('/add/', methods=['GET', 'POST'])
@login_required
@admin_required
def user_add():
    if request.method == 'POST':
        data = request.form
        user_sn = data.get('user_sn', None)
        username = data.get('username', None)
        password = data.get('password', None)
        confirm_password = data.get('confirm_password', None)
        gender = 0 if data.get('gender', 'man') == 'man' else 1
        birthday = data.get('birthday', '1970-01-01')
        telephone = data.get('telephone', None)
        address = data.get('address', None)
        role = data.get('role', 'User')

        if user_sn and username and password \
                and confirm_password and telephone and address:
            if password == confirm_password:
                # convert birthday type
                birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
                user = User(user_sn, username, password,
                            gender=gender, birthday=birthday,
                            telephone=telephone, address=address,
                            role=Role.query.filter_by(name=role).first())
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('admin.index'))
    return render_template('admin/userAdd.html')


# Add api
# --------------------------------------------------------
# TODO: 改前端代码，表单数据异步提交，页面访问与json 接口分离
# --------------------------------------------------------
# @blueprint.route('/api/add/', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def api_user_add():
#     if request.method == 'POST':
#         data = request.form
#         user_sn = data.get('user_sn', None)
#         username = data.get('username', None)
#         password = data.get('password', None)
#         confirm_password = data.get('confirm_password', None)
#         gender = 0 if data.get('gender', 'man') == 'man' else 1
#         birthday = data.get('birthday', '1970-01-01')
#         telephone = data.get('telephone', None)
#         address = data.get('address', None)
#         role = data.get('role', 'User')

#         if user_sn and username and password \
#                 and confirm_password and telephone and address:
#             if password == confirm_password:
#                 # convert birthday type
#                 birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
#                 user = User(user_sn, username, password,
#                             gender=gender, birthday=birthday,
#                             telephone=telephone, address=address,
#                             role=Role.query.filter_by(name=role).first())
#                 db.session.add(user)
#                 db.session.commit()
#                 messages = 'Add user successful.'
#                 status_code = 2   # FAILED
#             else:
#                 messages = 'Entered passwords differ.'
#                 status_code = 2
#         else:
#             messages = 'Exist empty fields.'
#             status_code = 0       # SUCCESS
#         return jsonify({'messages': messages, 'status_code': status_code})


# Delete api
@blueprint.route('/api/delete/', methods=['GET', 'POST'])
@login_required
@admin_required
def api_user_delete():
    if request.method == 'POST':
        user_sn = request.get_json().get('user_sn', None)
        if user_sn:
            user = User.query.filter_by(user_sn=user_sn).first()
            if user:
                db.session.delete(user)
                db.session.commit()
                messages = 'Delete user successful'
                status_code = 0
        else:
            messages = 'Cannot find user {}'.format(user_sn)
            status_code = 2
        return jsonify({'messages': messages, 'status_code': status_code})


# Edit api
@blueprint.route('/api/edit/', methods=['GET', 'POST'])
@login_required
@admin_required
def api_user_edit():
    if request.method == 'POST':
        data = request.get_json()
        user_sn = data.get('user_sn', None)
        gender = 0 if data.get('gender', 'man') == 'man' else 1
        birthday = data.get('birthday', '1970-01-01')
        telephone = data.get('telephone', None)
        address = data.get('address', None)
        role = data.get('role', 'User')
        if user_sn and telephone and address:
            user = User.query.filter_by(user_sn=user_sn).first()
            if user:
                # convert birthday type
                birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
                user.gender = gender
                user.birthday = birthday
                user.telephone = telephone
                user.address = address
                user.role = Role.query.filter_by(name=role).first()
                db.session.commit()
                messages = 'Update user info successful'
                status_code = 0
        else:
            messages = 'Cannot find user {} or empty fields'.format(user_sn)
            status_code = 2
        return jsonify({'messages': messages, 'status_code': status_code})


# List page
@blueprint.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    return render_template('admin/userList.html')


# List api
@blueprint.route('/api/list/', methods=['GET', 'POST'])
@login_required
@admin_required
def api_user_list():
    if request.method == 'GET':
        user_data = []
        users = User.query.all()
        if users:
            for user in users:
                birthday = user.birthday
                today = date.today()
                age = birthday.year - today.year
                gender = 'man' if user.gender else 'woman'
                user_data.append({
                    'user_sn': user.user_sn,
                    'username': user.username,
                    'gender': gender,
                    'age': age,
                    'birthday': birthday.strftime('%Y-%m-%d'),
                    'telephone': user.telephone,
                    'address': user.address,
                    'role': user.role.name
                })
            messages = 'Get users data successful.'
            status_code = 0
        else:
            messages = 'No users'
            status_code = 1
        return jsonify(
            {'data': user_data, 'messages': messages, 'status_code': status_code})


# Search api
@blueprint.route('/api/search/', methods=['GET', 'POST'])
@login_required
@admin_required
def api_user_search():
    if request.method == 'POST':
        username = request.get_json().get('username', None)
        user_data = []
        if username:
            user = User.query.filter_by(username=username).first()
            if user:
                birthday = user.birthday
                today = date.today()
                age = birthday.year - today.year
                gender = 'man' if user.gender else 'woman'
                user_data.append({
                    'user_sn': user.user_sn,
                    'username': user.username,
                    'gender': gender,
                    'birthday': birthday.strftime('%Y-%m-%d'),
                    'telephone': user.telephone,
                    'address': user.address,
                    'age': age,
                    'role': user.role.name
                })
                messages = 'Get user data successful.'
                status_code = 0
        else:
            messages = 'Cannot find user {} or empty fields'.format(username)
            status_code = 2
        return jsonify(
            {'data': user_data, 'messages': messages, 'status_code': status_code})
