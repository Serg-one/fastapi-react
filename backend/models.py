import datetime as dt

import sqlalchemy as sqla
import sqlalchemy.orm as orm
import passlib.hash as hash

import database as _database


class User(_database.Base):
    __tablename__ = "users"

    id = sqla.Column(sqla.Integer, primary_key=True, index=True)
    email = sqla.Column(sqla.String, unique=True, index=True)
    hashed_password = sqla.Column(sqla.String)

    leads = orm.relationship("Lead", back_populates="owner")

    def verify_password(self, password: str):
        return hash.bcrypt.verify(password, self.hashed_password)


class Lead(_database.Base):
    __tablename__ = "leads"

    id = sqla.Column(sqla.Integer, primary_key=True, index=True)
    owner_id = sqla.Column(sqla.Integer, sqla.ForeignKey("users.id"))
    first_name = sqla.Column(sqla.String, index=True)
    last_name = sqla.Column(sqla.String, index=True)
    email = sqla.Column(sqla.String, index=True)
    company = sqla.Column(sqla.String, index=True, default="")
    note = sqla.Column(sqla.String, default="")
    date_created = sqla.Column(
        sqla.DateTime, default=dt.datetime.now(dt.timezone.utc)
    )
    last_updated = sqla.Column(
        sqla.DateTime, default=dt.datetime.now(dt.timezone.utc)
    )

    owner = orm.relationship("User", back_populates="leads")
