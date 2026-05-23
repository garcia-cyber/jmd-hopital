from django.shortcuts import render , redirect

# Create your views here.

# 01
# ======================================================================
#  HOME 
# ======================================================================
def home(request):
    return render(request ,'front-end/index.html' ) 