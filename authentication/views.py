from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from authentication.serializers import UserSerializer
from authentication.models import UsersTab
from authentication.models import UsersWatchList

import bcrypt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
import requests
from django.contrib.auth.backends import ModelBackend
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def userApis(request,id=0):
    if request.method=='GET':
        student = UsersTab.objects.all()
        student_serializer=UserSerializer(student,many=True)
        return JsonResponse(student_serializer.data,safe=False)
    elif request.method=='POST':
        student_data = JSONParser().parse(request)
        
        student_data['password'] = make_password(student_data['password'])
        print(" inst pass "+student_data['password'])
        student_serializer = UserSerializer(data=student_data)
        if student_serializer.is_valid():
            student_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method=='PUT':
        student_data=JSONParser().parse(request)
        student=UsersTab.objects.get(id=id)
        student_serializer=UserSerializer(student,data=student_data)
        if student_serializer.is_valid():
            student_serializer.save()
            return JsonResponse("Updated Successfully",safe=False)
        return JsonResponse("Failed to Update")
    elif request.method=='DELETE':
        student=UsersTab.objects.get(id=id)
        student.delete()
        return JsonResponse("Deleted Successfully",safe=False)
    
    
@csrf_exempt
def loginApi(request):
    if request.method == 'POST':
        login_data = JSONParser().parse(request)
        name = login_data.get('name')
        password = login_data.get('password')

        try:
            user = UsersTab.objects.get(name=name)
        except UsersTab.DoesNotExist:
            return JsonResponse("Login Failed - User not found", status=401, safe=False)

        if check_password(password, user.password):

            user_data = {
                "id": user.uniqueId,
                "name": user.name,
                "email": user.email,
                "phone": user.phone,

            }
            return JsonResponse({"msg": "Login Successful", "user": user_data}, safe=False)
        else:
            return JsonResponse("Login Failed - Incorrect password", status=401, safe=False)



@csrf_exempt
def getStockDetail(request):
    if request.method == 'POST':
        try:
            stock = JSONParser().parse(request)
            name = stock.get('name')
            
            if not name:
                return JsonResponse({"error": "Name parameter is missing"}, status=400)
            
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={name}&interval=5min&apikey=PCBT0NXC5T218X89'
            r = requests.get(url)
            if r.status_code != 200:
                return JsonResponse({"error": "Failed to fetch data from external API"}, status=r.status_code)
            
            data = r.json()
            return JsonResponse({"response": data})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)


@csrf_exempt
def seacrhStock(request):
    if request.method == 'POST':
        try:
            stock = JSONParser().parse(request)
            search = stock.get('keyword')
            
            if not search:
                return JsonResponse({"error": "Name parameter is missing"}, status=400)
            
            url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={search}&apikey=PCBT0NXC5T218X89'


            r = requests.get(url)
            if r.status_code != 200:
                return JsonResponse({"error": "Failed to fetch data from external API"}, status=r.status_code)
            
            data = r.json()
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)

@csrf_exempt
def addToWatchList(request):
    if request.method == 'POST':
        try:
            stock = JSONParser().parse(request)
            symbol = stock.get('symbol')
            uniqueId = stock.get('uniqueId')

            if not symbol or not uniqueId:
                return JsonResponse({"error": "Symbol or uniqueId parameter is missing"}, status=400)
            
            
            user = UsersTab.objects.get(uniqueId=uniqueId)
            print("Symbol:", symbol, "UniqueId:", uniqueId, "User:", user.uniqueId)
            

            watchlist = UsersWatchList(uniqueId=user.uniqueId, symbol=symbol)
            watchlist.save()
            
            return JsonResponse({"message": "Added to watchlist successfully"})
        except UsersTab.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    elif request.method == 'DELETE':
        try:
            stock = JSONParser().parse(request)
            symbol = stock.get('symbol')
            uniqueId = stock.get('uniqueId')

            if not symbol or not uniqueId:
                return JsonResponse({"error": "Symbol or uniqueId parameter is missing"}, status=400)
            

            user = UsersTab.objects.get(uniqueId=uniqueId)



            UsersWatchList.objects.filter(uniqueId=user.uniqueId, symbol=symbol).delete()
            
            return JsonResponse({"message": f"Symbol {symbol} deleted from watchlist successfully"})
        except UsersTab.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
@csrf_exempt
def fetchWatchList(request):
    if request.method == 'POST':
        try:
            stock = JSONParser().parse(request)
            uniqueId = stock.get('uniqueId')

            if not uniqueId:
                return JsonResponse({"error": "uniqueId parameter is missing"}, status=400)
            

            watchlistOfParticularUser = UsersWatchList.objects.filter(uniqueId=uniqueId)
            

            watchlist_data = list(watchlistOfParticularUser.values())

            return JsonResponse(watchlist_data, safe=False) 
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)




# url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tesco&apikey=demo'
# r = requests.get(url)
# data = r.json()

# print(data)
