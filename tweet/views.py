from django.shortcuts import get_object_or_404,redirect,render
from django.http import JsonResponse
from .forms import *
from .models import Tweet
from django.contrib.auth.decorators import *
from django.contrib.auth import login

def index(request):
    return render(request , 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by("-created_at")
    return render(request,'tweet_list.html',{'tweets': tweets})

@login_required()
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForms(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user  
            tweet.save()
            return redirect('tweet_list')  
    else:
        form = TweetForms() 
    return render(request, 'tweet_form.html', {'form': form})


@login_required()
def tweet_edit(request , tweet_id):
    tweet = get_object_or_404(Tweet,pk=tweet_id , user=request.user)
    if request.method == 'POST' :  
        form = TweetForms(request.POST,request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit = False)
            tweet.user = request.user 
            tweet.save()
            return redirect('tweet_list')
    else: 
        form = TweetForms(instance=tweet)
    return render(request, 'tweet_form.html',{'form':form})

@login_required()
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet , pk = tweet_id , user = request.user)
    if request.method == "POST":
        tweet.delete()
        return redirect('tweet_list')
    return render(request , 'tweet_confirm_delete.html' , {'tweet':tweet})

def register(request):
    if request.method == 'POST':
        form = UserRegisterationform(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect("tweet_list")
    else:
        form = UserRegisterationform()
    return render(request,'registration/register.html',{'form':form})


def search_dropdown(request):
    query = request.GET.get('q', '')
    if query:
        results = Tweet.objects.filter(text__icontains=query)[:10] 
        results_list = [{'id': tweet.id, 'text': tweet.text[:50]} for tweet in results]  
    else:
        results_list = []

    return JsonResponse(results_list, safe=False)
def tweet_detail(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    return render(request, 'tweet_detail.html', {'tweet': tweet})