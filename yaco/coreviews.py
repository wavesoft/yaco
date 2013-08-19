from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.db.models import Q

def view_redirect(request):
	return redirect("index")

def view_index(request):

	# Populate data
	data = { }

	# Render to response
	return render_to_response(
		'basic.html',
		data,
		context_instance=RequestContext(request)
		)

def view_dashboard(request):
	pass