from account import views

def index(request):
    if 'user' in request.GET:
        return views.showProfile(request=request, id=request.GET['user'])
    elif 'user' in request.session:
        return views.showProfile(request)
    else:
        return login(request)

def register(request, response=None):
    if 'user' in request.session:
        return views.showProfile(request)
    else:
        return views.showRegister(request, response)


def login(request, response=None):
    if 'user' in request.session:
        return views.showProfile(request)
    else:
        return views.showLogin(request, response)

def logout(request):
    if 'user' in request.session:
        request.session.flush()
    return index(request)