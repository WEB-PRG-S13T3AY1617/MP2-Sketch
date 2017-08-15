from django import template
from account.models import Account
from post.models import Post, Offer

register = template.Library()

@register.filter
def getName(id):
    x = Account.objects.get(id=id)
    return x.name

@register.filter
def getUsername(id):
    x = Account.objects.get(id=id)
    return x.username

@register.filter
def getPicture(id):
    x = Account.objects.get(pk=id)
    return x.picture.url

@register.filter
def getEmail(id):
    x = Account.objects.get(pk=id)
    return x.email


@register.filter
def getContact(id):
    x = Account.objects.get(pk=id)
    return x.cell

@register.filter
def logged(req):
    if 'user' in req.session:
        return True
    else:
        return False

@register.filter
def getType(id):
    x = Account.objects.get(pk=id)
    return x.type

@register.filter
def split(str):
    return str.split()

@register.filter
def getPostItemName(id1):
    x = Post.objects.get(pk=id)
    return x.item.name

@register.filter
def getOffers(id):
    x = Offer.objects.filter(user__id=id)
    return x

@register.filter
def hasOffer(pId, uId):
    try:
        x = Offer.objects.get(post__id=pId, user_id=uId)
    except Offer.DoesNotExist:
        return False

    return True