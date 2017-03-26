import re
import requests
from django.shortcuts import render, reverse
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.models import User
from main.models import CVTUser

def home(request, uid=None):
    if uid is not None:
        try:
            user = User.objects.get(username=uid)
            cvt_user = CVTUser.objects.get(user)
            get_data = {"user": cvt_user.user.username}
        except Exception:
            get_data = {"info": "no logged in user"}
    else:
        get_data = {"info": "no uid provided"}
    return render(request, "home.html", {"data": get_data})

def login(request):
    if request.META['QUERY_STRING']:
        request.session['cas_get'] = request.GET
        return HttpResponseRedirect(reverse('login'))

    #return redirect('https://cas.nau.edu/cas/index.jsp?service=http://localhost:8000')
    #d = {'test': 1, 'blah': 2, 'foo': 3}
    if 'uid' in request.session:
        get_data = {'uid': request.session['uid']}
    else:
        get_data = request.session.get('cas_get', None)
        if get_data is not None and "ticket" in get_data.keys():
            link = "https://cas.nau.edu/cas/serviceValidate?ticket=%s" % get_data['ticket']
            link += "&service=http://localhost:8000"
            f = requests.get(link)
            get_data['link_return'] = f.text
            output = re.search('<cas:user>(.*)</cas:user>', f.text)
            if output is None:
                get_data["error"] = "invalid ticket"
            else:
                uid = output.group(1)
                try:
                    user = User.objects.get(username=uid)
                    cvt_user = CVTUser.objects.get(user=user)
                except User.DoesNotExist or CVTUser.DoesNotExist:
                    user = User.objects.create(username=uid)
                    cvt_user = CVTUser.objects.create(user=user)
                    cvt_user.is_logged_in = True
                    cvt_user.save()
                get_data["uid"] = uid
                request.session["uid"] = uid
    return render(request, "home.html", {"data": get_data})

def logout(request):
    if request.META['QUERY_STRING']:
        request.session.clear()
        return HttpResponseRedirect('home')