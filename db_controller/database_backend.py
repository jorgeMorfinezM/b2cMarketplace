# -*- coding: utf-8 -*-
"""
Requires Python 3.0 or later
"""

__author__ = "Jorge Morfinez Mojica (jorgemorfinez@ofix.mx)"
__copyright__ = "Copyright 2019, Jorge Morfinez Mojica"
__license__ = "Ofix S.A. de C.V."
__history__ = """ """
__version__ = "1.19.L20.Prod ($Rev: 3 $)"

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

    # TEST:
    # db_host = cfg['DB_ORACLE_TEST']['HOST_DB_TEST']
    # db_username = cfg['DB_ORACLE_TEST']['USER_DB_TEST']
    # db_password = cfg['DB_ORACLE_TEST']['PASSWORD_DB_TEST']
    # db_port = cfg['DB_ORACLE_TEST']['PORT_DB_TEST']
    # db_driver = cfg['DB_ORACLE_TEST']['SQL_DRIVER']

    # DB PROD:
    db_host = cfg['DB_ORACLE_PROD']['HOST_DB']
    db_username = cfg['DB_ORACLE_PROD']['USER_DB']
    db_password = cfg['DB_ORACLE_PROD']['PASSWORD_DB']
    db_port = cfg['DB_ORACLE_PROD']['PORT_DB']
    db_driver = cfg['DB_ORACLE_PROD']['SQL_DRIVER']

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
    host : str
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

    session = None

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

            # create session - SI
            Session = sessionmaker()

            Session.configure(bind=engine)

            session = Session()

            # another kind of connect to DB:
            # Session = sessionmaker(bind=engine)

            # conn = engine.connect()

            # session = Session(bind=conn)

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


# noinspection SqlInjection
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
                                                                      column_filter2, "'" + value2 + "'")

    row_exists = session.execute(sql_exists).scalar()

    logger.info('Exists Data Result: %s', row_exists)

    if not row_exists:
        row_exists = None

    return row_exists


def validate_brand_exists(session, integration_id, brand_id):
    brand_validation = session.query(BrandTable).filter(BrandTable.integracion_id == integration_id). \
        filter(BrandTable.marca_id == brand_id).scalar()

    logger.info('Datos a validar Marca almacenada en BD: %s', 'Integracion_Id: {}, Marca_Id: {}'.format(integration_id,
                                                                                                        brand_id))

    return brand_validation


def update_brand(session, integration_id, brand_id, brand):
    last_update_date = get_systimestamp_date(session)

    # update row to database
    session.query(BrandTable).filter(BrandTable.integracion_id == integration_id). \
        filter(BrandTable.marca_id == brand_id).update({"brand": brand,
                                                        "last_update_date": last_update_date},
                                                       synchronize_session='fetch')

    # check update correct
    row = session.query(BrandTable).filter(BrandTable.integracion_id == integration_id). \
        filter(BrandTable.marca_id == brand_id).first()

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
    row_inserted = session.query(BrandTable).filter(BrandTable.integracion_id == integration_id). \
        filter(BrandTable.marca_id == brand_id)

    for data_brand in row_inserted:
        logger.info('Brand inserted is: %s', 'Marca_ID: {}, Nombre_Marca: {}'.format(data_brand.marca_id,
                                                                                     data_brand.brand))

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

                logger.info('Brand stored on database: %s', brand_validation)

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
        filter(CategoryTable.category_id == category_id).scalar()

    logger.info('Data Category store validation: %s', 'Integracion_Id: {}, Category_Id: {}'.format(integration_id,
                                                                                                   category_id))

    return category_validation


def update_category_by_name(session, integration_id, category_id, category_name, parent_id):
    last_update_date = get_systimestamp_date(session)

    # update row to database
    session.query(CategoryTable).filter(CategoryTable.integracion_id == integration_id). \
        filter(CategoryTable.category_id == category_id).update({"category": category_name,
                                                                 "last_update_date": last_update_date,
                                                                 "parent_id": parent_id},
                                                                synchronize_session='fetch')

    # check update correct
    row = session.query(CategoryTable).filter(CategoryTable.integracion_id == integration_id). \
        filter(CategoryTable.category_id == category_id).first()

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
    row_inserted = session.query(CategoryTable).filter(CategoryTable.integracion_id == integration_id). \
        filter(CategoryTable.category_id == category_id)

    for data_category in row_inserted:
        logger.info('Category inserted is: %s', 'Category_Id: {}, '
                                                'Category_Name: {}'.format(data_category.category_id,
                                                                           data_category.category))

    session.commit()


class CategoryTable(Base):
    cfg = get_config_constant_file()

    __tablename__ = cfg['DB_ORACLE_OBJECTS']['INT_CATEGORIES']

    integracion_id = Column(cfg['DB_COLUMNS_DATA']['INTEGRATION_ID'], Integer, primary_key=True)
    category_id = Column(cfg['DB_COLUMNS_DATA']['CATEGORIES']['CAT_ID'], String, primary_key=True)
    parent_id = Column(cfg['DB_COLUMNS_DATA']['CATEGORIES']['PARENT_ID'], String)
    category = Column(cfg['DB_COLUMNS_DATA']['CATEGORIES']['CAT_NAME'], String)
    created_by = Column(cfg['DB_COLUMNS_DATA']['USER_ID'], Integer)
    last_updated_by = Column(cfg['DB_COLUMNS_DATA']['USER_UPD_ID'], String)
    last_update_date = Column(cfg['DB_COLUMNS_DATA']['LAST_UPDATE_DATE'], String)
    status = Column(cfg['DB_COLUMNS_DATA']['STATUS'], String)

    def manage_categories_database(self, integration_id, category_id, parent_cat_id, category_name):

        try:
            session = self

            category_exists = validate_category_exists(session, integration_id, category_id)

            if category_exists:

                logger.info('Category stored on database: %s', category_exists)

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
    price_validation = session.query(PricesTable).filter(PricesTable.integracion_id == integration_id). \
        filter(PricesTable.sku == sku).scalar()

    return price_validation


def update_product_price(session, integration_id, sku, stock_total, precio, moneda, tipo_cambio):
    last_update_date = get_systimestamp_date(session)

    # update row to database
    session.query(PricesTable).filter(PricesTable.integracion_id == integration_id). \
        filter(PricesTable.sku == sku).update({"stock_total": stock_total,
                                               "precio": precio,
                                               "moneda": moneda,
                                               "tipo_cambio": tipo_cambio,
                                               "last_update_date": last_update_date},
                                              synchronize_session='fetch')

    # check update correct
    row = session.query(PricesTable).filter(PricesTable.integracion_id == integration_id). \
        filter(PricesTable.sku == sku).first()

    logger.info('Producto Updated Price: %s',
                'Stock_Total: {}, Precio: {}, Moneda: {}, Tipo_Cambio: {}, '
                'Last_Update_Date: {}'.format(stock_total,
                                              precio,
                                              moneda,
                                              tipo_cambio,
                                              str(last_update_date)))

    logger.info('Price Updated: %s',
                'SKU -> {}, Precio -> {}, Stock_Total -> {}, Moneda -> {}, Tipo_Cambio -> {}'.format(row.sku,
                                                                                                     row.precio,
                                                                                                     row.stock_total,
                                                                                                     row.moneda,
                                                                                                     row.tipo_cambio))

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
    row_inserted = session.query(PricesTable).filter(PricesTable.integracion_id == integration_id). \
        filter(PricesTable.sku == sku)

    for data_price in row_inserted:
        logger.info('Price inserted is: %s', 'Producto: {}, Precio: {}, Existencia: {}'.format(data_price.sku,
                                                                                               data_price.precio,
                                                                                               data_price.stock_total))

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

            price_history = HistoryPrices()

            valid_product_price = validate_price_in_sku_exists(session, integration_id, sku)

            if valid_product_price:

                logger.info('Price of product stored on database: %s', valid_product_price)

                logger.info('Producto Updated Price: %s',
                            'Integracion_Id: {}, '
                            'Sku: {}, '
                            'Stock_Total: {}, '
                            'Precio: {}, '
                            'Moneda: {}, '
                            'Tipo_Cambio: {}'.format(integration_id,
                                                     sku,
                                                     stock_total,
                                                     price,
                                                     moneda,
                                                     tipo_cambio))

                update_product_price(session, integration_id, sku, stock_total, price, moneda, tipo_cambio)

                session2 = connect_to_db()

                price_history.manage_history_prices_database(session2,
                                                             integration_id,
                                                             sku,
                                                             stock_total,
                                                             price,
                                                             tipo_cambio,
                                                             moneda)

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


def update_all_products_status(session):
    cfg = get_config_constant_file()

    last_update_date = get_systimestamp_date(session)
    # user_id = cfg['DB_COL_DATA']['USER_ID']
    user_id_upd = cfg['DB_COL_DATA']['USER_ID']
    status = cfg['DB_COL_DATA']['STATUS_INACTIVO']
    integration_id = int(cfg['INTEGRACION_SOURCES']['INTEGRATION_ID'])

    # update row to database
    session.query(ProductsTable).filter(ProductsTable.integracion_id == integration_id). \
        filter(ProductsTable.status != status).update({"status": status,
                                                       "last_updated_by": user_id_upd,
                                                       "last_update_date": last_update_date},
                                                      synchronize_session='fetch')

    session.commit()


def validate_product_exists(session, integration_id, sku):
    product_validation = session.query(ProductsTable).filter(ProductsTable.integracion_id == integration_id). \
        filter(ProductsTable.sku == sku).scalar()

    return product_validation


def update_product_data(session,
                        integration_id,
                        sku,
                        codigo_fab,
                        nombre_prod,
                        length,
                        height,
                        width,
                        weight,
                        category_id,
                        marca_id,
                        short_desc,
                        long_description,
                        url_media,
                        description_producto):

    cfg = get_config_constant_file()

    last_update_date = get_systimestamp_date(session)
    # user_id = cfg['DB_COL_DATA']['USER_ID']
    user_id_upd = cfg['DB_COL_DATA']['USER_ID']
    status = cfg['DB_COL_DATA']['STATUS_ACTIVO']

    session.query(ProductsTable).filter(ProductsTable.integracion_id == integration_id). \
        filter(ProductsTable.sku == sku).update({"codigo_fabricante": codigo_fab,
                                                 "nombre_producto": nombre_prod,
                                                 "length": length,
                                                 "height": height,
                                                 "width": width,
                                                 "weight": weight,
                                                 "category_id": category_id,
                                                 "marca_id": marca_id,
                                                 "descripcion_corta": short_desc,
                                                 "descripcion_larga": long_description,
                                                 "last_updated_by": user_id_upd,
                                                 "last_update_date": last_update_date,
                                                 "status": status,
                                                 "media_url": url_media,
                                                 "description_producto": description_producto},
                                                synchronize_session='fetch')

    session.commit()


def insert_new_product(session,
                       integration_id,
                       sku,
                       codigo_fab,
                       nombre_prod,
                       length,
                       height,
                       width,
                       weight,
                       category_id,
                       marca_id,
                       short_desc,
                       large_description,
                       url_media,
                       description_producto):

    cfg = get_config_constant_file()

    last_update_date = get_systimestamp_date(session)
    user_id = cfg['DB_COL_DATA']['USER_ID']
    user_id_upd = cfg['DB_COL_DATA']['USER_ID']
    status = cfg['DB_COL_DATA']['STATUS_ACTIVO']

    new_product = ProductsTable(integracion_id=integration_id,
                                sku=sku,
                                nombre_producto=nombre_prod,
                                codigo_fabricante=codigo_fab,
                                length=length,
                                height=height,
                                width=width,
                                weight=weight,
                                category_id=category_id,
                                marca_id=marca_id,
                                descripcion_corta=short_desc,
                                descripcion_larga=large_description,
                                created_by=user_id,
                                last_updated_by=user_id_upd,
                                last_update_date=last_update_date,
                                status=status,
                                media_url=url_media,
                                description_producto=description_producto)

    session.add(new_product)

    session.commit()


class ProductsTable(Base):
    cfg = get_config_constant_file()

    __tablename__ = cfg['DB_ORACLE_OBJECTS']['INT_PRODUCTS']

    integracion_id = Column(cfg['DB_COLUMNS_DATA']['INTEGRATION_ID'], Integer, primary_key=True)
    sku = Column(cfg['DB_COLUMNS_DATA']['PRODUCTS']['SKU'], String, primary_key=True)
    codigo_fabricante = Column(cfg['DB_COLUMNS_DATA']['PRODUCTS']['CODIGO_FABRICANTE'], String)
    nombre_producto = Column(cfg['DB_COLUMNS_DATA']['PRODUCTS']['TITULO'], String)
    length = Column(cfg['DB_COLUMNS_DATA']['PRODUCTS']['LENGTH'], Numeric)
    height = Column(cfg['DB_COLUMNS_DATA']['PRODUCTS']['HEIGHT'], Numeric)
    width = Column(cfg['DB_COLUMNS_DATA']['PRODUCTS']['WIDTH'], Numeric)
    weight = Column(cfg['DB_COLUMNS_DATA']['PRODUCTS']['WEIGHT'], Numeric)
    created_by = Column(cfg['DB_COLUMNS_DATA']['USER_ID'], Integer)
    last_updated_by = Column(cfg['DB_COLUMNS_DATA']['USER_UPD_ID'], String)
    last_update_date = Column(cfg['DB_COLUMNS_DATA']['LAST_UPDATE_DATE'], String)
    status = Column(cfg['DB_COLUMNS_DATA']['STATUS'], String)
    category_id = Column(cfg['DB_COLUMNS_DATA']['PRODUCTS']['CATEGORY_ID'], String)
    marca_id = Column(cfg['DB_COLUMNS_DATA']['PRODUCTS']['MARCA_ID'], String)
    media_url = Column(cfg['DB_COLUMNS_DATA']['PRODUCTS']['URL_MEDIA'], String)
    descripcion_corta = Column(cfg['DB_COLUMNS_DATA']['PRODUCTS']['SHORT_DESCRIPTION'], String)
    descripcion_larga = Column(cfg['DB_COLUMNS_DATA']['PRODUCTS']['DESCRIPCION_LARGA'], String)
    description_producto = Column(cfg['DB_COLUMNS_DATA']['PRODUCTS']['DESCRIPCION_PRODUCTO'], String)

    def manage_products_database(self,
                                 integracion_id,
                                 sku,
                                 codigo_fab,
                                 nombre_prod,
                                 length,
                                 height,
                                 width,
                                 weight,
                                 category_id,
                                 marca_id,
                                 short_desc,
                                 large_description,
                                 url_media,
                                 description_producto):
        try:

            session = self

            product_exists = validate_product_exists(session, integracion_id, sku)

            if product_exists:

                # logger.info('Product Integrator stored on database: %s', product_exists)

                update_product_data(session,
                                    integracion_id,
                                    sku,
                                    codigo_fab,
                                    nombre_prod,
                                    length,
                                    height,
                                    width,
                                    weight,
                                    category_id,
                                    marca_id,
                                    short_desc,
                                    large_description,
                                    url_media,
                                    description_producto)

            else:

                insert_new_product(session,
                                   integracion_id,
                                   sku,
                                   codigo_fab,
                                   nombre_prod,
                                   length,
                                   height,
                                   width,
                                   weight,
                                   category_id,
                                   marca_id,
                                   short_desc,
                                   large_description,
                                   url_media,
                                   description_producto)

                # product_inserted = validate_product_exists(session, integracion_id, sku)

                logger.info('Product Inserted: %s', 'SKU: {}; '
                                                    'Producto: {}, '
                                                    'Descripcion_Larga: {}'.format(sku,
                                                                                   nombre_prod,
                                                                                   large_description))

        except SQLAlchemyError as error:
            session.rollback()
            logger.exception('An exception was occurred while execute transactions: %s', error)
            raise mvc_exc.ItemNotStored(
                'Can\'t insert product SKU: "{}" with Integracion_Id "{}" because it\'s not stored in "{}"'.format(
                    sku, integracion_id, ProductsTable.__tablename__
                )
            )
        finally:
            session.close()


def insert_new_price_history(session,
                             integration_id,
                             sku,
                             stock_total,
                             precio,
                             tipo_cambio,
                             moneda):

    cfg = get_config_constant_file()

    # last_update_date = get_systimestamp_date(session)
    user_id = cfg['DB_COL_DATA']['USER_ID']
    # user_id_upd = cfg['DB_COL_DATA']['USER_ID']

    new_price = HistoryPrices(integracion_id=integration_id,
                              sku=sku,
                              stock_total=stock_total,
                              precio=precio,
                              created_by=user_id,
                              tipo_cambio=tipo_cambio,
                              moneda=moneda)

    session.add(new_price)

    session.commit()


class HistoryPrices(Base):
    cfg = get_config_constant_file()

    __tablename__ = cfg['DB_ORACLE_OBJECTS']['INT_HIST_PRICES']

    integracion_id = Column(cfg['DB_COLUMNS_DATA']['INTEGRATION_ID'], Integer, primary_key=True)
    sku = Column(cfg['DB_COLUMNS_DATA']['PRICES_HIST']['SKU'], String)
    stock_total = Column(cfg['DB_COLUMNS_DATA']['PRICES_HIST']['STOCK_TOTAL'], Integer)
    precio = Column(cfg['DB_COLUMNS_DATA']['PRICES_HIST']['PRECIO'], Numeric)
    created_by = Column(cfg['DB_COLUMNS_DATA']['USER_ID'], Integer)
    tipo_cambio = Column(cfg['DB_COLUMNS_DATA']['PRICES_HIST']['TIPO_CAMBIO'], Integer)
    moneda = Column(cfg['DB_COLUMNS_DATA']['PRICES_HIST']['MONEDA'], String)

    def manage_history_prices_database(self, session2, integracion_id, sku, stock_total, precio, tipo_cambio, moneda):

        session = None

        try:

            session = session2

            logger.info('Producto Updated Price: %s',
                        'Integracion_Id: {}, '
                        'Sku: {}, '  
                        'Stock_Total: {}, '
                        'Precio: {}, '
                        'Moneda: {}, '
                        'Tipo_Cambio: {}'.format(integracion_id,
                                                 sku,
                                                 stock_total,
                                                 precio,
                                                 moneda,
                                                 tipo_cambio))

            insert_new_price_history(session,
                                     integracion_id,
                                     sku,
                                     stock_total,
                                     precio,
                                     tipo_cambio,
                                     moneda)

        except SQLAlchemyError as error:
            session.rollback()
            logger.exception('An exception was occurred while execute transactions: %s', error)
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

        sql = ("SELECT * FROM %(table_name)s "
               "WHERE EXISTS (SELECT * "
               "              FROM %(table_name2)s "
               "              WHERE tv_int_productos_ofix_v.marca_id = tv_int_marcas_ofix_v.marca_id) "
               "AND status = 'ACTIVO' "
               "and vender = 'SI' and %(column_filter)s' = %(value_filter)s'",
               dict(table_name=table_name, table_name2=table_name2, column_filter=column_filter,
                    value_filter=value_filter))

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

    # TEST
    # _constants_file = "constants/constants.yml"

    # PROD
    _constants_file = "constants/constants.yml"

    cfg = Const.get_constants_file(_constants_file)

    return cfg
