from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from users.models import User,DeviceInfo
from users.serializers import Userserializer
from rest_framework.pagination import LimitOffsetPagination
from django.http import HttpRequest
import geocoder
from user_agents import parse

def get_ip(request: HttpRequest) -> str:
    """Returns the ip address of the user

    Args:
        request (HttpRequest): HTTP request object

    Returns:
        str: ip address of the user
    """
    ip_adress = request.META.get('HTTP_X_FORWARDED_FOR')
    if not ip_adress :
        ip_adress = request.META.get('REMOTE_ADDR')
    return ip_adress

def get_location(ip_adress : str) -> str :
    """Function to get location from ip address

    Args:
        ip_adress (str): Ip Address passed into the function

    Returns:
        str: returns the location of the user country, city
    """
    location = geocoder.ip(ip_adress)
    country = location.country
    city = location.city
    return f'{country},{city}'

def get_device_info(request : HttpRequest):
    """Function To get device information

    Args:
        request (HttpRequest): Request Object

    Returns:
        _type_: device information
    """
    unparsed_useragent = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(unparsed_useragent)
    device_type = "Mobile" if user_agent.is_mobile else "Tablet" if user_agent.is_tablet else "PC"
    device_name = user_agent.device.family
    device_os = user_agent.os.family
    
    
    return device_type , device_name , device_os



def get_user_from_access_token(access_token : str, refresh_token : str , request, is_refreshing : bool = False):
    """Function that handles getting a User from access_token

    Args:
        access_token (str): access token generated during login

    Returns:
        dict: returns the users details
    """
    access = AccessToken(access_token)
    user  = User.objects.get(id = access.payload.get('user_id'))
    user_ip = get_ip(request)
    device = None
    if not is_refreshing:
        user_location = get_location(user_ip)
        device_type , device_name , device_os = get_device_info(request)
        deviceinfo = DeviceInfo.objects.create(
               user = user,
               ip_address = user_ip,
               device_name = device_name,
               device_type = device_type,
               device_os = device_os,
               access_token = access_token,
               refresh_token = refresh_token
            )
        device = deviceinfo.id
        user.location = user_location
        user.save()
    serializer = Userserializer(user, many=False, context={'request':request , 'device_id': device })
    return serializer.data

def success_response(
        status_code : int ,
        message : str ,
        access_token : str = None,
        refresh_token : str = None,
        data : any = None
        ) :
    """Function that handles success response

    Args:
        status_code (int): status code returned
        message (str): message returned
        access_token (str, optional): access_token returned during login Defaults to None.
        refresh_token (str, optional): refresh token returned during login. Defaults to None.
        data (any, optional): data returned Defaults to None.

    Returns:
        Json Response : returns a json Response
    """
    
    obj = {
       'status': status_code,
       'message':message
    }

    if access_token is not None :
        obj['access'] = access_token
    if refresh_token is not None :
        obj['refresh'] = refresh_token


    if data is not None :
        obj['data'] = data
    
    return Response(obj, status=status_code)


def error_validation(serializer: any, status_code : int):
    """returns back a json response of a list of fields with validated errors

    Args:
        serializer (any): serializer passed in to get errors
        status_code (int): status code shown on each error

    
    """
    errors = []
    for field,error_list in serializer.errors.items():
        for error in error_list :
            errors.append({"field": field , "message": str(error)})
    return Response({"errors": errors},status=status_code)

class CustomPagination(LimitOffsetPagination):
    """Class To overide django default pagination class

    Args:
        PageNumberPagination (class): Inherited class
    """
    def get_paginated_response(self,status:str,message : str, data : dict):
        """_summary_

        Args:
            status (str): status to show the user
            message (str): message to show the user
            data (dict): data to show the user

        """
        limit = self.request.query_params.get('limit', self.default_limit)
        offset = self.request.query_params.get('offset', 0)
        total_pages = (self.count + int(limit) - 1) // int(limit)

        try :
            int_limit = int(limit)
            int_offset = int(offset)
            return Response({
             'status': status,
             'links':{
                 'next_link':self.get_next_link(),
                 'previous_link' : self.get_previous_link()
             },
             'message' : message,
             'limit': int_limit,
             'offset':int_offset,
             'count': self.count,
             'total_pages' : total_pages,
             'data':data
            })
        except :
            return Response({
                'status': 400,
                'message': 'Bad offset and limit request'
            } , status=400) 
        
   

