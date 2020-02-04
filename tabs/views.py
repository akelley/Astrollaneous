from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from tabs.forms import MarsForm, NasaForm
import datetime, requests, random

API_KEY = "suY5NhcHycX1CIkDaMCXNdY8dIYdp0O5meo3cJso"

def home(request):
    video_url = None
    image_url = None
    image_hdurl = None
    copyright = 'NASA'
    response = requests.get('https://api.nasa.gov/planetary/apod?api_key=' + API_KEY)
    daily_image_data = response.json()

    if 'code' in daily_image_data and daily_image_data['code'] >= 400:
        context = {
            "home_page": "active",
            "date": datetime.date.today(),
            "title": "Chandra Spots a Mega-Cluster of Galaxies in the Making ",
            "description": "Astronomers using data from NASA's Chandra X-ray Observatory and other telescopes have put together a detailed map of a rare collision between four galaxy clusters. Eventually all four clusters — each with a mass of at least several hundred trillion times that of the Sun — will merge to form one of the most massive objects in the universe. Galaxy clusters are the largest structures in the cosmos that are held together by gravity. Clusters consist of hundreds or even thousands of galaxies embedded in hot gas, and contain an even larger amount of invisible dark matter. Sometimes two galaxy clusters collide, as in the case of the Bullet Cluster, and occasionally more than two will collide at the same time. The new observations show a mega-structure being assembled in a system called Abell 1758, located about 3 billion light-years from Earth. It contains two pairs of colliding galaxy clusters that are heading toward one another. Scientists first recognized Abell 1758 as a quadruple galaxy cluster system in 2004 using data from Chandra and XMM-Newton, a satellite operated by the European Space Agency (ESA). Each pair in the system contains two galaxy clusters that are well on their way to merging. In the northern (top) pair seen in the composite image, the centers of each cluster have already passed by each other once, about 300 to 400 million years ago, and will eventually swing back around. The southern pair at the bottom of the image has two clusters that are close to approaching each other for the first time.",
            "image_url": '/static/mySpaceStuff/img/backup_image.jpg',
            "image_hdurl": '/static/mySpaceStuff/img/backup_image_large.jpg',
            "copyright": "X-ray: NASA/CXC/SAO/G.Schellenberger et al.; Optical:SDSS"
        }
        return render(request, 'tabs/index.html', context)

    else:
        if daily_image_data['media_type'] == 'video':
            video_url = daily_image_data['url']
            temp = video_url.split("embed/", 1)[1].split('?')
            image_url = 'http://img.youtube.com/vi/' + temp[0] + '/0.jpg'
        else:
            image_url = daily_image_data['url']
            image_hdurl = daily_image_data['hdurl']

            if hasattr(daily_image_data, 'copyright'):
                copyright = daily_image_data['copyright']

        context = {
            "home_page": "active",
            "date": datetime.date.today(),
            "title": daily_image_data['title'],
            "description": daily_image_data['explanation'],
            "media_type": daily_image_data['media_type'],
            "video_url": video_url,
            "image_url": image_url,
            "image_hdurl": image_hdurl,
            "copyright": copyright
        }
        return render(request, 'tabs/index.html', context)

def mars(request):
    context = {}
    rovers = []
    rover_names = ['curiosity', 'spirit', 'opportunity']
    base_url = "https://api.nasa.gov/mars-photos/api/v1/manifests/"

    for rover in rover_names:
        response = requests.get(base_url + rover + '?api_key=' + API_KEY)
        rover_data = response.json()
        launch_date_time_obj = datetime.datetime.strptime(rover_data['photo_manifest']['launch_date'], '%Y-%m-%d')
        landing_date_time_obj = datetime.datetime.strptime(rover_data['photo_manifest']['landing_date'], '%Y-%m-%d')
        max_date_time_obj = datetime.datetime.strptime(rover_data['photo_manifest']['max_date'], '%Y-%m-%d')
        rover_object = {
            "name": rover_data['photo_manifest']['name'],
            "launch_date": launch_date_time_obj,
            "landing_date": landing_date_time_obj,
            "max_date": max_date_time_obj,
            "status": rover_data['photo_manifest']['status'],
            "total_photos": rover_data['photo_manifest']['total_photos']
        }
        rovers.append(rover_object)

    return render(request, 'tabs/mars.html', {"rovers": rovers})

def rover(request, rover_name):
    cameras = []
    base_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/"
    response = response = requests.get(base_url + rover_name + '/?api_key=' + API_KEY)
    rover_data = response.json()

    landing_date_time_obj = datetime.datetime.strptime(rover_data['rover']['landing_date'], '%Y-%m-%d')
    max_date_time_obj = datetime.datetime.strptime(rover_data['rover']['max_date'], '%Y-%m-%d')
    camera_data = rover_data['rover']['cameras']
    for camera in camera_data:
        camera_object = {camera['name']: camera['full_name']}
        cameras.append(camera)

    rover_object = {
        "rover_name": rover_name,
        "landing_date": landing_date_time_obj,
        "max_date": max_date_time_obj,
        "max_sol": rover_data['rover']['max_sol'],
        "status": rover_data['rover']['status'],
        "total_photos": rover_data['rover']['total_photos'],
        "cameras": cameras
    }

    return render(request, 'tabs/rover.html', {"rover": rover_object})

def search(request, rover_name):
    if request.method == 'POST':
        form = MarsForm(request.POST)
        if form.is_valid():
            date = request.POST.get('earth_date_selector')
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')
    else:
        form = MarsForm()

    return render(request, 'tabs/rover.html', {'rover_name': rover_name, 'form': form})

def neos(request):
    context = {"neos_page": "active"}
    return render(request, 'tabs/neos.html', context)

def satellites(request):
    context = {"satellites_page": "active"}
    return render(request, 'tabs/satellites.html', context)

def weather(request):
    data = []
    base_url = "https://api.nasa.gov/insight_weather"
    response = response = requests.get(base_url + '/?api_key=' + API_KEY + '&feedtype=json')
    weather_data = response.json()

    context = {"weather_page": "active", "weather_data": weather_data}
    return render(request, 'tabs/weather.html', context)

def nasa(request):
    collection = []

    if request.method == "POST":
        form = NasaForm(request.POST)
        if form.is_valid():
            query_term = form.cleaned_data['query_term']
            response = requests.get('https://images-api.nasa.gov/search?q=' + query_term)
            # response_data = response.json()

            # collection.append(response_data)

            # for item in response_data.collection.items:
            #     if item.data[0].media_type == 'video':
            #         data1 = json.load(item.href)
            #         data2 = json.dumps(data1)
            #         collection.append(data2)
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # NOTE: I'm forgoing the redirect AND the else case
            # since I always want a fresh form passed
            # if the form is valid, then appropriate context data is returned as well

    form = NasaForm()
    context = {"nasa_page": "active", "nasa_data": collection}
    return render(request, 'tabs/nasa.html', {'form': form, 'context': context})

def techport(request):
    data = []
    now = datetime.datetime.now()
    past_date_time = datetime.datetime(2019, now.month, now.day)
    past_date_time_string = past_date_time.strftime("%Y-%m-%d")

    base_url = "https://api.nasa.gov/techport/api/projects?updatedSince="
    response = response = requests.get(base_url + past_date_time_string + '&api_key=' + API_KEY)
    techport_data = response.json()

    context = {"techport_page": "active", "techport_data": techport_data}
    return render(request, 'tabs/techport.html', context)

def techport_search(request, project_id):
    base_url = "https://api.nasa.gov/techport/api/projects/"
    response = response = requests.get(base_url + str(project_id) + '?api_key=' + API_KEY)
    techport_search_data = response.json()
    context = {"techport_search_data": techport_search_data}
    return render(request, 'tabs/techport_search.html', context)
