class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "1962399469"
    sudo_users = "1962399469", "7378476666"
    GROUP_ID = -1002168488906
    TOKEN = "7466616506:AAGriSb83_Rn384dZoqYWCPOtG0lLeGhS_Q"
    mongo_url = "mongodb+srv://Narutoo:hinatahyuga@hater.0luw79s.mongodb.net/"
    PHOTO_URL = ["https://telegra.ph/file/3081e30be69daa65e0f61.jpg", "https://telegra.ph/file/79da4fefc64364f8301c5.jpg"]
    SUPPORT_CHAT = "blade_x_support"
    UPDATE_CHAT = "blade_x_community"
    BOT_USERNAME = "Devine_wifu_bot"
    CHARA_CHANNEL_ID = "-1002168367599"
    api_id = 26626068
    api_hash = "bf423698bcbe33cfd58b11c78c42caa2"

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
