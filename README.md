beew
====

Unofficial weeb.tv python script which allows you to watch weeb.tv streams using your favourite media player

### Requirements:
_python2.x_ with _simplejson_ module, _rtmpdump_, capable media player

### Usage:
Run as a python script, for example:
```python2 beew.py```

You need to provide your media player's executable name in _beew.py_ (line _8._)

If you want to have access to a larger array of channels you also need to provide your weeb.tv username and password in _beew.py_ (lines _6._ and _7._). If the channel you want to watch is currently premium-only, specified account has to have an active premium subscription.

##### All options:

```
usage: beew.py [-h] [-n CHANNELNAME | -c CHANNELID] [-l]

Watch weeb.tv streams in your favourite media player

optional arguments:
  -h, --help       show this help message and exit
  -n CHANNELNAME, --channelname CHANNELNAME
                   filter channel list by name
  -c CHANNELID, --channelid CHANNELID
                   skip channel selection and start playing
  -l, --lowquality force lower quality playback if higher quality is available
```
