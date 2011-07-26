from model.Youtube import Account
import gdata.youtube.service


YOUTUBE_DEVELOPER_KEY = 'AI39si5jtcW1nvinaUO-LaGn22pqmLVS_PuFmq0G5PObCWxMVU8u3Nm4By_dqXQiSEJp6g03Oh9Q54ZspGVDTXJPNPTNTR9D_w'
YOUTUBE_SOURCE = 'shiningjason1989'
YOUTUBE_CLIENT_ID = 'shiningjason1989'

YOUTUBE_DEFAULT_USER_FEED_URI = 'http://gdata.youtube.com/feeds/api/users/default/uploads'

    
def clientLogin():
    account = Account.all().get()

    if account:
        client = gdata.youtube.service.YouTubeService()
        client.email = account.email
        client.password = account.password
        client.source = YOUTUBE_SOURCE
        client.developer_key = YOUTUBE_DEVELOPER_KEY
        client.client_id = YOUTUBE_CLIENT_ID
        client.ProgrammaticLogin()
        
        return client
    
    else:
        return None
