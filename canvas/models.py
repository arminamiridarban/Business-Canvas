from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    def get_all_relationships(self):
        relationships = {
            'value_propositions': self.value_propositions.all(),
            'customer_segments': self.customer_segments.all(),
            'channels': self.channel.all(),
            'customer_relationships': self.customer_relationship.all(),
            'revenue_streams': self.revenue_stream.all(),
            'key_resources': self.key_resources.all(),
            'key_activities': self.key_activity.all(),
            'key_partners': self.key_partner.all(),
            'cost_structures': self.cost_structure.all(),
        }
        return relationships

class ValueProposition(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="value_propositions")
    value = models.CharField(max_length=255)
    description = models.CharField(max_length=1023)

    def __str__(self):
        return self.value

class CustomerSegment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="customer_segments")
    value_propositions = models.ManyToManyField(ValueProposition, related_name="customer_segments")
    customer_segment = models.CharField(max_length=255)

    def __str__(self):
        return self.customer_segment


class Channel(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="channel")
    customer_segments = models.ManyToManyField(CustomerSegment, related_name="channel")
    channels = models.CharField(max_length=255)

    def __str__(self):
        return self.channels

class CustomerRelationship(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE, related_name="customer_relationship")
    customer_segment = models.ManyToManyField(CustomerSegment, related_name="customer_relationship")
    relationship=models.CharField(max_length=511)
    description=models.TextField(max_length=1023,blank=True)

    def __str__(self):
        return f"{self.relationship} , {self.description}"


class RevenueStreams(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE, related_name="revenue_stream")
    customer_segment = models.ManyToManyField(CustomerSegment, related_name="revenue_stream")
    revenue = models.CharField(max_length=1023)

    def __str__(self):
        return self.revenue

class KeyResources(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE, related_name="key_resources")
    value_propositions = models.ManyToManyField(ValueProposition, related_name="key_resources")
    customer_segment = models.ManyToManyField(CustomerSegment, related_name="key_resources")
    customer_relationship = models.ManyToManyField(CustomerRelationship, related_name="key_resources")
    channel = models.ManyToManyField(Channel, related_name="key_resources")
    key_resource = models.CharField(max_length=255)
    description = models.TextField(max_length=1023,blank=True)

    def __str__(self):
        return f"{self.key_resource}, {self.description}"

class KeyActivities(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE, related_name="key_activity")
    value_propositions = models.ManyToManyField(ValueProposition, related_name="key_activity")
    customer_segment = models.ManyToManyField(CustomerSegment, related_name="key_activity")
    customer_relationship = models.ManyToManyField(CustomerRelationship, related_name="key_activity")
    channel = models.ManyToManyField(Channel, related_name="key_activity")
    key_activity = models.CharField(max_length=255)
    description = models.TextField(max_length=1023,blank=True)

    def __str__(self):
        return f"{self.key_activity}, {self.description}"

class KeyPartnership(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE, related_name="key_partner")
    value_propositions = models.ManyToManyField(ValueProposition, related_name="key_partner")
    customer_segment = models.ManyToManyField(CustomerSegment, related_name="key_partner")
    customer_relationship = models.ManyToManyField(CustomerRelationship, related_name="key_partner")
    channel = models.ManyToManyField(Channel, related_name="key_partner")
    key_partner = models.CharField(max_length=255)
    description = models.TextField(max_length=1023,blank=True)

    def __str__(self):
        return f"{self.key_partner} ,{self.description}"

class CostStructure(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE, related_name="cost_structure")
    value_propositions = models.ManyToManyField(ValueProposition, related_name="cost_structure",blank=True)
    customer_segment = models.ManyToManyField(CustomerSegment, related_name="cost_structure",blank=True )
    customer_relationship = models.ManyToManyField(CustomerRelationship, related_name="cost_structure",blank=True)
    channel = models.ManyToManyField(Channel, related_name="cost_structure",blank=True)
    cost = models.CharField(max_length=255)
    description = models.TextField(max_length=1023,blank=True)

    def __str__(self):
        return f"{self.cost},{self.description}"


