from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import Stories,LogIn,PostStory,DelStory,LogOut

urlpatterns = [
    path('getstories/<str:story_cat>/<str:story_region>/<str:story_date>', Stories.as_view()),
    path('login/',LogIn.as_view()),
    path('poststory/',PostStory.as_view()),
    path('logout/', csrf_exempt(LogOut.as_view())),
    path('deletestory/',csrf_exempt(DelStory.as_view())),
]
