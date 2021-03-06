from google.protobuf.descriptor import Descriptor

from project import options_pb2


class View:
    def __init__(self, cluster_name: str, db_name: str, message_descriptor: Descriptor) -> None:
        self.cluster_name = cluster_name
        self.db_name = db_name
        self.message_descriptor = message_descriptor
        self.view_meta = message_descriptor.GetOptions().Extensions[options_pb2.message_meta].view_meta

    @property
    def name(self) -> str:
        return self.view_meta.NAME or self.message_descriptor.name

    @property
    def materialized(self) -> bool:
        return self.view_meta.MATERIALIZED

    @property
    def as_select(self) -> str:
        return self.view_meta.AS_SELECT

    @property
    def to(self) -> str:
        return self.view_meta.TO

    def create_view_sql(self) -> str:
        materialized = 'MATERIALIZED' if self.materialized else ''
        sql = f'CREATE {materialized} VIEW IF NOT EXISTS {self.db_name}.{self.name}'
        if self.cluster_name:
            sql += f' ON CLUSTER {self.cluster_name}'
        sql += f' TO {self.db_name}.{self.to} AS SELECT {self.as_select}'
        return sql
