import requests
from token_key import APP_ACCESS_TOKEN

BASE_URL = 'https://api.instagram.com/v1/'



#function to get ur info(username,followers,following etc..
def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()


    #to check if the signal is good
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            #it enters here if any user is found
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'


#function to get the id of user from the username
def get_user_id(insta_username):
    request_url=(BASE_URL+"users/search?=%s&access_token+%s"%(insta_username,APP_ACCESS_TOKEN))
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



#function to get details of a user
def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print "User does not exist!"
        exit()
    request_url = (BASE_URL + "users/%s?access_token=%s") % (user_id, APP_ACCESS_TOKEN)
    print "GET request url : %s" % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print "Username: %s" % (user_info['data']['username'])
            print "No. of followers: %s" % (user_info['data']['counts']['followed_by'])
            print "No. of people you are following: %s" % (user_info['data']['counts']['follows'])
            print "No. of posts: %s" % (user_info['data']['counts']['media'])
        else:
            print "There is no data for this user!"
    else:
        print "Status code other than 200 received!"


def start_bot():
    while True:
        print "\n"
        print "Hey! Welcome to instaBot!"
        print "Choose from following  options:"
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.Exit"

        choice=raw_input("Enter you choice: ")
        if choice=="a":
            self_info()
        elif choice=="b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice=="c":
            exit()
        else:
            print "wrong choice"



start_bot()

