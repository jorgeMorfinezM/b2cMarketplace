# -*- coding: utf-8 -*-
"""
Requires Python 3.0 or later
"""

__author__ = "Jorge Morfinez Mojica (jorgemorfinez@ofix.mx)"
__copyright__ = "Copyright 2019, Jorge Morfinez Mojica"
__license__ = "Ofix S.A. de C.V."
__history__ = """ """
__version__ = "1.19.H10.Prod ($Rev: 1 $)"


# import logging
import requests
from app import *
from authentication.ws_auth import *
from constants.constants import Constants as Const
from logger_controller.logger_control import *
import json
import xml.etree.ElementTree as Et
import binascii
import os


logger = configure_ws_logger()


# Contiene conexion a WS de Documentos SIIO para envio a Avanttia:
def consume_clients_ws(self, lista_dias, rango):
    pass

    cfg = get_config_constant_file()

    customer_number = self

    logger.info('Customer_Number Param: ' + customer_number)
    logger.info('LISTA DIAS [inicio, fin]: %s: ', lista_dias)

    api_url = cfg['WS_DATA']['URL_WS_CLIENT_DATA']

    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }

    '''
    get_params = lambda cust_number, d_ini, d_fin: dict(CUSTOMER_NUMBER=cust_number) if (d_ini == 0 and d_fin == 0) \
                                                                                        and int(customer_number) != 0 \
        else (dict(CUSTOMER_NUMBER=cust_number, DINI=d_ini, DFIN=d_fin) if int(customer_number) != 0
              else dict(DINI=d_ini, DFIN=d_fin))
    '''

    params = get_params_customers_search(customer_number, lista_dias, rango)

    logger.info('Params to WS Get Client: %s', str(params))

    try:

        if len(params) == 0:
            response = requests.get(api_url, headers=headers, timeout=600)
        else:
            response = requests.get(api_url, headers=headers, params=params, timeout=600)

        response.raise_for_status()

    except requests.exceptions.RequestException as err:
        response = err
        logger.exception('RequestException in AV_CUSTOMERS WS resource: %s', err, exc_info=True)
        raise response
        pass
    except requests.exceptions.HTTPError as errh:
        response = errh
        logger.exception('HTTPError in AV_CUSTOMERS WS resource: %s', errh, exc_info=True)
        raise response
        pass
    except requests.exceptions.ConnectionError as errc:
        response = errc
        logger.exception('ConnectionError in AV_CUSTOMERS WS resource: %s', errc, exc_info=True)
        raise response
        pass
    except requests.exceptions.ConnectTimeout as errct:
        # response = errct
        logger.exception('ConnectionTimeOur in AV_CUSTOMERS WS resource: %s', errct, exc_info=True)
        raise response
        pass
    except requests.exceptions.Timeout as errt:
        try:
            response = requests.get(api_url, headers=headers, timeout=240)

            response.raise_for_status()
        except requests.exceptions.Timeout:
            logger.exception('TimeOut in AV_CUSTOMERS WS resource: %s', errt, exc_info=True)
            pass

    return response


# Contiene conexion a WS de Documentos SIIO para envio a Avanttia:
def consume_documents_ws(self, self1, lista_dias, m_rango):
    pass

    cfg = get_config_constant_file()

    folio = self
    customer_number = self1

    logger.info('Folio Param: %s', folio)
    logger.info('Customer_Number Param: ' + customer_number)
    logger.info('LISTA DIAS [inicio, fin]: %s: ', lista_dias)

    api_url = cfg['WS_DATA']['URL_WS_DOCTO_DATA']

    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }

    params = get_params_doctos_search(folio, customer_number, lista_dias, m_rango)

    logger.info('Params to WS Get Doctos: %s', str(params))

    try:

        if len(params) == 0:
            response = requests.get(api_url, headers=headers, timeout=300)
        else:
            response = requests.get(api_url, headers=headers, params=params, timeout=300)

        response.raise_for_status()

    except requests.exceptions.RequestException as err:
        response = err
        logger.exception('RequestException in AV_DOCUMENTS WS resource: %s', err, exc_info=True)
        raise response
        pass
    except requests.exceptions.HTTPError as errh:
        response = errh
        logger.exception('HTTPError in AV_DOCUMENTS WS resource: %s', errh, exc_info=True)
        raise response
        pass
    except requests.exceptions.ConnectionError as errc:
        response = errc
        logger.exception('ConnectionError in AV_DOCUMENTS WS resource: %s', errc, exc_info=True)
        raise response
        pass
    except requests.exceptions.ConnectTimeout as errct:
        # response = errct
        logger.exception('ConnectionTimeOur in AV_DOCUMENTS WS resource: %s', errct, exc_info=True)
        raise response
        pass
    except requests.exceptions.Timeout as errt:
        try:
            response = requests.get(api_url, headers=headers, timeout=350)

            response.raise_for_status()
        except requests.exceptions.Timeout:
            logger.exception('TimeOut in AV_DOCUMENTS WS resource: %s', errt, exc_info=True)
            pass

    return response


def consume_abonos_docto_ws(folio_docto):
    pass

    cfg = get_config_constant_file()

    api_url = cfg['WS_DATA']['URL_WS_DOCTO_ABONO_DATA']

    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }

    params = dict(
        DOC=folio_docto
    )

    try:
        response = requests.get(api_url, headers=headers, params=params, timeout=120)

        response.raise_for_status()

    except requests.exceptions.RequestException as err:
        response = err
        logger.exception("RequestException in WS_ABONOS resource: ", err, exc_info=True)
        raise response
        pass
    except requests.exceptions.HTTPError as errh:
        response = errh
        logger.exception("HTTPError in WS_ABONOS resource: %s", errh, exc_info=True)
        raise response
        pass
    except requests.exceptions.ConnectionError as errc:
        response = errc
        logger.exception("ConnectionError in WS_ABONOS resource: ", errc, exc_info=True)
        raise response
        pass
    except requests.exceptions.ConnectTimeout as errct:
        response = errct
        logger.exception("ConnectionTimeOur in WS_ABONOS resource: ", errct, exc_info=True)
        raise response
        pass
    except requests.exceptions.Timeout as errt:
        try:
            response = requests.get(api_url, headers=headers, params=params, timeout=240)

            response.raise_for_status()
        except requests.exceptions.Timeout:
            # logging.exception('TimeOut in CFDI_XML WS resource: %s', errt, exc_info=True)
            logger.exception("TimeOut in WS_ABONOS resource: ", errt, exc_info=True)
            raise
            pass

    return response


# SIIO : Consume el WS para obtener XML de un folio: FACTURA, PAGO o NC
def consume_ws_cfdi_xml(self, self1):
    pass

    cfg = get_config_constant_file()

    api_url = cfg['WS_DATA']['URL_WS_CFDI_XML']

    _folio = self
    _tipo_docto_num = self1

    tipo_docto = lambda tipo_doc: "FACTURA" if int(tipo_doc) == 4 else ("PAGO" if int(tipo_doc) == 9 else "NC")

    _doc_tipo = tipo_docto(_tipo_docto_num)

    logger.info('Tipo_documento Param: %s', _doc_tipo)

    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }

    params = dict(
        DOC=_folio,
        TIPO_DOC=_doc_tipo
    )

    try:
        response = requests.get(api_url, headers=headers, params=params, timeout=120)

        response.raise_for_status()

    except requests.exceptions.RequestException as err:
        response = err
        # logging.exception('RequestException in CFDI_XML WS resource: %s', err, exc_info=True)
        logger.exception("RequestException in CFDI_XML WS resource: ", err, exc_info=True)
        raise response
        pass
    except requests.exceptions.HTTPError as errh:
        response = errh
        # logging.exception('HTTPError in CFDI_XML WS resource: %s', errh, exc_info=True)
        logger.exception("HTTPError in CFDI_XML WS resource: %s", errh, exc_info=True)
        raise response
        pass
    except requests.exceptions.ConnectionError as errc:
        response = errc
        # logging.exception('ConnectionError in CFDI_XML WS resource: %s', errc, exc_info=True)
        logger.exception("ConnectionError in CFDI_XML WS resource: ", errc, exc_info=True)
        raise response
        pass
    except requests.exceptions.ConnectTimeout as errct:
        # response = errct
        # logging.exception('ConnectionTimeOur in CFDI_XML WS resource: %s', errct, exc_info=True)
        logger.exception("ConnectionTimeOur in CFDI_XML WS resource: ", errct, exc_info=True)
        raise response
        pass
    except requests.exceptions.Timeout as errt:
        try:
            response = requests.get(api_url, headers=headers, timeout=120)

            response.raise_for_status()
        except requests.exceptions.Timeout:
            # logging.exception('TimeOut in CFDI_XML WS resource: %s', errt, exc_info=True)
            logger.exception("TimeOut in CFDI_XML WS resource: ", errt, exc_info=True)
            raise
            pass

    return response


# Consume el WS de Avanttia para enviar Clientes
def consume_ws_cliente_avanttia(self):
    pass

    cfg = get_config_constant_file()

    # access_token_data = parse_xml_token_response()
    # Para version token por PULL de datos:
    # access_token_data = access_token_list

    access_token_data = parse_xml_token_response()

    oauth_token = access_token_data[2]
    token_type = access_token_data[0]
    refresh_token = access_token_data[3]

    api_url_master = cfg['AVANTTIA_WS_URL_MASTER']['URL_WS_AVANTTIA']
    api_url_operative = cfg['AVANTTIA_WS_OPERATIVES']['OPERATIVE_POST_CUSTOMERS']

    api_url = api_url_master + api_url_operative

    payload = self
    payload = payload.replace("\n", "")
    payload = payload.replace("b'", "")
    payload = payload.replace("'", "")

    # print("PARAMS API WS: ", payload)

    headers = {
        'Content-Type': 'application/xml charset=utf-8',
        'Content-Length': str(len(payload)),
        'Authorization': token_type + ' ' + oauth_token
    }

    try:

        response = requests.post(api_url, data=payload, headers=headers, timeout=60)
        # response = requests.request("POST", api_url, data=params, headers=headers)

        # response.raise_for_status()
    except requests.exceptions.RequestException as err:
        try:
            response = requests.post(api_url, data=payload, headers={
                'Content-Type': 'application/xml charset=utf-8',
                'Content-Length': str(len(payload)),
                'Authorization': token_type + ' ' + oauth_token
            }, timeout=60)
            # response = requests.post(api_url, data=params, headers=headers)

            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            logger.exception('RequestException in API_CUSTOMERS WS resource: %s', err, exc_info=True)
            response = '<?xml version="1.0" encoding="UTF-8"?>' \
                       '<DocumentsResponse>' \
                       '<Success>0</Success>' \
                       '</DocumentsResponse>'
            return
        return
    except requests.exceptions.HTTPError as errh:
        logger.exception('HTTPError in API_CUSTOMERS WS resource: %s', errh, exc_info=True)
        response = '<?xml version="1.0" encoding="UTF-8"?>' \
                   '<DocumentsResponse>' \
                   '<Success>0</Success>' \
                   '</DocumentsResponse>'
        return
    except requests.exceptions.ConnectionError as errc:
        logger.exception('ConnectionError in API_CUSTOMERS WS resource: %s', errc, exc_info=True)
        response = '<?xml version="1.0" encoding="UTF-8"?>' \
                   '<DocumentsResponse>' \
                   '<Success>0</Success>' \
                   '</DocumentsResponse>'
        return
    except requests.exceptions.Timeout as errt:
        try:
            response = requests.post(api_url, data=payload, headers=headers, timeout=90)

            response.raise_for_status()
        except requests.exceptions.Timeout:
            logger.exception("TimeOut in API_CUSTOMERS WS resource: ", errt, exc_info=True)
            response = '<?xml version="1.0" encoding="UTF-8"?>' \
                       '<DocumentsResponse>' \
                       '<Success>0</Success>' \
                       '</DocumentsResponse>'
            return
        return

    return response


# Avanttia : Consume el WS para enviar Documentos y Abonos
def consume_ws_docto_abono_avanttia(self):
    pass

    cfg = get_config_constant_file()

    # access_token_data = parse_xml_token_response()
    # Para version token por PULL de datos:
    # access_token_data = access_token_list

    access_token_data = parse_xml_token_response()

    oauth_token = access_token_data[2]
    token_type = access_token_data[0]
    refresh_token = access_token_data[3]

    # api_url = const.URL_WS_AVANTTIA + const.OPERATIVE_POST_DOCUMENTS
    api_url_master = cfg['AVANTTIA_WS_URL_MASTER']['URL_WS_AVANTTIA']
    api_url_operative = cfg['AVANTTIA_WS_OPERATIVES']['OPERATIVE_POST_DOCUMENTS']

    api_url = api_url_master + api_url_operative

    payload = self
    payload = payload.replace("\n", "")
    payload = payload.replace("b'", "")
    payload = payload.replace("'", "")

    # print("PARAMS API WS: ", payload)

    headers = {
        'Content-Type': 'application/xml charset=utf-8',
        'Content-Length': str(len(payload)),
        'Authorization': token_type + ' ' + oauth_token
    }

    try:

        response = requests.post(api_url, data=payload, headers=headers, timeout=60)
        # response = requests.request("POST", api_url, data=params, headers=headers)

        # response.raise_for_status()
    except requests.exceptions.RequestException as err:
        try:
            response = requests.post(api_url, data=payload, headers={
                'Content-Type': 'application/xml charset=utf-8',
                'Content-Length': str(len(payload)),
                'Authorization': token_type + ' ' + oauth_token
            }, timeout=60)
            # response = requests.post(api_url, data=params, headers=headers)

            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            logger.exception('RequestException in API_DOCUMENTOS ABONOS WS resource: %s', err, exc_info=True)
            response = '<?xml version="1.0" encoding="UTF-8"?>' \
                       '<DocumentsResponse>' \
                       '<Success>0</Success>' \
                       '</DocumentsResponse>'
            return
        return
    except requests.exceptions.HTTPError as errh:
        logger.exception('HTTPError in API_DOCUMENTS WS resource: %s', errh, exc_info=True)
        response = '<?xml version="1.0" encoding="UTF-8"?>' \
                   '<DocumentsResponse>' \
                   '<Success>0</Success>' \
                   '</DocumentsResponse>'
        return
    except requests.exceptions.ConnectionError as errc:
        logger.exception('ConnectionError in API_DOCUMENTS WS resource: %s', errc, exc_info=True)
        response = '<?xml version="1.0" encoding="UTF-8"?>' \
                   '<DocumentsResponse>' \
                   '<Success>0</Success>' \
                   '</DocumentsResponse>'
        return
    except requests.exceptions.Timeout as errt:
        try:
            response = requests.request("POST", api_url, data=payload, headers=headers, timeout=60)

            response.raise_for_status()
        except requests.exceptions.Timeout:
            logger.exception('TimeOut in API_DOCUMENTS WS resource: %s', errt, exc_info=True)
            response = '<?xml version="1.0" encoding="UTF-8"?>' \
                       '<DocumentsResponse>' \
                       '<Success>0</Success>' \
                       '</DocumentsResponse>'
            return
        return

    return response


# Avanttia : Consume el WS para enviar CFD de XML ENCODEADO
def consume_ws_cfd_avanttia(self):
    pass

    cfg = get_config_constant_file()

    access_token_data = parse_xml_token_response()

    oauth_token = access_token_data[2]
    token_type = access_token_data[0]
    refresh_token = access_token_data[3]

    api_url_master = cfg['AVANTTIA_WS_URL_MASTER']['URL_WS_AVANTTIA']
    api_url_operative = cfg['AVANTTIA_WS_OPERATIVES']['OPERATIVE_POST_DOCTO_CFDI']

    api_url = api_url_master + api_url_operative

    payload = self

    # print("PARAMS API WS: ", payload)

    headers = {
        'Content-Type': 'application/xml charset=utf-8',
        'Content-Length': str(len(payload)),
        'Authorization': token_type + ' ' + oauth_token
    }

    try:

        response = requests.request("POST", api_url, data=payload, headers=headers, timeout=60)
        # response = requests.post(api_url, data=params, headers=headers)

        # response.raise_for_status()
    except requests.exceptions.RequestException as err:
        try:
            response = requests.request("POST", api_url, data=payload, headers={
                'Content-Type': 'application/xml charset=utf-8',
                'Content-Length': str(len(payload)),
                'Authorization': token_type + ' ' + oauth_token
            }, timeout=60)
            # response = requests.post(api_url, data=params, headers=headers)

            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            # print("Connection Exception to Re Request to Avanttia CFD Encoded of Documents WS API: ", response)
            # response = err
            logger.exception('RequestException in API_DOCUMENTS CFD WS resource: %s', err, exc_info=True)
            return
        return
    except requests.exceptions.HTTPError as errh:
        # response = errh
        # logging.exception('HTTPError in AV_CUSTOMERS WS resource: %s', errh, exc_info=True)
        logger.exception('HTTPError in API_DOCUMENTS WS resource: %s', errh, exc_info=True)
        return
    except requests.exceptions.ConnectionError as errc:
        # response = errc
        # logging.exception('ConnectionError in AV_CUSTOMERS WS resource: %s', errc, exc_info=True)
        logger.exception('ConnectionError in API_DOCUMENTS WS resource: %s', errc, exc_info=True)
        return
    except requests.exceptions.ConnectTimeout as errct:
        # response = errct
        # logging.exception('ConnectionTimeOur in AV_CUSTOMERS WS resource: %s', errct, exc_info=True)
        logger.exception('ConnectionTimeOut in API_DOCUMENTS WS resource: %s', errct, exc_info=True)
        return
    except requests.exceptions.Timeout as errt:
        try:
            response = requests.request("POST", api_url, data=payload, headers=headers, timeout=60)

            response.raise_for_status()
        except requests.exceptions.Timeout:
            logger.exception('TimeOut in API_DOCUMENTS WS resource: %s', errt, exc_info=True)
            return

    return response


def parse_xml_avanttia_response(self):
    pass

    if self.status_code == 200:

        root_documents_response = Et.fromstring(self.text)

        for success in root_documents_response.findall("Success"):
            json_xml_resp = success.text

    else:
        json_xml_resp = 0

    return json_xml_resp


def get_params_doctos_search(folio, customer_number, lista_dias, m_rango):

    dia_ini = 0
    dia_fin = 0
    rango_minutos = ""

    params = {}

    if lista_dias and lista_dias is not None and len(lista_dias) is not 0:
        dia_ini = lista_dias[0]
        dia_fin = lista_dias[1]

    if m_rango and m_rango is not None and len(m_rango) != 0:
        rango_minutos = m_rango

    logger.info('Folio Trx: %s', folio)
    logger.info('Customer_Number: %s', customer_number)
    logger.info('Dias_Lista: [%s]: ', "{0}, {1}".format(str(dia_ini), str(dia_fin)))
    logger.info('Rango en Minutos para busqueda: %s', str(rango_minutos))

    if dia_ini == 0 and dia_fin == 0:
        if int(folio) != 0 and len(folio) >= 9:
            params = dict(
                DOC=folio
            )
        elif int(customer_number) != 0 and len(customer_number) >= 4:
            params = dict(
                CUSTOMER_NUMBER=customer_number
            )
    elif dia_ini != 0 and dia_fin != 0:
        if int(customer_number) != 0 and len(customer_number) >= 4:
            params = dict(
                CUSTOMER_NUMBER=customer_number,
                DINI=dia_ini,
                DFIN=dia_fin
            )
        elif int(customer_number) == 0:
            params = dict(
                DINI=dia_ini,
                DFIN=dia_fin
            )
    elif dia_ini != 0 and dia_fin == 0:
        if int(customer_number) != 0 and len(customer_number) >= 4 and len(rango_minutos) == 0:
            params = dict(
                CUSTOMER_NUMBER=customer_number,
                DINI=dia_ini,
                DFIN=dia_fin
            )
        elif int(customer_number) == 0 and len(rango_minutos) == 0:
            params = dict(
                DINI=dia_ini,
                DFIN=dia_fin
            )
        elif int(customer_number) != 0 and len(rango_minutos) != 0:
            params = dict(
                CUSTOMER_NUMBER=customer_number,
                DINI=dia_ini,
                RANGO=rango_minutos
            )

    return params


def get_params_customers_search(customer_number, lista_dias, m_rango):

    dia_ini = 0
    dia_fin = 0
    rango_minutos = ""

    params = {}

    if lista_dias and lista_dias is not None and len(lista_dias) != 0:
        dia_ini = lista_dias[0]
        dia_fin = lista_dias[1]

    if m_rango and m_rango is not None and len(m_rango) != 0:
        rango_minutos = m_rango

    logger.info('Customer_Number: %s', customer_number)
    logger.info('Dias_Lista: [%s]: ', "{0}, {1}".format(str(dia_ini), str(dia_fin)))
    logger.info('Rango en Minutos para busqueda: %s', str(rango_minutos))

    if dia_ini == 0 and dia_fin == 0:
        if int(customer_number) != 0 and len(customer_number) >= 4:
            params = dict(
                CUSTOMER_NUMBER=customer_number
            )
    elif dia_ini != 0 and dia_fin != 0:
        if int(customer_number) != 0 and len(customer_number) >= 4:
            params = dict(
                CUSTOMER_NUMBER=customer_number,
                DINI=dia_ini,
                DFIN=dia_fin
            )
        elif int(customer_number) == 0:
            params = dict(
                DINI=dia_ini,
                DFIN=dia_fin
            )
    elif dia_ini != 0 and dia_fin == 0:
        if int(customer_number) != 0 and len(customer_number) >= 4:
            params = dict(
                CUSTOMER_NUMBER=customer_number,
                DINI=dia_ini,
                DFIN=dia_fin
            )
        elif int(customer_number) == 0 and len(rango_minutos) == 0:
            params = dict(
                DINI=dia_ini,
                DFIN=dia_fin
            )
        elif int(customer_number) == 0 and len(rango_minutos) != 0:
            params = dict(
                DINI=dia_ini,
                RANGO=rango_minutos
            )

    return params


# --- MAYBE USE IT  --- Contiene conexion a WS de Boveda CFD_EMITIDOS:
def consume_ws_cfdi(self, self1):
    pass

    cfg = get_config_constant_file()

    api_url = cfg['WS_BOVEDA']['URL_WS_BOVEDA']

    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }

    if str(self).startswith("100") and len(self) is 11:
        _cia_cfd = 'ofixg.eo'
    else:
        _cia_cfd = 'ofixg.of'

    params = dict(
        _output='application/json',
        cia_cfd=_cia_cfd,
        version='3.3',
        rfc=self1,
        folio=self
    )

    try:
        response = requests.get(api_url, headers=headers, params=params)

        response.raise_for_status()

        data_response = json.loads(response.text)

    except requests.exceptions.RequestException as err:
        response = err
        logger.exception('RequestException in cfd_emitido WS resource: %s', err, exc_info=True)
    except requests.exceptions.HTTPError as errh:
        response = errh
        logger.exception('HTTPError in cfd_emitido WS resource: %s', errh, exc_info=True)
    except requests.exceptions.ConnectionError as errc:
        response = errc
        logger.exception('ConnectionError in cfd_emitido WS resource: %s', errc, exc_info=True)
    except requests.exceptions.ConnectTimeout as errct:
        response = errct
        logger.exception('ConnectionTimeOur in cfd_emitido WS resource: %s', errct, exc_info=True)
    except requests.exceptions.Timeout as errt:
        try:
            response = requests.get(api_url, headers=headers, params=params, timeout=10)

            response.raise_for_status()
        except requests.exceptions.Timeout:
            logger.exception('TimeOut in cfd_emitido WS resource: %s', errt, exc_info=True)
            pass

    return response


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


# ---- DO NOT USE IT ----
def encode_multipart_form_data(fields):
    pass

    boundary = binascii.hexlify(os.urandom(16)).decode('ascii')

    body = (
            "".join("--%s\r\n"
                    "Content-Disposition: form-data; name=\"%s\"\r\n"
                    "\r\n"
                    "%s\r\n" % (boundary, key, val)
                    for key, val in fields.items()) +
            "--%s--\r\n" % boundary
    )

    content_type = "multipart/form-data; boundary=%s" % boundary

    return body, content_type
