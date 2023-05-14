from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from .models import Tour, Review
from .utils import average_rating
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponseNotFound 
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .forms import ReviewForm
from django.contrib.auth import logout

def about(request):
  template = loader.get_template('about.html')
  return HttpResponse(template.render())

def index(request):
    tours = Tour.objects.all()
    return render(request, "index.html", {"tours": tours})

def tour_list(request):
  tours = Tour.objects.all()
  tours_with_reviews = []
  for tour in tours:
      reviews = tour.review_set.all()
      if reviews:
          tour_rating = average_rating([review.rating for review in reviews])
          number_of_reviews = len(reviews)
      else:
          tour_rating = None
          number_of_reviews = 0
      tours_with_reviews.append({"tour": tour,"tour_rating": tour_rating, "number_of_reviews": number_of_reviews})

  context = {
      "tour_list": tours_with_reviews,
  }
  return render(request, "tour_list.html", context)

def search(request):
  template = loader.get_template('tour_list.html')
  return HttpResponse(template.render())  

def search_results(request):
  if request.method == "GET":
    searched = request.GET['searched']
    results = Tour.objects.filter(name__contains = searched)
    return render(request,'search_results.html', {'searched':searched, 'results':results})
  else:
    return render(request, 'search_results.html', {})  

def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    reviews = tour.review_set.all()
    if reviews:
        tour_rating = average_rating([review.rating for review in reviews])
        context = {
            "tour": tour,
            "tour_rating": tour_rating,
            "reviews": reviews
        }
    else:
        context = {
            "tour": tour,
            "tour_rating": None,
            "reviews": None
        }
    if request.user.is_authenticated:
        max_viewed_tours_length = 10
        viewed_tours = request.session.get('viewed_tours', [])
        viewed_tour = [tour.id, tour.name]
        if viewed_tour in viewed_tours:
            viewed_tours.pop(viewed_tours.index(viewed_tour))
        viewed_tours.insert(0, viewed_tour)
        viewed_tours = viewed_tour[:max_viewed_tours_length]
        request.session['viewed_tours'] = viewed_tours
    return render(request, "reviews/tour_detail.html", context)

@login_required 
@permission_required('mysite.create', raise_exception=True)
def create(request):
    if request.method == "POST":
        tour = Tour()
        tour.name = request.POST.get("name")
        tour.description = request.POST.get("description")
        tour.destination = request.POST.get("destination")
        tour.price = request.POST.get("price")
        tour.duration = request.POST.get("duration")
        tour.image = request.POST.get("image")
        tour.save()
    return HttpResponseRedirect("/index")

@login_required 
@permission_required('mysite.edit', raise_exception=True)
def edit(request, id):
    try:
        tour = Tour.objects.get(id=id)
 
        if request.method == "POST":
            tour.name = request.POST.get("name")
            tour.description = request.POST.get("description")
            tour.destination = request.POST.get("destination")
            tour.price = request.POST.get("price")
            tour.duration = request.POST.get("duration")
            tour.image = request.POST.get("image")
            tour.save()
            return HttpResponseRedirect("/index")
        else:
            return render(request, "edit.html", {"tour": tour})
    except Movie.DoesNotExist:
        return HttpResponseNotFound("<h2>Tour not found</h2>")
     

@login_required
@permission_required('mysite.can_delete_movie', raise_exception=True)
def delete(request, id):
    try:
        tour = Tour.objects.get(id=id)
        tour.delete()
        return HttpResponseRedirect("/index")
    except Movie.DoesNotExist:
        return HttpResponseNotFound("<h2>Tour not found</h2>")    

def review_edit(request, tour_pk, review_pk=None):
    tour = get_object_or_404(Tour, pk=tour_pk)

    if review_pk is not None:
        review = get_object_or_404(Review, tour_id=tour_pk, pk=review_pk)
        user = request.user
        if not user.is_staff and review.creator.id != user.id:
            raise PermissionDenied
    else:
        review = None

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            updated_review = form.save(False)
            updated_review.tour = tour

            if review is None:
                messages.success(request, "Review for \"{}\" created.".format(tour))
            
            updated_review.save()
            return redirect("tour_detail", tour.pk)
    else:
        form = ReviewForm(instance=review)

    return render(request, "reviews/review_edit.html",{"form": form, "instance": review, "model_type": "Review", "related_instance": tour, "related_model_type": "Tour"})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/tour') 
    return render(request, 'registration/logout.html')   