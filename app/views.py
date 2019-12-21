from django.shortcuts import render, Http404, get_object_or_404, redirect
from .models import Board, Post, Topic
from django.contrib.auth.models import User
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import View, CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone


# Create your views here.
def index(req):
    board = Board.objects.all()
    return render(req, 'index.html', {'board':board})



def boardTopic(req,pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(req, 'topics.html', {'board':board, 'topics':topics})

@login_required
def newTopic(req,pk):
    board = get_object_or_404(Board, pk=pk)
    # user = User.objects.first()
    
    if req.method == 'POST':
        form = NewTopicForm(req.POST)

        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.startedBy = req.user
            topic.save()
            
            post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                topic = topic,
                created_by = req.user
            )

            return redirect('topics_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()

    return render(req, 'newTopic.html',{'board':board, 'form':form})

def topics_post(req,pk,topic_pk):
    topic = get_object_or_404(Topic,board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(req, 'topics_posts.html', {'topic':topic})

@login_required
def reply_topic(req,pk,topic_pk):
    topic = get_object_or_404(Topic,board__pk=pk, pk=topic_pk)
    if req.method == 'POST':
        form = PostForm(req.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = req.user
            post.save()
            return redirect('topics_posts',pk=pk,topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(req, 'reply_topic.html', {'topic':topic,'form':form})

@login_required
def home(request):
    return render(request, 'home.html')

# class NewPostView(View):
#     def post(self,req):
#         form= PostForm(req.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('post_list')
#         return render(req, 'new_post.html', {'form':form})

#     def get(self,req):
#         form= PostForm()
#         return render(req,'new_post.html', {'form':form})


#Generic class based views

class NewPostView(CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('post_list')
    template_name = "new_post.html"


class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name= 'post'

    def form_valid(self,form):
        post = form.save(commit= False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topics_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)