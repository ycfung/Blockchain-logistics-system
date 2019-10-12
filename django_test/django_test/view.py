from django.http import HttpResponse


def hello(request):
    # 此处根据请求内容调用test.py中的相应方法
    if(request.method == "POST"):
        # request.POST 返回 QueryDict 对象
        print(request.POST)
    elif(request.method == "GET"):
        print(request.GET)
    return HttpResponse(request)
