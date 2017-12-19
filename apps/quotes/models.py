from __future__ import unicode_literals
from django.db import models
import re, bcrypt
import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z\s]+$')
PWD_REGEX = re.compile(r'^[a-zA-Z0-9]+$')
##=========================================================================##
##                  Login and Registration validations                     ##
##=========================================================================##

class UserManager(models.Manager):
    def validateRegisterData(self,postData):
        errors = {}

        try:
            name = postData['name']
            alias = postData['alias']
            email = postData['remail']
            password = postData['rpassw']
            cpassword = postData['cpassw']
            dob = postData['dob']
            today = datetime.date.today()
            date = datetime.datetime.strptime(dob,'%Y-%m-%d')
        except:
            return {"blank": '* All fields required'}

        if not name or not alias or not email or not password or not cpassword or not dob:
            errors['blank'] = '* All fields required'

        else:
            if len(name) < 2 or len(alias) < 2 :
                errors['name'] = '* Names should be at least 2 characters'
            elif not NAME_REGEX.match(name) or not NAME_REGEX.match(alias):
                errors['name'] = '* Names should contain only alphabets'

            if not EMAIL_REGEX.match(email):
                errors['email'] = '* Invalid Email Address'

            if len(password) < 8 :
                errors['password'] =  '* Password should be atleast 8 characters'
            elif (cpassword != password) :
                errors['password'] =  '* Passwords are not matching'
            
            if dob == 'yyyy-mm-dd' :
                errors['dob'] =  '* enter your date of birth'

            elif date.year == int(today.strftime("%Y")) and date.day == int(today.strftime("%d")) and date.month == int(today.strftime("%m")) : 
                errors['dob'] =  "* date of birth cannot be today's date"
            
            elif date.year >= int(today.strftime("%Y")) and date.day >= int(today.strftime("%d")) and date.month >= int(today.strftime("%m")) : 
                errors['dob'] =  "* date of birth cannot be future date"

            if not errors:
                users = User.objects.filter(email=email)
                if users:
                    errors['email'] =  '* Email already exists. Please try another valid email'
        
        return errors
    
    def registerData(self,postData):
        try:
            name = postData['name']
            alias = postData['alias']
            email = postData['remail']
            password = postData['rpassw']
            dob = postData['dob']
        except:
            return False

        hashpwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return User.objects.create(name=name, alias=alias, email=email, password=hashpwd,dob=dob)

    def validateLogin(self,postData):
        errors = {}
        try:
            email = postData['lemail']
            password = postData['lpassw']
        except:
            return False

        if len(email) < 1:
            errors['lemail'] = '* Enter your login email'
        elif not EMAIL_REGEX.match(email):
            errors['lemail'] = '* Invalid email address'
        
        if len(password) < 1 :
            errors['lpassword'] = '* Please enter your password'

        return errors

    def validateLoginData(self,postData):
        try:
            email = postData['lemail']
            password = postData['lpassw']
            user = User.objects.get(email=email)
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                return user
        except:
            pass
        return False

    def get_user_postedQuotes(self,id):
        try:
            user_id=id

            user = User.objects.get(id=user_id)
            posted_quotes = Quote.objects.filter(posted_by=user.id)
            data = {
                "user" : user,
                "posted_quotes" : posted_quotes,
                "count" : len(posted_quotes)
            }
            print data
            return data
        except:
            return False

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.TextField()
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

##=========================================================================##
##                  Quotes Validations and models                          ##
##=========================================================================##

class QuoteManager(models.Manager):
    def validate_quotes_fields(self,postData):
        errors = {}

        try:
            quoted_by = postData['quoted_by']
            message = postData['message']

        except:
            return {"blank": '* Both fields required'}

        if not quoted_by or not message :
            errors['blank'] = '* Both fields required'

        else:
            if len(quoted_by) < 3 :
                errors['quoted_by'] = '* Quoter Name should be more than 3 characters'
            if len(message) < 10 :
                errors['message'] = '* Quotes should be  more than 10 characters'        
        return errors

    def add_quotes_data(self,postData,id):
        try:
            quoted_by = postData['quoted_by']
            message = postData['message']
            user_id = id
        except:
            return False
        if not user_id:
            return false
        else:
            user = User.objects.get(id=user_id)
            quote = Quote.objects.create(quoted_by=quoted_by, message=message,posted_by=user)
            return quote
    
    def add_quotes_fav(self,id,user_id):
        try:
            quote_id = id
            quote = Quote.objects.get(id=quote_id)
            user = User.objects.get(id=user_id)
            user.favorite_quotes.add(quote)
            return True
        except:
            return False
    
    def rem_quotes_fav(self,id,user_id):
        try:
            quote_id = id
            quote = Quote.objects.get(id=quote_id)
            user = User.objects.get(id=user_id)
            user.favorite_quotes.remove(quote)
            return True
        except:
            return False
    
    def get_quotes_fav(self,user_id):
        try:
            user = User.objects.get(id=user_id)
            fav_quotes = user.favorite_quotes.all()
            return fav_quotes
        except:
            return False
    

class Quote(models.Model):
    quoted_by = models.CharField(max_length=255)
    message = models.TextField()
    posted_by = models.ForeignKey(User,related_name="quotes")
    user_fav = models.ManyToManyField(User,related_name="favorite_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()
