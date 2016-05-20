from django.db import models

class Taxonomy(models.Model):
    """Information regarding each Taxonomy level

    Here we list all the Taxonomy of each kingdom
    """
    name = models.CharField(max_length=255)
    level = models.IntegerField(default=0)

    def __unicode__(self):
        """
        Return a unicode representation of the item
        """
        return u"{0}".format(self.name)

class Plant(models.Model):
    """Individual plant species

    Holds all the necessary information of an individual plant.
    If a plant is not accepted, ``unaccepted_reason`` should be filled out.
    """
    common_name = models.CharField(max_length=255, blank=True, null=True)
    scientific_name = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="children")
    taxonomy = models.ForeignKey(Taxonomy, blank=True, null=True)
    accepted = models.BooleanField(default=False)
    unaccepted_reason = models.TextField(blank=True, null=True)
    public = models.BooleanField(default=False)

    def __unicode__(self):
        """
        Return a unicode representation of the item
        """
        return u"{0}, {1}, accepted:{2}".format(self.scientific_name, self.taxonomy.name,
                self.accepted)
