# -*- coding: utf-8 -*-
"""
Requires Python 3.0 or later
"""

__author__ = "Jorge Morfinez Mojica (jorgemorfinez@ofix.mx)"
__copyright__ = "Copyright 2019, Jorge Morfinez Mojica"
__license__ = "Ofix S.A. de C.V."
__history__ = """ """
__version__ = "1.19.I24.Prod ($Rev: 3 $)"

import requests
from requests_toolbelt import MultipartEncoder
import xmltodict
import json
from constants.constants import Constants as Const


# WS que obtiene el Token de OAuth para conectar a los WS:
def consume_avanttia_token():
    pass

    cfg = get_config_constant_file()

    _grant_type = cfg['AVANTTIA_ACCESS_DATA']['GRANT_TYPE']
    _client_id = cfg['AVANTTIA_ACCESS_DATA']['CLIENT_ID']
    _client_secret = cfg['AVANTTIA_ACCESS_DATA']['CLIENT_SECRET']
    _rfc = cfg['AVANTTIA_ACCESS_DATA']['RFC']
    _licence = cfg['AVANTTIA_ACCESS_DATA']['LICENCE']

    api_url_master = cfg['AVANTTIA_WS_URL_MASTER']['URL_WS_AVANTTIA']
    api_url_operative = cfg['AVANTTIA_WS_OPERATIVES']['OPERATIVE_GET_TOKEN']

    api_url = api_url_master + api_url_operative

    m = MultipartEncoder(fields={'grant_type': _grant_type,
                                 'client_id': _client_id,
                                 'client_secret': _client_secret,
                                 'rfc': _rfc,
                                 'license': _licence})

    headers = {
        'Content-Type': m.content_type
    }

    response = requests.request("POST", api_url, data=m, headers=headers, timeout=60)

    return response


# Parsea el XML de respuesta de consumo de WS que obtiene el Token OAuth:
def parse_xml_token_response():
    pass

    token_response = consume_avanttia_token()

    if str(token_response).find("Error") is not -1 or str(token_response).find("error") is not -1 \
            or token_response is not None and token_response.status_code == 200:

        xml_token = token_response.text

        json_token = json.dumps(xmltodict.parse(xml_token))
        json_token_load = json.loads(json_token)

        # print("XML Token: " + xml_token)
        # print("JSON Token: " + json_token)

        access_auth_data = []

        token_type = '{}'.format(json_token_load["TokenResponse"]['TokenType'])
        expires_in = '{}'.format(json_token_load["TokenResponse"]['ExpiresIn'])
        access_token = '{}'.format(json_token_load["TokenResponse"]['AccessToken'])
        refresh_token = '{}'.format(json_token_load["TokenResponse"]['RefreshToken'])

        access_auth_data = [token_type, expires_in, access_token, refresh_token]

        return access_auth_data


# Define y obtiene el configurador para las constantes del sistema:
def get_config_constant_file():
    """
        Contiene la obtencion del objeto config
        para setear datos de constantes en archivo
        configurador

    :rtype: object
    """
    _constants_file = "/avanttia/cxc_avanttia_client/constants/constants.yml"
    cfg = Const.get_constants_file(_constants_file)

    return cfg


