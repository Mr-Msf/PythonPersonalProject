ASSET_INFO_DICT = {
    "Map(v0.1)" : ((0,0), 28, ), 
    "CharSword1" : ((0,0), 10, )

}

def retrieve_info():
    return ASSET_INFO_DICT

def retrieve_names():
    ASSET_NAMES_LIST = []
    for key in ASSET_INFO_DICT:
        ASSET_NAMES_LIST.append(key)
    return ASSET_NAMES_LIST