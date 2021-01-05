from project import tables_pb2, options_pb2

DB_NAME = tables_pb2.DESCRIPTOR.GetOptions().Extensions[options_pb2.db_name]
CLUSTER_NAME = tables_pb2.DESCRIPTOR.GetOptions().Extensions[options_pb2.cluster_name]