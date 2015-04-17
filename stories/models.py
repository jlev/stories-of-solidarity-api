from django.db import models
from localflavor.us.models import USStateField
from django.db.models import Count
import geopy
from geopy.geocoders import GeoNames
from geopy.exc import GeopyError

from people.models import Author


class LocationManager(models.Manager):
    def get_queryset(self):
        qs = super(LocationManager, self).get_queryset()
        qs_w_count = qs.annotate(story_grouped_count=Count('story'))
        return qs_w_count


class Location(models.Model):
    city = models.CharField(max_length=100, blank=True, null=True)
    state = USStateField(blank=True, null=True)
    county = models.CharField(max_length=100, null=True, blank=True)

    geocoded = models.BooleanField(default=False)

    lon = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)

    objects = LocationManager()

    def __unicode__(self):
        return "{}, {}".format(self.city.capitalize(), self.state.upper())

    def story_count(self):
        return self.story_grouped_count
    story_count.admin_order_field = 'story_grouped_count'

    def geocode(self, query):
        geolocator = GeoNames(username="jlevinger", country_bias="USA")
        location = geolocator.geocode(query)
        try:
            self.city = location.raw['toponymName']
            self.state = location.raw['adminCode1']
            self.lat = location.latitude
            self.lon = location.longitude
            self.geocoded = True
            self.save()
            return True
        except GeopyError:
            return False


class Story(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    anonymous = models.BooleanField(default=False)

    author = models.ForeignKey(Author, null=True)
    location = models.ForeignKey(Location, null=True)

    content = models.TextField()
    display = models.BooleanField(default=True)
    truncated = models.BooleanField(default=False, help_text="Some legacy stories truncated")

    class Meta:
        verbose_name_plural = "stories"
        ordering = ("-created_at",)

    def excerpt(self):
        if len(self.content) > 160:
            return self.content[:160] + ' ...'
        else:
            return self.content

    def employer(self):
        if self.author:
            return self.author.employer
        else:
            return None

    def __unicode__(self):
        if self.anonymous:
            return "Story by Anonymous"
        else:
            return "Story, by {}".format(self.author)
