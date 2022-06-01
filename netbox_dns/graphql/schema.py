from .view import ViewQuery
from .nameserver import NameServerQuery
from .zone import ZoneQuery
from .record import RecordQuery


class Query(ViewQuery, NameServerQuery, ZoneQuery, RecordQuery):
    pass


schema = Query
