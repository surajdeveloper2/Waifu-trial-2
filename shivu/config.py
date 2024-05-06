class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "5743248220"
    sudo_users = "1993048420", "1214348787"
    GROUP_ID = -1002001602255
    TOKEN = "7165106534:AAGrNNJMhqMlnt2z1uGOlwDD8yBMyqgaVOw"
    mongo_url = "mongodb+srv://nksharmas9835:waifu@cluster0.ouufhhw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    PHOTO_URL = ["https://graph.org/file/6d2dc744b00d2a40c5c55.jpg", "https://graph.org/file/cf556fb30cd3e40b0f57b.jpg"]
    SUPPORT_CHAT = "waifu_support_group"
    UPDATE_CHAT = "waifu_support_group"
    BOT_USERNAME = "Waifu_Station_Bot"
    CHARA_CHANNEL_ID = "-1002003134505"
    api_id = 22867431
    api_hash = "24ef0e76ceb137563dc33722e4cd79bd"

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
