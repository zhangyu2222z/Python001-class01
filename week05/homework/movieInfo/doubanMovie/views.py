from django.shortcuts import render
from .models import TFilmReview
# Create your views here.

def movieReview(request):
    # shorts = FileReview
    reviews = TFilmReview.objects.all()
    return render(request, 'movieReview.html', locals())

def favourableComment(request):
    # shorts = TFilmReview.objects.all()
    condtions = {'star__gte': 3}
    # result = TFilmReview.objects.filter(star__gte=3)
    result = TFilmReview.objects.filter(**condtions)
    return render(request, 'favourableComment.html', locals())