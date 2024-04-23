import ast
from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    search_fields = ['username', 'email']  
    readonly_fields = ['id']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name")
    list_filter = ['user']  
    readonly_fields = ['id'] 


class ValuePropositionAdmin(admin.ModelAdmin):
    list_display = ("id","value", "description")
    search_fields = ['value', 'description']
    readonly_fields = ['id']  


class CustomerSegmentAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_segment")
    readonly_fields = ['id']  


class ChannelAdmin(admin.ModelAdmin):
    list_display = ("id", "channels", "project")
    readonly_fields = ['id']
    search_fields = ['channels'] 



class CustomerRelationshipAdmin(admin.ModelAdmin):
    list_display = ("id" ,"relationship", "description")
    search_fields = ['relationship'] 
    readonly_fields = ['id']  

class RevenueStreamsAdmin(admin.ModelAdmin):
    list_display = ["id", "revenue"]
    search_fields = ['revenue'] 
    readonly_fields = ['id'] 

class KeyResourcesAdmin(admin.ModelAdmin):
    list_display = ["id", "key_resource","description"]
    search_fields = ['key_resource'] 
    readonly_fields = ['id'] 

class KeyActivitiesAdmin(admin.ModelAdmin):
    list_display = ["id", "key_activity","description"]
    search_fields = ['key_activity'] 
    readonly_fields = ['id'] 

class KeyPartnershipAdmin(admin.ModelAdmin):
    list_display = ["id", "key_partner","description"]
    search_fields = ['key_partner'] 
    readonly_fields = ['id'] 

class CostStructureAdmin(admin.ModelAdmin):
    list_display = ["id", "cost","description"]
    search_fields = ['cost'] 
    readonly_fields = ['id'] 


admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ValueProposition, ValuePropositionAdmin)
admin.site.register(CustomerSegment, CustomerSegmentAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(CustomerRelationship,CustomerRelationshipAdmin)
admin.site.register(RevenueStreams,RevenueStreamsAdmin)
admin.site.register(KeyResources,KeyResourcesAdmin)
admin.site.register(KeyActivities,KeyActivitiesAdmin)
admin.site.register(KeyPartnership,KeyPartnershipAdmin)
admin.site.register(CostStructure,CostStructureAdmin)