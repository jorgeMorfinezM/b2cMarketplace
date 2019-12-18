"""Oracle DB backend (db-oracle).

Each one of the CRUD operations should be able to open a database connection if
there isn't already one available (check if there are any issues with this).

Documentation:

"""

from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db_controller import mvc_exceptions as mvc_exc
from constants.constants import Constants as Const
from logger_controller.logger_control import *

Base = declarative_base()
logger = configure_db_logger()


def init_connection_data():

    init_cnx_db_data = []

    cfg = get_config_constant_file()

    db_host = cfg['DB_ORACLE_TEST']['HOST_DB_TEST']
    db_username = cfg['DB_ORACLE_TEST']['USER_DB_TEST']
    db_password = cfg['DB_ORACLE_TEST']['PASSWORD_DB_TEST']
    db_port = cfg['DB_ORACLE_TEST']['PORT_DB_TEST']
    db_driver = cfg['DB_ORACLE_TEST']['SQL_DRIVER']

    data_connection = [db_host, db_username, db_password, db_port, db_driver]

    init_cnx_db_data.append(data_connection)

    return data_connection


def connect_to_db():
    """Connect to Oracle DB.

    Opens a connection to a PostgreSQL DB.
    When a database is accessed by multiple connections, and one of the
    processes modifies the database, the SQLite database is locked until that
    transaction is committed.

    Parameters
    ----------
    hosts : str
    password : str
    username : str
    port : str
    service_name : str

        database data to stablish connection

    Returns
    -------
    connection : cx_Oracle.connect
        connection object
    """

    data_bd_connection = init_connection_data()

    try:

        if data_bd_connection[0] is not None and data_bd_connection[1] is not None \
           and data_bd_connection[4] is not None:

            db_url = {
                'drivername': data_bd_connection[4],
                'username': data_bd_connection[1],
                'password': data_bd_connection[2],
                'host': data_bd_connection[0],
                'port': data_bd_connection[3]
            }

            engine = create_engine(URL(**db_url))
            
            # create session
            Session = sessionmaker()
            
            Session.configure(bind=engine)
            
            session = Session()
            
        else:
            logger.error('Some data is not established to connect Oracle DB. Please verify it!')

    except SQLAlchemyError as session_error:
        session.rollback()
        logger.exception('Can not connect to database, verify data connection to %s', data_bd_connection[4],
                         session_error, exc_info=True)
        raise mvc_exc.ConnectionError(
            '"{}" Can not connect to database, verify data connection to "{}".\nOriginal Exception raised: {}'.format(
                data_bd_connection[0], data_bd_connection[4], session_error
            )
        )

    return session


def scrub(input_string):
    """Clean an input string (to prevent SQL injection).

    Parameters
    ----------
    input_string : str

    Returns
    -------
    str
    """
    return "".join(k for k in input_string if k.isalnum())


def disconnect_from_db(session):
    if session is not None:
        session.close()


def get_systimestamp_date(session):

    last_updated_date_column = session.execute('SELECT systimestamp from dual').scalar()

    logger.info('Timestamp from DUAL: %s', last_updated_date_column)

    return last_updated_date_column


def exists_data_row(session, table_name, column_name, column_filter1, value1, column_filter2, value2):

    value1 = scrub(value1)
    value2 = scrub(value2)

    # Column_validate = brand
    # table_name = tv_int_marcas_ofix_v
    # column_filter1 = integracion_id
    # value1 = 2
    # column_filter2 = marca_id
    # value2 = '102'

    sql_exists = 'SELECT {} FROM {} WHERE {} = {} AND {} = {}'.format(column_name, table_name,
                                                                      column_filter1, value1,
                                                                      column_filter2, "'"+value2+"'")

    row_exists = session.execute(sql_exists).scalar()

    logger.info('Exists Data Result: %s', row_exists)

    if not row_exists:
        row_exists = None

    return row_exists


def validate_brand_exists(session, integration_id, brand_id):

    brand_validation = session.query(BrandTable).filter(BrandTable.integracion_id == integration_id).\
        filter(BrandTable.marca_id == "'"+brand_id+"'").scalar()

    return brand_validation


def update_brand(session, integration_id, brand_id, brand):

    last_update_date = get_systimestamp_date(session)

    # update row to database
    session.query(BrandTable).filter(BrandTable.integracion_id == integration_id).\
        filter(BrandTable.marca_id == "'"+brand_id+"'").update({"brand": "'"+brand+"'",
                                                                "last_update_date": last_update_date},
                                                               synchronize_session='fetch')

    # check update correct
    row = session.query(BrandTable).filter(BrandTable.integracion_id == integration_id).\
        filter(BrandTable.marca_id == "'"+brand_id+"'").first()

    logger.info('Brand Updated: %s', row.brand)

    session.commit()


def insert_new_brand(session, integration_id, brand_id, brand):

    cfg = get_config_constant_file()

    last_update_date = get_systimestamp_date(session)
    user_id = cfg['DB_COL_DATA']['USER_ID']
    user_id_upd = cfg['DB_COL_DATA']['USER_ID']

    new_brand = BrandTable(integracion_id=integration_id,
                           marca_id=brand_id,
                           brand=brand,
                           created_by=user_id,
                           last_updated_by=user_id_upd,
                           last_update_date=last_update_date)
    session.add(new_brand)

    # check insert correct
    row_inserted = session.query(BrandTable).filter(BrandTable.integracion_id == integration_id).\
        filter(BrandTable.marca_id == brand_id)

    for data_brand in row_inserted:
        logger.info('Brand inserted is: %s', data_brand.marca_id, ' - ', data_brand.brand)

    session.commit()


class BrandTable(Base):

    cfg = get_config_constant_file()

    __tablename__ = cfg['DB_ORACLE_OBJECTS']['INT_MARCAS']

    integracion_id = Column(cfg['DB_COLUMNS_DATA']['INTEGRATION_ID'], Integer, primary_key=True)
    marca_id = Column(cfg['DB_COLUMNS_DATA']['BRANDS']['BRAND_ID'], String, primary_key=True)
    brand = Column(cfg['DB_COLUMNS_DATA']['BRANDS']['BRAND_NAME'], String)
    created_by = Column(cfg['DB_COLUMNS_DATA']['USER_ID'], Integer)
    last_updated_by = Column(cfg['DB_COLUMNS_DATA']['USER_UPD_ID'], Integer)
    last_update_date = Column(cfg['DB_COLUMNS_DATA']['LAST_UPDATE_DATE'], String)

    def manage_brands_database(self, integration_id, brand_id, brand):

        try:

            session = self

            brand_validation = validate_brand_exists(session, integration_id, brand_id)

            # insert validation
            if brand_validation:

                # update method
                update_brand(session, integration_id, brand_id, brand)

            else:
                # insert
                insert_new_brand(session, integration_id, brand_id, brand)

        except SQLAlchemyError as e:
            logger.exception('An exception was occurred while execute transactions: %s', e)
            raise mvc_exc.ItemNotStored(
                'Can\'t insert marca_id: "{}" with marca: {} because it\'s not stored in "{}"'.format(
                    brand_id, brand, BrandTable.__tablename__
                )
            )
        finally:
            session.close()


def validate_category_exists(session, integration_id, category_id):

    category_validation = session.query(CategoryTable).filter(CategoryTable.integracion_id == integration_id). \
        filter(CategoryTable.category_id == "'"+category_id+"'").scalar()

    return category_validation


def update_category_by_name(session, integration_id, category_id, category_name, parent_id):

    last_update_date = get_systimestamp_date(session)

    # update row to database
    session.query(CategoryTable).filter(CategoryTable.integracion_id == integration_id).\
        filter(CategoryTable.category_id == "'"+category_id+"'").update({"category": "'"+category_name+"'",
                                                                         "last_update_date": last_update_date,
                                                                         "parent_id": parent_id},
                                                                        synchronize_session='fetch')

    # check update correct
    row = session.query(CategoryTable).filter(CategoryTable.integracion_id == integration_id). \
        filter(CategoryTable.category_id == "'"+category_name+"'").first()

    logger.info('Category Updated: Category_Id -> %s', row.category_id + " Category_Name -> " + row.category +
                " Parent_Id -> " + row.parent_id)

    session.commit()


def insert_new_category(session, integration_id, category_id, category_name, parent_id):

    cfg = get_config_constant_file()

    last_update_date = get_systimestamp_date(session)
    user_id = cfg['DB_COL_DATA']['USER_ID']
    user_id_upd = cfg['DB_COL_DATA']['USER_ID']

    new_category = CategoryTable(integracion_id=integration_id,
                                 category_id=category_id,
                                 parent_id=parent_id,
                                 category=category_name,
                                 created_by=user_id,
                                 last_updated_by=user_id_upd,
                                 last_update_date=last_update_date,
                                 status=cfg['DB_COL_DATA']['STATUS_ACTIVO'])

    session.add(new_category)

    # check insert correct
    row_inserted = session.query(CategoryTable).filter(CategoryTable.integracion_id == integration_id).\
        filter(CategoryTable.category_id == category_id)

    for data_category in row_inserted:
        logger.info('Category inserted is: %s', data_category.category_id, ' - ', data_category.category_name)

    session.commit()


class CategoryTable(Base):

    cfg = get_config_constant_file()

    __tablename__ = cfg['DB_ORACLE_OBJECTS']['INT_CATEGORIES']

    integracion_id = Column(cfg['DB_COLUMNS_DATA']['INTEGRATION_ID'], Integer, primary_key=True)
    category_id = Column(cfg['DB_COLUMNS_DATA']['CATEGORIES']['CAT_ID'], String, primary_key=True)
    parent_id = Column(cfg['DB_COLUMNS_DATA']['CATEGORIES']['PARENT_ID'], String)
    category_name = Column(cfg['DB_COLUMNS_DATA']['CATEGORIES']['CAT_NAME'], String)
    created_by = Column(cfg['DB_COLUMNS_DATA']['USER_ID'], Integer)
    last_updated_by = Column(cfg['DB_COLUMNS_DATA']['USER_UPD_ID'], String)
    last_update_date = Column(cfg['DB_COLUMNS_DATA']['LAST_UPDATE_DATE'], String)
    status = Column(cfg['DB_COLUMNS_DATA']['STATUS'], String)

    def manage_categories_database(self, integration_id, category_id, parent_cat_id, category_name):

        try:
            session = self

            category_exists = validate_category_exists(session, integration_id, category_id)

            if category_exists:

                # update method
                update_category_by_name(session, integration_id, category_id, category_name, parent_cat_id)

            else:

                # insert method

                insert_new_category(session, integration_id, category_id, category_name, parent_cat_id)

        except SQLAlchemyError as error:
            logger.exception('An exception was occurred while execute transactions: %s', error)
            raise mvc_exc.ItemNotStored(
                'Can\'t insert category_id: "{}" with Category: {} because it\'s not stored in "{}"'.format(
                    category_id, category_name, CategoryTable.__tablename__
                )
            )
        finally:
            session.close()


def validate_price_in_sku_exists(session, integration_id, sku):

    price_validation = session.query(PricesTable).filter(PricesTable.integracion_id == integration_id).\
        filter(PricesTable.sku == "'"+sku+"'").scalar()

    return price_validation


def update_product_price(session, integration_id, sku, stock_total, precio, moneda, tipo_cambio):

    last_update_date = get_systimestamp_date(session)

    # update row to database
    session.query(PricesTable).filter(PricesTable.integracion_id == integration_id).\
        filter(PricesTable.sku == "'"+sku+"'").update({"stock_total": stock_total,
                                                       "precio": precio,
                                                       "moneda": moneda,
                                                       "tipo_cambio": tipo_cambio,
                                                       "last_update_date": last_update_date},
                                                      synchronize_session='fetch')

    # check update correct
    row = session.query(PricesTable).filter(PricesTable.integracion_id == integration_id).\
        filter(PricesTable.sku == "'"+sku+"'").first()

    logger.info('Category Updated: SKU -> %s', row.sku + " Precio -> " + row.precio +
                " Stock_Total -> " + row.stock_total)

    session.commit()


def insert_new_product_price(session, integration_id, sku, stock_total, precio, moneda, tipo_cambio):
    cfg = get_config_constant_file()

    last_update_date = get_systimestamp_date(session)
    user_id = cfg['DB_COL_DATA']['USER_ID']
    user_id_upd = cfg['DB_COL_DATA']['USER_ID']

    new_product_price = PricesTable(integracion_id=integration_id,
                                    sku=sku,
                                    stock_total=stock_total,
                                    precio=precio,
                                    created_by=user_id,
                                    last_updated_by=user_id_upd,
                                    last_update_date=last_update_date,
                                    moneda=moneda,
                                    tipo_cambio=tipo_cambio)

    session.add(new_product_price)

    # check insert correct
    row_inserted = session.query(PricesTable).filter(PricesTable.integracion_id == integration_id).\
        filter(PricesTable.sku == sku)

    for data_price in row_inserted:
        logger.info('Price inserted is: %s', data_price.sku, ' - ', data_price.price, ' - ', data_price.stock_total)

    session.commit()


class PricesTable(Base):

    cfg = get_config_constant_file()

    __tablename__ = cfg['DB_ORACLE_OBJECTS']['INT_PRICES']

    integracion_id = Column(cfg['DB_COLUMNS_DATA']['INTEGRATION_ID'], Integer, primary_key=True)
    sku = Column(cfg['DB_COLUMNS_DATA']['PRICES']['SKU'], String, primary_key=True)
    stock_total = Column(cfg['DB_COLUMNS_DATA']['PRICES']['STOCK_TOTAL'], Integer)
    precio = Column(cfg['DB_COLUMNS_DATA']['PRICES']['PRECIO'], Numeric)
    created_by = Column(cfg['DB_COLUMNS_DATA']['USER_ID'], Integer)
    last_updated_by = Column(cfg['DB_COLUMNS_DATA']['USER_UPD_ID'], String)
    last_update_date = Column(cfg['DB_COLUMNS_DATA']['LAST_UPDATE_DATE'], String)
    moneda = Column(cfg['DB_COLUMNS_DATA']['PRICES']['MONEDA'], String)
    tipo_cambio = Column(cfg['DB_COLUMNS_DATA']['PRICES']['TIPO_CAMBIO'], Numeric)

    def manage_prices_database(self, integration_id, sku, stock_total, price, moneda, tipo_cambio):
        try:
            session = self

            valid_product_price = validate_price_in_sku_exists(session, integration_id, sku)

            if valid_product_price:

                update_product_price(session, integration_id, sku, stock_total, price, moneda, tipo_cambio)

            else:

                insert_new_product_price(session, integration_id, sku, stock_total, price, moneda, tipo_cambio)

        except SQLAlchemyError as error:
            logger.exception('An exception was occurred while execute transactions: %s', error)
            raise mvc_exc.ItemNotStored(
                'Can\'t insert SKU: "{}" with Precio: {} because it\'s not stored in "{}"'.format(
                    sku, price, PricesTable.__tablename__
                )
            )
        finally:
            session.close()


# DO NOT USE IT
def select_all_by_filter(session, table_name, table_name2, column_filter, value_filter):

    value_filter = scrub(value_filter)

    # table_name = tv_int_productos_ofix_v
    # table_name2 = tv_int_marcas_ofix_v
    # column_filter = CATEGORY_ID
    # value_filter = 150

    try:
        sql = "SELECT * FROM {} " \
              "WHERE EXISTS (SELECT * " \
              "              FROM {} " \
              "              WHERE tv_int_productos_ofix_v.marca_id = tv_int_marcas_ofix_v.marca_id) " \
              "AND status = 'ACTIVO' " \
              "and vender = 'SI' and {} = {}".format(table_name, table_name2, column_filter, value_filter)

        result = session.execute(sql)

        for row in result:
            if row is not None:
                logger.info(row)
            else:
                logger.error('Can not read the recordset, beacause is not stored')
                raise SQLAlchemyError(
                    "Can\'t read data because it\'s not stored in table {}. SQL Exception".format(table_name)
                )

    except SQLAlchemyError as sql_exc:
        logger.exception(sql_exc)
    finally:
        session.close()

    return result


# Define y obtiene el configurador para las constantes del sistema:
def get_config_constant_file():
    """
        Contiene la obtencion del objeto config
        para setear datos de constantes en archivo
        configurador

    :rtype: object
    """
    _constants_file = "/ofix/tienda_virtual/constants/constants.yml"
    cfg = Const.get_constants_file(_constants_file)

    return cfg

