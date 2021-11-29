import pytest
from itertools import chain
from my_quickbase.quickbase_queries import QuickbaseRawQuery, AppQuery, RecordsQuery, Q_REALM


class TestQuickbaseRawQueries:

    @pytest.fixture
    def raw_query(self):
        return QuickbaseRawQuery()

    def test_headers(self, raw_query):
        assert isinstance(raw_query.headers, dict)

    def test_session(self, raw_query):
        assert hasattr(raw_query.session, 'request')


class TestQuickbaseAppQueries:

    @pytest.fixture
    def app_query(self):
        return AppQuery(app_id='555')

    @pytest.fixture
    def sample_table_data(self):
        return [{'name': 'table1', 'id': 'bbb222'}, {'name': 'table2', 'id': 'bbb333'}]

    def test_app_id(self, app_query):
        assert app_query.app_id == '555'
        assert isinstance(app_query.app_id, str)

    def test_collate_params(self, app_query):
        test_params_almost_empty = app_query.collate_params()
        assert len(test_params_almost_empty) == 1
        test_params_with_additional_params = app_query.collate_params(test1=1, test2=2)
        assert all(item in test_params_with_additional_params.keys() for item in ('appId', 'test1', 'test2'))
        assert all(item in test_params_with_additional_params.values() for item in (app_query.app_id, 1, 2))

    def test_get_tables(self, monkeypatch, app_query, mock_response, sample_table_data):
        def mock_get(*args, **kwargs):
            return mock_response(sample_table_data)
        monkeypatch.setattr(app_query, '_get_response', mock_get)
        tables = app_query.get_tables(params1=10, params2=20)
        assert len(tables) == 2
        assert tables[0]['name'] == 'table1'

    # def test_complete_backup(self, monkeypatch, app_query, mock_response, sample_table_data):
    #     def mock_tables():
    #         return sample_table_data
    #     monkeypatch.setattr(app_query, 'get_tables', mock_tables)


class TestQuickbaseRecordQueries:

    @pytest.fixture
    def records_query(self):
        query = RecordsQuery(app_id='555', table_id='666')
        query.field_mapping = {'11': 'Name', '12': 'Age', '13': 'Record ID'}
        yield query

    @pytest.fixture
    def sample_field_mapping_data(self, records_query):
        records_query.field_mapping = {'11': 'Name', '12': 'Age', '13': 'Record ID'}
        return [{'label': 'Name', 'id': '11'}, {'label': 'Age', 'id': '12'}, {'label': 'Record ID', 'id': '13'}]

    @pytest.fixture
    def sample_records_data(self, records_query):
        records_query.field_mapping = {'11': 'Name', '12': 'Age', '13': 'Record ID'}
        yield {'data': [
            {'11': {'value': 'John Smith'}, '13': {'value': '566'}},
            {'11': {'value': 'Barnaby Jones'}, '13': {'value': '567'}}]}

    @pytest.fixture
    def sample_reports_data(self, records_query):
        records_query.field_mapping = {'11': 'Name', '12': 'Age', '13': 'Record ID'}
        yield [{'id': '20', 'name': 'First Report'},
               {'id': '30', 'name': 'BACKUP Report'},
               {'id': '40', 'name': 'BACKUP Report2'}]

    def test_get_field_mapping(self, monkeypatch, records_query, mock_response, sample_field_mapping_data):
        def mock_get(*args, **kwargs):
            return mock_response(sample_field_mapping_data)
        monkeypatch.setattr(records_query, '_get_response', mock_get)
        assert records_query.field_mapping['11'] == 'Name'
        assert records_query.field_mapping['13'] == 'Record ID'

    def test_get_reports(self, monkeypatch, mock_response, records_query, sample_reports_data):
        def mock_get(*args, **kwargs):
            return mock_response(sample_reports_data)
        monkeypatch.setattr(records_query, '_get_response', mock_get)
        reports = records_query.get_reports('BACKUP')
        assert all(x in reports for x in ('30', '40'))
        assert len(reports) == 2

    def test_fix_data(self, records_query, sample_records_data):
        fixed_data = list(records_query._fix_data(sample_records_data))
        assert fixed_data[0]['Name'] == 'John Smith'
        assert fixed_data[1]['Record ID'] == '567'
        assert len(fixed_data) == 2

    def test_get_records(self, monkeypatch, records_query, mock_response, sample_records_data):
        def mock_get(*args, **kwargs):
            yield mock_response(sample_records_data).json()
        monkeypatch.setattr(records_query, '_get_records', mock_get)
        records = list(chain.from_iterable(records_query.get_records('ccc222')))  # flattens (generator) iterables
        assert records[1]['Name'] == 'Barnaby Jones'
        assert records[0]['Record ID'] == '566'
        assert len(records) == 2
