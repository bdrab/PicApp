from django.forms import ModelForm
from website.models import Profile


class CreateProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['tier']