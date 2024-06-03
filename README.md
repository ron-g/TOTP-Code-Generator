# This is a work in progress

```
usage: Totp.py [-h] [-a APPNAME] [-l] [-o ONEOFF]

Output a TOTP code given a base32 string.

options:
  -h, --help            show this help message and exit
  -a APPNAME, --appName APPNAME
                        The (comma-separated) Application Name(s) that is/are
                        the key of a record in Codes dict.
  -l, --list            Show the sites configured in the Codes dict.
  -o ONEOFF, --oneOff ONEOFF
                        Generate a code from this base32, skipping the Codes
                        dict.
```

