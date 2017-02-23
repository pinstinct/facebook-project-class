from django.shortcuts import render


def login_fbv(request):
    return render(request, 'member/login.html')
