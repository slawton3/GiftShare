from django.views import View
from django.shortcuts import render
from .forms import SignInUserForm, RegisterUsername, GiftForm
from .models import GLUser, Gift


class Home(View):
    def get(self, request):
        request.session.set_expiry(300)
        user = request.session.get('user')
        name = request.session.get('name')
        loginForm = SignInUserForm()
        return render(request, 'giftShare/index.html', {
            "loginForm": loginForm,
            "user": user,
            "name": name
        })

    def post(self, request):
        request.session.set_expiry(300)
        loggedInFlag = 1
        loginForm = SignInUserForm()
        f = SignInUserForm(request.POST)
        if f.is_valid():
            username = f.cleaned_data['username']
            password = f.cleaned_data['password']
            try:
                request.session.set_expiry(300)
                validUser = GLUser.objects.get(
                    username=username, password=password)
                request.session['user'] = validUser.username
                request.session[
                    'name'] = validUser.firstName + ' ' + validUser.lastName
                user = request.session.get("user")
                name = request.session.get('name')
                print(name)
                print(user)
                print(loggedInFlag)
                return render(request, "giftShare/index.html", {
                    "user": user,
                    "name": name,
                    "loggedInFlag": loggedInFlag
                })
            except GLUser.DoesNotExist:
                loggedInFlag = 0
                msg = 'Username and password combination does not exist.'
                return render(request, 'giftShare/index.html', {
                    "loginForm": loginForm,
                    'msg': msg
                })
        else:
            loggedInFlag = 0
            loginForm = SignInUserForm()
            return render(request, "giftShare/index.html", {
                "loginForm": loginForm,
                "loggedInFlag": loggedInFlag
            })


class Register(View):
    def get(self, request):
        request.session.set_expiry(300)
        f = RegisterUsername()
        return render(request, 'giftShare/register.html', {"f": f})

    def post(self, request):
        request.session.set_expiry(300)
        f = RegisterUsername(request.POST)
        if f.is_valid():
            f.save()
            return render(request, "giftShare/success.html")
        else:
            errorMessage = 'Username Taken'
            return render(request, 'giftShare/register.html', {
                "f": f,
                "errorMessage": errorMessage
            })


class User(View):
    def get(self, request):
        request.session.set_expiry(300)
        user = request.session.get("user")
        print(user)
        loginMessage = 'Please sign in to use this feature.'
        print(loginMessage)
        return render(request, "giftShare/user.html", {
            "user": user,
            "loginMessage": loginMessage
        })


class Gifts(View):
    def get(self, request):
        request.session.set_expiry(300)
        giftForm = GiftForm()
        username = request.session.get("user")
        giftList = list(Gift.objects.filter(user__username=username))
        print(giftList)
        print(username)
        loginMessage = 'Please sign in to use this feature.'
        print(loginMessage)
        return render(
            request, "giftShare/gifts.html", {
                "giftForm": giftForm,
                "user": username,
                "giftList": giftList,
                "loginMessage": loginMessage
            })

    def post(self, request):
        request.session.set_expiry(300)
        loggedInFlag = 1
        f = GiftForm(request.POST)
        if f.is_valid():
            username = request.session.get("user")
            g = Gift(
                user=GLUser.objects.get(username=username),
                name=f.cleaned_data['name'])
            g.save()
            giftForm = GiftForm()
            print(loggedInFlag)
            giftList = list(Gift.objects.filter(user__username=username))
            print(giftList)
            return render(
                request, "giftShare/gifts.html", {
                    "loggedInFlag": loggedInFlag,
                    "giftForm": giftForm,
                    "giftList": giftList,
                    "user": username
                })

        else:
            giftForm = GiftForm()
            user = request.session.get("user")
            print(user)
            return render(request, "giftShare/gifts.html", {
                "giftForm": giftForm,
                "user": user
            })


class GiftSearch(View):
    def get(self, request):
        request.session.set_expiry(300)
        loggedInFlag = 1
        user = request.session.get("user")
        allGifts = list(Gift.objects.all().order_by('name'))
        print(allGifts)
        return render(request, "giftShare/giftSearch.html", {
            "allGifts": allGifts,
            "loggedInFlag": loggedInFlag,
            "user": user
        })
