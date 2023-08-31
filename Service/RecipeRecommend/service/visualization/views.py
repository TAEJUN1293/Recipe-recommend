from django.shortcuts import render
from service.main.models import Food
import json
from django.http import JsonResponse
from django.db.models import Q
import re

# Create your views here.

def find(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            if isinstance(data, list):
                result = findFoods(data)
                
                response_data = {'message': '데이터를 성공적으로 처리했습니다.', "result":result}
                return JsonResponse(response_data)
            else:
                return JsonResponse({'error': '요청에 필요한 키가 누락되었습니다.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': '잘못된 JSON 데이터입니다.'}, status=400)
    else:
        return JsonResponse({'error': '올바른 HTTP 메서드가 아닙니다.'}, status=405)

def findFoods(tags):
    foods = Food.objects
    for tag in tags:
        query = Q(재료1__icontains=tag) | \
                Q(재료2__icontains=tag) | \
                Q(재료3__icontains=tag) | \
                Q(재료4__icontains=tag) | \
                Q(재료5__icontains=tag) | \
                Q(재료6__icontains=tag) | \
                Q(재료7__icontains=tag) | \
                Q(재료8__icontains=tag) | \
                Q(재료9__icontains=tag) | \
                Q(재료10__icontains=tag)
        foods = foods.filter(query)
    
    foods = foods.order_by('-rating').values()

    if len(foods) > 12:
        foods = foods[:12]
    
    result = []

    for food in foods:
        tmp = {}
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
        if food['data_source'] == 'API':
            tmp['url'] = None
        else:
            tmp['url'] = food['recipe_link']
        
        result.append(tmp)

    return result