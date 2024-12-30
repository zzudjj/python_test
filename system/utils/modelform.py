from django import forms
from system import models
from system.utils.encryption import md5


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs['class'] = 'layui-input'
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {
                    'class': 'layui-input',
                    'placeholder': field.label
                }


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {
                    'class': 'form-control',
                    'placeholder': field.label
                }


class LoginForm(forms.Form):
    username = forms.CharField(
        label='账号',
        widget=forms.TextInput(attrs={'placeholder': '账号'})
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'placeholder': '密码'})
    )


class RegisterModelForm(forms.ModelForm):
    telephone = forms.CharField(max_length=11, min_length=11,label='电话号码')
    password = forms.CharField(min_length=6,label='密码')

    class Meta:
        model = models.Passenger
        fields = ['name', 'telephone', 'password', 'sex']

    def __init__(self, *args, **kwargs):
        super(RegisterModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'password':
                field.widget = forms.PasswordInput()
            field.widget.attrs = {
                'placeholder': field.label
            }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return md5(password)


class SiteAdd(BaseModelForm):
    class Meta:
        model = models.Site
        fields = ['name']


class LineAdd(BaseModelForm):
    class Meta:
        model = models.Line
        fields = ['id']


class LineEdit(forms.ModelForm):
    class Meta:
        model = models.Line
        fields = ['id']

    def __init__(self, *args, **kwargs):
        super(LineEdit, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {
                'class': 'layui-input',
                'placeholder': field.label,
                'disabled': 'disabled',
            }


class BusAdd(BaseModelForm):
      class Meta:
        model = models.Bus
        fields = ['plate_number', 'passenger_capacity', 'line']


class BusEdit(BaseModelForm):
    plate_number = forms.CharField(disabled=True, label='车牌号')

    class Meta:
        model = models.Bus
        fields = ['plate_number', 'passenger_capacity', 'line']


class DriverAdd(BaseModelForm):
    password = forms.CharField(min_length=6, widget=forms.PasswordInput,label='密码')

    class Meta:
        model = models.Driver
        fields = ['id', 'name', 'sex', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return md5(password)


class ManagerAdd(BaseModelForm):
    password = forms.CharField(min_length=6, widget=forms.PasswordInput, label='密码')

    class Meta:
        model = models.Manager
        fields = ['id', 'name', 'sex', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return md5(password)


class DriverEdit(BaseModelForm):
    id = forms.CharField(disabled=True)

    class Meta:
        model = models.Driver
        fields = ['id', 'name', 'sex']


class WorkAdd(BaseModelForm):
    class Meta:
        model = models.Drive
        fields = ['driver', 'plate_number', 'start_time', 'end_time']
