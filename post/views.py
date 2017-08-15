from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django import forms
from .models import Post, PostForm, OfferForm, Offer
from account.models import Account

# Create your views here.
def postIndex(request):
    db = Post.objects.all()
    type = 'any'
    user = None
    tags = None
    limit = 10
    page = 1

    if 'user' in request.session:
        user = Account.objects.get(pk=request.session['user'])

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

    return render(request, 'index.html', {'logged': user != None, 'user': user, 'db': db, 'page': page, 'maxPage': maxPages,
                                          'type': type, 'tags': tags, 'limit': limit, 'top': top})


def showSell(request, response=None):
    form = PostForm
    error = None

    if response:
        error = response.get('error')

    return render(request, 'post.html', {'errors': error, 'form': form})

def changeForm(request):
    if request.method == 'GET':
        user = None
        post = None
        offer = None

        if 'user' in request.session:
            user = request.session['user']
        else:
            return HttpResponse(OfferForm(hidden='item', user=None).as_p())

        if 'post' in request.GET:
            try:
                post = Post.objects.get(pk=request.GET['post'])
            except Post.DoesNotExist:
                return HttpResponse(OfferForm(hidden='item', user=None).as_p())

            try:
                offer = Offer.objects.get(user=user, post=post)
            except Offer.DoesNotExist:
                if 'type' in request.GET:
                    return HttpResponse(OfferForm(user=user, initial={'offerType': 'item' if request.GET['type'] == 'item' else 'money'},hidden='money' if request.GET['type'] == 'item' else 'item').as_p())
                else:
                    return HttpResponse(OfferForm(instance=offer, hidden='item', user=user).as_p())

            if 'type' in request.GET:
                return HttpResponse(OfferForm(instance=offer, initial={'offerType': 'item' if request.GET['type'] == 'item' else 'money'} , user=user,
                                 hidden='money' if request.GET['type'] == 'item' else 'item').as_p())

    else:
        return HttpResponse(OfferForm(hidden='item', user=None).as_p())

def showItem(request, response=None):
    if 'post' in request.GET:
        offer = None
        post = request.GET['post']
        user = None
        order = 1

        offers = Offer.objects.filter(post=post)

        if 'order' in request.GET:
            order = request.GET['order']

        if 'user' in request.session:
            user = request.session['user']
        else:
            return HttpResponseRedirect('/')

        try:
            offer = Offer.objects.get(post=post, user=user)
        except Offer.DoesNotExist:
            offer = None

        user = Account.objects.get(pk=user)

        if offer is not None:
            form = OfferForm(instance=offer, user=user.pk, hidden='money' if offer.offerType == 'item' else 'item')
        else:
            form = OfferForm(user.pk, hidden='item')

        try:
            post = Post.objects.get(pk=post)
        except:
            return HttpResponseRedirect('/')

        if order != 1:
            offers = offers.order_by('-item__price', '-money')
        else:
            offers = offers.order_by('-timeoffered')

        return render(request, 'view_post.html',{'offers': offers, 'item': post, 'user': user.pk, 'form': form})
    else:
        return HttpResponseRedirect('/')


def acceptOffer(request):
    if 'offer' in request.GET:
        try:
            offer = Offer.objects.get(pk=request.GET['offer'])
        except Offer.DoesNotExist:
            return JsonResponse(dict(success=False))

        if offer.offerType == 'item' and offer != None:
            offer.post.quantity = offer.post.quantity - 1
            offer.item.quantity = offer.item.quantity - 1
            offer.item.save()
            offer.post.save()
            offer.save()

            if offer.item.quantity <= 0:
                offer.item.delete()

            if offer.post.quantity <= 0:
                offer.post.delete()

        offer.delete()
        return JsonResponse(dict(success=True))

def rejectOffer(request):
    if 'offer' in request.GET:
        try:
            offer = Offer.objects.get(pk=request.GET['offer'])
        except Offer.DoesNotExist:
            return JsonResponse(dict(success=False))

        offer.delete()
        return JsonResponse(dict(success=True))

def postItem(request):
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            f = form.save(commit=False)
            import account.models
            f.owner = account.models.Account.objects.get(pk=request.session['user'])
            f.save()

            # return postIndex(request) #for debugging
            return HttpResponseRedirect('/')
        else:
            return showSell(request=request, response={'error': form.errors})

    else:
        return HttpResponseRedirect('/')

def offerItem(request):
    if request.method == 'POST':
        user = None
        post = None

        if 'user' in request.session:
            try:
                user = Account.objects.get(pk=request.session['user'])
            except user.DoesNotExist:
                return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')

        if 'post' in request.POST:
            try:
                post = Post.objects.get(pk=request.POST['post'])
            except post.DoesNotExist:
                return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')

        form = OfferForm(data=request.POST, user=user.pk, hidden='money' if request.POST['offerType'] == 'item' else 'item')

        if form.is_valid():
            try:
                offer = Offer.objects.get(post=post, user=user)

                offer.offerType=form.cleaned_data['offerType']

                if offer.offerType == 'item':
                    offer.item=form.cleaned_data['item']

                if offer.offerType == 'money':
                    offer.money=form.cleaned_data['money']

                offer.save()
            except Offer.DoesNotExist:
                frm = form.save(commit=False)
                frm.user = user
                frm.post = post
                frm.save()

            return showItem(request)
        else:
            return showItem(request, response={'error': form.errors})

    else:
        return showItem(request, response=dict(success=False, error="Invalid request method!"))

def cancelOffer(request):
    if request.method == 'GET':
        if 'post' in request.GET:
            try:
                if 'user' not in request.GET and 'user' in request.session:
                    user = Account.objects.get(pk=request.session['user'])
                elif 'user' in request.GET:
                    user = Account.objects.get(pk=request.GET['user'])
                else:
                    return HttpResponseRedirect("/showItem/?post=" + request.GET['post'])

                offer = Offer.objects.get(post=request.GET['post'], user=user)
                offer.delete()

                return HttpResponseRedirect('/showItem/?post=' + request.GET['post'])
            except Offer.DoesNotExist:
                return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

def hasOffer(request):
    if request.method == "POST":
        if 'post' in request.POST and 'user' in request.POST:
            try:
                offer = Offer.objects.get(post=request.POST['user'], user=request.POST['post'])
            except Offer.DoesNotExist:
                return JsonResponse(dict(has=False))

            return JsonResponse(dict(has=True))
        else:
            return JsonResponse(dict(has=False))