from django.shortcuts import render
from django.http.response import JsonResponse
from django.http import HttpRequest
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from api.models import FlatfileEntry
from api.serializers import ApiSerializer

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
        entry_data = JSONParser.parse(request.data)
        api_serializer = ApiSerializer(entry, data=entry_data)
        if api_serializer.is_valid():
            api_serializer.save()
            return JsonResponse(api_serializer.data)
        return JsonResponse(api_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE': #Deletes entry by id
        entry.delete()
        return JsonResponse({'message': 'Entry was deleted'}, status=status.HTTP_204_NO_CONTENT)