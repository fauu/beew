import sys, os, argparse
import urllib, urllib2, urlparse
import simplejson as json

# USER SETTINGS
weeb_login = ''
weeb_password = ''
player_executable = 'mpv'
force_highdef = True                                        # Force high definition playback if available
# END

ROOT_URL = 'http://weeb.tv'
API_URL = ROOT_URL + '/api/getChannelList'
PLAYER_URL = ROOT_URL + '/api/setplayer'

arg_parser = argparse.ArgumentParser(description = 'Watch weeb.tv streams in your favourite media player')
arg_group = arg_parser.add_mutually_exclusive_group()
arg_group.add_argument('-n', '--channelname', help = 'filter channel list by name')
arg_group.add_argument('-c', '--channelid', type = int, help = 'skip channel selection and start playing')
arg_parser.add_argument('-l', '--lowquality', action = 'store_true', help = 'force lower quality playback if higher quality is available')

def channel_list_from_json(data):
    channel_list = dict()
    for key, vals in data.iteritems():
        channel_list[vals['cid']] = { 'name': vals['channel_title'], 'multibitrate': vals['multibitrate'] }
    return channel_list
    
def request(url):
    headers = { 'User-Agent': 'XBMC', 'ContentType': 'application/x-www-form-urlencoded' }
    params = { 'username': weeb_login, 'userpassword': weeb_password }
    params_encoded = urllib.urlencode(params)
    request_url = urllib2.Request(url, params_encoded, headers)
    handle = urllib2.urlopen(request_url)
    data = handle.read()
    result = json.loads(data)
    return result

def get_channel_list():
    return channel_list_from_json(request(API_URL))

def get_stream_params(channel_id):
    request_params = { 'cid': channel_id, 'platform': 'XBMC', 'username': weeb_login, 'userpassword': weeb_password }
    request_headers = { 'User-Agent': 'XBMC' }
    request_params_encoded = urllib.urlencode(request_params)
    request_url = urllib2.Request(PLAYER_URL, request_params_encoded, request_headers)
    handle = urllib2.urlopen(request_url)
    result = handle.read()
    params_raw = urlparse.parse_qs(result)
    params = { 'rtmp': params_raw['10'][0],
               'ticket': params_raw['73'][0],
               'playpath': params_raw['11'][0],
               'premium': params_raw['5'][0],
               'status': params_raw['0'][0] }
    return params

def get_rtmpdump_command(channel_id, bitrate):
    stream_params = get_stream_params(channel_id)
    if bitrate == 1 and force_highdef:
        stream_params['playpath'] += 'HI'
    command = 'rtmpdump'
    command += ' -v -r ' + stream_params['rtmp'] + '/' + stream_params['playpath']
    command += ' -s ' + stream_params['ticket']
    command += ' -p token'
    command += ' -cache 4096'
    return command

args = arg_parser.parse_args()

channels = get_channel_list()

if args.lowquality:
    force_highdef = False

if not args.channelid:
    if args.channelname:
        filter_string = ' (filter text: "' + args.channelname + '")'
    else:
        filter_string = ''
        
    print 'WEEB.tv - Available Channels' + filter_string + ':\n'

    for id, params in channels.iteritems():
        if (args.channelname and args.channelname.lower() in params['name'].lower()) or not args.channelname:
            print '[' + id + '] ' + params['name']

    channel_id = raw_input("\nEnter Channel ID: ")
else:
    channel_id = str(args.channelid)

if channel_id in channels:
    rtmp_command = get_rtmpdump_command(channel_id, channels[channel_id]['multibitrate'])
    shell_command = rtmp_command + ' | ' + player_executable + ' - 2 > /dev/null'
    os.system(shell_command)
else:
    print '\nERROR: Something went wrong! Make sure that:\n1. Selected channel is available in conventional way (through the website)\n2. Username and password you\'ve provided are correct\n3. Your premium subscription is active (if channel is currently in premium-only mode)\n'
