from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.db.models import Q

### CONFIGS ###

def view_cfg_list(request):
	pass

def view_cfg_new(request):
	pass

def view_cfg_display(request, uuid):
	# Populate data
	data = { }

	# Render to response
	return render_to_response(
		'editor/context.html',
		data,
		context_instance=RequestContext(request)
		)

def view_cfg_edit(request, uuid):
	pass


def view_cfg_api(request, uuid):
	pass


### SCRIPTLETS ###

def view_scpt_list(request):
	pass

def view_scpt_new(request):
	pass

def view_scpt_display(request, uuid):
	# Populate data
	data = {
		'name': uuid
	}

	# Render to response
	return render_to_response(
		'editor/scriptlet.html',
		data,
		context_instance=RequestContext(request)
		)

def view_scpt_edit(request, uuid):
	pass


def view_scpt_api(request, uuid):
	pass

