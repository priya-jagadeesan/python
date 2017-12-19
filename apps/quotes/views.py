from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib import messages

##=========================================================================##
##                              Render Routes                              ##
##=========================================================================##  

def index(request):
    return render(request,"quotes/index.html")

##=========================================================================##
##        Validate User Login data - set session to user_id                ##
##=========================================================================##  

def validate(request):
    # form fields validation 
    errors = User.objects.validateLogin(request.POST)
    if errors:
        for error, value in errors.iteritems():
            messages.error(request, value, extra_tags=error)
        return redirect(index)

    # user login data validation
    else:
        user = User.objects.validateLoginData(request.POST)
        if not user:
            messages.error(request, "Invalid login credentials", extra_tags='invalid')
            return redirect(index)
        else:
            request.session['user_id'] = user.id
            success_msg = "Welcome " + str(user.alias)
            where = "logged in"
            messages.success(request, success_msg, extra_tags='user')
            messages.success(request, where, extra_tags='where')
            return redirect(quotesWall)

##=========================================================================##
##        Validate User Registration data - set session to user_id         ##
##=========================================================================##  

def regvalidate(request):
    errors = User.objects.validateRegisterData(request.POST)
    if errors:
        for error, value in errors.iteritems():
            messages.error(request, value, extra_tags=error)
        # data = {"data" : request.POST}

    else:
        user = User.objects.registerData(request.POST)
        if user:
            request.session['user_id'] = user.id
            success_msg = "Welcome " + str(user.alias)
            where = "registered"
            messages.success(request, success_msg, extra_tags='user')
            messages.success(request, where, extra_tags='where')
            return redirect(quotesWall)
        
    return redirect(index)
##=========================================================================##
##        Quotes wall                                                      ##
##=========================================================================##  

def quotesWall(request):
    if not request.session['user_id']:
        return redirect(index)
    else:
        user = User.objects.get(id=request.session['user_id'])
        # quotes = Quote.objects.exclude(posted_by=request.session['user_id'])
        quotes  = Quote.objects.exclude(id__in=user.favorite_quotes.all())
        fav_quotes = Quote.objects.get_quotes_fav(request.session['user_id'])
        data = {"quotes" : quotes,
                "fav_quotes" : fav_quotes
        }
        return render(request,"quotes/quotesWall.html",data)

##=========================================================================##
##        Validate user added Quotes wall                                  ##
##=========================================================================##  

def quotesValidate(request):
    errors = Quote.objects.validate_quotes_fields(request.POST)
    if errors:
        for error, value in errors.iteritems():
            messages.error(request, value, extra_tags=error)
        # return redirect(quotesWall)
    else:
        quotes = Quote.objects.add_quotes_data(request.POST,request.session['user_id'])
        if not quotes :
            messages.error(request,"Invalid user", extra_tags='invalid')
            return redirect(logout)
    return redirect(quotesWall)

def quoteAddFav(request,id):
    fav_quotes = Quote.objects.add_quotes_fav(id,request.session['user_id'])
    if not fav_quotes:
        messages.error(request, "Cannot add to favorites", extra_tags='error')
    else:
        return redirect(quotesWall)

def quoteRemFav(request,id):
    fav_quotes = Quote.objects.rem_quotes_fav(id,request.session['user_id'])
    if not fav_quotes:
        messages.error(request, "Cannot remove to favorites", extra_tags='error')
    else:
        return redirect(quotesWall)


def userShow(request,id):
    user_details = User.objects.get_user_postedQuotes(id)
    if not user_details:
        messages.error(request, "No user found", extra_tags='error')
    else :
        data = {"user_details" : user_details}
    return render(request,"quotes/userDisplay.html",user_details)

def logout(request):
    del request.session
    return redirect(index)