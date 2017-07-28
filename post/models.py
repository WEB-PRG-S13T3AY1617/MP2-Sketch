from django import forms
from django.db import models
from account.models import Account

# Create your models here.
choices = (('office', 'Office Use'), ('academic', 'Academic Use'))

class Post(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    use = models.CharField(max_length=8, default="office", choices=choices)
    course = models.CharField(max_length=13)
    quantity = models.PositiveIntegerField(default=0)
    tags = models.TextField(max_length=255)
    picture = models.ImageField(upload_to='items/%Y/%m/%d', default='default.jpg')
    timeposted = models.DateTimeField(auto_now=True)

class PostForm(forms.ModelForm):

    class Meta:
        model = Post

        fields = ['name', 'description', 'use', 'course', 'quantity', 'tags', 'picture']

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
            'quantity': 'Item Quantity',
            'tags': 'Item Tags',
            'picture': 'Item Picture',
            'course': 'Item Course',
        }