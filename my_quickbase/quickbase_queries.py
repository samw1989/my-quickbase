# Built-ins
import json
import datetime
import pathlib
import itertools
from typing import Generator
# Externals
import requests
# Own Modules
from my_quickbase.settings import Q_REALM, Q_USER_TOKEN
from my_quickbase.helpers import check_attr_exists, parse_response, TokenAndRealmNotSet
from my_quickbase import logger


class QuickbaseRawQuery:

    def __init__(self, realm: str = None, token: str = None):
        """
        Passing in realm or token overrides Q_REALM and Q_USER_TOKEN,
        which are taken from .ini or environment variables
        """
        self.session = requests.Session()
        self.app_id = None
        try:
            self.headers = {
                'QB-Realm-Hostname': realm or Q_REALM,
                'Authorization': token or Q_USER_TOKEN,
            }
            if None in self.headers.values():
                raise NameError
        except NameError:
            raise TokenAndRealmNotSet("""Must either a) pass in realm and token parameters to class, or b) 
                                        set up QB Realm and QB User Token in settings.ini or as environment variable""")
        else:
            logger.info(f'Quickbase Query Initialized: {self}')

    def __repr__(self):
        return f"{self.__class__.__name__} - App ID: {self.app_id}. Realm: {self.headers['QB-Realm-Hostname']}"

    def _get_response(self, method: str, api_url: str, params: dict) -> requests.models.Response:
        response = self.session.request(method, api_url, params=params, headers=self.headers)
        return response


class AppQuery(QuickbaseRawQuery):

    def __init__(self, app_id: str, realm: str = None, token: str = None):
        super().__init__(realm, token)
        self.app_id = str(app_id)

    def get_tables(self, **additional_params) -> list:
        api_url = 'https://api.quickbase.com/v1/tables'
        params = self.collate_params(**additional_params)
        response = self._get_response('GET', api_url, params)
        return response.json()

    def collate_params(self, **additional_params) -> dict:
        return {'appId': self.app_id, **additional_params}

    def complete_backup(self, files_destination=None):
        """
        Backs up all reports across entire app if 'BACKUP' in report title,
        """
        tables = self.get_tables()
        logger.info(f'Backing up {len(tables)} tables')
        for table in tables:
            label = table_id, table_name = table['id'], table['name']
            record_query = RecordsQuery(self.app_id, table_id, *self.headers.values())
            record_query.get_field_mapping()
            report_ids = record_query.get_reports('BACKUP')
            for report_id in report_ids:
                logger.info(f'Backing up report {report_id} in {table_name}')
                records = itertools.chain.from_iterable(record_query.get_records(report_id, export=False))
                self.export(records, label, report_id, files_destination)

    def export(self, data, label, report_id, files_destination):
        path = (pathlib.Path(f'exports/{datetime.date.today()}')
                if files_destination is None else pathlib.Path(files_destination))
        path.mkdir(parents=True, exist_ok=True)
        final_path = f'{path}/{self.app_id}_{label[0]}_{label[1]}_report_{report_id}'
        print('\nExporting', label)
        with open(f'{final_path}.json', 'w') as file:
            final_data = list(data)
            json.dump(final_data, file, ensure_ascii=False, indent=4)
        logger.info(f'Produced .json at {final_path}, containing {len(final_data)} records')


@check_attr_exists('field_mapping')
class RecordsQuery(QuickbaseRawQuery):
    """ Requires both an app_id and table_id. Methods can only be run once field_mapping attribute is set (achieved
    by calling get_field_mapping method). """

    def __init__(self, app_id: str, table_id: str, realm: str = None, token: str = None):
        super().__init__(realm, token)
        self.app_id = str(app_id)
        self.table_id = str(table_id)
        self.params = {'tableId': self.table_id, 'top': 5000}
        self.field_mapping = None

    def get_field_mapping(self) -> None:
        api_url = 'https://api.quickbase.com/v1/fields'
        response = self._get_response('GET', api_url, self.params)
        self.field_mapping = {str(field_dict['id']): field_dict['label'] for field_dict in parse_response(response)}

    def get_reports(self, report_keyword):
        api_url = 'https://api.quickbase.com/v1/reports'
        response = self._get_response('GET', api_url, self.params)
        report_ids = [report['id'] for report in parse_response(response) if report_keyword in report['name']]
        return report_ids

    def get_records(self, report_id: str, export=True, **additional_params) -> Generator[Generator, None, None]:
        """ Returns a generator expression comprising an iterable of other generator objects,
        each representing an API call. The actual calls are only made when something is done with the data
        (e.g. exporting to JSON)"""

        api_url = f'https://api.quickbase.com/v1/reports/{report_id}/run'
        params = {**self.params, **additional_params}
        if not export:
            return (self._fix_data(data) for data in self._get_records(api_url, params))
        else:
            return itertools.chain.from_iterable(self._fix_data(data) for data in self._get_records(api_url, params))

    def _fix_data(self, data: dict):
        return ({self.field_mapping[key]: value['value'] for key, value in row.items()} for row in data['data'])

    def _get_records(self, api_url: str, params: dict):
        # Pagination
        skip, num_records = 0, 1
        while num_records > 0:
            response = self._get_response('POST', api_url, {**params, 'skip': skip})
            json_response = parse_response(response)
            num_records = json_response['metadata']['numRecords']
            skip += num_records
            print(f"\rProcessing table {self.table_id}: {skip} / {json_response['metadata']['totalRecords']} records",
                  end='')
            yield json_response
