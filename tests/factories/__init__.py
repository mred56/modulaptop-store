from factory.alchemy import SQLAlchemyModelFactory as Factory

from .customers import CustomersFactory


def inject_session(session, base_class=None):
    base_class = base_class or Factory
    for subclass in base_class.__subclasses__():
        subclass._meta.sqlalchemy_session = session
        inject_session(session, base_class=subclass)


__all__ = [
    "CustomersFactory",
    "inject_session"
]
