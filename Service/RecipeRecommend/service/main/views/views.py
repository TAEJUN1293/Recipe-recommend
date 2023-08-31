from django.shortcuts import render
from ..models import Food
import datetime
import re

# Create your views here.
from django.http import HttpResponse

def index(request):
    context = {'heads' : head_set('홈')}
    dropdown = []
    if request.path == '/views/':
        context['filter'] = {"url" : '/views/', 'name' : '조회순'}
        foods_model = Food.objects.order_by('-views').values()[:18]
        dropdown.append({"url" : '/', 'name' : '인기순'})
        dropdown.append({"url" : '/recent/', 'name' : '최신순'})
        dropdown.append({"url" : '/prefer/', 'name' : '선호순'})
    elif request.path == '/recent/':
        context['filter'] = {"url" : '/recent/', 'name' : '최신순'}
        foods_model = Food.objects.order_by('-created_date').values()[:18]
        dropdown.append({"url" : '/', 'name' : '인기순'})
        dropdown.append({"url" : '/views/', 'name' : '조회순'})
        dropdown.append({"url" : '/prefer/', 'name' : '선호순'})
    elif request.path == '/prefer/':
        context['filter'] = {"url" : '/prefer/', 'name' : '선호순'}
        foods_model = Food.objects.order_by('-likes').values()[:18]
        dropdown.append({"url" : '/', 'name' : '인기순'})
        dropdown.append({"url" : '/recent/', 'name' : '최신순'})
        dropdown.append({"url" : '/views/', 'name' : '조회순'})
    else:
        context['filter'] = {'url' : '/', 'name' : '인기순'}
        foods_model = Food.objects.order_by('-rating').values()[:18]
        dropdown.append({"url" : '/views/', 'name' : '조회순'})
        dropdown.append({"url" : '/recent/', 'name' : '최신순'})
        dropdown.append({"url" : '/prefer/', 'name' : '선호순'})
    carousel = []
    card = []
    for i, food in enumerate(foods_model):
        tmp = {}
        if i == 0:
            tmp['best'] = True
        else:
            tmp['best'] = False
        tmp['name'] = food['food_name']
        
        tmp['date'] = food['created_date'].strftime('%Y-%m-%d')
        if food['data_source'] == 'youtube':
            try:
                video_meta = re.search('vi(.+?)hqdefault', food['food_img']).group(1)
                tmp['img'] = 'https://img.youtube.com/vi' + video_meta + 'sddefault.jpg'
            except:
                tmp['img'] = None
        else:
            tmp['img'] = food['food_img']
        tmp['url'] = food['recipe_link']
        if i <3:
            carousel.append(tmp)
        else:
            card.append(tmp)
    
    context['carousel'] = carousel
    context['card'] = card
    context['dropdown'] = dropdown

    return render(request, 'main/index.html', context=context)

def recommend(request):
    context = {'heads' : head_set('요리추천')}
    return render(request, 'main/recommend.html', context=context)

def withs(request):
    context = {'heads' : head_set('어울리는 요리')}
    return render(request, 'main/index.html', context=context)

def head_set(tag):
    heads = [{'tag' : '홈', 'now' : False, 'url' : '/'}, 
             {'tag' : '요리추천', 'now' : False, 'url' : '/recommend'}, 
             {'tag' : '어울리는 요리', 'now' : False, 'url' : '/with'}]
    for head in heads:
        if head['tag'] == tag:
            if tag == '홈':
                head['url'] = ''
            head['now'] = True
    return heads
