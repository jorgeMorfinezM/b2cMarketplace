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
from db_controller import *


# Metodo para leer un XML desde un archivo almacenado en cualquier directorio:
def read_xml_from_file_to_parse(self):
    pass
    # se setea el nombre del archivo con su directorio en una variable,
    # en este caso el archivo esta dentro del proyecto
    _file_name = self

    _file = open(_file_name, 'rb')
    _data = _file.read()
    _file.close()

    # byte_array = xml_docto_base64_encoded(_data.decode())
    return _data


'''
def parse_xml_products():
    pass

    file_name = 'productos.xml'

    xml_data = read_xml_from_file_to_encode(file_name)

    print('Data en XML sin parsear: ', xml_data)

    root_layout_products = Et.fromstring(xml_data)

    sku_producto = []

    for sku in root_layout_products.findall("clave"):
        sku_producto.append(sku.text)

    return sku_producto
'''


def write_json_products_log(json_products):

    with codecs.open('logs/json_products.json', 'w', 'utf-8-sig') as outfile:
        json.dump(json_products, outfile)


def write_json_products_parsed(json_parsed):

    with codecs.open('logs/json_products_parsed.json', 'w', 'utf-8-sig') as outfile:
        json.dump(json_parsed, outfile)


def xml_products_layout_converter():
    pass

    # PROD - AWS EC2
    # file_name = '/ofix/tienda_virtual/layouts/integraciones/productos.xml'

    # TEST
    file_name = 'productos.xml'

    xml_data = read_xml_from_file_to_parse(file_name)

    data_2_json = xmltodict.parse(xml_data)

    json_productos = json.dumps(data_2_json)

    json_layout = json.loads(json_productos)

    return json_layout


def parser_products_integration():
    pass

    json_layout_prod = xml_products_layout_converter()

    articulos_rows = json_layout_prod["Articulo"]["Producto"]

    write_json_products_log(articulos_rows)

    print("File saving with Products in JSON!")

    articulos_d = json.dumps(articulos_rows)
    articulos = json.loads(articulos_d)

    contador_productos = 0

    lista_datos_productos = []

    for producto in articulos:

        especs_counter = 1

        caracteristicas = ''

        json_productos = json.dumps(producto)
        productos_json = json.loads(json_productos)

        _sku_producto = '{}'.format(productos_json['clave'])
        _nombre_producto = scrub_data('{}'.format(productos_json['nombre']))
        _id_marca = '{}'.format(productos_json['idMarca'])
        _marca = scrub_data('{}'.format(productos_json['marca']))
        _descripcion_corta_prodcuto = scrub_data('{}'.format(productos_json['descripcion_corta']))
        _id_categoria = '{}'.format(productos_json['idCategoria'])
        _nombre_categoria = '{}'.format(productos_json['categoria'])
        _id_subcategoria = '{}'.format(productos_json['idSubCategoria'])
        _nombre_subcategoria = '{}'.format(productos_json['subcategoria'])
        _imagen_producto = '{}'.format(productos_json['imagen'])
        _precio = '{}'.format(productos_json['precio'])
        _moneda = '{}'.format(productos_json['moneda'])
        _tipo_cambio = '{}'.format(productos_json['tipo_cambio'])

        contador_productos += 1

        _inventory_35a = '{}'.format(productos_json['existencia']['DFA'])

        print('SKU Producto: ', str(_sku_producto))
        print('Descripcion_Corta: ', str(_descripcion_corta_prodcuto))
        print('Inventario Producto DFA: ', str(_inventory_35a))

        # if validate_data_on_json(productos_json['especificacion']) is not None:
        # if hasattr(productos_json, 'especificacion'):

        # if int(_inventory_35a) >= 2:

        if 'especificacion' in productos_json:

            especificaciones = productos_json['especificacion']

            espects_d = json.dumps(especificaciones)
            espects_l = json.loads(espects_d)

            # print('Especificaciones en Producto: ', str(espects_l))
            print('LEN Especificaciones: ', str(len(espects_l)))

            while especs_counter <= len(espects_l):

                _espec_value = '{}'.format(espects_l['caracteristica'+str(especs_counter)]['valor'])
                _espec_type = '{}'.format(espects_l['caracteristica'+str(especs_counter)]['tipo'])

                # _espec_value = _espec_value.encode('utf-8')

                caracteristicas += '|* ' + scrub_data(_espec_type) + ': ' + scrub_data(_espec_value)

                especs_counter += 1

            lista_datos_productos += [{
                "Producto": {
                    "Num_Producto": contador_productos,
                    "SKU": _sku_producto,
                    "Nombre": _nombre_producto,
                    "Id_Marca": _id_marca,
                    "Marca": _marca,
                    "Descripcion_Corta": _descripcion_corta_prodcuto,
                    "Descripcion_Larga": caracteristicas,
                    "Categoria_Id": _id_categoria,
                    "Categoria": _nombre_categoria,
                    "SubCategoria_Id": _id_subcategoria,
                    "SubCategoria": _nombre_subcategoria,
                    "Imagen": _imagen_producto,
                    "Inventario": _inventory_35a
                }
            }]

            print('Descripcion_Larga: ', str(caracteristicas))
        else:
            # continue
            lista_datos_productos += [{
                "Producto": {
                    "Num_Producto": contador_productos,
                    "SKU": _sku_producto,
                    "Nombre": _nombre_producto,
                    "Id_Marca": _id_marca,
                    "Marca": _marca,
                    "Descripcion_Corta": _descripcion_corta_prodcuto,
                    "Descripcion_Larga": '',
                    "Categoria_Id": _id_categoria,
                    "Categoria": _nombre_categoria,
                    "SubCategoria_Id": _id_subcategoria,
                    "SubCategoria": _nombre_subcategoria,
                    "Imagen": _imagen_producto,
                    "Inventario": _inventory_35a
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

    # _str_converted = re.sub(r"[^\w\W\d\D]*[]\W]*", "", self)

    _str_converted = self

    return _str_converted


def main():
    pass
    # json_layout_prod = xml_products_layout_converter()

    # print('Layout JSON Productos CT: ', json_layout_prod)

    ws_clients = []

    dict_json_xml = []

    layout_products = parser_products_integration()

    print('Lista_Productos parseados: ', str(layout_products))


if __name__ == "__main__":
    pass

    start_time = datetime.now()

    main()

    end_time = datetime.now()

    print('Duration: {}'.format(end_time - start_time) + ' seconds')



