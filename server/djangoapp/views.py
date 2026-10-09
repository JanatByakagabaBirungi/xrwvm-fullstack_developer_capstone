from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.http import JsonResponse
import logging
import json
from django.views.decorators.csrf import csrf_exempt

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']

    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    try:
        User.objects.get(username=username)
        username_exist = True
    except Exception:
        logger.debug("{} is new user".format(username))

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    else:
        data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(data)


# View to return car makes and models for dropdowns
def get_cars(request):
    cars = [
        {"CarModel": "Pathfinder", "CarMake": "NISSAN"},
        {"CarModel": "Qashqai", "CarMake": "NISSAN"},
        {"CarModel": "XTRAIL", "CarMake": "NISSAN"},
        {"CarModel": "A-Class", "CarMake": "Mercedes"},
        {"CarModel": "C-Class", "CarMake": "Mercedes"},
        {"CarModel": "E-Class", "CarMake": "Mercedes"},
        {"CarModel": "A4", "CarMake": "Audi"},
        {"CarModel": "A5", "CarMake": "Audi"},
        {"CarModel": "A6", "CarMake": "Audi"},
        {"CarModel": "Sorrento", "CarMake": "Kia"},
        {"CarModel": "Carnival", "CarMake": "Kia"},
        {"CarModel": "Cerato", "CarMake": "Kia"},
        {"CarModel": "Corolla", "CarMake": "Toyota"},
        {"CarModel": "Camry", "CarMake": "Toyota"},
        {"CarModel": "Kluger", "CarMake": "Toyota"}
    ]
    return JsonResponse({"CarModels": cars})


# --- MOCKED ENDPOINTS TO BYPASS BROKEN BACKEND ---

# Create a `get_dealerships` view to render list of dealerships
def get_dealerships(request, state="All"):
    dealerships = [
        {"id": 1, "city": "El Paso", "state": "Texas", "st": "TX",
         "address": "3 Nova Court", "zip": "88563", "lat": 31.6948,
         "long": -106.3000, "short_name": "Holdlamis",
         "full_name": "Holdlamis Car Dealership"},
        {"id": 2, "city": "Minneapolis", "state": "Minnesota", "st": "MN",
         "address": "6337 Butternut Crossing", "zip": "55402", "lat": 44.9762,
         "long": -93.2759, "short_name": "Temp",
         "full_name": "Temp Car Dealership"},
        {"id": 3, "city": "Birmingham", "state": "Alabama", "st": "AL",
         "address": "9477 Twin Pines Center", "zip": "35285", "lat": 33.5446,
         "long": -86.9292, "short_name": "Sub-Ex",
         "full_name": "Sub-Ex Car Dealership"},
        {"id": 4, "city": "Dallas", "state": "Texas", "st": "TX",
         "address": "253 Hanson Junction", "zip": "75216", "lat": 32.6517,
         "long": -96.7905, "short_name": "Job",
         "full_name": "Job Car Dealership"},
        {"id": 5, "city": "Topeka", "state": "Kansas", "st": "KS",
         "address": "288 Larry Place", "zip": "66642", "lat": 39.0429,
         "long": -95.7697, "short_name": "Bytecard",
         "full_name": "Bytecard Car Dealership"}
    ]

    if state != "All":
        dealerships = [d for d in dealerships if d['state'] == state]

    return JsonResponse({"status": 200, "dealers": dealerships})


# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    if dealer_id:
        dealership = [
            {"id": dealer_id, "city": "El Paso", "state": "Texas",
             "st": "TX", "address": "3 Nova Court", "zip": "88563",
             "lat": 31.6948, "long": -106.3000, "short_name": "Holdlamis",
             "full_name": "Holdlamis Car Dealership"}
        ]
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# Create a `get_dealer_reviews` view to render the reviews
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        reviews = [
            {"id": 1, "name": "Berkly Shepley", "dealership": dealer_id,
             "review": "Total grid-enabled service-desk", "purchase": True,
             "purchase_date": "07/11/2020", "car_make": "Audi",
             "car_model": "A6", "car_year": 2010, "sentiment": "positive"},
            {"id": 2, "name": "Gwenora", "dealership": dealer_id,
             "review": "Loved the service!", "purchase": True,
             "purchase_date": "01/05/2021", "car_make": "Toyota",
             "car_model": "Corolla", "car_year": 2023, "sentiment": "positive"}
        ]
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# Create an `add_review` view to submit a review
@csrf_exempt
def add_review(request):
    if not request.user.is_anonymous:
        return JsonResponse({"status": 200})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
        