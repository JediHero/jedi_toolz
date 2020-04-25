import jedi_toolz as jt
from jedi_toolz.config import *
import pydomo

def test_config():
    set_path(None)
    assert select("domo", "client_id")
    assert select("domo", "secret")

def test_connect():
    conn = jt.domo.connect()
    assert isinstance(conn, pydomo.Domo)

def test_tables():
    columns = set(jt.domo.tables()[0].keys())
    expected = {"id", "name", "description", "rows", "columns", "owner", "owner_id"}
    assert columns & expected == expected

def test_get_id():
    assert jt.domo.get_id("Analytics-StepTracker") == '7f5ba21a-6359-4f71-a2e6-46af8d1740cb'

def test_query():
    query_columns = set(jt.domo.query("Analytics-StepTracker")[0].keys())
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