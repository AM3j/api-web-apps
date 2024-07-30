from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.views import View

# Class Based Views 
class Github_View(View):

    def get(self, request):

        if request.GET.get('language'):
            # get what inside the input field
            lang = request.GET.get('language', '')
            context = self.lang_search(lang)
        else:
            context = {}

        return render(request, 'github_api/index.html', context)
    
    def lang_search(self, lang):
        url = f'https://api.github.com/search/repositories?q=language:{lang}&sort=stars'
        response = requests.get(url=url)
        status_code  = response.status_code

        response_dict = response.json()
        if status_code == 200:
            items = [ {
                'full_name' : item['full_name'],
                'description' : item['description'],
                'url' : item['html_url'],
                'created_at' : item['created_at'],
                'updated_at' : item['updated_at'],
                'stars' : item['stargazers_count'],
                'topics' : item['topics']
            } for item in response_dict['items'][:10] ]

            context = {'status_code': status_code, 'items': items}
        elif status_code == 422:
            message = response_dict['errors'][0]['message']
            context ={'status_code2': status_code, 'message': message}
        else:
            context ={'status_code': 'There is an error'}

        return context
