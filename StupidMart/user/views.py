# -*- coding: utf-8 -*-
"""User views."""

# import json

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user

from StupidMart.database import db
from StupidMart.user.models import Provider, Bill

blueprint = Blueprint('user', __name__, url_prefix='/user',
                      static_folder='../static/assets')


@blueprint.route('/change_password/', methods=['GET', 'POST'])
@login_required
def change_password():
    messages = ''
    if request.method == 'POST':
        old_password = request.form.get('old_password', None)
        new_password = request.form.get('new_password', None)
        confirm_password = request.form.get('confirm_password', None)

        if old_password and new_password and confirm_password:
            if current_user.verify_password(old_password):
                if new_password == confirm_password:
                    print(
                        "new password: {} - {}".format(new_password, type(new_password)))
                    current_user.set_password(new_password)
                    db.session.commit()
                    flash('Your password has been updated.')
                    return redirect(url_for('user.bills'))
                else:
                    messages = 'Entered passwords differ.'
            else:
                messages = 'Invalid password.'
    msg = {'msg': messages}
    return render_template("users/change_password.html", messages=msg)


'''Provider routes'''


# Provider add api
@blueprint.route('/api/provider/add/', methods=['GET', 'POST'])
@login_required
def api_provider_add():
    if request.method == 'POST':
        data = request.get_json()
        provider_sn = data.get('provider_sn', None)
        provider_name = data.get('provider_name', None)
        contact = data.get('contact', None)
        telephone = data.get('telephone', None)
        address = data.get('address', None)
        fax = data.get('fax', None)
        description = data.get('description', None)

        if provider_sn and provider_name and contact and telephone:
            provider = Provider(provider_sn, provider_name,
                                contact=contact,
                                telephone=telephone,
                                address=address,
                                fax=fax,
                                description=description)
            db.session.add(provider)
            db.session.commit()
            messages = 'Add provider successful.'
            status_code = 0   # Success
        else:
            messages = 'Exist empty fields.'
            status_code = 2       # FAILED
        return jsonify({'messages': messages, 'status_code': status_code})


# Provider delete api
@blueprint.route('/api/provider/delete/', methods=['GET', 'POST'])
@login_required
def api_provider_delete():
    if request.method == 'POST':
        provider_sn = request.get_json().get('provider_sn', None)
        if provider_sn:
            provider = Provider.query.filter_by(
                provider_sn=provider_sn).first()
            if provider:
                db.session.delete(provider)
                db.session.commit()
                messages = 'Delete provider successful'
                status_code = 0
        else:
            messages = 'Cannot find provider {}'.format(provider_sn)
            status_code = 2
        return jsonify({'messages': messages, 'status_code': status_code})


# Provider edit api
@blueprint.route('/api/provider/edit/', methods=['GET', 'POST'])
@login_required
def api_provider_edit():
    if request.method == 'POST':
        data = request.get_json()
        provider_sn = data.get('provider_sn', None)
        provider_name = data.get('provider_name', None)
        contact = data.get('contact', None)
        telephone = data.get('telephone', None)
        address = data.get('address', None)
        fax = data.get('fax', None)
        description = data.get('description', None)

        if provider_sn and provider_name and contact and telephone:
            provider = Provider.query.filter_by(
                provider_sn=provider_sn).first()
            if provider:
                provider.provider_sn = provider_sn
                provider.provider_name = provider_name
                provider.contact = contact
                provider.telephone = telephone
                provider.address = address
                provider.fax = fax
                provider.description = description
                db.session.commit()
                messages = 'Update provider info successful.'
                status_code = 0   # Success
        else:
            messages = 'Exist empty fields.'
            status_code = 2       # FAILED
        return jsonify({'messages': messages, 'status_code': status_code})


# Provide list page
@blueprint.route('/providers/', methods=['GET', 'POST'])
@login_required
def providers():
    return render_template('users/providerList.html')


# Provider list api
@blueprint.route('/api/provider/list/', methods=['GET', 'POST'])
@login_required
def api_provider_list():
    if request.method == 'GET':
        provider_data = []
        providers = Provider.query.all()
        if providers:
            for provider in providers:
                created_at = provider.created_at.strftime('%Y-%m-%d %H:%M')
                provider_data.append({
                    'provider_sn': provider.provider_sn,
                    'provider_name': provider.provider_name,
                    'contact': provider.contact,
                    'telephone': provider.telephone,
                    'description': provider.description,
                    'fax': provider.fax,
                    'address': provider.address,
                    'created_at': created_at
                })
            messages = 'Get providers data successful.'
            status_code = 0
        else:
            messages = 'No providers'
            status_code = 1
        return jsonify(
            {'data': provider_data, 'messages': messages, 'status_code': status_code})


# Provider search api
@blueprint.route('/api/provider/search/', methods=['GET', 'POST'])
@login_required
def api_provider_search():
    if request.method == 'POST':
        provider_name = request.get_json().get('provider_name', None)
        if provider_name:
            data = []
            provider = Provider.query.filter_by(
                provider_name=provider_name).first()
            if provider:
                created_at = provider.created_at.strftime('%Y-%m-%d %H:%M')
                data.append({
                    'provider_sn': provider.provider_sn,
                    'provider_name': provider.provider_name,
                    'contact': provider.contact,
                    'telephone': provider.telephone,
                    'description': provider.description,
                    'fax': provider.fax,
                    'created_at': created_at
                })
                messages = 'Get providers data successful.'
                status_code = 0
            else:
                messages = 'Cannot find provider {}'.format(provider_name)
                status_code = 1
        return jsonify(
            {'data': data, 'messages': messages, 'status_code': status_code})


'''Bill routes'''


# Bill add page
@blueprint.route('/bill/add/', methods=['GET', 'POST'])
@login_required
def bill_add():
    return render_template('users/billAdd.html')


# Bill add api
@blueprint.route('/api/bill/add/', methods=['GET', 'POST'])
@login_required
def api_bill_add():
    if request.method == 'POST':
        data = request.get_json()
        bill_sn = data.get('bill_sn', None)
        product = data.get('product', None)
        unit = data.get('unit', None)
        numbers = float(data.get('numbers', '0.00'))
        amount = float(data.get('amount', '0.00'))
        provider_name = data.get('provider_name', None)
        is_paid = 0 if data.get('is_paid', '未付款') == '未付款' else 1

        if bill_sn and product and unit and provider_name:
            provider = Provider.query.filter_by(
                provider_name=provider_name).first()
            if provider:
                bill = Bill(bill_sn=bill_sn, product=product, unit=unit,
                            numbers=numbers, amount=amount, provider=provider,
                            is_paid=is_paid)
                db.session.add(bill)
                db.session.commit()
                messages = 'Add bill successful.'
                status_code = 0   # Success
            else:
                messages = 'no provider {}'.format(provider_name)
                status_code = 2
        else:
            messages = 'Exist empty fields.'
            status_code = 2       # FAILED
        return jsonify({'messages': messages, 'status_code': status_code})


# Bill delete api
@blueprint.route('/api/bill/delete/', methods=['GET', 'POST'])
@login_required
def api_bill_delete():
    if request.method == 'POST':
        bill_sn = request.get_json().get('bill_sn', None)
        if bill_sn:
            bill = Bill.query.filter_by(
                bill_sn=bill_sn).first()
            if bill:
                db.session.delete(bill)
                db.session.commit()
                messages = 'Delete bill successful'
                status_code = 0
        else:
            messages = 'Cannot find bill {}'.format(bill_sn)
            status_code = 2
        return jsonify({'messages': messages, 'status_code': status_code})


# Bill edit page
@blueprint.route('/bill/edit/', methods=['GET', 'POST'])
@login_required
def bill_edit():
    return render_template('users/billUpdate.html')


# Bill edit api
@blueprint.route('/api/bill/edit/', methods=['GET', 'POST'])
@login_required
def api_bill_edit():
    if request.method == 'POST':
        data = request.get_json()
        bill_sn = data.get('bill_sn', None)
        product = data.get('product', None)
        unit = data.get('unit', None)
        numbers = float(data.get('numbers', '0.00'))
        amount = float(data.get('amount', '0.00'))
        provider_name = data.get('provide_rname', None)
        is_paid = 0 if data.get('is_paid', '未付款') == '未付款' else 1

        if bill_sn and product and unit and provider_name:
            bill = Bill.query.filter_by(bill_sn=bill_sn).first()
            if bill:
                bill.bill_sn = bill_sn
                bill.product = product
                bill.unit = unit
                bill.numbers = numbers
                bill.amount = amount
                bill.provider = Provider.query.filter_by(
                    provider_name=provider_name).first()
                bill.is_paid = is_paid
                db.session.commit()
                messages = 'Update bill info successful.'
                status_code = 0   # Success
        else:
            messages = 'Exist empty fields.'
            status_code = 2       # FAILED
        return jsonify({'messages': messages, 'status_code': status_code})


# Bill list page
@blueprint.route('/bills/', methods=['GET', 'POST'])
@login_required
def bills():
    return render_template('/users/billList.html')


# Bill list api
@blueprint.route('/api/bill/list/', methods=['GET', 'POST'])
@login_required
def api_bill_list():
    if request.method == 'GET':
        bill_data = []
        bills = Bill.query.all()
        if bills:
            for bill in bills:
                created_at = bill.created_at.strftime('%Y-%m-%d %H:%M')
                bill_data.append({
                    'bill_sn': bill.bill_sn,
                    'product': bill.product,
                    'provider_name': bill.provider.provider_name,
                    'unit': bill.unit,
                    'numbers': bill.numbers,
                    'amount': float(bill.amount),
                    'is_paid': bill.is_paid,
                    'created_at': created_at
                })
            messages = 'Get bills data successful.'
            status_code = 0
        else:
            messages = 'No bills'
            status_code = 1
        return jsonify(
            {'data': bill_data, 'messages': messages, 'status_code': status_code})


# Bill search api
@blueprint.route('/api/bill/search/', methods=['GET', 'POST'])
@login_required
def api_bill_search():
    if request.method == 'POST':
        data = request.get_json()
        product = data.get('product', None)
        if product:
            bill = Bill.query.filter_by(
                product=product).first()
            if bill:
                created_at = bill.created_at.strftime('%Y-%m-%d %H:%M')
                data = {
                    'bill_sn': bill.bill_sn,
                    'product': bill.product,
                    'unit': bill.unit,
                    'numbers': bill.numbers,
                    'amount': float(bill.amount),
                    'provider_name': bill.provider.provider_name,
                    'is_paid': bill.is_paid,
                    'created_at': created_at
                }
                messages = 'Get bills data successful.'
                status_code = 0
        else:
            messages = 'No bills'
            status_code = 1
        return jsonify(
            {'data': data, 'messages': messages, 'status_code': status_code})
