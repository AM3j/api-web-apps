from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.views import View
import plotly.express as px
from plotly.offline import plot
import pandas as pd

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

            figuer = self.generate_interactive_figure(items, lang)
            context = {'status_code': status_code, 'items': items, 'fig': figuer}
        elif status_code == 422:
            message = response_dict['errors'][0]['message']
            context ={'status_code2': status_code, 'message': message}
        else:
            context ={'status_code': 'There is an error'}

        return context

    def generate_interactive_figure(self, items, lang):
        df = pd.DataFrame(items)
        df['repo_url'] = df.apply(lambda row: f"<a href='{row['url']}' target='_blank'>{row['full_name']}</a>", axis=1)
        # Create the bar chart
        fig = px.bar(
            df,
            x='repo_url',
            y='stars',
            title="Repositories by Star Count",
            labels={'repo_url': 'Repository Name', 'stars': 'Star Count'},
            text='stars',
            color_discrete_sequence=['#013220']  # Set the color of the bars
        )

        # Customize the layout
        fig.update_layout(
            title={
                'text': f"Top 10 Repositories for {lang}",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Urls for repostries",
            yaxis_title="Star Count",
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor="#f8f9fa",
            plot_bgcolor="white",
            width= 800,
            height= 600
        )

        fig.update_traces(
        texttemplate='%{text:.2s}', 
        textposition='outside',
        hovertemplate='%{x}<br>Stars: %{y}<extra></extra>',
        customdata=df[['url']].values
        )

        plot_div = plot(fig, output_type='div', include_plotlyjs='cdn')
        return plot_div