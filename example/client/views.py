from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

import opentracing
import urllib2

# Create your views here.

def client_index(request):
    return HttpResponse("Client index page")

def client_simple(request):
    url = "http://localhost:8000/server/simple"
    new_request = urllib2.Request(url)
    current_span = settings.OPENTRACING_TRACER.get_span(request)
    inject_as_headers(settings.OPENTRACING_TRACER, current_span, new_request)
    try:
        response = urllib2.urlopen(new_request)
        return HttpResponse("Made a simple request")
    except urllib2.URLError as e:
        return HttpResponse("Error: " + str(e))

def client_log(request):
    url = "http://localhost:8000/server/log"
    new_request = urllib2.Request(url)
    current_span = settings.OPENTRACING_TRACER.get_span(request)
    inject_as_headers(settings.OPENTRACING_TRACER, current_span, new_request)
    try:
        response = urllib2.urlopen(new_request)
        return HttpResponse("Sent a request to log")
    except urllib2.URLError as e:
        return HttpResponse("Error: " + str(e))

def client_child_span(request):
    url = "http://localhost:8000/server/childspan"
    new_request = urllib2.Request(url)
    current_span = settings.OPENTRACING_TRACER.get_span(request)
    inject_as_headers(settings.OPENTRACING_TRACER, current_span, new_request)
    try:
        response = urllib2.urlopen(new_request)
        return HttpResponse("Sent a request that should produce an additional child span")
    except urllib2.URLError as e:
        return HttpResponse("Error: " + str(e))

def inject_as_headers(tracer, span, request):
    text_carrier = {}
    tracer._tracer.inject(span.context, opentracing.Format.TEXT_MAP, text_carrier)
    for k, v in text_carrier.iteritems():
        request.add_header(k,v)
