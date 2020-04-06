# -*- coding: utf-8 -*-
"""
Requires Python 3.0 or later
"""

__author__ = "Jorge Morfinez Mojica (jorgemorfinez@ofix.mx)"
__copyright__ = "Copyright 2019, Jorge Morfinez Mojica"
__license__ = "Ofix S.A. de C.V."
__history__ = """ """
__version__ = "1.19.L20.Prod ($Rev: 1 $)"


import requests
from app import *
from authentication.ws_auth import *
from constants.constants import Constants as Const
from logger_controller.logger_control import *
import json


logger = configure_ws_logger()


# CT Online: Consume el WS de CT: UTILERIAS - Volumetria
def consume_ws_volumetria(oauth_token, sku_ct):
    pass

    cfg = get_config_constant_file()

    # oauth_token = parse_json_token_response()

    api_url_master = cfg['CT_WS_URL_MASTER']['URL_WS_CT']
    api_url_operative = cfg['CT_WS_OPERATIVES']['UTILITIES_WS']['GET_DIMENSIONES_PROD']

    payload = sku_ct

    api_url = api_url_master + api_url_operative + payload

    headers = {
        'Content-Type': 'application/json',
        'x-auth': oauth_token
    }

    try:

        response = requests.get(api_url, headers=headers, timeout=15)

        # response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        logger.exception('HTTPError in Utilities Volumetria WS resource: %s', errh, exc_info=True)
        return
    except requests.exceptions.ConnectionError as errc:
        logger.exception('ConnectionError in API_CUSTOMERS WS resource: %s', errc, exc_info=True)
        return
    except requests.exceptions.Timeout as errt:
        try:
            response = requests.get(api_url, headers=headers, timeout=20)

            response.raise_for_status()
        except requests.exceptions.Timeout:
            logger.exception("TimeOut in Utilities Volumetria WS resource: ", errt, exc_info=True)
            return
        return
    except requests.exceptions.RequestException as err:
        try:
            response = requests.get(api_url, data=payload, headers={
                'Content-Type': 'application/json',
                'x-auth': oauth_token
            }, timeout=15)

            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            logger.exception('RequestException in Utilities Volumetria WS resource: %s', err, exc_info=True)
            return
        return

    return response


# CT Online: Consume el WS de CT: UTILERIAS - Tipo de Cambio
def consume_ws_tipo_cambio(oauth_token):
    pass

    cfg = get_config_constant_file()

    # oauth_token = parse_json_token_response()

    api_url_master = cfg['CT_WS_URL_MASTER']['URL_WS_CT']
    api_url_operative = cfg['CT_WS_OPERATIVES']['UTILITIES_WS']['GET_TIPO_CAMBIO']

    api_url = api_url_master + api_url_operative

    headers = {
        'Content-Type': 'application/json',
        'x-auth': oauth_token
    }

    try:

        response = requests.get(api_url, headers=headers, timeout=5)
        # response = requests.request("POST", api_url, data=params, headers=headers)

        # response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        logger.exception('HTTPError in Utilities Tipo_Cambio WS resource: %s', errh, exc_info=True)
        return
    except requests.exceptions.ConnectionError as errc:
        logger.exception('ConnectionError in Utilities Tipo_Cambio WS resource: %s', errc, exc_info=True)
        return
    except requests.exceptions.Timeout as errt:
        try:
            response = requests.get(api_url, headers=headers, timeout=10)

            response.raise_for_status()
        except requests.exceptions.Timeout:
            logger.exception('TimeOut in Utilities Tipo_Cambio WS resource: %s', errt, exc_info=True)
            return
        return
    except requests.exceptions.RequestException as err:
        try:

            response = requests.get(api_url, headers={
                'Content-Type': 'application/xml charset=utf-8',
                'x-auth': oauth_token
            }, timeout=5)

            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            logger.exception('RequestException in Utilities Tipo_Cambio WS resource: %s', err, exc_info=True)
            return
        return

    return response


# CT Online : Consume el WS de CT: EXISTENCIAS - Articulo en Almacenes
def consume_ws_existencias_todos_almacenes(oauth_token, sku_ct):
    pass

    cfg = get_config_constant_file()

    # oauth_token = parse_json_token_response()

    api_url_master = cfg['CT_WS_URL_MASTER']['URL_WS_CT']
    api_url_operative = cfg['CT_WS_OPERATIVES']['EXISTENCIAS_WS']['GET_PROD_X_ALM']

    api_url = api_url_master + api_url_operative

    payload = sku_ct

    headers = {
        'Content-Type': 'application/json',
        'x-auth': oauth_token
    }

    try:

        response = requests.get(api_url, data=payload, headers=headers, timeout=3)
        # response = requests.post(api_url, data=params, headers=headers)

        # response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        logger.exception('HTTPError in Existencias Todos_Almacenes WS resource: %s', errh, exc_info=True)
        return
    except requests.exceptions.ConnectionError as errc:
        logger.exception('ConnectionError in Existencias Todos_Almacenes WS resource: %s', errc, exc_info=True)
        return
    except requests.exceptions.Timeout as errt:
        try:
            response = requests.get(api_url, data=payload, headers=headers, timeout=5)

            response.raise_for_status()
        except requests.exceptions.Timeout:
            logger.exception('TimeOut in Existencias Todos_Almacenes WS resource: %s', errt, exc_info=True)
            return
    except requests.exceptions.RequestException as err:
        try:
            response = requests.get(api_url, data=payload, headers={
                'Content-Type': 'application/json charset=utf-8',
                'x-auth': oauth_token
            }, timeout=5)

            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            logger.exception('RequestException in Existencias Todos_Almacenes WS resource: %s', err, exc_info=True)
            return
        return

    return response


# CT Online : Consume el WS de CT: EXISTENCIAS - Articulo por Almacen
def consume_ws_existencia_por_almacen(oauth_token, sku_ct, almacen_ct):
    pass

    cfg = get_config_constant_file()

    # oauth_token = parse_json_token_response()

    api_url_master = cfg['CT_WS_URL_MASTER']['URL_WS_CT']
    api_url_operative = cfg['CT_WS_OPERATIVES']['EXISTENCIAS_WS']['GET_PROD_EN_ALM']

    api_url = api_url_master + api_url_operative

    payload = sku_ct + '/' + almacen_ct

    headers = {
        'Content-Type': 'application/json',
        'x-auth': oauth_token
    }

    try:

        response = requests.get(api_url, data=payload, headers=headers, timeout=5)
        # response = requests.post(api_url, data=params, headers=headers)

        # response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        logger.exception('HTTPError in Existencia Por_Almacen WS resource: %s', errh, exc_info=True)
        return
    except requests.exceptions.ConnectionError as errc:
        logger.exception('ConnectionError in Existencia Por_Almacen WS resource: %s', errc, exc_info=True)
        return
    except requests.exceptions.Timeout as errt:
        try:
            response = requests.get(api_url, data=payload, headers=headers, timeout=10)

            response.raise_for_status()
        except requests.exceptions.Timeout:
            logger.exception('TimeOut in Existencia Por_Almacen WS resource: %s', errt, exc_info=True)
            return
    except requests.exceptions.RequestException as err:
        try:

            response = requests.get(api_url, data=payload, headers={
                'Content-Type': 'application/json charset=utf-8',
                'x-auth': oauth_token
            }, timeout=5)

            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            logger.exception('RequestException in Existencia Por_Almacen WS resource: %s', err, exc_info=True)
            return
        return

    return response


# CT Online : Consume el WS de CT: EXISTENCIAS - Detalle por Almacen
def consume_ws_existencia_detalle_almacen(oauth_token, sku_ct, almacen_ct):
    pass

    cfg = get_config_constant_file()

    # oauth_token = parse_json_token_response()

    api_url_master = cfg['CT_WS_URL_MASTER']['URL_WS_CT']
    api_url_operative = cfg['CT_WS_OPERATIVES']['EXISTENCIAS_WS']['GET_DETALLE_ALM']

    payload = sku_ct + '/' + almacen_ct

    api_url = api_url_master + api_url_operative + payload

    headers = {
        'Content-Type': 'application/json',
        'x-auth': oauth_token
    }

    try:

        response = requests.get(api_url, headers=headers, timeout=30)

        '''
        json_data = response.json()

        if str(response).find("HTTPConnectionPool") != -1 or response is None or str(response).find("HTTPError") != -1 \
                or 'errorCode' in json_data:

            logger.error('Error de Conexion al WS, intente mas tarde la Busqueda: %s', str(response.text))

            error_code = json_data['errorCode']
            error_message = json_data['errorMessage']

            logger.error('Retry: An error was occurred while request web service: %s',
                         'ErrorCode: "{}", ErrorMessage: "{}"'.format(error_code, error_message))

            if int(error_code) == 4011:

                auth_token_ws = get_token_auth_ws()

                response = requests.get(api_url, headers={
                    'Content-Type': 'application/json',
                    'x-auth': auth_token_ws
                }, timeout=20)
        '''

    # response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        logger.exception('HTTPError in Existencia Detalle Por_Almacen WS resource: %s', errh, exc_info=True)
        response = 'HTTPError'
        return response
    except requests.exceptions.ConnectionError as errc:
        logger.exception('ConnectionError in Existencia Detalle Por_Almacen WS resource: %s', errc, exc_info=True)
        # response.raise_for_status()
        response = 'ConnectionError'
        return response
    except requests.exceptions.Timeout as errt:
        try:
            response = requests.get(api_url, headers=headers, timeout=40)

        except requests.exceptions.Timeout:
            logger.exception('TimeOut in Existencia Detalle Por_Almacen WS resource: %s', errt, exc_info=True)
            response = 'TimeOut'
            return response
    except requests.exceptions.RequestException as err:
        try:
            response = requests.get(api_url, headers={
                'Content-Type': 'application/json',
                'x-auth': oauth_token
            }, timeout=50)

            # response.raise_for_status()
        except requests.exceptions.ConnectionError:
            logger.exception('RequestException in Existencia Detalle Por_Almacen WS resource: %s', err, exc_info=True)
            response = 'RequestException'
            return response
        return response

    return response


# CT Online : Consume el WS de CT: EXISTENCIAS - Sumatoria TOTAL
def consume_ws_existencia_total(oauth_token, sku_ct):
    pass

    cfg = get_config_constant_file()

    # oauth_token = parse_json_token_response()

    api_url_master = cfg['CT_WS_URL_MASTER']['URL_WS_CT']
    api_url_operative = cfg['CT_WS_OPERATIVES']['EXISTENCIAS_WS']['GET_TOTAL_INV_PROD']

    api_url = api_url_master + api_url_operative

    payload = sku_ct + '/TOTAL'

    headers = {
        'Content-Type': 'application/json',
        'x-auth': oauth_token
    }

    try:

        response = requests.get(api_url, data=payload, headers=headers, timeout=3)

        # response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        logger.exception('HTTPError in Existencia Total_Almacenes WS resource: %s', errh, exc_info=True)
        return
    except requests.exceptions.ConnectionError as errc:
        logger.exception('ConnectionError in Existencia Total_Almacenes WS resource: %s', errc, exc_info=True)
        return
    except requests.exceptions.Timeout as errt:
        try:
            response = requests.get(api_url, data=payload, headers=headers, timeout=10)

            response.raise_for_status()
        except requests.exceptions.Timeout:
            logger.exception('TimeOut in Existencia Total_Almacenes WS resource: %s', errt, exc_info=True)
            return
    except requests.exceptions.RequestException as err:
        try:
            response = requests.get(api_url, data=payload, headers={
                'Content-Type': 'application/json charset=utf-8',
                'x-auth': oauth_token
            }, timeout=5)

            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            logger.exception('RequestException in Existencia Total_Almacenes WS resource: %s', err, exc_info=True)
            return
        return

    return response


# CT Online : Consume el WS de CT: EXISTENCIAS - Todas Promociones
def consume_ws_promociones_general(oauth_token):
    pass

    cfg = get_config_constant_file()

    # oauth_token = parse_json_token_response()

    api_url_master = cfg['CT_WS_URL_MASTER']['URL_WS_CT']
    api_url_operative = cfg['CT_WS_OPERATIVES']['EXISTENCIAS_WS']['GET_PROMO_PRICE']

    api_url = api_url_master + api_url_operative

    headers = {
        'Content-Type': 'application/json',
        'x-auth': oauth_token
    }

    try:

        response = requests.get(api_url, headers=headers, timeout=5)

        # response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        logger.exception('HTTPError in Todas Promociones WS resource: %s', errh, exc_info=True)
        return
    except requests.exceptions.ConnectionError as errc:
        logger.exception('ConnectionError in Todas Promociones WS resource: %s', errc, exc_info=True)
        return
    except requests.exceptions.Timeout as errt:
        try:
            response = requests.get(api_url, headers=headers, timeout=10)

            response.raise_for_status()
        except requests.exceptions.Timeout:
            logger.exception('TimeOut in Todas Promociones WS resource: %s', errt, exc_info=True)
            return
    except requests.exceptions.RequestException as err:
        try:

            response = requests.get(api_url, headers={
                'Content-Type': 'application/json charset=utf-8',
                'x-auth': oauth_token
            }, timeout=7)

            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            logger.exception('RequestException in Todas Promociones WS resource: %s', err, exc_info=True)
            return
        return

    return response


# CT Online : Consume el WS de CT: EXISTENCIAS - Promociones por Producto
def consume_ws_promociones_producto(oauth_token, sku_ct):
    pass

    cfg = get_config_constant_file()

    # oauth_token = parse_json_token_response()

    api_url_master = cfg['CT_WS_URL_MASTER']['URL_WS_CT']
    api_url_operative = cfg['CT_WS_OPERATIVES']['EXISTENCIAS_WS']['GET_PROMO_PRICE_X_PROD']

    api_url = api_url_master + api_url_operative

    headers = {
        'Content-Type': 'application/json',
        'x-auth': oauth_token
    }

    payload = sku_ct

    try:

        response = requests.get(api_url, data=payload, headers=headers, timeout=6)

        # response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        logger.exception('HTTPError in Promociones por Producto WS resource: %s', errh, exc_info=True)
        return
    except requests.exceptions.ConnectionError as errc:
        logger.exception('ConnectionError in Promociones por Producto WS resource: %s', errc, exc_info=True)
        return
    except requests.exceptions.Timeout as errt:
        try:
            response = requests.get(api_url, data=payload, headers=headers, timeout=10)

            response.raise_for_status()
        except requests.exceptions.Timeout:
            logger.exception('TimeOut in Promociones por Producto WS resource: %s', errt, exc_info=True)
            return
    except requests.exceptions.RequestException as err:
        try:

            response = requests.get(api_url, data=payload, headers={
                'Content-Type': 'application/json charset=utf-8',
                'x-auth': oauth_token
            }, timeout=8)

            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            logger.exception('RequestException in Promociones por Producto WS resource: %s', err, exc_info=True)
            return
        return

    return response


# Define y obtiene el configurador para las constantes del sistema:
def get_config_constant_file():
    """
        Contiene la obtencion del objeto config
        para setear datos de constantes en archivo
        configurador

    :rtype: object
    """
    # TEST
    _constants_file = "/home/jorge/Documents/Projects/tecnofinLayouts/projects/PaginaB2COFIXNORMAL/integrators/" \
                      "ct_online/getProductsInt/constants/constants.yml"

    # PROD
    # _constants_file = "/ofix/tienda_virtual/parserCt/constants/constants.yml"

    cfg = Const.get_constants_file(_constants_file)

    return cfg

