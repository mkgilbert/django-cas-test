import re
import requests
from django.shortcuts import render, reverse
from django.shortcuts import HttpResponseRedirect

def home(request):
    if request.META['QUERY_STRING']:
        if "logout" in request.META['QUERY_STRING']:
            request.session.clear()
        else:
            request.session['cas_get'] = request.GET
        return HttpResponseRedirect(reverse('home'))

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
                get_data["uid"] = uid
                request.session["uid"] = uid
    return render(request, "home.html", {"data": get_data})
