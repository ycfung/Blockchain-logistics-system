from django.http import HttpResponse
from django_test.sawtooth_client.test import *
import json


def hello(request):
    # 此处根据请求内容调用test.py中的相应方法
    if (request.method == "POST"):
        # request.POST 返回 QueryDict 对象
        function = request.POST['func']
        f = {'status': 'success', 'data': 'this is data you POST'}
        try:
            m = method()
            if (len(request.POST) == 2):
                f = str(getattr(m, function)(request.POST['arg1']))
            elif (len(request.POST) == 3):
                f = getattr(m, function)(request.POST['arg1'], request.POST['arg2'])
            elif (len(request.POST) == 4):
                f = getattr(m, function)(request.POST['arg1'], request.POST['arg2']), request.POST['arg3']
        except TypeError:
            f = {'status': 'failed', 'message': 'Wrong argument(s)'}
        return HttpResponse(json.dumps(f), content_type='application/json')


    elif request.method == "GET":
        function = request.GET['func']
        f = {'status': 'success', 'message': 'this is a success message'}
        try:
            m = method()
            if (len(request.GET) == 1):
                f = getattr(m, function)()
            if (len(request.GET) == 2):
                f = getattr(m, function)(request.GET['arg1'])
            elif (len(request.GET) == 3):
                f = getattr(m, function)(request.GET['arg1'], request.GET['arg2'])
            elif (len(request.GET) == 4):
                f = getattr(m, function)(request.GET['arg1'], request.GET['arg2']), request.GET['arg3']
        except TypeError:
            f = {'status': 'failed', 'message': 'Wrong argument(s)'}
        return HttpResponse(json.dumps(f), content_type='application/json')
