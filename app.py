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
from json2xml import readfromstring, readfromjson
from datetime import datetime
import time
import json
import codecs
import xml.etree.ElementTree as Et
import base64
import re
import os
import argparse
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

        PricesTable.manage_prices_database(session, integracion_id, sku, stock_total, price, moneda, tipo_cambio)

        logger.info('Precio for producto inserted/updated: %s',
                    'SKU: "{}", Precio: "{}", Stock: "{}", Moneda: "{}", Tipo_Cambio: "{}"'.format(sku,
                                                                                                   price,
                                                                                                   stock_total,
                                                                                                   moneda,
                                                                                                   tipo_cambio))

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
                                         large_description):
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
                                               large_description)

    except SQLAlchemyError as error:
        raise mvc_exc.ConnectionError(
            '"{}@{}" Can\'t connect to database, verify data connection to "{}".\nOriginal Exception raised: {}'.format(
                database_cnx_data[1], database_cnx_data[0], database_cnx_data[4], error
            )
        )
    # finally:
    #    session.close()


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

    cfg = get_config_constant_file()

    # PROD - AWS EC2
    # file_name = cfg['PATH_LAYOUT_PRODUCTS_CT']['NAME_LAYOUT_PRODUCTS_CT']
    # NOT USE IT: file_name = '/ofix/tienda_virtual/layouts/integraciones/productos.xml'

    # TEST - Localhost
    file_name = 'resources/productos.xml'

    # PROD
    # file_name = cfg['PATH_LAYOUT_PRODUCTS_CT']['NAME_LAYOUT_PRODUCTS_CT']

    xml_data = read_xml_from_file_to_parse(file_name)

    data_2_json = xmltodict.parse(xml_data)

    json_productos = json.dumps(data_2_json)

    json_layout = json.loads(json_productos)

    return json_layout


def get_tipo_cambio_ws(oauth_token, moneda):

    tipo_cambio = 1.0

    if str(moneda).find("MXN") == -1:

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
    else:
        tipo_cambio = 1

    return tipo_cambio


def get_volumetria_producto(oath_token, sku_ct):

    volumetria_producto = []

    response = ws_control.consume_ws_volumetria(oath_token, sku_ct)

    _status_code = response.status_code

    logger.info('Status Response Object from Tipo_Cambio WS: %s', str(response.status_code))

    json_data = response.json()

    if str(response).find("HTTPConnectionPool") != -1 or response is None or str(response).find("HTTPError") != -1 \
            or 'errorCode' in json_data:
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

                if 'peso' in json_volume:

                    if '{}'.format(json_volume['peso']) is None or \
                            str('{}'.format(json_volume['peso'])).find("None") != -1 or \
                            str('{}'.format(json_volume['peso'])).find("null") != -1:
                        peso = 0
                    else:
                        peso = '{}'.format(json_volume['peso'])

                    if '{}'.format(json_volume['largo']) is None or \
                            str('{}'.format(json_volume['largo'])).find("None") != -1 or \
                            str('{}'.format(json_volume['largo'])).find("null") != -1:
                        largo = 0
                    else:
                        largo = '{}'.format(json_volume['largo'])

                    if '{}'.format(json_volume['alto']) is None or \
                            str('{}'.format(json_volume['alto'])).find("None") != -1 or \
                            str('{}'.format(json_volume['alto'])).find("null") != -1:
                        alto = 0
                    else:
                        alto = '{}'.format(json_volume['alto'])

                    if '{}'.format(json_volume['ancho']) is None or \
                            str('{}'.format(json_volume['ancho'])).find("None") != -1 or \
                            str('{}'.format(json_volume['ancho'])).find("null") != -1:
                        ancho = 0
                    else:
                        ancho = '{}'.format(json_volume['ancho'])

                    logger.info('Peso en Producto: %s', 'Peso: {}, Largo: {}, Alto: {}, Ancho: {}'.format(str(peso),
                                                                                                          str(largo),
                                                                                                          str(alto),
                                                                                                          str(ancho)))
                else:
                    peso = 0
                    largo = 0
                    alto = 0
                    ancho = 0

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

    logger.info('Status Response Object from Existencia_Detalle_Producto CT WS: %s', str(response.status_code))

    status_code = response.status_code

    json_data = response.json()

    logger.info('Existencia_Detalle_Producto from WS: %s', str(json_data))

    if str(response).find("HTTPConnectionPool") != -1 or response is None or str(response).find("HTTPError") != -1 \
            or 'errorCode' in json_data:

        logger.error('Error de Conexion al WS, intente mas tarde la Busqueda: %s', str(response.text))

        error_code = json_data['errorCode']
        error_message = json_data['errorMessage']

        logger.error('An error was occurred while request web service: %s',
                     'ErrorCode: "{}", ErrorMessage: "{}"'.format(error_code, error_message))
    else:
        if status_code == 200:

            tipo_cambio = 1.00

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

        detail_data_product = json.dumps(producto_detalle_data)

    return detail_data_product


def parser_products_integration():
    pass

    session = None

    session = connect_to_db()

    cfg = get_config_constant_file()

    oauth_token_ws = get_token_auth_ws()

    json_layout_prod = xml_products_layout_converter()

    articulos_rows = json_layout_prod["Articulo"]["Producto"]

    # write_json_products_log(articulos_rows)

    # print("File saving with Products in JSON!")

    articulos_d = json.dumps(articulos_rows)
    articulos = json.loads(articulos_d)

    contador_productos = 0

    lista_datos_productos = []

    integrador_id = cfg['INTEGRACION_SOURCES']['INTEGRATION_ID']

    vendor_id = cfg['INTEGRACION_SOURCES']['VENDOR_ID']

    for producto in articulos:

        almacen_ct = cfg['INTEGRACION_SOURCES']['INVENTARIO_ALM_CT']
        id_almacen_ct = cfg['INTEGRACION_SOURCES']['ID_INVENTARIO_CT']

        json_productos = json.dumps(producto)
        productos_json = json.loads(json_productos)

        _sku_producto = '{}'.format(productos_json['clave'])
        _nombre_producto = scrub_data('{}'.format(productos_json['nombre']))
        _codigo_fabricante = '{}'.format(productos_json['no_parte'])
        _modelo = '{}'.format(productos_json['modelo'])
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

        data_detailed_product = get_request_promo_inventory_price_product(oauth_token_ws, _sku_producto, id_almacen_ct)

        logger.info('Data Detailed Products: %s', data_detailed_product)

        # data_detailed = json.dumps(data_detailed_product)
        data_product_detailed = json.loads(data_detailed_product)

        existencia_producto = data_product_detailed["existencia"]

        logger.info('Product Inventory: %s', 'SKU: "{}", Inventory: "{}"'.format(str(_sku_producto),
                                                                                 str(existencia_producto)))

        precio_detalle_producto = data_product_detailed["precio"]
        moneda_detalle_producto = data_product_detailed["moneda"]

        tipo_cambio_moneda = get_tipo_cambio_ws(oauth_token_ws, moneda_detalle_producto)

        # tipo_cambio_descto = get_tipo_cambio_ws(oauth_token_ws, moneda_detalle_producto)

        # promociones_product = data_product_detailed["promociones"]

        # promo_prod = json.dumps(promociones_product)
        # json_promo = json.loads(promo_prod)

        logger.info('Promociones: %s', 'Tamanio_Promos_aplica: {}, Promos: {}'.format(
            str(len(data_product_detailed["promociones"])), data_product_detailed["promociones"]))

        if data_product_detailed["promociones"] is None or str(data_product_detailed["promociones"]).find("[]") != -1 \
                or len(data_product_detailed["promociones"]) == 0:

            descuento = 0

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

                    descuento = ((porcentaje_descto_promo / 100) * precio_detalle_producto) * tipo_cambio_moneda

                elif int(precio_descto_promo) > 0:
                    descuento = tipo_cambio_moneda * precio_descto_promo

                elif int(cantidad_descto_promo):
                    descuento = tipo_cambio_moneda * cantidad_descto_promo

                else:
                    descuento = 0
            else:

                descuento = 0

        precio_final_producto = decimal_formatting((precio_detalle_producto * tipo_cambio_moneda) - descuento)

        contador_productos += 1

        _inventory_35a = '{}'.format(productos_json['existencia']['DFA'])

        logger.info('Producto en Integrador CT: %s',
                    'SKU: "{}" - "{}", Inventario Total Suc[35A-DFA]: "{} == {}"'.format(_sku_producto,
                                                                                         _nombre_producto,
                                                                                         _inventory_35a,
                                                                                         existencia_producto))

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

        try:

            # Actualiza todos los estatus de los productos del integrador CT:
            update_all_products_integration(session)

            # Realiza transacciones con datos de Marcas para cada producto:
            manage_marcas_database(session, integrador_id, _id_marca, _marca)

            # Realiza transacciones con datos en Categorias para cada productos y cada categoria:
            if int(_id_categoria) < int(_id_subcategoria):

                manage_categorias_database(session, integrador_id, _id_categoria, '0', _nombre_categoria)
            else:

                manage_categorias_database(session, integrador_id, _id_subcategoria, _id_categoria, _nombre_subcategoria)

            # if int(_inventory_35a) >= 2:

            manage_precios_productos_database(session,
                                              integrador_id,
                                              _sku_producto,
                                              existencia_producto,
                                              precio_final_producto,
                                              moneda_detalle_producto,
                                              tipo_cambio_moneda)

            especs_counter = 1

            descripcion_larga = ' '

            descripcion_larga += '|* Modelo: ' + _modelo

            if 'especificacion' in productos_json:

                especificaciones = productos_json['especificacion']

                espects_d = json.dumps(especificaciones)
                espects_l = json.loads(espects_d)

                logger.info('LEN Especificaciones: %s', str(len(espects_l)))

                while especs_counter <= len(espects_l):
                    _espec_value = '{}'.format(espects_l['caracteristica' + str(especs_counter)]['valor'])
                    _espec_type = '{}'.format(espects_l['caracteristica' + str(especs_counter)]['tipo'])

                    # _espec_value = _espec_value.encode('utf-8')

                    descripcion_larga += '|* ' + scrub_data(_espec_type) + ': ' + scrub_data(_espec_value)

                    especs_counter = especs_counter + 1

                '''
                lista_datos_productos += [{
                    "Producto": {
                        "Num_Producto": contador_productos,
                        "SKU": _sku_producto,
                        "Nombre": _nombre_producto,
                        "Id_Marca": _id_marca,
                        "Marca": _marca,
                        "Descripcion_Corta": _descripcion_corta_prodcuto,
                        "Descripcion_Larga": descripcion_larga,
                        "Categoria_Id": _id_categoria,
                        "Categoria": _nombre_categoria,
                        "SubCategoria_Id": _id_subcategoria,
                        "SubCategoria": _nombre_subcategoria,
                        "Imagen": _imagen_producto,
                        "Inventario": existencia_producto,
                        "Precio": precio_final_producto,
                        "Volumetria": {
                            "Weight": weight,
                            "Length": length,
                            "Height": height,
                            "Width": width
                        }
                    }
                }]
                '''

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
                                                     _id_categoria,
                                                     _id_marca,
                                                     _descripcion_corta_prodcuto,
                                                     descripcion_larga)

            else:

                # continue
                '''
                lista_datos_productos += [{
                    "Producto": {
                        "Num_Producto": contador_productos,
                        "SKU": _sku_producto,
                        "Nombre": _nombre_producto,
                        "Id_Marca": _id_marca,
                        "Marca": _marca,
                        "Descripcion_Corta": _descripcion_corta_prodcuto,
                        "Descripcion_Larga": descripcion_larga,
                        "Categoria_Id": _id_categoria,
                        "Categoria": _nombre_categoria,
                        "SubCategoria_Id": _id_subcategoria,
                        "SubCategoria": _nombre_subcategoria,
                        "Imagen": _imagen_producto,
                        "Inventario": existencia_producto,
                        "Precio": precio_final_producto,
                        "Volumetria": {
                            "Weight": weight,
                            "Length": length,
                            "Height": height,
                            "Width": width
                        }
                    }
                }]
                '''

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
                                                     _id_categoria,
                                                     _id_marca,
                                                     _descripcion_corta_prodcuto,
                                                     descripcion_larga)

        except SQLAlchemyError as error:
            raise mvc_exc.ConnectionError(
                'An exception was occurred while execute transactions:\nOriginal Exception raised: {}'.format(
                    error
                )
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

        # else:
        #    continue

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

    self = self.replace("á", "a")
    self = self.replace("é", "e")
    self = self.replace("í", "i")
    self = self.replace("ó", "o")
    self = self.replace("ú", "u")

    self = self.replace("m²", "m2")

    self = self.replace("°", "grados ​")

    _str_converted = re.sub(r"[^a-z A-Z0-9+-,./_%*:;(){}[\]]", "", self)

    _str_converted = self

    return _str_converted


def decimal_formatting(value):
    return ('%.2f' % value).rstrip('0').rstrip('.')


# Define y obtiene el configurador para las constantes del sistema:
def get_config_constant_file():
    """Contiene la obtencion del objeto config
        para setear datos de constantes en archivo
        configurador

    :rtype: object
    """
    # TEST
    _constants_file = "constants/constants.yml"

    # PROD
    # _constants_file = "/ofix/tienda_virtual/parserCt/constants/constants.yml"
    cfg = Const.get_constants_file(_constants_file)

    return cfg


def write_json_products_log(json_products):
    with codecs.open('logs/json_products.json', 'w', 'utf-8-sig') as outfile:
        json.dump(json_products, outfile)


def write_json_products_parsed(json_parsed):
    with codecs.open('logs/json_products_parsed.json', 'w', 'utf-8-sig') as outfile:
        json.dump(json_parsed, outfile)


def main():
    pass
    # json_layout_prod = xml_products_layout_converter()

    # print('Layout JSON Productos CT: ', json_layout_prod)

    ws_clients = []

    dict_json_xml = []

    layout_products = parser_products_integration()

    logger.info('Lista_Productos parseados: %s', str(layout_products))


if __name__ == "__main__":
    pass

    start_time = datetime.datetime.now()

    logger.info('CT Products\' Parsing Process Starting: %s', str(start_time))

    main()

    end_time = datetime.datetime.now()

    logger.info('CT Products\' Parsing Process Completed: %s', str(end_time))

    logger.info('CT Products\' Parsing Process execution in: {}'.format(end_time - start_time) + ' seconds')
