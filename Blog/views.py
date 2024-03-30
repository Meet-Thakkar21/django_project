from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate,login,logout
from .models import BlogPost,User,Category,Like,Comment
from datetime import datetime
from django.db.models import Count


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
            return redirect('/home')
        else: 
            return HttpResponse ("Username or Password is incorrect!!!")
    else:
      return render (request,'login.html')

def home(request):
  name={'username': request.session.get('username')}
  blogs=BlogPost.objects.all()
  user=User.objects.get(username=request.session.get('username'))
  my_blogs = BlogPost.objects.filter(UserID=user)
  other_blogs = blogs.exclude(pk__in=my_blogs.values_list('pk', flat=True))
  user_has_liked_blog_ids = {}
  if user.is_authenticated:
      user_has_liked_blog_ids = Like.objects.filter(UserID=user).values_list('BlogID', flat=True)

  other_blogs_with_counts = other_blogs.annotate(
        likes_count=Count('like'),
        comments_count=Count('comment')
    )  
  context = {
      'name': request.user,  
      'blogs': other_blogs_with_counts,
      'user_has_liked_blog_ids': user_has_liked_blog_ids
  }
  return render(request, 'home.html', context)
  

def logout_request(request):
  logout(request)
  request.session.flush()
  return redirect('/login')

from datetime import datetime 

def create_blog_post(request):
    if request.method == 'POST':
        title = request.POST.get('Title')
        blog_data = request.POST.get('BlogData')
        category_id = request.POST.get('CategoryId')
        category = Category.objects.get(CategoryId=category_id)

        user = User.objects.get(username=request.session.get('username'))

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

        return redirect('/home')  
    else:
        category = Category.objects.all()
        return render(request, 'create_blog_post.html', {'category': category})


def myallblogs(request):
  blogs=BlogPost.objects.all()
  user=User.objects.get(username=request.session.get('username'))
  my_blogs = BlogPost.objects.filter(UserID=user)
  my_blogs_with_like_count = my_blogs.annotate(likes_count=Count('like'))
  return render(request,'Myblogs.html',{'my_blogs' :my_blogs_with_like_count})


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


def like_blog(request, pk):
    current_datetime = datetime.now()
    blog = BlogPost.objects.get(BlogId = pk)
    user = User.objects.get(username=request.session.get('username'))
    like = Like.objects.create(
        DateLiked=current_datetime,
        UserID = user,
        BlogID = blog
    )
    blog.Likes = blog.Likes + 1
    blog.save()
    return redirect('home')
  
def remove_like(request,pk):
  blog = BlogPost.objects.get(BlogId = pk)
  user = User.objects.get(username=request.session.get('username'))
  like = Like.objects.get(BlogID = blog, UserID = user)
  like.delete()
  blog.Likes = blog.Likes - 1
  blog.save()
  return redirect('home')

def add_comment(request ,pk):
  if request.method == 'POST':
        content = request.POST.get('content')
        blog = BlogPost.objects.get(BlogId = pk)
        user = User.objects.get(username=request.session.get('username'))

        comment = Comment.objects.create(
            DatePosted=datetime.now(),
            Content=content,
            UserID=user,
            BlogID=blog
        )
        blog.Comments += 1
        blog.save()
        return redirect('home')  # Redirect to the home page after adding the comment
  else:
      return redirect('home')
  
def get_comments(request):
    if request.method == 'GET' and 'blog_id' in request.GET:
          blog_id = request.GET['blog_id']
          print(blog_id)
          blog = BlogPost.objects.get(BlogId = blog_id)
          comments = Comment.objects.filter(BlogID=blog)
          comments_data = [{'Content': comment.Content, 'username' : comment.UserID.username, 'commentId' : comment.CommentId} for comment in comments]
          print(comments_data)
          return JsonResponse({'comments': comments_data})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
def delete_comment(request, blog_id, comment_id):   
   if request.method == 'GET':
        try:
            comment = Comment.objects.get(CommentId=comment_id, BlogID=blog_id)
            comment.delete()
            
            blog = BlogPost.objects.get(BlogId=blog_id)
            blog.Comments -= 1
            blog.save()
            return JsonResponse({'message': 'Comment deleted successfully'}, status=200)
        except Comment.DoesNotExist:
            return JsonResponse({'error': 'Comment does not exist'}, status=404)
   else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)