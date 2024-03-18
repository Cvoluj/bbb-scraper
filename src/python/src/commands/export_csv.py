import os
import csv
import datetime
from os import path
from sqlalchemy import Table
from database.models import Company
from typing import List, Dict


from commands.base import BaseCSVExporter

from typing import List, Dict, Union

from MySQLdb.cursors import DictCursor
from sqlalchemy import select, Table
from sqlalchemy.dialects.mysql import dialect
from sqlalchemy.sql import update
from sqlalchemy.sql.base import Executable as SQLAlchemyExecutable
from twisted.enterprise import adbapi
from twisted.enterprise.adbapi import Transaction
from twisted.internet import reactor, defer



class ExportCSV(BaseCSVExporter):
    table: Table = Company
    file_timestamp_format: str = '%Y%b%d%H%M%S'
    export_date_column: str = 'sent_to_customer'
    file_extension: str = 'csv'
    chunk_size = 10000
    excluded_columns: List[str] = []
    specific_columns: List[str] = []
    headers: List[str] = []
    new_mapping: Dict[str, str] = {}
    filename_prefix: str = ''
    filename_postfix: str = ''
    file_path: str = ''
    file_exists: bool = False
    
    bucket_id = 0
    
    def init(self) -> None:
        if not isinstance(self.table.__table__, Table):
            raise ValueError(f'{type(self).__name__} must have a valid table object')
        self.file_path = self.get_file_path()
        self.init_db_connection_pool()
        self.logger.debug('Connection established.')

    def split_into_buckets(self, rows: List[Dict]) -> List[List[Dict]]:
        offset = 0
        buckets = []
        while offset < len(rows):
            bucket = rows[offset:offset + self.chunk_size]
            buckets.append(bucket)
            offset += self.chunk_size
        return buckets
    
    def export(self, rows: Union[tuple, Dict]) -> None:
        if not rows:
            if self.file_exists:
                self.logger.debug(f'Export finished successfully to {path.basename(self.file_path)}.')
            else:
                self.logger.warning('Nothing found')
            reactor.stop()
        else:
            if self.chunk_size == 1:
                rows = [rows]
            else:
                rows = list(rows)
            rows = self.map_columns(rows)
            self.get_headers(rows[0])
            buckets = self.split_into_buckets(rows) 
            for bucket in buckets:
                self.save(bucket)
            deferred_interactions = []
            for row in rows:
                deferred_interactions.append(self.db_connection_pool.runInteraction(self.update, row))
            deferred_list = defer.DeferredList(deferred_interactions, consumeErrors=True)
            deferred_list.addCallback(self._on_row_update_completed)
            deferred_list.addErrback(self._on_row_update_error)

    def get_file_path(self, timestamp_format=None, prefix=None, postfix=None, extension=None):
        if timestamp_format is None:
            timestamp_format = self.file_timestamp_format
        if prefix is None:
            prefix = self.filename_prefix
        if postfix is None:
            postfix = self.filename_postfix
        if extension is None:
            extension = self.file_extension
        export_path = path.join(path.abspath('..'), 'src\\storage')
        file_name = f'{prefix}{datetime.datetime.now().strftime(timestamp_format)}{postfix}_bucket{self.bucket_id}.{extension}'
        self.bucket_id += 1
        return path.join(export_path, file_name)

    def save(self, rows: List[Dict]) -> None:
        self.file_path = self.get_file_path()
        with open(self.file_path, 'a', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            if not self.file_exists:
                writer.writeheader()
            self.logger.debug(f'Exporting to {self.file_path}...')
            writer.writerows(rows)
