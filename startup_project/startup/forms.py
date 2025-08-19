from django import forms
from django.forms import inlineformset_factory
from django.forms import BaseInlineFormSet, ValidationError

from startup.models import Startup, StartupDeveloper


class StartupForm(forms.ModelForm):
    class Meta:
        model = Startup
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
        }


class UniqueUserInlineFormSet(BaseInlineFormSet):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.exclude(role='owner')
    
    def clean(self):
        if any(self.errors):
            print('Есть ошибки в отдельных формах:', self.errors)
            return
        users = []
        for form in self.forms:
            if form.cleaned_data.get('DELETE', False):
                continue
            user = form.cleaned_data.get('user')
            if user:
                if user in users:
                    print('Пользователь уже добавлен дважды!')
                    raise ValidationError(
                        'Каждый пользователь может быть добавлен только один раз.')
                users.append(user)


class StartupDeveloperForm(forms.ModelForm):
    class Meta:
        model = StartupDeveloper
        fields = ['user', 'role']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].choices = [
            (k, v) for k, v in StartupDeveloper.ROLECHOICES if k != 'owner'
        ]
        self.fields['user'].empty_label = None


StartupDeveloperFormSet = inlineformset_factory(
    Startup,
    StartupDeveloper,
    form=StartupDeveloperForm,
    extra=0,
    can_delete=True,
    formset=UniqueUserInlineFormSet,
)
