import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime
import sqlalchemy as sa
from sqlalchemy.inspection import inspect


class utcnow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"  # pragma: no cover


class Base(DeclarativeBase):
    __abstract__ = True

    # basic fields all tables should have
    id = sa.Column(UUID(as_uuid=True),
                   primary_key=True,
                   default=uuid.uuid4)
    created_at = sa.Column(sa.DateTime, server_default=utcnow())
    updated_at = sa.Column(sa.DateTime, server_default=utcnow(), onupdate=utcnow())

    # naming conventions for various constraints
    # https://medium.com/@chjiang15/dont-forget-your-naming-constraints-sqlalchemy-alembic-top-tip-89022a54a4b0
    convention = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
    metadata = sa.MetaData(naming_convention=convention)

    # more ideas in https://dev.to/chidioguejiofor/making-sqlalchemy-models-simpler-by-creating-a-basemodel-3m9c

    def to_dict(self, nested=True):
        data = {}
        mapper = inspect(self)
        for column in mapper.attrs:
            value = getattr(self, column.key)
            if nested and hasattr(value, 'to_dict'):
                data[column.key] = value.to_dict(nested=False)  # pragma: no cover
            elif nested and isinstance(value, list):
                data[column.key] = [item.to_dict(nested=False) for item in value]  # pragma: no cover
            else:  # pragma: no cover
                data[column.key] = value

        utc_format = "%Y-%m-%dT%H:%M:%SZ"

        data["created_at"] = self.created_at.strftime(utc_format)
        data["updated_at"] = self.updated_at.strftime(utc_format)

        return data
