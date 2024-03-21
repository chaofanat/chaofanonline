import sys
import json
import urllib.parse
import urllib.request
# 获取token
def fetch_token(API_KEY, SECRET_KEY,TOKEN_URL):
    params = {  
                'grant_type': 'client_credentials',
                'client_id': API_KEY,
                'client_secret': SECRET_KEY
                }
    post_data = urllib.parse.urlencode(params)
    req = urllib.request.Request(TOKEN_URL, data=post_data.encode('utf-8'))
    f = urllib.request.urlopen(req)
    result_str = f.read().decode()
    result = json.loads(result_str)
    return result['access_token']

def get_TTspeech(text, per, spd, pit, vol, aue, file_path):
    # 设置API密钥和其他参数
    API_KEY = 'Wv3ytSZ0WaBXqcnPLwFjEozJ'
    SECRET_KEY = 'fpsJhI4jOZcFfu0bRv1R2scfcTpeu8V1'
    CUID = "E4439AF1-E561-403D-90D2-F0663B14E8DF"
    TTS_URL = 'http://tsn.baidu.com/text2audio'
    TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + API_KEY + '&client_secret=' + SECRET_KEY
    token = fetch_token(API_KEY, SECRET_KEY,TOKEN_URL)

    # 对文本进行URL编码并设置其他参数
    tex = urllib.parse.quote_plus(text)
    params = {'tok': token, 'tex': tex, 'per': per, 'spd': spd, 'pit': pit, 'vol': vol, 'aue': aue, 'cuid': CUID,
              'lan': 'zh', 'ctp': 1}
    data = urllib.parse.urlencode(params)

    # 请求TTS API并保存响应到文件
    req = urllib.request.Request(TTS_URL, data.encode('utf-8'))
    try:
        f = urllib.request.urlopen(req)
        result_str = f.read()

        headers = dict((name.lower(), value) for name, value in f.headers.items())

        if 'content-type' not in headers.keys() or headers['content-type'].find('audio/') < 0:
            raise Exception('API error')

        with open(file_path, 'wb') as of:
            of.write(result_str)

    except urllib.error.URLError as err:
        print('API http response http code : ' + str(err.code))
        result_str = err.read()
        raise Exception('API error:' + result_str)

    return True

# 示例
#get_TTspeech("欢迎使用百度语音合成。", 4, 5, 5, 5, 3, "output.mp3")
