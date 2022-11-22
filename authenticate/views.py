
from django.shortcuts import render, redirect

from django.contrib.auth import logout, login
from django.contrib.auth.models import User, auth
from .models import UserData, Tasks, PhotoData, Tags, Phototag
from datetime import datetime

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['email']
            password = request.POST.get('pwd')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'index.html')
        else:
            return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('index')


def home(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        if request.method == 'GET' and 'task_status' in request.GET:
            task_stat = request.GET['task_status']
            if task_stat == 'AC':
                request.session['task_status'] = 'AC'
            elif task_stat == 'CO':
                request.session['task_status'] = 'CO'
            else:
                request.session['task_status'] = ''
        if Tasks.objects.filter(username__pk=user_id):
            tasks = Tasks.objects.filter(username=UserData.objects.get(pk=user_id))
        else:
            tasks = None
        if tasks is not None:
            return render(request, 'home.html', {'task': tasks})
        else:
            return render(request, 'home.html', {'task': None})
    else:
        return redirect('index')


def register(request):
    if request.method == 'POST':
        username = request.POST['user_name']
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        profilepic = request.FILES['profilepic']
        if pass1 == pass2:
            user = User.objects.create_user(username=username, password=pass1, email=email)
            userdata = UserData(username=username, firstname=firstname, lastname=lastname, email=email, profilepic=profilepic)
            user.save()
            userdata.save()
            return render(request, 'index.html')
        else:
            print('password not same')
            return render(request, 'register.html')
    else:
        return render(request, 'register.html')


def createteask(request):
    if request.method == 'POST':
        task_name = request.POST['task_name']
        username = request.user.id
        task = Tasks(username=UserData.objects.get(pk=username), task_name=task_name)
        task.save()
        return redirect('home')
    else:
        return render(request, 'createTask.html')


def completetask(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            if 'id' in request.GET:
                id = request.GET['id']
                task = Tasks.objects.get(pk=int(id))
                task.task_status = 'CO'
                task.save()
                return redirect('home')
            else:
                return redirect('home')
        else:
            return redirect('home')
    else:
        return redirect('index')

def deletetask(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            if 'id' in request.GET:
                id = request.GET['id']
                task = Tasks.objects.get(pk=int(id))
                task.delete()
                return redirect('home')
            else:
                return redirect('home')
        else:
            return redirect('home')
    else:
        return redirect('index')


def deletealltasks(request):
    if request.user.is_authenticated:
        Tasks.objects.filter(task_status='CO').delete()
        return redirect('home')
    else:
        return redirect('index')


def profile(request):
    if request.user.is_authenticated:
        user_id = request.user.username
        data = UserData.objects.get(username=user_id)

        return render(request, 'profile.html', {'user_data': data})
    else:
        return redirect('index')
    # if request.method == 'POST':


def photogrid(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            tag = request.POST['search']
            tag_photos = Phototag.objects.filter(tag__name__icontains=tag)

            ids = []
            for i in tag_photos:
                ids.append(i.photo.id)
            photos = PhotoData.objects.filter(id__in=ids)
            return render(request, 'photogrid.html', {'photos': photos, 'search':tag})
        else:
            user_id = request.user.username
            user_obj = UserData.objects.get(username=user_id)
            photo = PhotoData.objects.filter(username=user_obj).order_by('-upload_date')
            return render(request, 'photogrid.html', {'photos': photo})
    else:
        return redirect('index')


def addimage(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            img = request.FILES['photo']
            tags = request.POST['tags']
            split_tags = tags.split(', ')
            usr = UserData.objects.get(username=request.user.username)
            img_obj = PhotoData(username=usr, photo=img)
            img_obj.save()
            for tag in split_tags:
                is_exist = Tags.objects.filter(name=tag).exists()
                if not is_exist:
                    new_tag = Tags(name=tag)
                    new_tag.save()
                else:
                    new_tag = Tags.objects.get(name=tag)
                PhotoTag = Phototag(tag=new_tag, photo=img_obj)
                PhotoTag.save()
            return redirect('photogrid')
        else:
            return render(request, 'addimage.html')


def deletephoto(request,photoid):
    if request.user.is_authenticated:
        photo_obj = PhotoData.objects.get(id=photoid)
        phototags = Phototag.objects.filter(photo=photo_obj)
        for i in phototags:
            i.delete()
        photo_obj.delete()
        return redirect('photogrid')
    else:
        return redirect('index')


def editphoto(request, photoid):
    if request.user.is_authenticated:
        if request.method == 'POST':

            tags = request.POST['tags']
            tags = tags.split(', ')
            tags_to_be_deleted = Phototag.objects.filter(photo__id = photoid)
            img_obj = PhotoData.objects.get(id=photoid)
            for i in tags_to_be_deleted:
                i.delete()
            for tag in tags:
                is_exist = Tags.objects.filter(name=tag).exists()
                if not is_exist:
                    new_tag = Tags(name=tag)
                    new_tag.save()
                else:
                    new_tag = Tags.objects.get(name=tag)

                PhotoTag = Phototag(tag=new_tag, photo=img_obj)
                PhotoTag.save()
            if len(request.FILES) != 0:
                img_obj.photo = request.FILES['newphoto']
                img_obj.upload_date = datetime.now()
                img_obj.save()
            return redirect('photogrid')
        else:
            photo_obj = PhotoData.objects.get(id=photoid)
            tags = Phototag.objects.filter(photo=photo_obj)
            all_tags = ""
            for i in tags:
                if(all_tags == ""):
                    all_tags = all_tags + i.tag.name
                else:
                    all_tags = all_tags + ', '+ i.tag.name
            return render(request, 'editimage.html', {'photo':photo_obj, 'tag':all_tags})

    else:
        return redirect('index')