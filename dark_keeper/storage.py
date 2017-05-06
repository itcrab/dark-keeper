import csv
import os

import xlsxwriter

from .exceptions import DarkKeeperStorageExcelMaxLenStringError
from .parse import create_new_data_row


class Storage(list):
    def __init__(self, model, export_dir, mongo_client, xls_strmax_mul=1):
        super().__init__()

        self.model = model
        self.model_keys = [item[0] for item in model]
        self.model_values = [item[1] for item in model]

        self.export_dir = export_dir
        self.mongo_client = mongo_client
        self.create_dirs(self.export_dir)

        self.xls_strmax_mul = xls_strmax_mul

        self._set_head_row()

    def append_row(self, soup):
        row = create_new_data_row(soup, self.model_values)
        if row:
            self.append(row)

    def export(self, log):
        self.export_files(log)
        self.export_mongo(log)

    def export_files(self, log):
        exported_files = []
        for file_type in ['csv', 'xlsx']:
            log.info('- generating {} file...'.format(file_type))

            export_file = os.path.join(
                self.export_dir, 'export.{}'.format(file_type)
            )
            getattr(self, '_export_to_{}'.format(file_type))(export_file)
            exported_files.append(export_file)

        return exported_files

    def export_mongo(self, log):
        coll_name = os.path.basename(self.export_dir)
        log.info('- generating {} collection...'.format(coll_name))

        db = self.mongo_client.podcasts

        coll = getattr(db, coll_name)
        if coll.count():
            coll.drop()

        for row, data in enumerate(self):
            if not row:
                continue

            coll.insert_one(
                dict(zip(self.model_keys, data))
            )

    def _export_to_csv(self, export_file):
        # fix for Excel and utf8
        with open(export_file, 'wb') as f:
            f.write(b'\xEF\xBB\xBF')

        with open(export_file, 'w', encoding='utf-8', newline='') as f:
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerows(self)

    def _export_to_xlsx(self, export_file):
        workbook = xlsxwriter.Workbook(export_file)
        worksheet = workbook.add_worksheet()

        # hack for largest strings
        if self.xls_strmax_mul:
            worksheet.xls_strmax *= self.xls_strmax_mul

        col = 0
        bold = workbook.add_format({'bold': True})
        max_length = worksheet.xls_strmax

        for row, data in enumerate(self):
            self._check_fail(data, max_length)

            if bold and row > 0:
                bold = None

            worksheet.write_row(row, col, data, bold)

        workbook.close()

    def _check_fail(self, data, max_length):
        length = len(''.join(data))
        if length > max_length:
            raise DarkKeeperStorageExcelMaxLenStringError(
                length, max_length, self.xls_strmax_mul
            )

    def _set_head_row(self):
        if len(self) == 0:
            self.append(self.model_keys)
        else:
            self[0] = self.model_keys

    @staticmethod
    def create_dirs(export_dir):
        if export_dir and not os.path.isdir(export_dir):
            os.makedirs(export_dir, exist_ok=True)

            return True
