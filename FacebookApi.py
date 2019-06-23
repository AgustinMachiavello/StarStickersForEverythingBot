import facebook
"""IMPORTANT: Facebook doesn't allow any more automated post so this script doesn't work any more :( """
FACEBOOK_PAGE_ID = "aaa"
ACCESS_TOKEN = "aaa"
  
def PostString(graph_instance, txt):
    """Returns a Boolean

    Post a text
    """
    try:
        graph_instance.put_object(FACEBOOK_PAGE_ID, "feed", message=txt)
    except:
        print("Exception at PostString")
        return False
    return True
    
def GetGraphInstance():
    """Returns a facebook GraphicAPI instance object

    Returns GraphAPI instance
    """
    instance = facebook.GraphAPI(access_token=ACCESS_TOKEN)
    print("Session:", instance.session)
    return instance

def PostImage(graph_instance, img_route, msg):
    """Returns a Boolean

    Post an image
    """
    try:
        image = open(img_route, 'rb')
    except:
        print("Exception at PostImage")
        return False
    graph_instance.put_photo(image, message=msg)
    return True

# EXAMPLE:
# PostImage(GetGraphInstance(), 'image_generated.png', '')
