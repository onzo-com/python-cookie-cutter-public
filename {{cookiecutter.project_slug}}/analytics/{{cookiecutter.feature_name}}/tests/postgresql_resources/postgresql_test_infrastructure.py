import uuid
import functools
import logging
import os
import string
import time
import unittest
from collections import namedtuple

import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import adapt, AsIs, ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import execute_values
from sqlalchemy import create_engine

_state = None
_skipping = None
_connection = None

_default_host = '127.0.0.1'
_default_port = 5432
_default_db = "test_db"
_schema = "analytics_test"+str(uuid.uuid4()).replace("-","")

class ComponentFixture(object):
    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db

    @property
    def schema(self):
        global _schema
        return _schema


class ContextManager(object):
    def __init__(self, state):
        self._state = state

    def __enter__(self):
        global _connection
        logging.info('Closing test Postgresql connection...')
        self._state._connection.close()
        logging.info('Closed test Postgresql connection')

        s = self._state
        return ComponentFixture(s._host, s._port, s._user, s._password, s._db)

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.info('Reregistering test Postgresql connection...')

        postgresql_host = os.getenv("TEST_PG_HOST", _default_host)
        postgresql_port = os.getenv("TEST_PG_PORT", _default_port)
        postgresql_user = os.getenv("USER")
        postgresql_pass = os.getenv("TEST_PG_PASSWORD", "")
        postgresql_db = os.getenv("TEST_PG_DB", _default_db)

        try:
            test_db_connection = psycopg2.connect(
                host=postgresql_host,
                port=postgresql_port,
                user=postgresql_user,
                password=postgresql_pass,
                dbname=postgresql_db
            )
            test_db_connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        except psycopg2.OperationalError as e:
            _skipping = "Cannot send message to postgresql: {}".format(str(e))
            return

        current_db = test_db_connection.get_dsn_parameters()["dbname"]
        if not (current_db == _default_db):
            # Skip tests if we are not connected to the test_db db
            _skipping = "Refusing to run against postgres db {}".format(current_db)
            return

        logging.info('Reregistered test Postgresql connection')
        _connection = test_db_connection
        self._state._connection = test_db_connection


class Fixture(object):
    def __init__(self, host, state, engine, pyscho_pg_engine):
        self.temporary_disconnect = ContextManager(state)
        self.state = state
        self.host = host
        self._pandas_engine = engine
        self._psycho_pg_engine = pyscho_pg_engine

    @property
    def schema(self):
        global _schema
        return _schema

    @property
    def connection(self):
        return self.state._connection

    @property
    def cursor(self):
        return self.connection.cursor

    @property
    def pandas_engine(self):
        return self._pandas_engine

    @property
    def psycho_pg_engine(self):
        return self._psycho_pg_engine


class _State(object):
    def __init__(self, connection, postgresql_host, postgresql_port, postgresql_user, postgresql_pass, postgresql_db):
        self._connection = connection
        self._host = postgresql_host
        self._port = postgresql_port
        self._user = postgresql_user
        self._password = postgresql_pass
        self._db = postgresql_db
        self._pandas_engine = create_engine(f'postgresql://{postgresql_user}:{postgresql_pass}@{postgresql_host}:{postgresql_port}/{postgresql_db}')
        self._psyscho_engine = create_engine(f'postgresql+psycopg2://{postgresql_user}:{postgresql_pass}@{postgresql_host}:{postgresql_port}/{postgresql_db}')
        global _schema

        # drop schema only on initial connection, as otherwise it will slow us down too much
        self._execute("DROP SCHEMA IF EXISTS {} CASCADE".format(_schema))
        self.initialise_test_db()

    def _execute(self, sql):
        # logging.debug(sql)
        with self._connection.cursor() as cursor:
            cursor.execute(sql)

    def initialise_test_db(self):
        global _schema
        self._execute(self.get_sql('initialise.sql'))
        time.sleep(2)

    def cleanup_test_db(self):
        global _schema
        self._execute(self.get_sql('cleanup.sql'))
        time.sleep(2)

    def fixture(self):
        return Fixture(self._host, self, self._pandas_engine, self._psyscho_engine)

    def get_sql(self, filename):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)) as file_handle:
            class CustomTemplate( string.Template ):
                # We use default delimiter in postgres queries ($$ - dolar quoting)
                delimiter = "@"
            template = CustomTemplate(file_handle.read())
        return template.substitute(schema=_schema)


def _lazy_init():

    logging.getLogger('postgresql').setLevel(logging.WARN)

    global _state
    global _skipping
    global _fail_postgresql_tests
    global _connection

    if _state is not None or _skipping is not None:
        return

    always_run_integration_tests = os.getenv("ALWAYS_RUN_INT_TESTS", "False").lower() == "true"
    postgresql_host = os.getenv("TEST_PG_HOST", _default_host)
    postgresql_port = os.getenv("TEST_PG_PORT", _default_port)
    postgresql_user = os.getenv("USER")
    postgresql_pass = os.getenv("TEST_PG_PASSWORD", "")
    postgresql_db = os.getenv("TEST_PG_DB", _default_db)

    if postgresql_host.lower() == "skip" or not postgresql_host:
        _skipping = "Skipping as requested"
        return

    try:
        logging.info("Attempting to connect to postgres DB at %s:%s with username '%s'",
            postgresql_host, postgresql_port, postgresql_user
        )

        default_db_conn = psycopg2.connect(
            host=postgresql_host,
            port=postgresql_port,
            user=postgresql_user,
            password=postgresql_pass,
            database='postgres'
        )
        postgresql_is_running = True
        default_db_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    except psycopg2.OperationalError as e:
        logging.error("Could not connect to DB '%s' at %s:%s", postgresql_db, postgresql_host, postgresql_port)
        logging.error("Error returned by postgres was: %s", e)
        postgresql_is_running = False

    test_db_exists = False
    if postgresql_is_running:

        c = default_db_conn.cursor()

        c.execute(
            """
            SELECT 1 
            FROM pg_database 
            WHERE datname = %s
            """, (postgresql_db,))

        results = c.fetchall()
        if not results:
            logging.info("Test DB %s does not exist, creating", postgresql_db)
            try:
                c.execute(
                    sql.SQL("CREATE DATABASE {db}").format(
                        db=sql.Identifier(postgresql_db)
                    )
                )
                logging.info("Successfully created test DB %s", postgresql_db)
                test_db_exists = True
            except psycopg2.ProgrammingError as e:
                if e.pgcode == "42P04":
                    logging.info("Couldn't create test DB %s as it already exists", postgresql_db)
                    test_db_exists = True
                else:
                    logging.error("Error attempting to create test DB: %s", e)
            except Exception as ex:
                logging.error(
                    "Test DB %s does not exist and an error occurred attempting to create it: %s",
                    (postgresql_db, str(ex))
                )
            finally:
                c.close()
                default_db_conn.close()
        else:
            c.close()
            test_db_exists = True

    connected_to_test_db = False
    if test_db_exists:
        try:
            test_db_connection = psycopg2.connect(
                host=postgresql_host,
                port=postgresql_port,
                user=postgresql_user,
                password=postgresql_pass,
                dbname=postgresql_db
            )

            logging.info("Successfully connected to test DB %s", postgresql_db)
            test_db_connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            connected_to_test_db = True
        except psycopg2.OperationalError as e:
            logging.error(
                "Could not connect to test DB %s, error was %s",
                (postgresql_db, e)
            )

    if connected_to_test_db:
        _fail_postgresql_tests = False
    elif always_run_integration_tests:
        _fail_postgresql_tests = True
        return
    else:
        _skipping = "Could not connect to Postgresql test DB"
        return

    current_db = test_db_connection.get_dsn_parameters()["dbname"]
    if not (current_db == _default_db):
        # Skip tests if we are not connected to the test db
        _skipping = "Refusing to run against postgres db {}".format(current_db)
        return

    _state = _State(
        connection=test_db_connection,
        postgresql_host=postgresql_host,
        postgresql_port=postgresql_port,
        postgresql_user=postgresql_user,
        postgresql_pass=postgresql_pass,
        postgresql_db=postgresql_db
    )

    _connection = test_db_connection
    logging.debug("_lazy_init() completed successfully")


def postgresqlTestCase(func):
    """Mark a test case as using a Postgresql connection .

    The test case will get a fixture in its `postgres` argument containing schema, connection and cursor properties.
    The cursor property must be called in order to return a new cursor from the connection.

    If you are testing code which sets up its own connection to postgres, you should test that code within a
    `with postgres.temporary_disconnect as p:` block.  You can then get  connection details as follows:
    host `p.host`,
    port `p.port`,
    user `p.user`,
    pass `p.password`,
    db: `p.db`,
    """

    _lazy_init()

    @functools.wraps(func)
    @unittest.skipIf(_skipping is not None, _skipping)
    def decorated_test_case(*args, **kwargs):
        if _fail_postgresql_tests:
            raise AssertionError("Cannot connect to Postgresql, failing this test")
        else:
            _state.cleanup_test_db()
            return func(*args, postgres=_state.fixture(), **kwargs)
    return decorated_test_case


def insert_data(postgres, data_object):

    to_insert = []
    for record in data_object.itertuples():
        to_insert.append((
            record.test_id_1,
            record.test_id_2,
            record.test_date,
            record.test_value
        ))
    query = f"""
            INSERT into {postgres.schema}.test_table_name
            (
                test_id_1,
                test_id_2,
                test_date,
                test_value
            ) VALUES %s
            """
    with postgres.cursor() as c:
        execute_values(c, query, to_insert)
