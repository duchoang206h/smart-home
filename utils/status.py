TURN_ON = ['Mở', 'Bật']
TURN_OFF = ['Tắt', 'Đống']
def getStatusFromKeyword(keyword: str):
    for i in TURN_ON:
        if(keyword.find(i) != -1):
            print(i)
            return True
    for i in TURN_OFF:
        if(keyword.find(i) != -1):
            return False
    else :
        return None
def getPkFromKeyword(keyword: str):
    for i in TURN_ON:
        keyword = keyword.replace(i, "")
    for i in TURN_OFF:
        keyword = keyword.replace(i, "")
    return keyword.strip()