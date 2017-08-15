from django import forms
from django.db import models
from account.models import Account

# Create your models here.
choices = (('office', 'Office Use'), ('academic', 'Academic Use'))
choices2 = (('item', 'Item'), ('money', 'Money'))

class Post(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=100)
    use = models.CharField(max_length=8, default="office", choices=choices)
    course = models.CharField(max_length=13)
    quantity = models.PositiveIntegerField(default=0)
    tags = models.TextField(max_length=255)
    picture = models.ImageField(upload_to='items/%Y/%m/%d', default='default.jpg')
    timeposted = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
class Offer(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="buy")
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    offerType = models.CharField(max_length=5, default='money', choices=choices2)
    money = models.PositiveIntegerField(default=0)
    item = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, default=None, related_name="trade")
    timeoffered = models.DateTimeField(auto_now=True)
    
class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer

        fields = ['offerType', 'money', 'item']

        labels = {
            'offerType': 'Type of Offer',
            'money': 'Amount in PHP',
            'item': 'Item to Trade',
        }

    def __init__(self, user, hidden, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)

        if hidden == 'item':
            del self.fields['item']
        elif hidden == 'money':
            print(self.fields['offerType'].initial)
            self.fields['item'] = forms.ModelChoiceField(
                queryset=Post.objects.filter(owner__pk=user), required=False
            )

            self.fields['item'].label_from_instance = lambda obj: "%s" % obj.name

            del self.fields['money']



class PostForm(forms.ModelForm):

    class Meta:
        model = Post

        fields = ['name', 'description', 'use', 'course', 'price','quantity', 'tags', 'picture']

        widgets = {
            'name': forms.TextInput(attrs={'required': True, 'placeholder': "Item Name..."}),
            'description': forms.TextInput(attrs={'required': True, 'placeholder': 'Item Description...'}),
            'quantity': forms.NumberInput(),
            'course': forms.TextInput(attrs={'required': True, 'placeholder': 'Input course code if academic, else input N/A...'}),
            'tags': forms.Textarea(attrs={'required': True, 'placeholder': "Item tags"}),
        }

        labels = {
            'name': 'Item Name',
            'description': 'Item Description',
            'use': 'Item Use',
            'price': 'Item Price',
            'quantity': 'Item Quantity',
            'tags': 'Item Tags',
            'picture': 'Item Picture',
            'course': 'Item Course',
        }