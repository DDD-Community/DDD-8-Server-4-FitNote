from allauth.account.adapter import DefaultAccountAdapter
from attention.views import jwt_signup

class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        # 기본 저장 필드: first_name, last_name, username, email
        user = super().save_user(request, user, form, False)

        # 추가 저장 필드: profile_image
        fullname = data.get("fullname")
        if fullname:
            user.fullname = fullname

        user.save()

        ## 이 곳에 멤버십 회원 DB 추가 
        jwt_signup(user.id, user, fullname)

        return user
