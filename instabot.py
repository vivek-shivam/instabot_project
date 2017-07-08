import requests,urllib,re,pylab
import matplotlib.pyplot as plt
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from wordcloud import WordCloud,STOPWORDS
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
    request_url = (BASE_URL + "users/search?q=%s&access_token=%s" % (insta_username, APP_ACCESS_TOKEN))
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



def get_own_post():
    request_url = (BASE_URL + "users/self/media/recent/?access_token=%s") % (APP_ACCESS_TOKEN)
    print "GET request url : %s" % (request_url)
    own_media = requests.get(request_url).json()

    if own_media["meta"]["code"] == 200:
        if len(own_media["data"]):
            image_name = own_media["data"][0]["id"] + ".jpeg"
            print "image id : %s"%(own_media["data"][0]["id"])
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print "Your image has been downloaded!"
        else:
            print "Post does not exist!"
    else:
        print "Status code other than 200 received!"


def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            print "POST ID : %s" + (user_media['data'][0]['id'])
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):

            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()

def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'



def get_own_post_id():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            return own_media['data'][0]['id']
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    print "The comment you can post should have :\n 1.not more than 300 characters \n 2.not more than 4 hashtags \n 3.not more than 1 url \n 4.not all capital letters \n "
    comment_text = raw_input("Your comment: ")
    if len(comment_text) <= 300 and comment_text.isupper()==False and comment_text.count("#")<=4:
        c = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',comment_text)

        if len(c) <= 1:
            payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
            request_url = (BASE_URL + 'media/%s/comments') % (media_id)
            print 'POST request url : %s' % (request_url)
            make_comment = requests.post(request_url, payload).json()
            if make_comment['meta']['code'] == 200:
                print "Successfully added a new comment!"
            else:
                print "Unable to add comment. Try again!"

        else:
            print "Comment cannot be posted as it is not appropriate"

    else:
        print "Comment cannot be posted as it is not appropriate"

#function to get comments info on friends recent post
def comment_info(insta_username):
    get_user_id(insta_username)


    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info1 = requests.get(request_url).json()
    if comment_info1['meta']['code'] == 200:
        if len(comment_info1):
            a=0
            for a in range(0, len(comment_info1["data"])):
                print "%s commented : %s"%(comment_info1["data"][a]["from"]["username"],comment_info1["data"][a]["text"])
                a=a+1
        else:
            print "no data"
    else:
        print"code not 200"



#get comments of own recent post
def own_comment_info():
    media_id = get_own_post_id()
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info1 = requests.get(request_url).json()
    if comment_info1['meta']['code'] == 200:
        if len(comment_info1):
            a = 0
            for a in range(0,len(comment_info1["data"])):
                print "%s commented : %s" % (comment_info1["data"][a]["from"]["username"], comment_info1["data"][a]["text"])
                a = a + 1
        else:
            print "no data"
    else:
        print"code not 200"

#to delete bad comments on post
def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            #Here's a naive implementation of how to delete the negative comments :)
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'





def compare_comments():
    media_id = get_own_post_id()
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()
    negative = 0
    positive = 0

    if comment_info['meta']['code'] == 200 and len(comment_info['data']):
    # Plot
        for x in range(0, len(comment_info['data'])):
            comment_id = comment_info['data'][x]['id']
            comment_text = comment_info['data'][x]['text']
            blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
            if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                print "Negative comment : %s by %s\n" % (comment_text,comment_info["data"][x]["from"]["username"])
                negative=negative+1
            else:
                print "Positive comment : %s by %s\n" % (comment_text,comment_info["data"][x]["from"]["username"])
                positive=positive+1


        print"positive comments : %s"%(positive)
        print"negative comments : %s"%(negative)
        labels = "Positive Comments", "Negative Comments"
        numbers = [positive, negative]
        colors = ['gold', 'green']
        explode = (0.1, 0)  # explode 1st slice
        # Plot
        plt.pie(numbers, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140)

        plt.axis('equal')
        plt.show()




#extra objective 1
#functions target a particular tag and comment a appropriate comment of ur wish to the meadia of that tag
def post_a_targetted_comment(media_id):

    comment_text =raw_input("Enter the comment you want to post? \n")

    if len(comment_text) <= 300 and comment_text.isupper()==False and comment_text.count("#")<=4:
        c = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',comment_text)

        if len(c) <= 1:
            payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
            request_url = (BASE_URL + 'media/%s/comments') % (media_id)
            print 'POST request url : %s' % (request_url)
            make_comment = requests.post(request_url, payload).json()
            if make_comment['meta']['code'] == 200:
                print "Successfully added a new comment!"
            else:
                print "Unable to add comment. Try again!"

        else:
            print "Comment cannot be posted as it is not appropriate"

    else:
        print "Comment cannot be posted as it is not appropriate"

def get_media_of_tag(tag):
    request_url=BASE_URL+ 'tags/%s/media/recent?access_token=%s'%(tag,APP_ACCESS_TOKEN)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            for x in range(0,len(user_media['data'])):
                post_a_targetted_comment(user_media['data'][x]['id'])
        else:
            print "There is no recent post!"
    else:
        print "Status code other than 200 received!"


#end of objective 1



def recent_media_liked():
    request_url = BASE_URL + "users/self/media/liked?access_token=%s" % (APP_ACCESS_TOKEN)
    recently_liked_media=requests.get(request_url).json()

    if recently_liked_media["meta"]["code"] == 200:
        if len(recently_liked_media["data"]):
            image_name = recently_liked_media["data"][0]["id"] + ".jpeg"
            image_url = recently_liked_media["data"][0]["images"]["standard_resolution"]["url"]
            urllib.urlretrieve(image_url, image_name)
            print "Your image has been downloaded!"
        else:
            print "User does not exist!"
    else:
        print "Status code other than 200 received!"


def download_recent_posts():
    a=True
    while a==True:
        print "\n"
        print "a.Download own recent posts"
        print "b. Download other user's recent post"
        choice = raw_input("enter the choice:")

        if choice=="a":
            request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
            print 'GET request url : %s' % (request_url)
            own_media = requests.get(request_url).json()

            if own_media['meta']['code'] == 200:
                if len(own_media['data']):
                    x=0
                    for x in range(0,len(own_media["data"])):
                        image_name = own_media['data'][x]['id'] + '.jpeg'
                        image_url = own_media['data'][x]['images']['standard_resolution']['url']
                        urllib.urlretrieve(image_url, image_name)
                    print 'Your images have been downloaded!'
                else:
                    print 'Post does not exist!'
            else:
                print 'Status code other than 200 received!'


        elif choice=="b":
            insta_username=raw_input("Enter the username :")
            user_id = get_user_id(insta_username)
            if user_id == None:
                print 'User does not exist!'
                exit()
            request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
            print 'GET request url : %s' % (request_url)
            user_media = requests.get(request_url).json()

            if user_media['meta']['code'] == 200:
                if len(user_media['data']):
                    x=0
                    for x in range(0,len(user_media["data"])):
                        image_name = user_media['data'][x]['id'] + '.jpeg'
                        image_url = user_media['data'][x]['images']['standard_resolution']['url']
                        urllib.urlretrieve(image_url, image_name)
                    print 'Your images have been downloaded!'
                else:
                    print 'Post does not exist!'
            else:
                print 'Status code other than 200 received!'

        else:
            print "Wrong Choice"
            a=False



def find_subtrends(tag):
    request_url=BASE_URL+ "tags/%s/media/recent?access_token=%s"%(tag,APP_ACCESS_TOKEN)

    hash_items = {}
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            for x in range(0, len(user_media['data'])):
                for y in range(0, len(user_media['data'][x]['tags'])):

                    if user_media['data'][x]['tags'][y] in hash_items:
                        hash_items[user_media['data'][x]['tags'][y]] += 1
                    else:
                        hash_items[user_media['data'][x]['tags'][y]] = 1


        else:
            print "There is no recent post!"
    else:
        print "Status code other than 200 received!"
    hash_items.pop(tag)
    print hash_items
    pylab.figure()

    x = range(len(hash_items))
    pylab.xticks(x, hash_items.keys())
    pylab.plot(x, hash_items.values(), "g")
    pylab.show()


    wordcloud = WordCloud(font_path=r"C:\Windows\Fonts\FREESCPT.TTF",
                      stopwords=STOPWORDS,
                      background_color="white",
                      width=1200,
                      height=1000,
                      ).generate_from_frequencies(hash_items)

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()



def start_bot():
    while True:
        print "\n"
        print "Hey! Welcome to instaBot!"
        print "Choose from following  options:"
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.get your recent pic downloaded \n"
        print "d.get recent pic of a username\n"
        print "e. like recent media of a username \n"
        print "f. comment on recent media of user\n"
        print "g. view comments on own recent post \n"
        print "h. view comments on user's recent post \n"
        print "i. delete bad comments on the picture \n"
        print "j. compare the comments on own recent post an creat a pie chart of the same\n"
        print "k. Target a particular tag and comment a appropriate comment of ur wish to the media of that tag\n"
        print "l. Download the recent media you just liked \n"
        print "m. Download the recent media of anyone \n"
        print "n. to find and plot subtrends of a trend \n"
        print "o.Exit"

        choice=raw_input("Enter you choice: ")
        if choice=="a":
            self_info()
        elif choice=="b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice=="c":
            get_own_post()
        elif choice=="d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice=="e":
            insta_username=raw_input("enter username of the user :")
            like_a_post(insta_username)
        elif choice=="f":
            insta_username=raw_input("enter the username of the user")
            post_a_comment(insta_username)
        elif choice == "g":
            own_comment_info()
        elif choice == "h":
            insta_username = raw_input("Enter the username of the user: ")
            comment_info(insta_username)
        elif choice == "i":
            insta_username = raw_input("Enter the username of the user")
            delete_negative_comment()
        elif choice=="j":
            compare_comments()
        elif choice=="k":
            tag_name=raw_input("enter the tag you want to search? \n")
            get_media_of_tag(tag_name)
        elif choice=="l":
            recent_media_liked()
        elif choice=="m":
            download_recent_posts()
        elif choice=="n":
            trend = raw_input("Enter trend to be searched : ")
            find_subtrends(trend)
        elif choice=="o":
            exit()

        else:
            print "wrong choice"



start_bot()

