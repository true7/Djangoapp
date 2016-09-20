from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, render_to_response, get_list_or_404
from django.utils import timezone
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import Post

today = timezone.now().date()


@login_required
def post_create(request):
    if not request.user.is_authenticated:
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        if instance.publish < today:
            instance.publish = today
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {"form": form,
               "foreword": "Create new Post!",
               "inset": "Create",
               }
    return render(request, "post_form.html", context)


def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if not request.user.is_authenticated:
        raise Http404
    context = {"title": instance.title, "instance": instance, "today": today}
    return render(request, "post_detail.html", context)


def post_edit(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)

    if not request.user.is_superuser and not instance.user == request.user:
        response = HttpResponse('You do not have permission!')
        response.status_code = 403
        return response

    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.publish < today:
            instance.publish = today
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {"title": instance.title, "instance": instance,
               "form": form, "foreword": "Edit this Post!",
               "inset": "Edit",
               }
    return render(request, "post_form.html", context)


def post_delete(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    context = {}
    context.update(csrf(request))
    context['instance'] = instance

    if not request.user.is_superuser and not instance.user == request.user:
        response = HttpResponse('You do not have permission!')
        response.status_code = 403
        return response

    if request.method == 'POST':
        instance.delete()
        return redirect('posts:list')
    return render_to_response('confirm_delete.html', context)

# now it's a class view - look at the urlconf file.
# def post_about(request):
    # content = {"info": "Brief About..."}
    # return render(request, "about.html", content)


def user_posts(request):
    context = {}
    if not request.user.is_authenticated:
        raise Http404
    queryset_list = Post.objects.filter(user=request.user.id)
    if not queryset_list.exists():
        context['foreword'] = "I have no posts yet."
        return render_to_response('message.html', context)

    paginator = Paginator(queryset_list, 5)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context['object_list'] = queryset
    context['foreword'] = "My posts ({})".format(request.user.username)
    context['page_request_var'] = page_request_var
    context['today'] = today
    return render_to_response('post_list.html', context)


def post_list(request):
    queryset_list = Post.objects.active() #.order_by("-timestamp")

    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__username__icontains=query)
            ).distinct()
    paginator = Paginator(queryset_list, 8) # Show 8 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {"object_list": queryset,
               "page_request_var": page_request_var,
               "today": today,
               "foreword": "Welcome to DjangoApp!"
               }
    return render(request, "post_list.html", context)