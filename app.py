# -*- coding: utf-8 -*-
"""
Requires Python 3.0 or later
"""

__author__ = "Jorge Morfinez Mojica (jorgemorfinez@ofix.mx)"
__copyright__ = "Copyright 2019, Jorge Morfinez Mojica"
__license__ = "Ofix S.A. de C.V."
__history__ = """ """
__version__ = "1.19.I20.Prod ($Rev: 100 $)"

import xmltodict
from json2xml import readfromstring
from datetime import datetime
import codecs
import re
from ws_controller import ws_control
from authentication.ws_auth import *
from db_controller.database_backend import *
from constants.constants import Constants as Const
from logger_controller.logger_control import *

logger = configure_logger()


def get_token_auth_ws():

    oauth_token = parse_json_token_response()

    return oauth_token


def update_all_products_integration(session):
    database_cnx_data = []
    # session = None

    try:

        database_cnx_data = init_connection_data()

        # session = connect_to_db()

        update_all_products_status(session)

    except SQLAlchemyError as error:
        raise mvc_exc.ConnectionError(
            '"{}@{}" Can\'t connect to database, verify data connection to "{}".\nOriginal Exception raised: {}'.format(
                database_cnx_data[1], database_cnx_data[0], database_cnx_data[4], error
            )
        )
    # finally:
    #    session.close()


def manage_marcas_database(session, integracion_id, marca_id, marca_nombre):
    database_cnx_data = []
    # session = None

    try:
        database_cnx_data = init_connection_data()

        # session = connect_to_db()

        BrandTable.manage_brands_database(session, integracion_id, marca_id, marca_nombre)

        logger.info('Marca inserted/updated in database: %s', ' Id_Marca: "{}", Marca: "{}" '.format(marca_id,
                                                                                                     marca_nombre))

    except SQLAlchemyError as error:
        raise mvc_exc.ConnectionError(
            '"{}@{}" Can\'t connect to database, verify data connection to "{}".\nOriginal Exception raised: {}'.format(
                database_cnx_data[1], database_cnx_data[0], database_cnx_data[4], error
            )
        )
    # finally:
    #    session.close()


def manage_categorias_database(session, integracion_id, category_id, parent_cat_id, category_name):
    database_cnx_data = []
    # session = None

    try:
        database_cnx_data = init_connection_data()

        # session = connect_to_db()

        CategoryTable.manage_categories_database(session, integracion_id, category_id, parent_cat_id, category_name)

        logger.info('Categoria/Subcategoria inserted/updated in database: %s',
                    'Id_Categoria: "{}", Categoria: "{}", Parent_Category_Id: "{}"'.format(category_id,
                                                                                           category_name,
                                                                                           parent_cat_id))

    except SQLAlchemyError as error:
        raise mvc_exc.ConnectionError(
            '"{}@{}" Can\'t connect to database, verify data connection to "{}".\nOriginal Exception raised: {}'.format(
                database_cnx_data[1], database_cnx_data[0], database_cnx_data[4], error
            )
        )
    # finally:
    #    session.close()


def manage_precios_productos_database(session, integracion_id, sku, stock_total, price, moneda, tipo_cambio):
    database_cnx_data = []
    # session = None

    try:

        database_cnx_data = init_connection_data()

        # session = connect_to_db()

        logger.info('Precio for producto inserted/updated: %s',
                    'SKU: "{}", Precio: "{}", Stock: "{}", Moneda: "{}", Tipo_Cambio: "{}"'.format(sku,
                                                                                                   price,
                                                                                                   stock_total,
                                                                                                   moneda,
                                                                                                   tipo_cambio))

        PricesTable.manage_prices_database(session, integracion_id, sku, stock_total, price, moneda, tipo_cambio)

    except SQLAlchemyError as error:
        raise mvc_exc.ConnectionError(
            '"{}@{}" Can\'t connect to database, verify data connection to "{}".\nOriginal Exception raised: {}'.format(
                database_cnx_data[1], database_cnx_data[0], database_cnx_data[4], error
            )
        )
    # finally:
    #    session.close()


# noinspection PyArgumentList
def manage_productos_integrador_database(session,
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
    database_cnx_data = []
    # session = None

    try:

        database_cnx_data = init_connection_data()

        # session = connect_to_db()

        logger.info('A Producto was inserted/updated in database: %s',
                    'SKU: "{}", Nombre: "{}", Codigo_Fabricante: "{}"'.format(sku, nombre_prod, codigo_fab))

        # noinspection PyArgumentList
        ProductsTable.manage_products_database(session,
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

    except SQLAlchemyError as error:
        raise mvc_exc.ConnectionError(
            '"{}@{}" Can\'t connect to database, verify data connection to "{}".\nOriginal Exception raised: {}'.format(
                database_cnx_data[1], database_cnx_data[0], database_cnx_data[4], error
            )
        )
    # finally:
    #    session.close()


def manage_history_prices_database(session, integracion_id, sku, stock_total, precio, tipo_cambio, moneda):

    database_cnx_data = []

    try:

        database_cnx_data = init_connection_data()

        logger.info('History Price inserted/updated in database: %s',
                    'SKU: {}, Stock_Total: {}, Price: {}'.format(sku, stock_total, precio))

        HistoryPrices.manage_history_prices_database(session,
                                                     integracion_id,
                                                     sku,
                                                     stock_total,
                                                     precio,
                                                     tipo_cambio,
                                                     moneda)

    except SQLAlchemyError as error:
        raise mvc_exc.ConnectionError(
            '"{}@{}" Can\'t connect to database, verify data connection to "{}".\nOriginal Exception raised: {}'.format(
                database_cnx_data[1], database_cnx_data[0], database_cnx_data[4], error
            )
        )


# Metodo para leer un XML desde un archivo almacenado en cualquier directorio:
def read_xml_from_file_to_parse(self):
    pass
    # se setea el nombre del archivo con su directorio en una variable,
    # en este caso el archivo esta dentro del proyecto
    _file_name = self

    with open(_file_name, 'rb') as _file:
        _data = _file.read()
        _file.close()

    return _data


def xml_products_layout_converter():
    pass

    json_layout = {}

    cfg = get_config_constant_file()

    # PROD - AWS EC2
    # file_name = cfg['PATH_LAYOUT_PRODUCTS_CT']['NAME_LAYOUT_PRODUCTS_CT']
    # file_name = '/ofix/tienda_virtual/layouts/integraciones/productos.xml'

    # TEST - Localhost
    # path_layout = cfg['PATH_LAYOUT_PRODUCTS_TEST']
    # name_layout = cfg['NAME_LAYOUT_PRODUCTS_CT']
    file_name = 'resources/productos.xml'
    # file_name = path_layout + name_layout

    # PROD
    # file_name = cfg['PATH_LAYOUT_PRODUCTS_CT']['NAME_LAYOUT_PRODUCTS_CT']

    xml_data = read_xml_from_file_to_parse(file_name)

    data_2_json = xmltodict.parse(xml_data)

    json_productos = json.dumps(data_2_json)

    json_layout = json.loads(json_productos)

    articulos_rows = json_layout["Articulo"]["Producto"]

    articulos_d = json.dumps(articulos_rows)
    articulos = json.loads(articulos_d)

    productos = {}

    lista_datos_productos = []

    for producto in articulos:

        json_productos = json.dumps(producto)
        productos_json = json.loads(json_productos)

        _inventory_35a = '{}'.format(productos_json['existencia']['DFA'])

        if int(_inventory_35a) > 1:

            _sku_producto = '{}'.format(productos_json['clave'])
            _nombre_producto = scrub_data('{}'.format(productos_json['nombre']))
            _codigo_fabricante = scrub_data('{}'.format(productos_json['no_parte']))
            _modelo = scrub_data('{}'.format(productos_json['modelo']))
            _id_marca = '{}'.format(productos_json['idMarca'])
            _marca = scrub_data('{}'.format(productos_json['marca']))
            _descripcion_corta_prodcuto = scrub_data('{}'.format(productos_json['descripcion_corta']))
            _id_categoria = '{}'.format(productos_json['idCategoria'])
            _nombre_categoria = scrub_data('{}'.format(productos_json['categoria']))
            _id_subcategoria = '{}'.format(productos_json['idSubCategoria'])
            _nombre_subcategoria = scrub_data('{}'.format(productos_json['subcategoria']))
            _imagen_producto = '{}'.format(productos_json['imagen'])
            _precio = '{}'.format(productos_json['precio'])
            _moneda = '{}'.format(productos_json['moneda'])
            _tipo_cambio = '{}'.format(productos_json['tipo_cambio'])
            upc = '{}'.format(productos_json['upc'])
            ean = '{}'.format(productos_json['ean'])
            status = '{}'.format(productos_json['status'])
            sustituto = '{}'.format(productos_json['sustituto'])

            especificaciones = {}

            existencia = productos_json['existencia']

            inventory = json.dumps(existencia)
            inventories = json.loads(inventory)

            if 'especificacion' in productos_json:

                especificaciones = productos_json['especificacion']

                espects_d = json.dumps(especificaciones)
                espects_l = json.loads(espects_d)

            else:

                especificaciones = {}

            lista_datos_productos += [{
                "Producto": {
                    "clave": _sku_producto,
                    "no_parte": _codigo_fabricante,
                    "nombre": _nombre_producto,
                    "modelo": _modelo,
                    "idMarca": _id_marca,
                    "marca": _marca,
                    "descripcion_corta": _descripcion_corta_prodcuto,
                    "idCategoria": _id_categoria,
                    "categoria": _nombre_categoria,
                    "idSubCategoria": _id_subcategoria,
                    "subcategoria": _nombre_subcategoria,
                    "imagen": _imagen_producto,
                    "precio": _precio,
                    "moneda": _moneda,
                    "tipo_cambio": _tipo_cambio,
                    "upc": upc,
                    "ean": ean,
                    "status": status,
                    "sustituto": sustituto,
                    "especificacion": espects_l,
                    "existencia": inventories
                }
            }]

    productos = {
        "Articulo": lista_datos_productos
    }

    layout_parsed = json.dumps(productos)
    parsed_layout = json.loads(layout_parsed)

    write_json_products_log(parsed_layout)

    return parsed_layout


def get_tipo_cambio_ws(oauth_token):

    tipo_cambio = 1.0

    # if str(moneda).find("MXN") == -1:

    response = ws_control.consume_ws_tipo_cambio(oauth_token)

    if response.content is not None:

        if 'errorCode' in response.json():

            json_response = response.json()

            error_code = json_response['errorCode']
            error_message = json_response['errorMessage']

            logger.error('An error was occurred while request web service: %s',
                         'ErrorCode: "{}", ErrorMessage: "{}"'.format(error_code, error_message))

        elif response.json() is not None:

            _status_code = response.status_code

            logger.info('Status Response Object from Tipo_Cambio WS: %s', str(_status_code))

            json_data = response.json()  # ESTE SI VA

            if _status_code == 200:
                _text = response.text  # NO VA

                tipo_cambio = json_data['tipoCambio']

    else:
        logger.error('Error de Conexion al WS, intente mas tarde la Busqueda: %s', str(response.content))
    # else:
    #    tipo_cambio = 1

    return tipo_cambio


def get_volumetria_producto(oath_token, sku_ct):

    volumetria_producto = []

    response = ws_control.consume_ws_volumetria(oath_token, sku_ct)

    json_data = response.json()

    peso = 0
    largo = 0
    alto = 0
    ancho = 0

    if str(response).find("HTTPConnectionPool") != -1 or str(response).find("HTTPError") != -1 or \
            str(response).find("ConnectionError") != -1 or str(response).find("TimeOut") != -1 or \
            str(response).find("RequestException") != -1:

        peso = 0
        largo = 0
        alto = 0
        ancho = 0

    else:

        _status_code = response.status_code

        logger.info('Status Response Object from Volumetria WS: %s', str(response.status_code))

        if response is None or 'errorCode' in json_data:
            logger.error('Error de Conexion al WS, intente mas tarde la Busqueda: %s', str(response.text))

            error_code = json_data['errorCode']
            error_message = json_data['errorMessage']

            logger.error('An error was occurred while request web service: %s',
                         'ErrorCode: "{}", ErrorMessage: "{}"'.format(error_code, error_message))
        else:
            if _status_code == 200:

                data_product = json.dumps(json_data)
                product_volume = json.loads(data_product)

                for volume in product_volume:

                    volume_prod = json.dumps(volume)
                    json_volume = json.loads(volume_prod)

                    if 'peso' not in json_volume or (str('{}'.format(json_volume['peso'])).find("None") != -1 or
                                                     str('{}'.format(json_volume['peso'])).find("null") != -1):
                        peso = 0
                    else:
                        peso = '{}'.format(json_volume['peso'])

                    if 'largo' not in json_volume or (str('{}'.format(json_volume['largo'])).find("None") != -1 or
                                                      str('{}'.format(json_volume['largo'])).find("null") != -1):
                        largo = 0
                    else:
                        largo = '{}'.format(json_volume['largo'])

                    if 'alto' not in json_volume or (str('{}'.format(json_volume['alto'])).find("None") != -1 or
                                                     str('{}'.format(json_volume['alto'])).find("null") != -1):
                        alto = 0
                    else:
                        alto = '{}'.format(json_volume['alto'])

                    if 'ancho' not in json_volume or (str('{}'.format(json_volume['ancho'])).find("None") != -1 or
                                                      str('{}'.format(json_volume['ancho'])).find("null") != -1):
                        ancho = 0
                    else:
                        ancho = '{}'.format(json_volume['ancho'])

                    logger.info('Peso en Producto: %s', 'Peso: {}, Largo: {}, Alto: {}, Ancho: {}'.format(str(peso),
                                                                                                          str(largo),
                                                                                                          str(alto),
                                                                                                          str(ancho)))

    volumetria_producto.append(peso)
    volumetria_producto.append(largo)
    volumetria_producto.append(alto)
    volumetria_producto.append(ancho)

    data_volume = [peso, largo, alto, ancho]

    return volumetria_producto


def get_request_promo_inventory_price_product(oauth_token, sku_ct, almacen_ct):

    producto_detalle_data = {}

    detail_data_product = {}

    response = ws_control.consume_ws_existencia_detalle_almacen(oauth_token, sku_ct, almacen_ct)

    if str(response).find("HTTPConnectionPool") != -1 or str(response).find("HTTPError") != -1 or \
            str(response).find("ConnectionError") != -1 or str(response).find("TimeOut") != -1 or \
            str(response).find("RequestException") != -1:

        producto_detalle_data = {
            "existencia": 0,
            "precio": 0,
            "moneda": 'MXN',
            "tipo_cambio": 1.0,
            "promociones": []
        }

    else:

        # logger.info('Status Response Object from Existencia_Detalle_Producto CT WS: %s', str(response.status_code))

        status_code = response.status_code

        json_data = response.json()

        logger.info('Existencia_Detalle_Producto from WS: %s', str(json_data))

        if response is None or 'errorCode' in json_data:

            logger.error('Error de Conexion al WS, intente mas tarde la Busqueda: %s', str(response.text))

            error_code = json_data['errorCode']
            error_message = json_data['errorMessage']

            logger.error('An error was occurred while request web service: %s',
                         'ErrorCode: "{}", ErrorMessage: "{}"'.format(error_code, error_message))

            producto_detalle_data = {
                "existencia": 0,
                "precio": 0,
                "moneda": 'MXN',
                "tipo_cambio": 1.0,
                "promociones": []
            }

        else:
            if status_code == 200:

                tipo_cambio = 1.0

                existencia = json_data['existencia']
                precio = json_data['precio']
                moneda = json_data['moneda']

                if 'tipoCambio' in json_data:
                    tipo_cambio = json_data['tipoCambio']

                aplica_promociones = []

                promocion = json_data['promocion']

                logger.info('Promociones: %s', str(promocion))

                if promocion is not None:

                    almacen = json_data['promocion']['almacen']
                    codigo_promo = json_data['promocion']['codigo']
                    fecha_inicio = json_data['promocion']['fechaInicio']
                    fecha_fin = json_data['promocion']['fechaFin']
                    cantidad_descto_promo = json_data['promocion']['cantidad']
                    descto_precio = json_data['promocion']['descuentoPrecio']
                    descto_porcentaje = json_data['promocion']['descuentoPorcentaje']

                    aplica_promociones = {
                        "almacen": almacen,
                        "codigo_promo": codigo_promo,
                        "fecha_inicio": fecha_inicio,
                        "fecha_fin": fecha_fin,
                        "cantidad_descto_promo": cantidad_descto_promo,
                        "precio_descuento": descto_precio,
                        "porcentaje_descuento": descto_porcentaje
                    }

                producto_detalle_data = {
                    "existencia": existencia,
                    "precio": precio,
                    "moneda": moneda,
                    "tipo_cambio": tipo_cambio,
                    "promociones": aplica_promociones
                }

            # detail_data_product = json.dumps(producto_detalle_data)

    detail_data_product = json.dumps(producto_detalle_data)

    return detail_data_product


def parser_products_integration():
    pass

    session = connect_to_db()

    cfg = get_config_constant_file()

    oauth_token_ws = get_token_auth_ws()

    json_layout_prod = xml_products_layout_converter()

    articulos_rows = json_layout_prod["Articulo"]["Producto"]

    articulos_d = json.dumps(articulos_rows)
    articulos = json.loads(articulos_d)

    contador_productos = 0

    lista_datos_productos = []

    integrador_id = cfg['INTEGRACION_SOURCES']['INTEGRATION_ID']

    vendor_id = cfg['INTEGRACION_SOURCES']['VENDOR_ID']

    tipo_cambio_moneda = get_tipo_cambio_ws(oauth_token_ws)

    # Actualiza todos los estatus de los productos del integrador CT:
    update_all_products_integration(session)

    for producto in articulos:

        almacen_ct = cfg['INTEGRACION_SOURCES']['INVENTARIO_ALM_CT']
        id_almacen_ct = cfg['INTEGRACION_SOURCES']['ID_INVENTARIO_CT']

        json_productos = json.dumps(producto)
        productos_json = json.loads(json_productos)

        _inventory_35a = '{}'.format(productos_json['existencia']['DFA'])
        _inventory_01a = '{}'.format(productos_json['existencia']['HMO'])

        # if int(_inventory_35a) > 1:
        _sku_producto = '{}'.format(productos_json['clave'])
        _nombre_producto = scrub_data('{}'.format(productos_json['nombre']))
        _codigo_fabricante = scrub_data('{}'.format(productos_json['no_parte']))
        _modelo = scrub_data('{}'.format(productos_json['modelo']))
        _id_marca = '{}'.format(productos_json['idMarca'])
        _marca = scrub_data('{}'.format(productos_json['marca']))
        _descripcion_corta_prodcuto = scrub_data('{}'.format(productos_json['descripcion_corta']))
        _id_categoria = '{}'.format(productos_json['idCategoria'])
        _nombre_categoria = scrub_data('{}'.format(productos_json['categoria']))
        _id_subcategoria = '{}'.format(productos_json['idSubCategoria'])
        _nombre_subcategoria = scrub_data('{}'.format(productos_json['subcategoria']))
        _imagen_producto = '{}'.format(productos_json['imagen'])
        _precio = '{}'.format(productos_json['precio'])
        _moneda = '{}'.format(productos_json['moneda'])
        _tipo_cambio = '{}'.format(productos_json['tipo_cambio'])

        data_detailed_product = get_request_promo_inventory_price_product(oauth_token_ws,
                                                                          _sku_producto,
                                                                          id_almacen_ct)

        logger.info('Data Detailed Products: %s', str(data_detailed_product))

        # data_detailed = json.dumps(data_detailed_product)
        data_product_detailed = json.loads(data_detailed_product)

        existencia_producto = data_product_detailed["existencia"]

        if int(existencia_producto) > 1:

            # Obtiene la volumetria del producto CT:
            volumetria_producto = get_volumetria_producto(oauth_token_ws, _sku_producto)

            if len(volumetria_producto) != 0:

                weight = volumetria_producto[0]
                length = volumetria_producto[1]
                height = volumetria_producto[2]
                width = volumetria_producto[3]
            else:
                weight = 0
                length = 0
                height = 0
                width = 0

            if length != 0 and height != 0 and width != 0:

                weight = weight_converter(weight)

                contador_productos += 1

                moneda_producto = None
                tipo_cambio = 1.0

                logger.info('Product Inventory: %s', 'SKU: "{}", Inventory: "{}"'.format(str(_sku_producto),
                                                                                         str(existencia_producto)))

                logger.info('Producto en Integrador CT: %s',
                            'SKU: "{}" - "{}", Inventario Total Suc[35A-DFA]: "{} == {}"'.format(_sku_producto,
                                                                                                 _nombre_producto,
                                                                                                 _inventory_35a,
                                                                                                 existencia_producto
                                                                                                 ))

                precio_detalle_producto = data_product_detailed["precio"]
                moneda_detalle_producto = data_product_detailed["moneda"]

                logger.info('Promociones: %s', 'Tamanio_Promos_aplica: {}, Promos: {}'.format(
                    str(len(data_product_detailed["promociones"])), data_product_detailed["promociones"]))

                precio_final_producto = 0

                if moneda_detalle_producto is not None:
                    moneda_producto = moneda_detalle_producto
                elif _moneda is not None:
                    moneda_producto = _moneda

                logger.info('Moneda Producto: %s', str(moneda_producto))

                if str(moneda_producto).find("MXN") == -1:
                    tipo_cambio = tipo_cambio_moneda
                else:
                    tipo_cambio = 1.0

                if data_product_detailed["promociones"] is None or \
                        str(data_product_detailed["promociones"]).find("[]") != -1 \
                        or len(data_product_detailed["promociones"]) == 0:

                    descuento = precio_detalle_producto * tipo_cambio

                    precio_final_producto = decimal_formatting(descuento)

                else:
                    fecha_inicio_promo = data_product_detailed['promociones']['fecha_inicio']
                    fecha_fin_promo = data_product_detailed['promociones']['fecha_fin']
                    cantidad_descto_promo = data_product_detailed['promociones']['cantidad_descto_promo']
                    precio_descto_promo = data_product_detailed['promociones']['precio_descuento']
                    porcentaje_descto_promo = data_product_detailed['promociones']['porcentaje_descuento']

                    today_date_now = datetime.datetime.now()

                    extrae_fecha_inicio_promo = fecha_inicio_promo.split("T")

                    fecha_inicial_promo = extrae_fecha_inicio_promo[0]

                    extrae_fecha_fin_promo = fecha_fin_promo.split("T")

                    fecha_final_promo = extrae_fecha_fin_promo[0]

                    vigencia_inicio_promo = datetime.datetime.strptime(fecha_inicial_promo, "%Y-%m-%d")

                    vigencia_fin_promo = datetime.datetime.strptime(fecha_final_promo, "%Y-%m-%d")

                    logger.info('Aplica Vigencia de la promocion por producto: %s', 'Fecha Inicio Promo: "{}", '
                                                                                    'Fecha Final Promo: "{}", '
                                                                                    'Fecha Actual: "{}"'
                                .format(str(vigencia_inicio_promo), str(vigencia_fin_promo), str(today_date_now)))

                    if vigencia_fin_promo >= today_date_now >= vigencia_inicio_promo:

                        if int(porcentaje_descto_promo) > 0:

                            descuento = ((porcentaje_descto_promo / 100) * precio_detalle_producto) * tipo_cambio

                            precio_final_producto = decimal_formatting((precio_detalle_producto * tipo_cambio) -
                                                                       descuento)

                        elif int(precio_descto_promo) > 0:

                            descuento = tipo_cambio * precio_descto_promo

                            precio_final_producto = decimal_formatting(descuento)

                        # elif int(cantidad_descto_promo):

                        #    descuento = tipo_cambio * cantidad_descto_promo

                        else:
                            descuento = tipo_cambio * precio_detalle_producto

                            precio_final_producto = decimal_formatting(descuento)
                    else:

                        descuento = tipo_cambio * precio_detalle_producto

                        precio_final_producto = decimal_formatting(descuento)

                try:

                    # Realiza transacciones con datos de Marcas para cada producto:
                    manage_marcas_database(session, integrador_id, _id_marca, _marca)

                    # Realiza transacciones con datos en Categorias para cada productos y cada categoria:
                    # if int(_id_categoria) < int(_id_subcategoria):

                    manage_categorias_database(session,
                                               integrador_id,
                                               _id_categoria,
                                               '0',
                                               _nombre_categoria)
                    # else:
                    manage_categorias_database(session,
                                               integrador_id,
                                               _id_subcategoria,
                                               _id_categoria,
                                               _nombre_subcategoria)

                    # Realiza transacciones con datos en Precios para cada producto:
                    manage_precios_productos_database(session,
                                                      integrador_id,
                                                      _sku_producto,
                                                      existencia_producto,
                                                      precio_final_producto,
                                                      moneda_producto,
                                                      tipo_cambio)

                    especs_counter = 1

                    if 'especificacion' in productos_json:

                        especificaciones = productos_json['especificacion']

                        espects_d = json.dumps(especificaciones)
                        espects_l = json.loads(espects_d)

                        logger.info('LEN Especificaciones: %s', str(len(espects_l)))

                        while especs_counter <= len(espects_l):
                            _espec_value = '{}'.format(espects_l['caracteristica' + str(especs_counter)]['valor'])
                            _espec_type = '{}'.format(espects_l['caracteristica' + str(especs_counter)]['tipo'])

                            # _espec_value = _espec_value.encode('utf-8')

                            desc_type = scrub_data(_espec_type)
                            desc_value = scrub_data(_espec_value)
                            
                            descripcion_larga = '|* Modelo: ' + _modelo

                            descripcion_larga += '|* ' + str(desc_type) + ': ' + str(desc_value)

                            especs_counter = especs_counter + 1

                        logger.info('Descripcion_Larga Producto: %s', str(descripcion_larga))

                        manage_productos_integrador_database(session,
                                                             integrador_id,
                                                             _sku_producto,
                                                             _codigo_fabricante,
                                                             _nombre_producto,
                                                             length,
                                                             height,
                                                             width,
                                                             weight,
                                                             _id_subcategoria,
                                                             _id_marca,
                                                             _descripcion_corta_prodcuto,
                                                             descripcion_larga,
                                                             _imagen_producto,
                                                             _descripcion_corta_prodcuto)

                        # session.commit()

                    else:
                        
                        descripcion_larga = '|* Modelo: ' + _modelo

                        logger.info('Descripcion_Larga Producto: %s', str(descripcion_larga))

                        manage_productos_integrador_database(session,
                                                             integrador_id,
                                                             _sku_producto,
                                                             _codigo_fabricante,
                                                             _nombre_producto,
                                                             length,
                                                             height,
                                                             width,
                                                             weight,
                                                             _id_subcategoria,
                                                             _id_marca,
                                                             _descripcion_corta_prodcuto,
                                                             descripcion_larga,
                                                             _imagen_producto,
                                                             _descripcion_corta_prodcuto)

                        # session.commit()

                except SQLAlchemyError as error:
                    session.rollback()
                    raise mvc_exc.ConnectionError(
                        'An exception was occurred while execute transactions:\n'
                        'Original Exception raised: {}'.format(error)
                    )
                finally:
                    session.close()

                lista_datos_productos += [{
                    "Producto": {
                        # "Num_Producto": contador_productos,
                        "SKU": _sku_producto,
                        # "Nombre": _nombre_producto,
                        # "Id_Marca": _id_marca,
                        # "Marca": _marca,
                        # "Descripcion_Corta": _descripcion_corta_prodcuto,
                        # "Descripcion_Larga": descripcion_larga,
                        # "Categoria_Id": _id_categoria,
                        # "Categoria": _nombre_categoria,
                        # "SubCategoria_Id": _id_subcategoria,
                        # "SubCategoria": _nombre_subcategoria,
                        "Imagen": _imagen_producto,
                        "Integrador_Id": integrador_id,
                        "Vendor_Id": vendor_id
                        # "Inventario": existencia_producto,
                        # "Precio": precio_final_producto,
                        # "Volumetria": {
                        #    "Weight": weight,
                        #    "Length": length,
                        #    "Height": height,
                        #    "Width": width
                        # }
                    }
                }]

            else:
                continue

        else:
            continue

        # else:
        # continue

    dict_json_products = {
        "Productos": lista_datos_productos
    }

    products = json.dumps(dict_json_products)

    layout_parsed = readfromstring(products)

    write_json_products_parsed(layout_parsed)

    return products


def validate_data_on_json(json_dict_data):
    pass

    if str(json_dict_data) or json_dict_data is not None or str(json_dict_data) is not None \
            or str(json_dict_data).find("") != -1 or str(json_dict_data).find("null") != -1 \
            or str(json_dict_data).find(" "):
        return json_dict_data
    else:
        return None


def scrub_data(self):
    pass

    import unidecode
    import unicodedata

    # return ' '.format([*filter(str.isalnum, self)])
    self = self.replace("Ä".lower(), "A".lower())
    self = self.replace("Ë".lower(), "E".lower())
    self = self.replace("Ï".lower(), "I".lower())
    self = self.replace("Ö".lower(), "O".lower())
    self = self.replace("Ü".lower(), "U".lower())

    self = self.replace("Â".lower(), "A".lower())
    self = self.replace("Ê".lower(), "E".lower())
    self = self.replace("Î".lower(), "I".lower())
    self = self.replace("Ô".lower(), "O".lower())
    self = self.replace("Û".lower(), "U".lower())

    self = self.replace("Á".lower(), "A".lower())
    self = self.replace("É".lower(), "E".lower())
    self = self.replace("Í".lower(), "I".lower())
    self = self.replace("Ó".lower(), "O".lower())
    self = self.replace("Ú".lower(), "U".lower())

    self = self.replace("À".lower(), "A".lower())
    self = self.replace("È".lower(), "E".lower())
    self = self.replace("Ì".lower(), "I".lower())
    self = self.replace("Ò".lower(), "O".lower())
    self = self.replace("Ù".lower(), "U".lower())

    self = self.replace("Ä", "A")
    self = self.replace("Ë", "E")
    self = self.replace("Ï", "I")
    self = self.replace("Ö", "O")
    self = self.replace("Ü", "U")

    self = self.replace("Â", "A")
    self = self.replace("Ê", "E")
    self = self.replace("Î", "I")
    self = self.replace("Ô", "O")
    self = self.replace("Û", "U")

    self = self.replace("Á", "A")
    self = self.replace("É", "E")
    self = self.replace("Í", "I")
    self = self.replace("Ó", "O")
    self = self.replace("Ú", "U")

    self = self.replace("À", "A")
    self = self.replace("È", "E")
    self = self.replace("Ì", "I")
    self = self.replace("Ò", "O")
    self = self.replace("Ù", "U")

    self = self.replace("Ñ", "N")
    self = self.replace("ñ", "n")

    self = self.replace("m²", "m2")

    self = self.replace("°C", "grados C​")

    self = self.replace("’s", "s")

    self = self.replace("’", "")

    self = self.replace("'", "")

    # self = self.encode("ascii", errors="ignore").decode("utf-8")

    self = self.replace("á", "a")
    self = self.replace("é", "e")
    self = self.replace("í", "i")
    self = self.replace("ó", "o")
    self = self.replace("ú", "u")

    _str_converted = re.sub(r"[^a-z A-Z0-9+-,./_%*:;(){}[\]]", "", self)

    _str_converted = unicodedata.normalize('NFD', _str_converted).encode('ascii', 'ignore').decode("utf-8")

    _str_converted = unidecode.unidecode(_str_converted)

    return _str_converted


def decimal_formatting(value):
    return ('%.2f' % value).rstrip('0').rstrip('.')


def weight_converter(weight):
    return decimal_formatting(float(weight))*1000


# Define y obtiene el configurador para las constantes del sistema:
def get_config_constant_file():
    """Contiene la obtencion del objeto config
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


def write_json_products_log(json_products):
    with codecs.open('logs/json_products.json', 'w', 'utf-8-sig') as outfile:
        json.dump(json_products, outfile)


def write_json_products_parsed(json_parsed):

    today_date_now = datetime.datetime.now()

    extrae_fecha = str(today_date_now).split(" ")

    fecha_layout = extrae_fecha[0]

    cfg = get_config_constant_file()

    layout_path_dir = cfg['PATH_LAYOUT_IMAGES_CT']
    layout_path_name = cfg['NAME_LAYOUT_IMAGES_CT']
    layout_extension_name = cfg['EXT_LAYOUT_IMAGES_CT']

    images_layout = layout_path_dir + layout_path_name + '_' + str(fecha_layout) + '.json'

    # with codecs.open('logs/json_products_images.json', 'w', 'utf-8-sig') as outfile:
    with codecs.open(images_layout, 'w', 'utf-8-sig') as outfile:
        json.dump(json_parsed, outfile)


def main():
    pass
    # json_layout_prod = xml_products_layout_converter()

    # print('Layout JSON Productos CT: ', json_layout_prod)

    ws_clients = []

    dict_json_xml = []

    layout_products = parser_products_integration() # Sí se usa para PROD

    logger.info('Lista_Productos parseados: %s', str(layout_products)) # Sí se usa para PROD


if __name__ == "__main__":
    pass

    start_time = datetime.datetime.now()

    logger.info('CT Products\' Parsing Process Starting: %s', str(start_time))

    main()

    end_time = datetime.datetime.now()

    logger.info('CT Products\' Parsing Process Completed: %s', str(end_time))

    logger.info('CT Products\' Parsing Process execution in: {}'.format(end_time - start_time) + ' seconds')
