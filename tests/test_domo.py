import jedi_toolz as jt
from jedi_toolz.domo import *
import pydomo

def test_config():
    jt.config.set_path(None)
    assert jt.config.select("domo", "client_id") is not None
    assert jt.config.select("domo", "secret") is not None

def test_connect():
    conn = connect()
    assert isinstance(conn, pydomo.Domo)

def test_tables():
    columns = set(tables()[0].keys())
    expected = {"id", "name", "description", "rows", "columns", "owner", "owner_id"}
    assert columns & expected == expected

def test_get_id():
    assert get_id("Analytics-StepTracker") == '7f5ba21a-6359-4f71-a2e6-46af8d1740cb'

def test_query():
    query_columns = set(query("Analytics-StepTracker")[0].keys())
    expected_query_columns = {
        'Effective Date',
        'Miles',
        'Team Member',
        '_BATCH_FILE_ID_',
        '_BATCH_FILE_NAME_',
        '_BATCH_ID_',
        '_BATCH_LAST_RUN_',
        '_BATCH_ROW_NUM_'
    }
    assert query_columns & expected_query_columns == expected_query_columns