# -*- coding: utf-8 -*-

"""User models."""


# import datetime as dt
from datetime import datetime, date
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask import current_app, url_for
from flask_login import UserMixin, AnonymousUserMixin


from StupidMart.database import Column, Model, SurrogatePK, db, relationship
from StupidMart.extensions import bcrypt, login_manager


class Permission(object):
    USER_CONTROL = 1
    BILL_CONTROL = 2
    PROVIDER_CONTROL = 4


class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'roles'
    id = Column(db.Integer, autoincrement=True, primary_key=True)
    name = Column(db.String(80), unique=True, nullable=False)
    default = Column(db.Boolean, default=False, index=True)
    permissions = Column(db.Integer)
    users = relationship('User', backref='role', lazy='dynamic')

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.BILL_CONTROL, Permission.PROVIDER_CONTROL],
            'Amaldar': [Permission.BILL_CONTROL, Permission.PROVIDER_CONTROL],
            'Administrator': [Permission.BILL_CONTROL, Permission.PROVIDER_CONTROL,
                              Permission.USER_CONTROL],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    id = Column(db.Integer, autoincrement=True, primary_key=True)
    user_sn = Column(db.String(32), unique=True, nullable=False)
    username = Column(db.String(80), unique=True, nullable=False)
    gender = Column(db.Boolean, nullable=True)
    telephone = Column(db.String(16), nullable=True)
    role_id = Column(db.Integer, db.ForeignKey('roles.id'))
    #: The hashed password
    password = Column(db.Binary(128), nullable=False)
    birthday = Column(db.Date, default=date.today)
    address = Column(db.String(120), nullable=True)
    created_at = Column(db.DateTime, default=datetime.now)
    last_seen = Column(db.DateTime, default=datetime.now)
    active = Column(db.Boolean, default=False)
    confirmed = Column(db.Boolean, default=False)

    def __init__(self, user_sn, username, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, user_sn=user_sn, username=username, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    # @property
    # def password(self):
    #     raise AttributeError('password is not a readable attribute')

    # @password.setter
    # def password(self, password):
    #     """Set password."""
    #     self.password = bcrypt.generate_password_hash(password)

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def verify_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except Exception:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    # def check_password(self, value):
    #     """Check password."""
    #     return bcrypt.check_password_hash(self.password, value)

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except Exception:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def ping(self):
        self.last_seen = datetime.now()
        db.session.add(self)

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id),
            'username': self.username,
            'last_seen': self.last_seen
        }
        return json_user

    @staticmethod
    def insert_users():
        birthday = date(1996, 5, 25)
        role = Role.query.filter_by(name='Administrator').first()
        admin = User(user_sn='0x01', username='admin',
                     password='123456', birthday=birthday, role=role)
        db.session.add(admin)
        db.session.commit()

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)


class AnonymousUser(AnonymousUserMixin):

    def __init__(self):
        self.username = 'Guest'

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
