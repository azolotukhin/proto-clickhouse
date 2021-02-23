import logging
import click
from google.protobuf.symbol_database import Default
try:
    from project import options_pb2
    from project.tables_pb2 import *
    from schema_migration.table import Table
    from schema_migration.view import View
    from .settings import DB_NAME, CLUSTER_NAME
except ImportError:
    logging.warning("Proto isn't built yet.")


@click.group()
def cli():
    pass


@cli.command('create_tables')
@click.option('-p', '--package')
def create_tables(package):
    sym_db = Default()
    for message_type in sym_db._classes:
        if package and package not in message_type.file.package:
            continue
        message_meta = message_type.GetOptions().Extensions[options_pb2.message_meta]
        meta_object = message_meta.WhichOneof('Meta')
        if meta_object == 'table_meta':
            if message_meta.table_meta.WhichOneof('ENGINE'):
                table = Table(CLUSTER_NAME, DB_NAME, message_type)
                print(table.create_table_sql())
        elif meta_object == 'view_meta':
            table = View(CLUSTER_NAME, DB_NAME, message_type)
            print(table.create_view_sql())


@cli.command('alter_tables')
def alter_tables():
    """
    DETACH TABLE ww2.video_consumer
    ALTER TABLE ww2.Video ADD COLUMN PS_create_is_frictionless UInt8, ADD COLUMN PS_is_frictionless UInt8
    ALTER TABLE ww2.d_Video ADD COLUMN PS_create_is_frictionless UInt8, ADD COLUMN PS_is_frictionless UInt8

    DROP TABLE ww2.VideoKafka
    CREATE TABLE IF NOT EXISTS ww2.VideoKafka as ww2.Video ENGINE = Kafka() SETTINGS
     kafka_broker_list = '192.168.10.8:9092,192.168.10.9:9092,192.168.10.10:9092',
     kafka_topic_list = 'ww2_video_topic',
     kafka_group_name = 'video_group',
     kafka_format = 'JSONEachRow'


    DROP TABLE ww2.video_consumer
    CREATE MATERIALIZED VIEW IF NOT EXISTS ww2.video_consumer TO ww2.Video AS SELECT * FROM ww2.VideoKafka
    """
    pass