from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.db.models import Q
from time import time
import json

def signed_response(data):

	# Calculate signature
	data['signature'] = 'checksum'

	# Send response
	json_txt = json.dumps(data)
	return HttpResponse(json_txt, content_type="text/json")


def api_config(request, uuid=""):

	# Fetch configuration from the URL
	cluster_id=""
	if 'cluster' in request.GET:
		cluster_id = request.GET['cluster']

	# Calculate expiry time
	time_now = time()
	time_expire = time_now + 60

	# Prepare configuration hash
	config = {
		'cluster'	: cluster_id,
		'timestamp'	: time_now,
		'expires'	: time_expire
	}

	# Return signed response
	return signed_response(config)

def api_refresh(request, uuid=""):

	# Calculate current time
	time_now = time()

	# Prepare configuration hash
	config = {
		'timestamp'	: time_now
	}

	# Return signed response
	return signed_response(config)
