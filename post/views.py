from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Post, PostForm

# Create your views here.
def postIndex(request):
    db = Post.objects.all()
    type = 'any'
    tags = None
    limit = 10
    page = 1

    if request.method == "GET":
        if 'limit' in request.GET:
            limit = request.GET['limit']
            limit = int(limit)

        if 'user' in request.GET:
            db = Post.objects.filter(owner_id=request.GET['user'])

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

    top = []

    if db.count() > 3:
        for i in range(0, 3):
            x = db.first()
            top.append(x)
            db = db.exclude(pk=x.pk).order_by("-timeposted")

    maxPages = db.count() // limit;
    paginator = Paginator(db, limit)
    try:
        db = paginator.page(page)
    except PageNotAnInteger:
        db = paginator.page(1)
    except EmptyPage:
        db = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'logged': 'user' in request.session, 'db': db, 'page': page, 'maxPage': maxPages,
                                          'type': type, 'tags': tags, 'limit': limit, 'top': top})


def showSell(request, response=None):
    form = PostForm
    error = None

    if response:
        error = response.get('error')

    return render(request, 'post.html', {'errors': error, 'form': form})


def postItem(request):
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            f = form.save(commit=False)
            import account.models
            f.owner = account.models.Account.objects.get(pk=request.session['user'])
            f.save()

            #return postIndex(request) for debugging
            return HttpResponseRedirect('/')
        else:
            return showSell(request=request, response={'error': form.errors})

    else:
        return showSell(request)