# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     first_name = forms.CharField(max_length=30, required=True)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'first_name', 'password1', 'password2')
    
#     def save(self, commit=True):
#         user = super(SignUpForm, self).save(commit=False)
#         user.email = self.cleaned_data['email']
#         user.first_name = self.cleaned_data['first_name']
#         if commit:
#             user.save()
#         return user
    