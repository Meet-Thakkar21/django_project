from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate,login,logout
from .models import BlogPost,Blogger,User,Category
from datetime import datetime
# Create your views here.
def register(request):
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect("/login")
  else:
    form = UserRegistrationForm()
  return render(request,"signup.html", {'form':form})

def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            request.session['username'] = user.username
            request.session['email'] = user.email
            request.session['first_name'] = user.first_name
            request.session.save() 
            
            name={
                'username': request.session.get('username')
            }
            return render(request,'home.html',{'name':name})
        else: 
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def home(request):
   name={'username': request.session.get('username')}
   blogs=BlogPost.objects.all()
   user=User.objects.get(username=request.session.get('username'))
   my_blogs = BlogPost.objects.filter(UserID=user)
   other_blogs = blogs.exclude(pk__in=my_blogs.values_list('pk', flat=True))
   return render(request,'home.html',{'name':name , 'blogs': other_blogs})
  

def logout_request(request):
  logout(request)
  request.session.flush()
  return redirect('/login')

from datetime import datetime  # Import datetime module

def create_blog_post(request):
    if request.method == 'POST':
        title = request.POST.get('Title')
        blog_data = request.POST.get('BlogData')
        category_id = request.POST.get('CategoryId')
        category = Category.objects.get(CategoryId=category_id)

        user = User.objects.get(username=request.session.get('username'))

        # Get current date and time
        current_datetime = datetime.now()

        blog_post = BlogPost.objects.create(
            Title=title,
            BlogData=blog_data,
            DatePosted=current_datetime,  
            Likes=0,
            Comments=0,
            UserID=user,
            CategoryId=category
        )
        # blog_post.save()

        return redirect('/home')  
    else:
        category = Category.objects.all()
        return render(request, 'create_blog_post.html', {'category': category})


def myallblogs(request):
   blogs=BlogPost.objects.all()
   user=User.objects.get(username=request.session.get('username'))
   my_blogs = BlogPost.objects.filter(UserID=user)
   return render(request,'Myblogs.html',{'my_blogs' :my_blogs})


def update_blog(request,pk):
    if request.method == 'POST':
      blog = BlogPost.objects.get(BlogId=pk)
      blog.Title = request.POST.get('Title')
      blog.BlogData = request.POST.get('BlogData')
      category_id = request.POST.get('CategoryId')
      category = Category.objects.get(CategoryId=category_id)
      blog.CategoryId = category
      blog.save()
      return redirect('myallblogs')
    else:
      category = Category.objects.all()
      blog = BlogPost.objects.get(BlogId = pk)
      return render(request,"update.html", {'blog' : blog , 'category' : category})
    
def delete_blog(request,pk):
    blog = BlogPost.objects.get(BlogId = pk)
    if request.method == 'POST':
     blog.delete()
     return redirect('myallblogs')  
    
    else:
     return render(request, 'confirm_delete.html', {'blog': blog})
