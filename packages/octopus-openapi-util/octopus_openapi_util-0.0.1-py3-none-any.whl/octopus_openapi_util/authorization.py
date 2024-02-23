import base64
import hashlib
import hmac
import urllib.parse
from collections import OrderedDict

ALGORITHM = "OC-HMAC-SHA256"
ALGORITHM_V2 = "OC-HMAC-SHA256-2"


def build_authorization_header(app_id, app_secret, http_method, path, query_string, signed_headers,
                               timestamp_in_second):
    return build_header(app_id, app_secret, http_method, path, query_string, None, signed_headers, timestamp_in_second,
                        ALGORITHM)


def build_authorization_header_v2(app_id, app_secret, http_method, path, query_string, request_payload, signed_headers,
                                  timestamp_in_second):
    return build_header(app_id, app_secret, http_method, path, query_string, request_payload, signed_headers,
                        timestamp_in_second, ALGORITHM_V2)


def build_header(app_id, app_secret, http_method, path, query_string, request_payload, signed_headers,
                 timestamp_in_second, algorithm):
    headers_with_lowercase_name = {key.lower(): value for key, value in signed_headers.items()}
    signed_headers_string = ';'.join(sorted(headers_with_lowercase_name.keys()))
    signature = build_signature(
        build_canonical_sign_string(http_method, path, query_string, request_payload, headers_with_lowercase_name,
                                    signed_headers, algorithm, timestamp_in_second), app_secret)

    authorization_header = '{algorithm} Credential={app_id}/, Timestamp={timestamp_in_second}, SignedHeaders={signed_headers}, Signature={signature}'.format(
        algorithm=algorithm,
        app_id=app_id,
        timestamp_in_second=timestamp_in_second,
        signed_headers=signed_headers_string,
        signature=signature
    )

    return authorization_header


def build_signature(canonical_sign_string, app_secret):
    sign = hmac.new(bytes(app_secret, 'utf-8'), bytes(canonical_sign_string, 'utf-8'), hashlib.sha256).digest()
    return base64.b64encode(sign).decode()


def build_canonical_sign_string(http_method, path, query_string, request_payload, headers_with_lowercase_name,
                                signed_headers, algorithm, timestamp_in_second):
    canonical_request = (http_method.upper() + '\n' + path + '\n' + build_canonical_query_string(query_string)
                         + '\n' + get_canonical_headers(headers_with_lowercase_name, signed_headers)
                         + '\n' + get_signed_headers(signed_headers))

    if algorithm == ALGORITHM_V2:
        canonical_request += '\n' + hashlib.sha256(request_payload.encode()).hexdigest()

    final_string = (algorithm + '\n' + str(timestamp_in_second) + '\n' + "" + '\n' + hashlib.sha256(
        canonical_request.encode()).hexdigest())

    return final_string


def build_canonical_query_string(query_string):
    if query_string is None or len(query_string) == 0:
        return ""

    parsed_qs = urllib.parse.parse_qs(query_string.lstrip("?"))
    sorted_qs = OrderedDict(sorted(parsed_qs.items()))
    params_str_list = ["{}={}".format(key, value[0]) for key, value in sorted_qs.items()]

    return '&'.join(params_str_list)


def get_canonical_headers(headers_with_lowercase_name, signed_headers):
    signed_header_list = {header.lower(): headers_with_lowercase_name[header.lower()] for header in signed_headers}
    sorted_headers = OrderedDict(sorted(signed_header_list.items()))
    canonical_headers = '\n'.join(['{}:{}'.format(key, value) for key, value in sorted_headers.items()])

    return canonical_headers + '\n'


def get_signed_headers(signed_headers):
    return ";".join(sorted([header.lower() for header in signed_headers]))
