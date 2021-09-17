"""
API RESPONSE PARSER
"""

from rest_framework import status
from rest_framework.response import Response


class APIResponseParser:
    """
    ApiResponseParser
    Common api Response Parser for all API Response.
    """

    def __init__(self):
        pass

    @staticmethod
    def response(**_api_response_data):
        """
        kwargs: all Kwargs Parameter comes from to APIView Class.
        return: Response
        """
        try:
            if _api_response_data['status']:
                return Response(
                    {_api_response_data.get('api_name', 'data'): _api_response_data.get('data', {}),
                     'status': _api_response_data.get('status', True),
                     'errors':  _api_response_data.get('errors', []),
                     'message': _api_response_data.get('message', 'DONE')})
            return Response(
                {'message': _api_response_data.get('message', 'DONE-ERROR'),
                 'errors': _api_response_data.get('errors', []),
                 _api_response_data.get('api_name', 'data'): _api_response_data.get('data', {}),
                 'status': False})
        except Exception as msg:
            return Response(
                {'message': "APIResponseParser.response.errors",
                 'errors': str(msg), 'status': False})

    @staticmethod
    def responses(**_api_response_data):
        """
        kwargs: all Kwargs Parameter comes from to APIView Class.
        return: Response
        """
        json_response = {}
        try:
            if _api_response_data['status']:
                for key, values in _api_response_data['data'].items():
                    json_response[key] = values
                json_response['message'] = _api_response_data['message']
                json_response['status'] = _api_response_data['status']
                return Response(json_response)
            return Response(
                {
                    'message': _api_response_data['message'],
                    'status': False
                }
            )
        except Exception as msg:
            return Response(
                {
                    'message': "APIResponseParser.response.errors",
                    'errors': str(msg),
                    'status': False
                }
            )

    @staticmethod
    def response_with_status(**_api_response_data):
        """
        response_with_status
        This response_with_status() methods used to get and create the response with status
        code api structure data
        kwargs: all Kwargs Parameter comes from to APIView Class.
        return: Response
        """
        response = {}
        try:
            if _api_response_data.get('status', True):
                # response data manupulation
                for key, values in _api_response_data['data'].items():
                    response[key] = values
                # api status response structure
                response['message'] = _api_response_data.get('message', 'DONE')
                response['status'] = _api_response_data.get('status', True)
                response['errors'] = _api_response_data.get('errors', [])
                return Response(response, status=_api_response_data.get('status_code'))
            return Response(
                {
                    'message': _api_response_data.get('message', 'ERRORs'),
                    'status': False,
                    'errors': _api_response_data.get('errors', []),
                    'data': _api_response_data.get('data', {})
                }, status=_api_response_data.get('status_code', status.HTTP_302_FOUND)
            )
        except Exception as msg:
            return Response({'message': "APIResponseParser.response.errors",
                             'errors': [str(msg)],
                             'status': False},
                            status=_api_response_data.get('status_code', status.HTTP_302_FOUND))
