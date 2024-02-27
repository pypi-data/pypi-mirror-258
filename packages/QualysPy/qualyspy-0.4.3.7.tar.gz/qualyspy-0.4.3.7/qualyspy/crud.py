import pydantic
import sqlalchemy.orm as orm
from typing import Any

from qualyspy.db import Base


def CrudFactory(model: Base) -> Any:
    class Crud:
        def __init__(self, model: Base):
            self.model = model

        @classmethod
        def create(
            cls, session: orm.Session, obj: pydantic.BaseModel
        ) -> pydantic.BaseModel:
            session.add(obj)
            session.commit()
            return obj

        @classmethod
        def read(cls, session: orm.Session, id: int) -> Any:
            return session.query(model).filter(model.id == id).one()

        @classmethod
        def update(
            cls, session: orm.Session, obj: pydantic.BaseModel
        ) -> pydantic.BaseModel:
            session.add(obj)
            session.commit()
            return obj

        @classmethod
        def delete(cls, session: orm.Session, id: int) -> pydantic.BaseModel:
            obj = cls.read(session, id)
            session.delete(obj)
            session.commit()
            return obj

    Crud.model = model
    return Crud
