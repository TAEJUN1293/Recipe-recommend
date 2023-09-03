from django.shortcuts import render
from service.main.models import Food
import json
from django.http import JsonResponse
from django.db.models import Q
import re
import numpy as np

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
        if food['data_source'] == 'API':
            tmp['url'] = None
        else:
            tmp['url'] = food['recipe_link']
        tmp['id'] = food['id']
        result.append(tmp)

    return result


def boxplot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            if isinstance(data, list):
                result = make_boxplot(data[0])
                
                response_data = {'message': '데이터를 성공적으로 처리했습니다.', "result":result}
                return JsonResponse(response_data)
            else:
                return JsonResponse({'error': '요청에 필요한 키가 누락되었습니다.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': '잘못된 JSON 데이터입니다.'}, status=400)
    else:
        return JsonResponse({'error': '올바른 HTTP 메서드가 아닙니다.'}, status=405)

def make_boxplot(id):
    values = ['rating', 'views']
    food = Food.objects.get(id=id)
    food = food.__dict__

    if food['data_source'] == 'API':
        return {}
    
    boxes = []
    for ele in values:
        tmp = {}
        if ele == 'rating':
            tlst = list(Food.objects.exclude(data_source='API').order_by(ele).values_list(ele))
            lst = [float(item[0]) for item in tlst]
            food_val = int(food[ele] * 100)
        else:
            tlst = list(Food.objects.filter(data_source='youtube').values_list(ele))
            y_lst = [float(item[0]) for item in tlst]
            klst = list(Food.objects.filter(data_source='website').values_list(ele))
            w_lst = [float(item[0]) for item in klst]
            if food['data_source'] == 'youtube':
                food_val = int(((food[ele] - min(y_lst)) / (max(y_lst) - min(y_lst))) * 100)
            elif food['data_source'] == 'website':
                food_val = int(((food[ele] - min(w_lst)) / (max(w_lst) - min(w_lst))) * 100)
            y_lst = min_max_normalize(y_lst, ele)
            w_lst = min_max_normalize(w_lst, ele)
            lst = sorted(y_lst + w_lst)

        mini = int(lst[0] * 100)
        q1 = int(np.percentile(lst, 25) * 100)
        q2 = int(np.percentile(lst, 50) * 100)
        q3 = int(np.percentile(lst, 75) * 100)
        maxi = int(lst[-1] * 100)
        tmp['mini'] = mini
        tmp['q1'] = q1
        tmp['q2'] = q2
        tmp['q3'] = q3
        tmp['maxi'] = maxi
        tmp['food_val'] = food_val
        boxes[ele] = tmp
    return boxes


            
def min_max_normalize(input_list, ele):
    min_val = min(input_list)
    max_val = max(input_list)
    
    
    normalized_list = []

    for value in input_list:
        normalized_value = (value - min_val) / (max_val - min_val)
        normalized_list.append(normalized_value)

    return normalized_list