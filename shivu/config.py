class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "6848223695"
    sudo_users = "6968763387"
    GROUP_ID = -1002023182491
    TOKEN = "6850137736:AAGBOBgnxK6SV2LhDNE0HvweCmgOS1Bc9o4"
    mongo_url = "mongodb+srv://HaremDBBot:ThisIsPasswordForHaremDB@haremdb.swzjngj.mongodb.net/?retryWrites=true&w=majority"
    PHOTO_URL = ["https://telegra.ph/file/b925c3985f0f325e62e17.jpg", "https://telegra.ph/file/4211fb191383d895dab9d.jpg"]
    SUPPORT_CHAT = "Waifu_catcher_support_pills"
    UPDATE_CHAT = "Waifu_catcher_support_pills"
    BOT_USERNAME = "Waifu_catcher_pills_bot"
    CHARA_CHANNEL_ID = "-1002023182491"
    api_id = 26626068
    api_hash = "bf423698bcbe33cfd58b11c78c42caa2"

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
