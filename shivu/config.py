class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "6087651372"
    sudo_users = "6087651372", "7667987606"
    GROUP_ID = -1002133191051
    TOKEN = "7589023976:AAFerTqtgkPEhmNsAU_5XOFtBaTcd7g-3EE"
    mongo_url = "mongodb+srv://surajgod112:surajgod113@cluster0.v52wo.mongodb.net/"
    PHOTO_URL = ["https://graph.org/file/87c05126a35a66d1d1d37-6f7a824e7306b10bd6.jpg", "https://graph.org/file/40d3df88f6d827ff48af5-9e72ee221223e291ed.jpg"]
    SUPPORT_CHAT = "ntpcraj"
    UPDATE_CHAT = "ntpcdjk"
    BOT_USERNAME = "Waifugrls17bot"
    CHARA_CHANNEL_ID = "-1002300918510"
    api_id = 29830137
    api_hash = "4fdb6b13530915e7b513ee4318f109b9"

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
