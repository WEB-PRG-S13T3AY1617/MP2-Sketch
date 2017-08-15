from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import RegisterForm, Account, LoginForm
from post.models import Post

# Create your views here.
def showProfile(request, id=None):
    type = 'any'
    tags = None
    limit = 10
    page = 1

    if id:
        user = Account.objects.get(pk=id)
    else:
        user = Account.objects.get(pk=request.session['user'])

    db = Post.objects.filter(owner=user)

    if 'limit' in request.GET:
        limit = request.GET['limit']
        limit = int(limit)

    if 'type' in request.GET:
        type = request.GET['type']
        if type != "any" and (type == 'office' or type == 'academic'):
            db = Post.objects.filter(use=type)

    if 'tags' in request.GET:
        tags = request.GET['tags']
        if tags:
            tags1 = tags.split()
            limFilter = Q()
            for t in tags1:
                limFilter = limFilter | Q(tags__contains=t)
            db = db.filter(limFilter)

    if 'page' in request.GET:
        page = request.GET['page']
        page = int(page)

    db = db.order_by('-timeposted')
    maxPage = db.count() // limit

    paginator = Paginator(db, limit)

    try:
        db = paginator.page(page)
    except PageNotAnInteger:
        db = paginator.page(1)
    except EmptyPage:
        db = paginator.page(paginator.num_pages)

    return render(request, 'profile.html', {'user': user.pk, 'db': db, 'page': page, 'maxPage': maxPage,
                                          'type': type, 'tags': tags, 'limit': limit})


def showRegister(request, response=None):
    form = RegisterForm
    error = None

    if response:
        error = response.get('error')

    return render(request, 'register.html', {'errors': error, 'form': form})


def showLogin(request, response=None):
    form = LoginForm
    error = None

    if response:
        error = response.get('error')

    return render(request, 'login.html', {'errors': error, 'form': form})


def registerAccount(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            user = Account.objects.filter(username=form.data.get('username'))

            if user.count() == 0:
                user = Account.objects.filter(email=form.data.get('email'))

                if user.count() == 0:
                    form.save()
                    return HttpResponseRedirect('/account/login/')
                else:
                    return showRegister(request=request, response=dict(error={'Email Address is already in use.'}))
            else:
                return showRegister(request=request, response=dict(error={'Username is already taken.'}))
        else:
            return showRegister(request=request, response=dict(error=form.errors))
    else:
        return showRegister(request=request)


def loginAccount(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        print(form)

        if form.is_valid():
            try:
                account = Account.objects.get(username=form.cleaned_data['username'],
                                              password=form.cleaned_data['password'])

                request.session['user'] = account.id
                return HttpResponseRedirect('/account/')

            except Account.DoesNotExist:
                return showLogin(request=request, response=dict(error={'Invalid Username/Password.'}))
        else:
            return showLogin(request=request, response=dict(error=form.errors))
    else:
        return showLogin(request=request)