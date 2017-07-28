import post.views
import account.views

def index(request):
    return post.views.postIndex(request)

def sell(request):
    if 'user' in request.session:
        return post.views.showSell(request, None)
    else:
        return account.views.showLogin(request)