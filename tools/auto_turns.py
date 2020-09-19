import time
import sys
import os

if len(sys.argv) == 1:
	print("Not enough args provided.")
	sys.exit()

t_interval = int(sys.argv[1])

if type(t_interval) != int:
	print("Not a number!")
	sys.exit()

while True:
	print("AUTOTURN: Sleeping for {} seconds...".format(t_interval))
	time.sleep(t_interval)
	print("AUTOTURN: Timer is up! Processing turn.")
	os.system('python2 ../outerspace.py ai-pool')
	os.system('python2 ./osclient_cli.py --turns=1 admin')
