class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "7297953309"
    sudo_users = "7297953309", "6584789596", "2010819209", "5881272524"
    GROUP_ID = -1002248124267
    TOKEN = "7394897153:AAFZE-1Ns9lHXDbCVeeqvg7qUEt54wMzT1g"
    mongo_url = "mongodb+srv://ananyag558:uEbJ31IYq4lNThZo@cluster0.ptpbkk5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    PHOTO_URL = ["https://telegra.ph/file/2958a27849a6bef853370.jpg"]
    SUPPORT_CHAT = "Seize_your_waifu"
    UPDATE_CHAT = "spirit_updates"
    BOT_USERNAME = "Seize_your_waifu_bot"
    CHARA_CHANNEL_ID = "-1002248124267"
    api_id = 20910948
    api_hash = "1a7e76d89ecf4ee54823308f789e6d3d"

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
