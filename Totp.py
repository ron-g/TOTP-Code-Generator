#!/usr/bin/python3

import pyotp
import datetime
from TotpVars import Codes
import argparse
from sys import argv, exit, stdout, stderr
from math import floor, ceil
from time import sleep as zzz

clear="\x1b[H\x1b[2J"
CHR=' '
widthAppName = -1

try:
	from colorama import Back, Fore, Style
	C1 = Fore.YELLOW
	C2 = Fore.GREEN

	BGOK, FGOK = Back.GREEN, Fore.GREEN
	BGCAUTION, FGCAUTION = Back.YELLOW, Fore.YELLOW
	BGERR, FGERR = Back.RED, Fore.RED

	RST = Style.RESET_ALL
except:
	print('colorama not available', file=stderr)
	C1, C2, RST = '', '', ''
	OK, CAUTION, ERR = '', '', ''
	C1, C2 = '', ''

	BGOK, FGOK = '', ''
	BGCAUTION, FGCAUTION = '', ''
	BGERR, FGERR = '', ''

ValidBase32Chars="234567ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NonExistentAppNames=[]

parser = argparse.ArgumentParser(description="Output a TOTP code given a base32 string.")

parser.add_argument(
	"-l",
	"--list",
	action="store_true",
	default = False,
	help="Show the sites configured in the Codes dict."
	)

parser.add_argument(
	"-a",
	"--appName",
	type=str,
	default = "N/A",
	help="The (comma-separated) Application Name(s) that is/are the key of a record in Codes dict."
	)

parser.add_argument(
	"-o",
	"--oneOff",
	type=str,
	help="Generate a code from this base32, skipping the Codes dict."
	)

parser.add_argument(
	"-w",
	"--whyle",
	action="store_true",
	default = False,
	help="Show the TOTP token(s) in a loop. Ctrl+c to quit."
	)

args = parser.parse_args()

if args.list:
	print(f"{C1}These are the configured apps/sites.:{RST}")
	for _ in sorted(Codes):
		print(f'\t"{C2}{_}{RST}"')
	print()
	exit(0)

if args.oneOff:
	#print(f"""TOTP code for One Off "{args.oneOff}":""")
	args.appName = 'One Off'
	Codes = { args.appName : args.oneOff }

TheApplications = args.appName.split(',')
TheApplications = sorted(set(TheApplications))

for eachApp in TheApplications:
	if eachApp in Codes:
		widthAppName = max(len(eachApp), widthAppName)

widthAppName += 2

while True:
	try:
		if args.whyle:
			print(clear, end='')
		for eachApp in TheApplications:
			InvalidChars=''
			InvalidCherrors=False
			Plural= [ "was", '' ]

			if eachApp in Codes:

				TheCode = Codes[eachApp].replace(' ','')

				for char in TheCode:
					if char in ValidBase32Chars:
						continue
					else:
						InvalidCherrors=True
						InvalidChars=f"{InvalidChars}{char}"
						if len(InvalidChars) >1:
							Plural[0]="were"
							Plural[1]="s"

				if InvalidCherrors:
					print(f"{FGERR}-There {Plural[0]} {len(InvalidChars)} invalid character{Plural[1]} in value for \"{eachApp}\".{RST}\n\t{', '.join(InvalidChars)}\n", file=stderr)
					exit(1)
				else:
					totp = pyotp.TOTP(TheCode)
					time_remaining = ceil(totp.interval - datetime.datetime.now().timestamp() % totp.interval)
					if time_remaining <= ceil(.15 * totp.interval):
						TimeLeftColor = BGERR
						CodeColor = FGERR
					elif time_remaining <= ceil(.30 * totp.interval):
						TimeLeftColor = BGCAUTION
						CodeColor = FGCAUTION
					else:
						TimeLeftColor = BGOK
						CodeColor = FGOK

					print(f"""{eachApp + ':': <{widthAppName}}{CodeColor}{totp.now()} [{time_remaining: >2}] {TimeLeftColor}{CHR * time_remaining}{RST}""")

			else:
				NonExistentAppNames.append(eachApp)
				continue

		if args.whyle:
			zzz(1)
		else:
			break
	except KeyboardInterrupt as e:
		print("Exiting.")
		exit(0)

if len(NonExistentAppNames) >0:
	for eachApp in NonExistentAppNames:
		print(f"""{FGERR}-"{eachApp}" isn't a valid App Name in the dictionary. Skipped.{RST}""", file=stderr)


