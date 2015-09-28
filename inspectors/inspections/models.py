import datetime as dt

from inspectors.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)

class Supervisor(Model):
    """A person who supervises building inspectors"""
    __tablename__ = 'supervisor'

    id = Column(db.Integer, primary_key=True, index=True)
    full_name = Column(db.String(150), nullable=False)
    email = Column(db.String(80), nullable=False)
    active = Column(db.Boolean(), default=True)
    inspectors = db.relationship('Inspector', backref='supervisor')
    last_report = Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Supervisor({0})>'.format(self.full_name)

    def send_report(self):
        raise NotImplementedError

    def unsubscribe(self):
        raise NotImplementedError


class Inspector(Model):
    """A person who does inspections."""
    __tablename__ = 'inspector'

    id = Column(db.Integer, primary_key=True, index=True)
    inspector_id = Column(db.String(25), unique=True, nullable=False,
            index=True)
    first_name = Column(db.String(80), nullable=False)
    last_name = Column(db.String(80), nullable=False)
    photo_url = Column(db.String(80), nullable=True)
    supervisor_id = Column(db.Integer, db.ForeignKey('supervisor.id'),
            nullable=False)
    inspections = db.relationship('Inspection', backref='inspector')

    def __repr__(self):
        return '<Inspector(id:{0}, name:{1})>'.format(self.inspector_id,
            " ".join([self.first_name, self.last_name]))

class Inspection(Model):
    """An inspection of a some construction by an inspector"""
    __tablename__ = 'inspections'
    id = Column(db.Integer, primary_key=True, index=True)
    permit_number = Column(db.String(25), nullable=False, index=True)
    date_inspected = Column(db.DateTime, nullable=False, index=True)
    permit_type = Column(db.String(10), nullable=False)
    permit_description = Column(db.String(50), nullable=True)
    display_description = Column(db.String(50), nullable=False)
    job_site_addresss = Column(db.String(200), nullable=False)
    inspector_id = Column(db.Integer, db.ForeignKey('inspector.id'),
            nullable=False)
    feedback_form = Column(db.String(100), nullable=True)
    feedback_form_sent = Column(db.Boolean(), default=False)

    def __repr__(self):
        return '<Inspection({0}:{1})>'.format(self.permit_number,
                self.date_inspected.strftime("%Y-%m-%d"))

    def send_feedback_form(self):
        raise NotImplementedError

