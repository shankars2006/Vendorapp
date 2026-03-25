from django import forms
from django.contrib.auth.models import User
from .models import Product


class VendorRegisterForm(forms.Form):

    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    location = forms.CharField(max_length=200)
    mobile_number = forms.CharField(max_length=15)

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):

        data = super().clean()

        if data.get("password") != data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match")

        if User.objects.filter(username=data.get("username")).exists():
            raise forms.ValidationError("Username already exists")

        return data


# Vendor Login Form
class VendorLoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# Product Upload Form
class ProductForm(forms.ModelForm):

    class Meta:

        model = Product

        fields = ["name", "description", "price", "image", "quantity", "category", "unit_or_size"]
        
        widgets = {
            'unit_or_size': forms.TextInput(attrs={'placeholder': 'Enter size for Dress or "KGs" for produce'}),
        }


class CustomerRegisterForm(forms.Form):

    username = forms.CharField(max_length=100)

    email = forms.EmailField()

    password = forms.CharField(widget=forms.PasswordInput)

    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):

        data = super().clean()

        if data.get("password") != data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match")

        if User.objects.filter(username=data.get("username")).exists():
            raise forms.ValidationError("Username already exists")

        return data


class CustomerLoginForm(forms.Form):

    username = forms.CharField()

    password = forms.CharField(widget=forms.PasswordInput)


class ReviewForm(forms.ModelForm):
    class Meta:
        from .models import Review
        model = Review
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.Select(choices=Review.RATING_CHOICES),
            'review_text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your review here (optional)...', 'required': False}),
        }
