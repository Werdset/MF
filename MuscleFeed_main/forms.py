import re

from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .models import *


class NameField(forms.CharField):
    def validate(self, value):
        t = WrapperTranslations.objects.get(active=True)
        super(NameField, self).validate(value)
        if bool(re.compile(r'[^ A-zА-яЁё\u0590-\u05FF()+0-9-]+').search(value)):
            raise ValidationError(t.try_again)


class AgreedField(forms.BooleanField):
    def validate(self, value):
        t = WrapperTranslations.objects.get(active=True)
        super(AgreedField, self).validate(value)
        if not value:
            raise ValidationError(t.agreed_error)


class SignupFormStep1(SignupForm):
    email = forms.EmailField()
    agreed = AgreedField()

    def clean(self):
        super(SignupFormStep1, self).clean()
        if 'username' in self.errors.keys():
            del self.errors['username']


class SignupFormStep3(forms.Form):
    user_name = NameField()
    user_surname = NameField()
    user_sex = forms.CharField()
    user_phone = forms.CharField()
    user_address = forms.CharField()


class AccountChangeEmailForm(AuthenticationForm):
    new_email = forms.EmailField()


class AccountChangePersonalDataForm(AuthenticationForm):
    new = NameField()


class WriteReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'url', 'name']


class CallMeForm(forms.ModelForm):
    class Meta:
        model = CallRequest
        fields = ['name', 'phone']


class OrderCallForm(forms.ModelForm):
    email = forms.CharField(max_length=150, required=False)
    comment = forms.CharField(max_length=200, required=False)

    class Meta:
        model = Order
        fields = ['name', 'address']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'email', 'phone', 'payment_type', 'referral_id']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['url', 'name', 'name_he', 'content', 'content_he', 'photo']
