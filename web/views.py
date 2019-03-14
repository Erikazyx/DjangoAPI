from django.core import signing
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse,HttpResponseBadRequest,Http404,HttpResponse
from .models import Story,Author
from django.utils.decorators import method_decorator
import json


class Stories(View):
    def get(self,request,story_cat,story_region,story_date):
        try:
            dic = {}
            if story_cat != '*': dic['category'] = story_cat
            if story_region != '*': dic['region'] = story_region
            if story_date != '*': dic['pub_date__gte'] = story_date
            result = []
            for story in Story.objects.filter(**dic):
                result.append({'key': story.pk, 'headline': story.headline, 'story_cat': story.category,
                               'story_region': story.region, 'author': story.author.name, 'story_date': story.pub_date,
                               'story_details': story.detail})
            if not result:
                raise Http404
            payload = {"stories": result,"status_code":200,"reason_phrase":"OK"}
            resp = JsonResponse(payload)
            return resp
        except:
            raise Http404


@method_decorator(csrf_exempt,name='dispatch')
class LogIn(View):
    def post(self,request):
        data = json.loads(request.body)
        try:
            usr = data["username"]
            pwd = data["password"]
            author = Author.objects.filter(username=usr, password=pwd).first()
            if author:
                request.session['author'] = author.id
                return JsonResponse({"status_code":200,"reason_phrase":"OK"})
            else:
                return JsonResponse({"error":"wrong username or password,try again"})
        except:
            raise JsonResponse({"status_code":400,"reason_phrase":"Bad Request","Content-Type": "failed"})


@method_decorator(csrf_exempt,name='dispatch')
class LogOut(View):
    def post(self,request):
        if request.session.get('author'):
            request.session.clear()
            return JsonResponse({"status_code": 200, "reason_phrase": "OK"})
        else:
            return JsonResponse({"status_code": 400, "reason_phrase": "you should login first"})


@method_decorator(csrf_exempt,name='dispatch')
class PostStory(View):
    def post(self,request):
        data = json.loads(request.body)
        id=request.session.get('author')
        if id:
            try:
                author = Author.objects.get(pk=id)
                new_story=Story(headline=data["headline"],category=data['category'],region=data['region'],
                                detail=data['detail'],author=author)
                new_story.save()
                return JsonResponse({"status_code":201,"reason_phrase":"CREATED"})
            except:
                return JsonResponse({"status_code": 503, "Content-Type": "post failed"})
        else:
            return JsonResponse({"status_code": 503, "Content-Type": "login before post"})


@method_decorator(csrf_exempt, name='dispatch')
class DelStory(View):
    def post(self, request):
        data = json.loads(request.body)
        id=request.session.get('author')
        if id:
            try:
                del_story = Story.objects.get(pk=data['story_key'])
                del_story.delete()
                return JsonResponse({"status_code": 201, "reason_phrase": "CREATED"})
            except:
                return JsonResponse({"status_code": 503, "Content-Type": "delete failed"})
        else:
            return JsonResponse({"status_code": 503, "Content-Type": "login before delete"})
