# -*- coding: utf-8 -*-
"""
Requires Python 3.0 or later
"""

__author__ = "Jorge Morfinez Mojica (jorgemorfinez@ofix.mx)"
__copyright__ = "Copyright 2019, Jorge Morfinez Mojica"
__license__ = "Ofix S.A. de C.V."
__history__ = """ """
__version__ = "1.19.L20.Prod ($Rev: 3 $)"

import requests
import urllib3
from logger_controller.logger_control import *
import json
from constants.constants import Constants as Const


logger = configure_ws_logger()


# WS que obtiene el Token de OAuth para conectar a los WS:
def consume_ct_token():
    pass

    cfg = get_config_constant_file()

    _email_auth = cfg['CT_ACCESS_DATA']['EMAIL']
    _cliente_auth = cfg['CT_ACCESS_DATA']['CLIENTE']
    _rfc_auth = cfg['CT_ACCESS_DATA']['RFC']

    api_url_master = cfg['CT_WS_URL_MASTER']['URL_WS_CT']
    api_url_operative = cfg['CT_WS_OPERATIVES']['UTILITIES_WS']['POST_TOKEN']

    api_url = api_url_master + api_url_operative

    params = {'email': _email_auth,
              'cliente': _cliente_auth,
              'rfc': _rfc_auth}

    payload = json.dumps(params)

    # logger.info('Params WS Request: %s', str(payload))

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", api_url, data=payload, headers=headers)

    except requests.exceptions.HTTPError as errh:
        logger.exception('HTTPError in POST to WS Auth CT resource: %s', errh, exc_info=True)
        return
    except requests.exceptions.ConnectTimeout as errct:
        logger.exception('ConnectionTimeOut in POST to WS Auth CT resource: %s', errct, exc_info=True)
        return
    except requests.exceptions.ConnectionError as errc:
        logger.exception('ConnectionError in POST to WS Auth CT resource: %s', errc, exc_info=True)
        return
    except requests.exceptions.Timeout as errt:
        try:
            response = requests.request("POST", api_url, data=params, headers=headers, timeout=60)

            response.raise_for_status()
        except requests.exceptions.Timeout:
            logger.exception('TimeOut in POST to WS Auth CT resource: %s', errt, exc_info=True)
            return
    except requests.exceptions.RequestException as err:
        try:
            response = requests.request("POST", api_url, data=params, headers={
                'Content-Type': 'application/xml charset=utf-8'}, timeout=5)

            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            logger.exception('RequestException in POST to WS Auth CT resource: %s', err, exc_info=True)
            return
        return

    return response


# Parsea el XML de respuesta de consumo de WS que obtiene el Token OAuth:
def parse_json_token_response():
    pass

    access_token = ''

    token_response = consume_ct_token()

    json_data = token_response.json()

    if str(token_response).find("HTTPConnectionPool") != -1 or token_response is None or \
            str(token_response).find("HTTPError") != -1 or 'errorCode' in json_data:

        logger.error('Error de Conexion al WS, intente mas tarde la Busqueda: %s', str(token_response.text))

        error_code = json_data['errorCode']
        error_message = json_data['errorMessage']

        logger.error('An error was occurred while request web service: %s',
                     'ErrorCode: "{}", ErrorMessage: "{}"'.format(error_code, error_message))
    else:

        if token_response.status_code == 200:

            json_token = token_response.json()

            json_token = json.dumps(json_token)
            json_token_load = json.loads(json_token)

            # print("XML Token: " + xml_token)
            # print("JSON Token: " + json_token)

            access_token = '{}'.format(json_token_load["token"])

            logger.info('Token Response Validity: %s', '{}'.format(json_token_load["time"]))

    return access_token


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


