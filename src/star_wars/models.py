from django.db import models


class CollectionRequest(models.Model):
    """
    CollectionRequest model
    """

    file = models.FileField(upload_to="collection_requests", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Collection request #{self.id}"


class HomeWorld(models.Model):
    """
    HomeWorld model with map of homeworlds urls and titles
    {url: title}
    """

    homeworld_map = models.JSONField()

    def __str__(self):
        return f"Homeworld #{self.id}"
