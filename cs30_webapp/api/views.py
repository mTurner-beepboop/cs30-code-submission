from django.shortcuts import render
from django.http.response import JsonResponse
from django.http import HttpRequest
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from api.models import FlatfileEntry, NavigationInfo, CalculationInfo, OtherInfo
from api.serializers import ApiSerializer, NavigationSerializer

@api_view(['GET','POST','DELETE'])
def entry_list(request):
    #GET list of entries, POST new entry, DELETE all entries
    if request.method == 'GET': #Retreive all entries or find entries by title
        entries = FlatfileEntry.objects.all()
        
        ref_num = request.GET.get('ref_num', None)
        if ref_num is not None:
            entries = entries.filter(ref_num__icontains=ref_num)
            
        api_serializer = ApiSerializer(entries, many=True)
        return JsonResponse(api_serializer.data, safe=False)
    elif request.method == 'POST': #Create and save new entry
        entry_data = request.data

        api_serializer = ApiSerializer(data=entry_data)
        if api_serializer.is_valid():
            api_serializer.save()
            return JsonResponse(api_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(api_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE': #Delete all entries - likely not needed in final implementation
        count = FlatfileEntry.objects.all().delete()
        #delete artifacts from nav, calc and other info
        NavigationInfo.objects.all().delete()
        CalculationInfo.objects.all().delete()
        OtherInfo.objects.all().delete()
        return JsonResponse({'message': '{} entires were deleted'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(['GET','PUT','DELETE'])
def entry_detail(request, pk):
    #find entry by id
    try:
        entry = FlatfileEntry.objects.get(pk=pk)
    except entry.DoesNotExist:
        return JsonResponse({'message': 'Entry not found'})
        
    #GET / PUT / DELETE entry
    if request.method == 'GET': #Gets entry by specified id
        api_serializer = ApiSerializer(entry)
        return JsonResponse(api_serializer.data)
    elif request.method == 'PUT': #Update an existing entry
        entry_data = request.data
        api_serializer = ApiSerializer(entry, data=entry_data)
        if api_serializer.is_valid():
            api_serializer.save()
            return JsonResponse(api_serializer.data)
        return JsonResponse(api_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE': #Deletes entry by id
        entry.delete()
        return JsonResponse({'message': 'Entry was deleted'}, status=status.HTTP_204_NO_CONTENT)
        
@api_view(['GET','POST'])
def categories(request):
    if request.method == 'GET': #Complete
        #Return a list of scopes
        dict_scope_list = list(NavigationInfo.objects.all().values('scope').distinct())
        scopes = []
        for dict in dict_scope_list:
            scopes.append(dict['scope'])
        return JsonResponse({'message':scopes})
    if request.method == 'POST':
        #Return list of possible levels
        path = request.data
        levels = ['scope','level1','level2','level3','level4','level5']
        nav_data = NavigationInfo.objects.all()
        i=0
        for level in levels:
            if level in path.keys():
                i+=1
                if level == 'scope':
                    nav_data = nav_data.filter(scope__exact=path[level])
                elif level == 'level1':
                    nav_data = nav_data.filter(level1__exact=path[level])
                elif level == 'level2':
                    nav_data = nav_data.filter(level2__exact=path[level])
                elif level == 'level3':
                    nav_data = nav_data.filter(level3__exact=path[level])
                elif level == 'level4':
                    nav_data = nav_data.filter(level4__exact=path[level])
                elif level == 'level5':
                    nav_data = nav_data.filter(level5__exact=path[level])
                continue
            break
        #nav_data should now contain only those entries down the path specified in the request
        #Now find all unique levels below
        level_vals = list(nav_data.values(levels[i]).distinct())
        level_names = []
        for dict in level_vals:
            level_names.append(dict[levels[i]])
            
        if len(nav_data) > 1: #If there's more than one available path, no one id associated so leave as 0
            return JsonResponse({'subcategories':level_names, 'id':0})
        elif len(nav_data) == 1: #If there's one available path, find id associated and return it
            nav_id = list(nav_data.values('id'))[0]['id']
            entry = FlatfileEntry.objects.get(navigation_info=nav_id)
            id = entry.ref_num
            return JsonResponse({'subcategories':level_names, 'id':id})
        else: #If there are no paths, an error occurred in API call, return error message
            return JsonResponse({'message': 'Path not found'})
            
@api_view(['POST'])
def item_calc(request):
    if request.method == 'POST':
        #Find entry of given id
        try:
            entry = FlatfileEntry.objects.filter(pk=request.data['id'])[0]
        except:
            return JsonResponse({"message":"Entry not found"})
        
        #Collect the right information
        source = entry.other_info.source
        unit = entry.calculation_info.cu
        factor = entry.calculation_info.ef
        
        #Calculate the total
        total = factor * request.data['amount']
        
        return JsonResponse({"total":total, "calc_unit":unit, "source":source})