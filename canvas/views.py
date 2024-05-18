from django.contrib.auth import authenticate , login, logout
from django.shortcuts import render , redirect
from django.http import JsonResponse, Http404
from django.db import IntegrityError, transaction
from django.contrib.auth.decorators import login_required
from .models import *
import json
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist 

def tutorial(request):
    if request.method == "GET":
        return render(request, "tutorial.html")
    else:
        pass

def premium(request):
    return render (request, "premium.html")

def index(request):
    return render(request, "index.html")

def login_view(request):
    if request.method == "POST":
        action = request.POST.get('action')
        if action == "register":
            username = request.POST.get('registeruser')
            password = request.POST.get('registerpass')
            confirmpassword = request.POST.get('registerconfirmpass')
            if password == confirmpassword:
                try:
                    user = User.objects.create_user(username=username, password=password)
                    login(request, user)
                    return redirect('home')
                except Exception as error:
                    return JsonResponse({"error": str(error)}, status=400)
            else:
                return JsonResponse({"error": "User or Password is Invalid."})
        elif action == "login":
            username = request.POST.get('loginuser')
            password = request.POST.get('loginpass')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                message = {"error": "Invalid username or password"}
                return JsonResponse(message, status=400)
    else:
        return render(request, "login.html")
    
@login_required
def logout_view(request):
    logout(request)
    return render(request,"index.html")


def canvas(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render (request, "canvas.html")
        else:
            return Http404("Access Denied")
    else:
        message = "You need to Login/Register first to create a Canvas"
        return render(request,"login.html",{'message':message})

@login_required  
def valueproposition(request):
    if request.method == "POST":
        user = request.user
        webdata = json.loads(request.body)
        projectname = webdata["projectname"]
        data = webdata["data"]
        try:
            with transaction.atomic():
                project , created = Project.objects.update_or_create(
                    user=user,
                    name=projectname
                    )
        except Exception as e:
            return JsonResponse("Error happening")
        for k in data:
            try:
                with transaction.atomic():
                    try:
                        item = ValueProposition.objects.get(
                            project=project,
                            value= k['input']
                        )
                        item.description = k['description']
                        item.save()
                    except:
                        add_value , created = ValueProposition.objects.update_or_create(
                            project=project,
                            value=k['input'],
                            description=k['description']
                            )
            except Exception as e:
                print(e)
        retrive_updated_values = ValueProposition.objects.filter(
            project=project,
            )
        values = []
        for __ in retrive_updated_values:
            values.append(__.value)

        return JsonResponse(values, safe=False)
    else:
        return Http404("Access Denied")

@login_required
def customersegment(request):
    if request.method == "POST":
        user=request.user
        webdata=json.loads(request.body)
        print(webdata)
        projectname= webdata['projectname']
        customersegmentlist= webdata['customersegment']
        try:
            project = Project.objects.get(
             user=user,
             name=projectname   
            )
        except Exception as e:
            print(f"Failed to get the project {e}")
            return JsonResponse("The project doesn't exists", 400)
        channels = []
        for segment in customersegmentlist:
            values = segment['valueproposition']
            eachcustomersegment= segment['customersegment']
            description = segment['description']
            channels.append(eachcustomersegment)
            for item in values:
                try:
                    val= ValueProposition.objects.get(
                        project = project,
                        value = item
                    )
                    try:
                        CS_retrival = CustomerSegment.objects.get(
                            project = project,
                            customer_segment = eachcustomersegment
                        )
                    except ObjectDoesNotExist:  
                        add_customer_segment, created = CustomerSegment.objects.update_or_create(
                            project = project,
                            customer_segment = eachcustomersegment,
                            description = description,
                        )
                        add_customer_segment.value_propositions.add(val)

                except Exception as e:
                    print(f"the item doesnt exist {e}")
                    return JsonResponse("There is a problem with creating Customer segment", 500)

        data = set()
        export_CS = CustomerSegment.objects.filter(project=project)
        for __ in export_CS:
            data.add(__.customer_segment)
        data= list(data)

        return JsonResponse(data, safe=False)
    else:
        return Http404("Access Denied")


# The return is not available

@login_required
def channels(request):
    if request.method == "POST":
        user = request.user
        webdata = json.loads(request.body)
        print(webdata)
        projectname= webdata['projectname']
        channellist = webdata['channel']
        try:
            project = Project.objects.get(
                user=user,
                name=projectname
            )
        except Exception as e:
            print(f"the project doesn't exists {e}")
            return JsonResponse("Could not find the project", 500)
        
        for eachchannel in channellist:
            ch = eachchannel['channel']
            cs_list = eachchannel['customersegment']
            description = eachchannel['description']
            for cs in cs_list:
                with transaction.atomic():
                    try:
                        cs_retrival = CustomerSegment.objects.get(
                            project = project,
                            customer_segment = cs
                        )
                        add_channel, created = Channel.objects.update_or_create(
                        project = project,
                        channels = ch,
                        description = description,
                        )
                        add_channel.customer_segment.add(cs_retrival)
                    except ObjectDoesNotExist:
                        print("customer segment didnt find")
                        return JsonResponse("Error occured while handeling the Channel", 400)
                    except Exception as e:
                        print(f"There is an error with retriving the cs_retrival {e}")
                        return JsonResponse("There is an error occured while we were processing your request", 400) 
                    
        update_query_for_customer_segment= CustomerSegment.objects.filter(
            project=project
        )
        export_data = []
        for __ in update_query_for_customer_segment:
            export_data.append(__.customer_segment)
        return JsonResponse(export_data, safe=False)
    else:
        return Http404("Access Denied")

@login_required
def customerrelationship(request):
    if request.method == "POST":
        user= request.user
        data = json.loads(request.body)
        projectname=data["projectname"]
        webdata=data["data"]
        try:
            project = Project.objects.get(
                user=user,
                name=projectname
            )
        except Exception as e:
            print(f"Project doesn't exists {e}")
            return JsonResponse("The Project doesn't exists", 400)
        for item in webdata:
            relation = item['relation']
            relation_description = item['relation_description']
            customer_segment_list = item['customer_segment']
            try:
                with transaction.atomic():
                    try:
                        CS_relationship = CustomerRelationship.objects.get(
                            project=project,
                            relationship = relation
                            )
                    except ObjectDoesNotExist:
                        CS_relationship, created = CustomerRelationship.objects.update_or_create(
                            project=project,
                            relationship = relation,
                            description = relation_description,
                        )
                        for cs in customer_segment_list:
                            print(f"The customer_segment is {cs}")
                            try:
                                CS_retrival = CustomerSegment.objects.get(
                                    project=project,
                                    customer_segment = cs
                                )
                                try:
                                    CS_relationship.customer_segment.add(CS_retrival)
                                except Exception as e:
                                    print(f"Failed to add the CS_retrival to customer_segment {CS_retrival}")
                            except Exception as e:
                                print(f"Failed to retrive the customer segment for {cs}")
                        
            except Exception as e:
                print(f"failed to create relation for relation {relation}")
                return JsonResponse("Failed", 400)
        update_query_for_customer_segment= CustomerSegment.objects.filter(
            project=project
        )
        export_data = []
        for __ in update_query_for_customer_segment:
            export_data.append(__.customer_segment)
        print(f"Updated channel list is {export_data}")
        return JsonResponse(export_data, safe=False)
    else:
        return Http404("Access Denied")

@login_required
def revenuestream(request):
    if request.method == "POST":
        user= request.user
        data = json.loads(request.body)
        projectname=data["projectname"]
        webdata=data["data"]
        try:
            project = Project.objects.get(
                user=user,
                name=projectname
            )
        except Exception as e:
            print(f"Project doesn't exists {e}")
            return JsonResponse("The Project doesn't exists", 400)
        for item in webdata:
            revenue = item['revenue']
            customer_segment_list = item['customer_segment']
            description = item['description']
            print(description)
            try:
                with transaction.atomic():
                    try:
                        revenue = RevenueStreams.objects.get(project=project,revenue=revenue)
                    except ObjectDoesNotExist:
                        revenue, created = RevenueStreams.objects.update_or_create(
                            project = project,
                            revenue = revenue,
                            description = description,
                        )
                        if created:
                            print("created")
                        else:
                            print("updated")
                        for eachcs in customer_segment_list:
                            print(f"the customer segment is {eachcs}")
                            try:
                                CS_retrival = CustomerSegment.objects.get(
                                    project=project,
                                    customer_segment=eachcs,
                                )
                                revenue.customer_segment.add(CS_retrival)
                            except:
                                print(f"Couldn't add the customer segment to revenue {eachcs} {CS_retrival}")
            except Exception as e:
                print(f"An error occured while adding revenue stram {e}")
        name="keyresource"
        export_data = Retrival(project,name)
        
        return JsonResponse(export_data, status=200)
    else:
        return Http404("Access Denied")


@login_required
def keysection(request):
    if request.method == "POST":
        user= request.user
        data = json.loads(request.body)
        projectname= data['projectname']
        keysection_info = data['keysection_info']
        section = data['section']
        try:
            project = Project.objects.get(name=projectname, user=user)
        except Exception as e:
            message = "Project doesn't exist"
            return JsonResponse({"message": message , "error": e}, status=400)

        for item in keysection_info:
            keyvalue = item['keysectionvalue']
            keysection_description = item['keysection_description']
            keysection_data = item['data']
            if section == "keyresource":
                try:
                    created_model , created = KeyResources.objects.update_or_create(
                        project=project,
                        key_resource=keyvalue,
                        description=keysection_description,
                    )
                except Exception as e:
                    message = "couldn't create/update the Key Resource"
                    print(f"the error is {e}")
                    return JsonResponse({message:message}, 400)
            elif section == "keyactivities":
                try:
                    created_model , created = KeyActivities.objects.update_or_create(
                        project=project,
                        key_activity=keyvalue,
                        description=keysection_description,
                    )
                except Exception as e:
                    message = "couldn't create/update the Key Resource"
                    print(f"the error is {e}")
                    return JsonResponse({message:message}, 400)
            elif section == "keypartnership":
                try:
                    created_model , created = KeyPartnership.objects.update_or_create(
                        project=project,
                        key_partner=keyvalue,
                        description=keysection_description,
                    )
                except Exception as e:
                    message = "couldn't create/update the Key Resource"
                    print(f"the error is {e}")
                    return JsonResponse({message:message}, 400)
            elif section == "coststructure":
                try:
                    created_model , created = CostStructure.objects.update_or_create(
                        project=project,
                        cost=keyvalue,
                        description=keysection_description,
                    )
                except Exception as e:
                    message = "couldn't create/update the Key Resource"
                    print(f"the error is {e}")
                    return JsonResponse({message:message}, 400)
            else:
                return Http404("Unauthorize Access")
            
            for key in keysection_data:
                with transaction.atomic():
                    if key == "value proposition":
                        for value in keysection_data[key]:
                            try:
                                VP_retrival = ValueProposition.objects.get(
                                    project=project,
                                    value=value
                                )
                                created_model.value_propositions.add(VP_retrival)
                            except Exception as e:
                                error(key)
                    elif key == "customer segment":
                        for value in keysection_data[key]:
                            try:
                                CS_retrival = CustomerSegment.objects.get(
                                    project=project,
                                    customer_segment=value
                                )
                                created_model.customer_segment.add(CS_retrival)
                            except Exception as e:
                                error(key)
                    elif key == "customer relationship":
                        for value in keysection_data[key]:
                            try:
                                CR_retrival = CustomerRelationship.objects.get(
                                    project=project,
                                    relationship=value
                                )
                                created_model.customer_relationship.add(CR_retrival)
                            except Exception as e:
                                error(key)
                    elif key == "channel":
                        for value in keysection_data[key]:
                            try:
                                CH_retrival = Channel.objects.get(
                                    project=project,
                                    channels=value
                                )
                                created_model.channel.add(CH_retrival)
                            except Exception as e:
                                error(key)
                    else:
                        message = "invalid request"
                        return JsonResponse({'message':message},400)
        
        export_data = Retrival(project,section)
        return JsonResponse(export_data, status=200)
    
    else:
        return Http404("Access Denied")
    
                    
def error(key):
    message = f"there is an error while adding {key}"
    return JsonResponse({message:message},400)


def buildcanvas(request, project=None):
    if request.user.is_authenticated:
        user = request.user
        if request.method == "GET":
            total_projects = Project.objects.filter(user=user)
            return render(request, "buildcanvas.html", {'projects': total_projects})
        elif request.method == "POST":
            project_id = request.POST.get('project')
            if request.POST.get('direct'):
                project = Project.objects.get(user=user,name=project_id)    
            else:
                project = Project.objects.get(id=project_id)

            # To get all items of the project
            all = project.get_all_relationships()

            value_propositions = [(vp.value, vp.description, vp.id) for vp in project.value_propositions.all()]
            customer_segments = [(cs.customer_segment, cs.id , cs.description) for cs in project.customer_segments.all()]
            channels = [(ch.channels, ch.id, ch.description) for ch in project.channel.all()]
            customer_relationships = [(cr.relationship,cr.description,cr.id) for cr in project.customer_relationship.all()]
            revenue_streams = [(rs.revenue,rs.id,rs.description) for rs in project.revenue_stream.all()]
            key_resources = [(kr.key_resource,kr.description,kr.id) for kr in project.key_resources.all()]
            key_activities = [(ka.key_activity,ka.description,ka.id) for ka in project.key_activity.all()]
            key_partnerships = [(kp.key_partner,kp.description,kp.id) for kp in project.key_partner.all()]
            cost_structure = [(cs.cost, cs.description,cs.id) for cs in project.cost_structure.all()]

            return render(request, "buildcanvas.html", {
                'project': project,
                'value_propositions': value_propositions,
                'customer_segments': customer_segments,
                'channels': channels,
                'customer_relationships': customer_relationships,
                'revenue_streams': revenue_streams,
                'key_resources': key_resources,
                'key_activities': key_activities,
                'key_partnerships': key_partnerships,
                'cost_structure': cost_structure,
            })
        else:
            raise Http404("Access Denied")
    else:
        message = "You need to Login/Register first to create a Canvas"
        return render(request,"login.html",{'message':message})
    
def canvasretrival(request, projectname):
    if request.method == "POST":
        user = request.user
        webdata = json.loads(request.body)
        projectname = webdata["projectname"]
        project = Project.objects.get(
            user=user,
            name=projectname
        )
        return buildcanvas(request, project)
    else:
        return Http404("Acess Denied")
    


def Retrival(project,section):
    export_value = ValueProposition.objects.filter(project=project)
    val = [item.value for item in export_value]

    export_CS = CustomerSegment.objects.filter(project=project)
    cs = [item.customer_segment for item in export_CS]

    ch = set()
    export_CH = Channel.objects.filter(project=project)
    ch = [item.channels for item in export_CH]

    export_CR = CustomerRelationship.objects.filter(project=project)
    cr = [item.relationship for item in export_CR]

    name = "keyresource" if section == "keyresource" else ("keyactivities" if section == "keyactivities" else "keypartnership")


    export_data = {
        'value proposition': val,
        'customer segment': cs,
        'customer relationship': cr,
        'channel': ch,
    }
    return export_data


def editcanvas(request):
    if request.method == "POST":
        user = request.user
        webdata = json.loads(request.body)
        pk = webdata['pk']
        model_to_submit = webdata['func']
        new_value = webdata['value']
        if 'description' in webdata:
            new_description = webdata['description']
        else:
            new_description = None
        
        if model_to_submit in handler_functions:
            try:
                item = handler_functions[model_to_submit](pk=pk)
                value_field = handler_field_name[model_to_submit]
                setattr(item, value_field, new_value)
                if (new_description):
                    item.description = new_description
                item.save()
                return JsonResponse({"message": f"{model_to_submit} updated successfully"}, status=200)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Object Does Not Exist"}, status=404)
            except Exception as e:
                print(f"error is {e}")
                return JsonResponse({"error": str(e)}, status=400)
        else:
            return JsonResponse({"error": f"No handler found for {model_to_submit}"}, status=400)
    else:
        return Http404("Unauthorized Access")




def removeincanvas(request):
    if request.method == "POST":
        user = request.user
        webdata = json.loads(request.body)
        itemId = webdata['itemId']
        itemtype = webdata['type']
        if itemtype in handler_functions:
            try:
                item = handler_functions[itemtype](pk=itemId)
                item.delete()
                return JsonResponse({"message": f"{itemtype} removed successfully"}, status=200)
            except ObjectDoesNotExist:
                print(f"Couldn't find item with id {itemId} for {itemtype} to delete")
                return JsonResponse({"error": "Object Does Not Exist"}, status=404)
            except Exception as e:
                print(f"while removing the error is {e}")
                return JsonResponse({"error": str(e)}, status=400)
    else:
        return Http404("Access Denied")


def addincanvas(request):
    user = request.user
    webdata = json.loads(request.body)
    model_to_submit = addincanvasfunctions[webdata['model']]
    value = webdata['value']
    description =""
    projectname = webdata['projectname']
    handler = handler_field_name[webdata['model']]
    if value == "":
        return JsonResponse({"message": "The 'value' field cannot be empty"}, status=400)

    try:
        project = Project.objects.get(user=user, name=projectname)
    except ObjectDoesNotExist:
        return JsonResponse({"message":"Project Doesn't Exists"}, status=500)
    except Exception as e:
        return JsonResponse({"message": e}, status=400)
    
    try:
        instance, created = model_to_submit.update_or_create(
            project=project,
            **{handler: value}
        )
        if created:
            print("New Value Proposition Created")
        else:
            print("Value Proposition Found and Updated")
        if 'description' in webdata:
            description = webdata['description']
            instance.description = webdata['description']
            instance.save()
        
        if 'value-proposition' in webdata and len(webdata['value-proposition'])>0:
            model_to_add = webdata['value-proposition']
            for each in model_to_add:
                try:
                    foreignItem = ValueProposition.objects.get(value=each,project=project)
                    getattr(instance, 'value_propositions').add(foreignItem)
                except Exception as e:
                    print(e)

        if 'customer-segment' in webdata and len(webdata['customer-segment'])>0:
            model_to_add = webdata['customer-segment']
            for each in model_to_add:
                try:
                    foreignItem = CustomerSegment.objects.get(customer_segment=each,project=project)
                    getattr(instance, 'customer_segment').add(foreignItem)
                except Exception as e:
                    print(f"error in customer-segment {e}")

        if 'customer-relationship' in webdata and len(webdata['customer-relationship']) > 0:
            model_to_add = webdata['customer-relationship']

            for each in model_to_add:
                try:
                    foreignItem = CustomerRelationship.objects.get(relationship=each,project=project)
                    getattr(instance, 'customer_relationship').add(foreignItem)
                except Exception as e:
                    print(e)

        if 'channels' in webdata:
            model_to_add = webdata['channels']
            for each in model_to_add:
                try:
                    foreignItem = Channel.objects.get(channels=each,project=project)
                    getattr(instance, 'channel').add(foreignItem)
                except Exception as e:
                    print(e)
        data = {'value':value, 'description': description, 'id': instance.id, 'message': f"{webdata['model']} is added successfully"}
        return JsonResponse({"data": data, "section": webdata['model']}, status=200)

    except Exception as e:
        print(e)


def fetchforcanvas(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            webdata = json.loads(request.body)
            func = webdata['func']
            projectID = webdata['projectID']
            project = Project.objects.get(id=projectID)
            if func == 'channel' or func == 'revenue-stream' or func == 'customer-relationship':
                data = {'customer-segment': [cs.customer_segment for cs in project.customer_segments.all()]}
            elif func == 'key-resources' or func == 'key-activities' or func == 'key-partnership' or func == 'cost-structure':
                data = {
                    'value-proposition': [vp.value for vp in project.value_propositions.all()],
                    'customer-segment': [cs.customer_segment for cs in project.customer_segments.all()],
                    'customer-relationship': [cr.relationship for cr in project.customer_relationship.all()],
                    'channels': [ch.channels for ch in project.channel.all()]
                }
            elif func == 'customer-segment':
                data = {'value-proposition': [vp.value for vp in project.value_propositions.all()]}
            elif func == "value-proposition":
                data={}
            else:
                raise ValueError("Invalid function: {}".format(func))
            return JsonResponse(data,status=200,safe=False)
        
        else:
            return Http404("Access Denied")

#### Complete this section to retrive View in Canvas
@login_required
def ViewInCanvas(request):
    user = request.user
    webdata = json.loads(request.body)
    projectname = webdata['projectname']
    section = webdata['section']
    itemID = webdata['itemID']
    try:
        project = Project.objects.get(name=projectname, user=user)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "Project Doesn't Exist"}, status=500)

    try:
        item = handler_functions[section](pk=itemID)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "Item Doesn't Exist"}, status=500)
    data= {}
    if section == "value-proposition":
        data['customer-segment']= [cs.id for cs in item.customer_segments.all()]
        data['key-resources']= [kr.id for kr in KeyResources.objects.filter(project=project,value_propositions=item)]
        data['key-activities']= [ka.id for ka in KeyActivities.objects.filter(project=project,value_propositions=item)]
        data['key-partner']= [kp.id for kp in KeyPartnership.objects.filter(project=project,value_propositions=item)]
        data['cost-structure']= [cost.id for cost in CostStructure.objects.filter(project=project,value_propositions=item)]

    if section == "customer-segment":
        data['value-proposition']= [va.id for va in item.value_propositions.all()]
        data['channel']= [ch.id for ch in Channel.objects.filter(project=project,customer_segment=item)]
        data['customer-relationships']= [cr.id for cr in CustomerRelationship.objects.filter(project=project,customer_segment=item)]
        data['revenue-stream']= [rev.id for rev in RevenueStreams.objects.filter(project=project,customer_segment=item)]
        data['key-resources']= [kr.id for kr in KeyResources.objects.filter(project=project,customer_segment=item)]
        data['key-activities']= [ka.id for ka in KeyActivities.objects.filter(project=project,customer_segment=item)]
        data['key-partner']= [kp.id for kp in KeyPartnership.objects.filter(project=project,customer_segment=item)]
        data['cost-structure']= [cost.id for cost in CostStructure.objects.filter(project=project,customer_segment=item)]

    if section == "channel":
        data['customer-segment']= [cs.id for cs in item.customer_segment.all()]
        data['key-resources']= [kr.id for kr in KeyResources.objects.filter(project=project,channel=item)]
        data['key-activities']= [ka.id for ka in KeyActivities.objects.filter(project=project,channel=item)]
        data['key-partner']= [kp.id for kp in KeyPartnership.objects.filter(project=project,channel=item)]
        data['cost-structure']= [cost.id for cost in CostStructure.objects.filter(project=project,channel=item)]
    
    if section == "customer-relationship":
        data['customer-segment']= [cs.id for cs in item.customer_segment.all()]
        data['key-resources']= [kr.id for kr in KeyResources.objects.filter(project=project,customer_relationship=item)]
        data['key-activities']= [ka.id for ka in KeyActivities.objects.filter(project=project,customer_relationship=item)]
        data['key-partner']= [kp.id for kp in KeyPartnership.objects.filter(project=project,customer_relationship=item)]
        data['cost-structure']= [cost.id for cost in CostStructure.objects.filter(project=project,customer_relationship=item)]

    if section == "revenue-stream":
        data['customer-segment']= [cs.id for cs in item.customer_segment.all()]

    if section == "key-resources" or section == "key-activities" or section == "key-partnership" or section == "cost-structure":
        data['value-proposition']= [dummy.id for dummy in item.value_propositions.all()]
        data['customer-segment']= [dummy.id for dummy in item.customer_segment.all()]
        data['customer-relationships']= [dummy.id for dummy in item.customer_relationship.all()]
        data['channel']= [dummy.id for dummy in item.channel.all()]

    if data:
        return JsonResponse({"data":data},status=200)
    else:
        return JsonResponse({"message":"There are no related datas"}, status=500)


addincanvasfunctions = {
    "value-proposition": ValueProposition.objects,
    "customer-segment": CustomerSegment.objects,
    "channel": Channel.objects,
    "customer-relationship": CustomerRelationship.objects,
    "revenue-stream": RevenueStreams.objects,
    "key-resources": KeyResources.objects,
    "key-activities": KeyActivities.objects,
    "key-partnership": KeyPartnership.objects,
    "cost-structure": CostStructure.objects,
}

handler_field_name = {
    "value-proposition": "value",
    "customer-segment": "customer_segment",
    "channel": "channels",
    "customer-relationship": "relationship",
    "revenue-stream": "revenue",
    "key-resources": "key_resource",
    "key-activities": "key_activity",
    "key-partnership": "key_partner",
    "cost-structure": "cost",
}

handler_functions = {
    "value-proposition": ValueProposition.objects.get,
    "customer-segment": CustomerSegment.objects.get,
    "channel": Channel.objects.get,
    "customer-relationship": CustomerRelationship.objects.get,
    "revenue-stream": RevenueStreams.objects.get,
    "key-resources": KeyResources.objects.get,
    "key-activities": KeyActivities.objects.get,
    "key-partnership": KeyPartnership.objects.get,
    "cost-structure": CostStructure.objects.get,
}

def handler404(request,exception):
    return render(request, "404.html")

