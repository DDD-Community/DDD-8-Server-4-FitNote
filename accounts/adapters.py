from allauth.account.adapter import DefaultAccountAdapter
from attention.views import jwt_signup

class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data

        user = super().save_user(request, user, form, False)

        fullname = data.get("fullname")

        if fullname:
            user.fullname = fullname

        user.save()

        ## 이 곳에 멤버십 회원 DB 추가 
        jwt_signup(user.id, fullname, user)

        return user
