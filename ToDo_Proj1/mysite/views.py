from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect


class Home(View):
    def get(self, request):
        return render(request, 'mysite/home.html')


class Resume(View):
    def get(self, request):
        return HttpResponseRedirect("https://raw.githubusercontent.com/g-kartik/resume/main/G_Karthik_Resume.pdf")