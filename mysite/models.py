from django.db import models
from django.contrib import auth

class Tour(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    destination = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()
    image = models.ImageField(upload_to='tours/', null=True, blank=True)
    
    def __str__(self):
        return self.name

class Booking(models.Model):
    date_booked = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    number_of_tickets = models.IntegerField()

class Review(models.Model):
    rating = models.IntegerField()
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(null=True, help_text="The date and time the review was last edited.")
    creator = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)

def __str__(self):
        return self.tour