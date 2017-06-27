import requests
from token_key import APP_ACCESS_TOKEN

BASE_URL = 'https://api.instagram.com/v1/'

def get_user_id(insta_username):
    request_url=(BASE_URL+"users/search?q=%s&access_token=%s"%(insta_username,APP_ACCESS_TOKEN))
    print"Get Request Url : %s"%(request_url)

    #to convert to data only
    user_info=requests.get(request_url).json()



    if user_info["meta"]["code"]==200:
        if len(user_info["data"]):
            #to return the first search user as no two users can have same user name
            return user_info["data"][0]["id"]
        else:
            return None
    else:
        print"Status other than 200 received !!!!!"

get_user_id('AVinstaBot.test0')