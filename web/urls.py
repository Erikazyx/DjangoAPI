from django.urls import path

from .views import Stories,LogIn,PostStory,DelStory,LogOut

urlpatterns = [
    path('getstories/<str:story_cat>/<str:story_region>/<str:story_date>', Stories.as_view()),
    path('login/',LogIn.as_view()),
    path('poststory/',PostStory.as_view()),
    path('logout/',LogOut.as_view),
    path('deletestory/',DelStory.as_view),
]
