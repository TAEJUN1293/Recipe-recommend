from django.shortcuts import render, get_object_or_404
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
        tmp['name'] = food['recipe_name']
        
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
        tmp['id'] = food['id']
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

def withs(request, food_id):
    food = Food.objects.get(id=food_id)

    food = food.__dict__

    result = {}
    result['name'] = food['recipe_name']
    result['id'] = food_id
    
    result['date'] = food['created_date'].strftime('%Y-%m-%d')
    if food['data_source'] == 'youtube':
        try:
            video_meta = re.search('vi(.+?)hqdefault', food['food_img']).group(1)
            result['img'] = 'https://img.youtube.com/vi' + video_meta + 'sddefault.jpg'
        except:
            result['img'] = None
    else:
        result['img'] = food['food_img']
    if food['data_source'] == 'API':
        result['url'] = None
    else:
        result['url'] = food['recipe_link']
    result['views'] = food['views']
    result['likes'] = food['likes']
    result['rating'] = str(round((food['rating'] * 100), 2)) + '%'
    result['answer'] = food['static_food_name']
    result['comments'] = food['comments']
    result['category_type'] = food['category_type_level']
    result['category_situation'] = food['category_situation_level']
    result['category_ingredient'] = food['category_ingredient_level']
    result['category_method'] = food['category_method_level']

    rel = []
    for i in range(1,11):
        tmp = {}
        tmp['id'] = food[f'음식{i}_id']
        try:
            now = Food.objects.get(category_id=tmp['id'])
            now = now.__dict__
            tmp['id'] = now['id']
            tmp['name'] = now['recipe_name']
        
            tmp['date'] = now['created_date'].strftime('%Y-%m-%d')
            if now['data_source'] == 'youtube':
                try:
                    video_meta = re.search('vi(.+?)hqdefault', now['food_img']).group(1)
                    tmp['img'] = 'https://img.youtube.com/vi' + video_meta + 'sddefault.jpg'
                except:
                    tmp['img'] = None
            else:
                tmp['img'] = now['food_img']
            if now['data_source'] == 'API':
                tmp['url'] = None
            else:
                tmp['url'] = now['recipe_link']
            tmp['answer'] = now['static_food_name']
            tmp['category_type'] = now['category_type_level']
            tmp['category_situation'] = now['category_situation_level']
            tmp['category_ingredient'] = now['category_ingredient_level']
            tmp['category_method'] = now['category_method_level']
            rel.append(tmp)
        except:
            pass

    context = {'heads' : head_set('어울리는요리'), 'result' : result, 'rel': rel}
    return render(request, 'main/withs.html', context=context)

def head_set(tag):
    heads = [{'tag' : '홈', 'now' : False, 'url' : '/'}, 
             {'tag' : '요리추천', 'now' : False, 'url' : '/recommend'}, 
             {'tag' : '어울리는요리', 'now' : False, 'url' : '/'}]
    for head in heads:
        if head['tag'] == tag:
            if tag == '홈':
                head['url'] = ''
            head['now'] = True
    return heads
