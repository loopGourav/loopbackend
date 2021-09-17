"""Controllars Module used to control the allbd query set for code 
optimize and re-use the code
"""

from helper.messages import MSG


class BackendQueryController:
    """
    BackendQueryController
    This "BackendQueryControllerr" class module used to controll all type 
    query of db handling the re-use code and optimization
    """

    def __init__(self, **kwargs):
        self.controller_data = kwargs
        self.model_class = kwargs.get('model_name', None)
        self.filter_req_data = kwargs.get('filter_req_data', {})
        self.input_req_data = kwargs.get('input_req_data', {})

    def get_query_instance(self):
        """
        This "get_query_instance" function used to get the auth user instance 
        according to filter request data
        params:
            ex: filter_req_data: {'id': 1}
        return: query_instance
        """
        try:
            return self.model_class.objects.get(**self.filter_req_data)
        except Exception as e:
            print(e)
            print('G29')
            return None

    def get_query_set(self):
        """
        This "get_query_set" function used to get the user profile instance 
        according to filter request data
        params:
            ex: filter_req_data: {'id': 1}
        return: query_instance
        """
        try:
            return self.model_class.objects.filter(**self.filter_req_data)
        except Exception as e:
            print('G45')
            return None

    def create_query_set(self):
        """
        This "create_query_set" function used to update the all 
        user profile related data using update query data
        """
        return self.model_class.objects.create(**self.input_req_data)

    def update_query_set(self):
        """
        This "update_user_profile_details" function used to update the all 
        user profile related data using update query data
        """
        return self.model_class.objects.filter(**self.filter_req_data).update(**self.input_req_data)


class BackendSerializerController:
    """
    BackendSerializerController
    This "BackendSerializerController" class module used to controll all type 
    serializer of db handling the re-use code and optimization
    """

    def __init__(self, **kwargs):
        self.controller_data = kwargs
        self.model_instance = kwargs.get('model_instance', None)
        self.serializer_class = kwargs.get('serializer_class_name', None)
        self.type_serializer_data = kwargs.get('type_serializer_data', None)
        self.input_req_data = kwargs.get('input_req_data', {})

    def get_serializer_data(self):
        """
        This "get_serializer_data" function used to get the all serilizer data 
        """
        if self.type_serializer_data == '__SINGLE__':
            serializer_data = self.serializer_class(self.model_instance)
            if serializer_data:
                return serializer_data.data, MSG['DONE']
            return {}, MSG['SERIALIZER_ERROR']
        if self.type_serializer_data == '__MULTIPLE__':
            serializer_data = self.serializer_class(
                self.model_instance, many=True)
            if serializer_data:
                return serializer_data.data, MSG['DONE']
            return {}, MSG['SERIALIZER_ERROR']

    def create_serializer_data(self):
        """8
        This "create_serializer_data" function used to create the serializer data of passing instance 
        """
        serializer = self.serializer_class(data=self.input_req_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return serializer.data, MSG['DONE']
        serializer_error_instance = SerializerErrorParser(serializer.errors)
        key_name, error = serializer_error_instance()
        return {}, str(key_name) + ':' + str(error)

    def update_serializer_data(self):
        """
        This 'update_serializer_data' function used to update the serializer data
        """
        serializer = self.serializer_class(self.model_instance,
                                           data=self.input_req_data,
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data, MSG['DONE']
        serializer_error_instance = SerializerErrorParser(serializer.errors)
        key_name, error = serializer_error_instance()
        return {}, str(key_name) + ':' + str(error)


class SerializerErrorParser:
    """
    SerializerErrorParser : Serializer error Parser Class Used to split the serializer errors in 
    two parts key and Values, key define the error of key and value define what is the
    error in this Key.
    # {'email': ['Enter a valid e-mail address.'], 'created': ['This field is required.']}
    """

    def __init__(self, un_error_message):
        self.error_message = un_error_message

    def __call__(self):
        return self.serializer_error_parser()

    def serializer_error_parser(self):
        """
        manipulate the serializer error for api response
        return: key and error
        """
        try:
            if isinstance(self.error_message, dict):
                error_keys = list(self.error_message.keys())
                if len(error_keys) > 0:
                    return error_keys[0], self.error_message[error_keys[0]][0]
                return None, None

            if isinstance(self.error_message, list):
                error_list = list(
                    filter(lambda x: list(x.keys()), self.error_message))
                if error_list:
                    error_parse = error_list[0]
                    error_keys = list(error_parse.keys())
                    if len(error_keys) > 0:
                        return error_keys[0], error_parse[error_keys[0]][0]
                    return None, None
        except Exception as exception_error:
            print(exception_error)
            return None, None
