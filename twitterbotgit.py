import tweepy
import json
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream
from tweepy.streaming import StreamListener

# Replace the "None"s by your own credentials
CONSUMER_KEY = '' #keep the quotes, enter your consumer key
CONSUMER_SECRET = ''#keep the quotes, enter your consumer secret key
ACCESS_KEY = ''#keep the quotes, enter your access token
ACCESS_SECRET =  ''#keep the quotes, enter your access token secret

keywords = ["rt to", "rt and win", "retweet and win", "rt for", "rt 4", "retweet to"]
secondaryWords = ["win", "#win", "winner", "competition", "giveaway", "give away", "#competition", "#giveaway"]

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = API(auth, wait_on_rate_limit=True,
          wait_on_rate_limit_notify=True)
SCREEN_NAME = api.me().screen_name

bannedwords = ["vote", "bot", "b0t", "tag" , "#teenchoice", "onlyfans"]
bannedusers = ["ProductReviewMY", "followandrt2win", 'b0t', 'bottybotbotl','bot', 'spot', 'lvbroadcasting', 'jflessauSpam', 'bryster125', 'MobileTekReview', 'ilove70315673', 'traunte', 'ericsonabby', '_aekkaphon'] # does not need to be the entire username! you can just put 'bot' for names like 'b0tspotter', etc.


twitter_client = API(auth)
friends = api.friends_ids(SCREEN_NAME)

def is_user_bot_hunter(username):
    clean_username = username.replace("0", "o")
    clean_username = clean_username.lower()
    for i in bannedusers:
        if i in clean_username:
            return True
        else:
            return False



def search(i):
    if i.id > 1141668107372638208 : 
        if any(k in i.text.lower() for k in keywords) and any(k in i.text.lower() for k in secondaryWords) and not any(k in i.text.lower() for k in bannedwords):
                    
                    if not any(k in i.author.screen_name.lower().replace("0", "o") for k in bannedusers):
                        if not i.retweeted:
                            try:
                                api.retweet(i.id)
                                print("rt " + (i.text))
                            
                                if "follow" in i.text or "#follow" in i.text or "Follow" in i.text or "#Follow" in i.text or "FOLLOW" in i.text or "#FOLLOW" in i.text or "following" in i.text or "#following" in i.text or "FOLLOWING" in i.text or "#FOLLOWING" or "Following" in i.text or "#Following" in i.text:

                                    if len(friends) >= 2000:
                                        api.destroy_friendship(friends[0])
                                        
                                    user_id = i.retweeted_status.user.id
                                    api.create_friendship(user_id)

                            except Exception:
                                pass
                        
                        if ("fav" in i.text.lower() or "like" in i.text.lower()) and not i.favorited:
                            try:
                                api.create_favorite(i.id)
                                print("fav " + (i.text))
                            except Exception:
                                pass
                
 
class MyStreamListener(StreamListener):
    
        
    def on_status(self, data):
        
        search(data) 
        return True
 
    def on_error(self, status):
        print(status)

    # When reach the rate limit
    def on_limit(self, track):
        
        # Print rate limiting error
        print("Rate limited, continuing")
        
        # Continue mining tweets
        return True

    # When timed out
    def on_timeout(self):
        
        # Print timeout message
        print(sys.stderr, 'Timeout...')
        
        # Wait 10 seconds
        time.sleep(10)
        
        # Return nothing
        return
 
 
if __name__ == '__main__':
    listener = MyStreamListener()
    stream = Stream(auth, listener)
    stream.filter(track=keywords)
