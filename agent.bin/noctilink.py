#!/usr/bin/python
import argparse
import logging
import urllib, urllib2
import sys, os
import uuid
import json
import time

####################################
CFG_DOMAIN = "localhost:8000"
CFG_UUID_FILE = "C:/Users/icharala/Local/Develop/Devin/yaco/agent.bin/machine_uuid.txt"
CFG_CONFIG_FILE = "C:/Users/icharala/Local/Develop/Devin/yaco/agent.bin/machine_config.json"
CFG_STATE_FILE = "C:/Users/icharala/Local/Develop/Devin/yaco/agent.bin/machine_state.json"
####################################

logging.basicConfig()
log = logging.getLogger("NoctiLink")

"""
Generic I/O function to the NoctiChain server
"""
def http_io(uuid, action, data={}):

	# Prepare request
	url = 'http://%s/machine/%s/%s' % ( CFG_DOMAIN, uuid, action )
	url_data = urllib.urlencode(data)
	log.debug("HTTP GET '%s'" % url)
	req = urllib2.Request(url + "?" + url_data)

	# Collect response
	try:

		# Get response
		response = urllib2.urlopen(req)
		contents = response.read()

		# Parse to json
		try:
			json_data = json.loads( contents )
			return json_data

		except ValueError, e:
			log.error("HTTP Parsing Error: %s" % str(e))
			return None

	except urllib2.URLError, e:
		log.error("HTTP Error: %s" % e.reason)
		return None


"""
Fetch from local storage or download (if not yet available) the machine
configuration string.
"""
def machine_config(uuid, cluster=""):

	# Check if we have local configuration
	if os.path.exists(CFG_CONFIG_FILE):
		with file(CFG_CONFIG_FILE) as f:
			config_str = f.read()
		try:
			log.info("Using cached configuration for this machine")
			cached_data = json.loads(config_str)

			# Validate the integrity of the cached data
			time_now = time.time()
			if (time_now <= cached_data['expires']) and (cached_data['cluster'] == cluster):
				return cached_data

			# (Cache is invalid, re-download)
			log.info("Local cache is invalid")

		except ValueError, e:
			log.error("Config parsing error: %s" % e.reason)
			return None

	# Nope, we don't have one: Download
	log.info("Donwloading configuration for this machine")
	config = http_io(uuid, "config", { 'cluster': cluster })
	if config != None:
		config_str = json.dumps(config, indent=4, separators=(',',':'))
		with file(CFG_CONFIG_FILE, 'w') as f:
			f.write( config_str )

	# Return the configuration hash
	return config


"""
Get or generate a new unique ID for this machine
"""
def machine_uuid():
	if os.path.exists(CFG_UUID_FILE):
		with file(CFG_UUID_FILE) as f:
		    mid = f.read()
		return mid
	else:
		mid = uuid.uuid4().hex
		with file(CFG_UUID_FILE, 'w') as f:
			f.write( mid )
		return mid

# ENTRY POINT
if __name__ == '__main__':

	# Prepare command-line parser
	parser = argparse.ArgumentParser(description='Starts the NoctiChain client node, making the machine a NoctiChain slave.')
	parser.add_argument('-c', type=str, default="", metavar="CLUSTER",
						help='The UUID of the cluster this VM belongs to')
	parser.add_argument('-v', action="count",
						help='Increase the log verbosity')
	parser.add_argument('--boot', action='store_true',
						help='Informs the noctilink that runs at boot time')
	args = parser.parse_args()

	# Tune logger
	if not args.v:
		log.setLevel(logging.INFO)
	else:
		log.setLevel(logging.DEBUG)

	# Get machine UUID
	machine_id = machine_uuid()
	log.info("Machine #%s" % machine_id)
	config = machine_config( machine_id, args.c )