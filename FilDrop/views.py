from django.shortcuts import render,redirect
from FilDrop.models import *
# Create your views here.
def Home(request):
    
    return render(request,'home.html')


def Login(request):
    request.session['WalletAddress'] = "xxx"
    if request.POST:
        WalletAddress = request.POST.get('WalletAddress')
        request.session['WalletAddress'] = WalletAddress
        obj = User.objects.get_or_create(WalletAddress=WalletAddress)
        return render(request,'userpage.html',{'WalletAddress':WalletAddress})
    else:
        return redirect('home')