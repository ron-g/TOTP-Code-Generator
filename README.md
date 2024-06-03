# TOTP Code generator

## This is a work in progress

```
usage: Totp.py [-h] [-l] [-a APPNAME] [-o ONEOFF]

Output a TOTP code given a base32 string.

options:
  -h, --help            show this help message and exit
  -l, --list            Show the sites configured in the Codes dict.
  -a APPNAME, --appName APPNAME
                        The (comma-separated) Application Name(s) that is/are
                        the key of a record in Codes dict.
  -o ONEOFF, --oneOff ONEOFF
                        Generate a code from this base32, skipping the Codes
                        dict.
```

`-l` / `--list` This shows the items configured in the `TotpVars.py` file's `Codes` dictionary, alphabetically.

`-o` / `--oneOff` This shows a TOTP code given a secret key.

`-a` / `--appName` This will show the TOTP code given a comma-separated list of App Names configured in the `TotpVars.py` file's `Codes` dictionary.


