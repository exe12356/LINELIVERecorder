import requests
import sys
import os
import subprocess
import time
import getopt

G_channel_id = '3573156'


def rec_hls(filename, m3u8, format):
    m3u8 = str(m3u8).replace('240/chunklist.m3u8', '720/chunklist.m3u8')
    filename = str(filename).replace('/', '_')
    nowtime = time.strftime("%Y%m%d%H%M%S", time.localtime())
    filename = '[' + nowtime + ']' + filename
    command = 'ffmpeg -c copy "' + filename + \
        '.' + format + '"' + ' -i "' + m3u8 + '"'
    print(command)
    code = subprocess.call(command)
    print(str(code))


def GetRequest(url):
    response = requests.get(url)
    data = response.json()
    return data
# channel_response = requests.get('https://live-api.line-apps.com/app/channel/4369341')


def get_hls(liveid, channel_id):

    hls_api = 'https://live-api.line-apps.com/app/v2/channel/{channel_id}/broadcast/{live_id}'
    hls_api = hls_api.format(channel_id=channel_id, live_id=liveid)
    print(hls_api)
    hls_data = GetRequest(hls_api)
    m3u8 = hls_data['liveHLSURLs']['720']
    return m3u8

# data = channel_response.json()

# print(data['liveBroadcasts']['hasNextPage'])


def main(argv):
    channel_id = ''
    try:
        opts, args = getopt.getopt(argv, "c:")
        # for item in opts:
        #     print(item)
        channel_id = opts[0][1]
    except:
        channel_id = G_channel_id
    while(1):

        channel_api = 'https://live-api.line-apps.com/app/channel/' + channel_id
        data = GetRequest(channel_api)
        if(len(data['liveBroadcasts']['rows']) > 0):
            m3u8 = get_hls(data['liveBroadcasts']['rows'][0]['id'], channel_id)
            print(m3u8)
            rec_hls(data['liveBroadcasts']['rows'][0]['title'],
                    m3u8, 'ts')
        else:
            nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(nowtime + ' ' + data['title'] + 'has no live now')
            for num in range(1, 6):
                print('wait ' + str(num) + 's then refresh')
                time.sleep(1)


if __name__ == "__main__":
    main(sys.argv[1:])

# for item in data['liveBroadcasts']['rows']:
#     print(item['autoPlayURL'])
