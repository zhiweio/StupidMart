# -*- coding: utf-8 -*-


from datetime import datetime

from sqlalchemy.dialects.mysql import DOUBLE

from StupidMart.database import Column, Model, SurrogatePK, db, relationship
# from StupidMart.extensions import login_manager


class Provider(SurrogatePK, Model):
    __tablename__ = 'providers'
    # __table_args__ = {
    #     'mysql_engine': 'InnoDB'
    # }
    id = Column(db.Integer, autoincrement=True, primary_key=True)
    provider_sn = Column(db.String(32), unique=True, nullable=False)
    provider_name = Column(db.String(80), unique=True, nullable=False)
    bills = relationship('Bill', backref='provider', lazy='dynamic')
    contact = Column(db.String(80), unique=True, nullable=False)
    telephone = Column(db.String(16), nullable=False)
    fax = Column(db.String(32), nullable=True)
    description = Column(db.Text, nullable=True)
    address = Column(db.String(120), nullable=True)
    created_at = Column(db.DateTime, default=datetime.now)

    def __init__(self, provider_sn, provider_name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, provider_sn=provider_sn,
                          provider_name=provider_name, **kwargs)

    @staticmethod
    def insert_providers():
        test_provider = Provider(
            '3AFC68-H72FHA-87BA0P-G6DT2K',
            '苏州科技大学计算机科学与技术系',
            contact='wangzhiwei',
            telephone='18896506666')
        db.session.add(test_provider)
        db.session.commit()


class Bill(SurrogatePK, Model):
    __tablename__ = 'bills'
    # __table_args__ = {
    #     'mysql_engine': 'InnoDB'
    # }
    id = Column(db.Integer, autoincrement=True, primary_key=True)
    bill_sn = Column(db.String(32), unique=True, nullable=False)
    product = Column(db.String(80), nullable=False)
    unit = Column(db.String(32), nullable=False)
    amount = Column(DOUBLE, default=0.00)
    numbers = Column(db.Float(2), default=0.00)
    is_paid = Column(db.Boolean, default=False)
    provider_id = Column(db.Integer, db.ForeignKey('providers.id'))
    created_at = Column(db.DateTime, default=datetime.now,
                        onupdate=datetime.now)

    def __init__(self, bill_sn, product, **kwargs):
        """Create instance."""
        db.Model.__init__(self, bill_sn=bill_sn, product=product, **kwargs)
