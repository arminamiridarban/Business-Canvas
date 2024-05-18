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
            print("create a new user")
            username = request.POST.get('registeruser')
            password = request.POST.get('registerpass')
            print(username,password)
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
            print(username, password, user)  # Debug print
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
        print(webdata)
        projectname = webdata["projectname"]
        print(projectname)
        data = webdata["data"]
        print(type(data))
        try:
            with transaction.atomic():
                project , created = Project.objects.update_or_create(
                    user=user,
                    name=projectname
                    )
                if created:
                    print(f"New Project Created by name of {projectname} for user {user}")
                else:
                    print("project Updated")
        except Exception as e:
            return JsonResponse("Error happening")
        print("Now Add Value Propositions")
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
                        print('item modified')
                    except:
                        add_value , created = ValueProposition.objects.update_or_create(
                            project=project,
                            value=k['input'],
                            description=k['description']
                            )
                        if created:
                            print('add_value created')
                        else:
                            print('add_value updated')
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
        print(f"the webdata is {webdata}")
        projectname= webdata['projectname']
        print(f"the project name is {projectname}")
        customersegmentlist= webdata['customersegment']
        print(f"the customersegmentlist name is {customersegmentlist}")
        print(type(customersegmentlist))
        try:
            project = Project.objects.get(
             user=user,
             name=projectname   
            )
            print(f'the project is {project}')
        except Exception as e:
            print(f"Failed to get the project {e}")
            return JsonResponse("The project doesn't exists", 400)
        print("Adding customer segments")
        channels = []
        for segment in customersegmentlist:
            print(segment)
            values= segment['valueproposition']
            eachcustomersegment= segment['customersegment']
            channels.append(eachcustomersegment)
            print(f"eachcustomersegment is {eachcustomersegment}")
            for item in values:
                print(f'ValueProposition is {item}')
                try:
                    val= ValueProposition.objects.get(
                        project=project,
                        value=item
                    )
                    print(f"the query for ValueProposition is {val}")
                    try:
                        CS_retrival = CustomerSegment.objects.get(
                            project=project,
                            customer_segment=eachcustomersegment
                        )
                    except ObjectDoesNotExist:  
                        add_customer_segment, created = CustomerSegment.objects.update_or_create(
                            project=project,
                            customer_segment=eachcustomersegment
                        )
                        add_customer_segment.value_propositions.add(val)
                        if created:
                            print("customer segment created")
                        else:
                            print("customer segment updated")
                except Exception as e:
                    print(f"the item doesnt exist {e}")

        data = set()
        export_CS = CustomerSegment.objects.filter(project=project)
        for __ in export_CS:
            data.add(__.customer_segment)
        data= list(data)

        return JsonResponse(data, safe=False)
    else:
        return Http404("Access Denied")

@login_required
def channels(request):
    if request.method == "POST":
        user = request.user
        webdata = json.loads(request.body)
        projectname= webdata['projectname']
        print(f"the project name is {projectname}")
        channellist = webdata['channel']
        print(f"the channel list is {channellist}")
        try:
            print("retriving the project")
            project = Project.objects.get(
                user=user,
                name=projectname
            )
        except Exception as e:
            print(f"the project doesn't exists {e}")
        for eachchannel in channellist:
            print(f"each channel is {eachchannel}")
            ch = eachchannel['channel']
            print(f"channel {ch}")
            cs_list = eachchannel['customersegment']
            print(f"each cs {eachchannel['customersegment']}")
            for cs in cs_list:
                print(f'cs is {cs}')
                with transaction.atomic():
                    try:
                        cs_retrival = CustomerSegment.objects.get(
                            project=project,
                            customer_segment=cs
                        )
                        print(f"the cs_retrival completed {cs_retrival}")
                        add_channel, created = Channel.objects.update_or_create(
                        project=project,
                        channels=ch
                        )
                        add_channel.customer_segments.add(cs_retrival)
                        if created:
                            print("New Channel created")
                        else:
                            print("the channel updated")
                    except ObjectDoesNotExist:
                        print("customer segment didnt find")
                        return JsonResponse("Error occured while handeling the Channel", 400)
                    except Exception as e:
                        print(f"There is an error with retriving the cs_retrival {e}")
                        return JsonResponse("There is an error occured while we were processing your request", 400) 
                    
        print("Exporting data")
        update_query_for_customer_segment= CustomerSegment.objects.filter(
            project=project
        )
        export_data = []
        for __ in update_query_for_customer_segment:
            print(f"channels are {__.customer_segment}")
            export_data.append(__.customer_segment)
        print(f"Updated channel list is {export_data}")
        return JsonResponse(export_data, safe=False)
    else:
        return Http404("Access Denied")

@login_required
def customerrelationship(request):
    if request.method == "POST":
        user= request.user
        data = json.loads(request.body)
        print(user)
        print(data)
        projectname=data["projectname"]
        print(f"the project name is {projectname}")
        webdata=data["data"]
        print(f"the web data is{webdata}")
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
            print(f"item is {relation}")
            print(f"item relation_description is {relation_description}")
            print(f"item customer_segment is {customer_segment_list}")
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
                        if created:
                            print("New Relationship created")
                        else:
                            print(f"Relationship updated relationship:{relation}")
                        for cs in customer_segment_list:
                            print(f"The customer_segment is {cs}")
                            try:
                                CS_retrival = CustomerSegment.objects.get(
                                    project=project,
                                    customer_segment = cs
                                )
                                print(f"Successful in retrive CS_retrival")
                                try:
                                    CS_relationship.customer_segment.add(CS_retrival)
                                except Exception as e:
                                    print(f"Failed to add the CS_retrival to customer_segment {CS_retrival}")
                            except Exception as e:
                                print(f"Failed to retrive the customer segment for {cs}")
                        
            except Exception as e:
                print(f"failed to create relation for relation {relation}")
                return JsonResponse("Failed", 400)
        print("Export data")
        update_query_for_customer_segment= CustomerSegment.objects.filter(
            project=project
        )
        export_data = []
        for __ in update_query_for_customer_segment:
            print(f"channels are {__.customer_segment}")
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
        print(user)
        print(data)
        projectname=data["projectname"]
        print(f"the project name is {projectname}")
        webdata=data["data"]
        print(f"the web data is{webdata}")
        try:
            project = Project.objects.get(
                user=user,
                name=projectname
            )
        except Exception as e:
            print(f"Project doesn't exists {e}")
            return JsonResponse("The Project doesn't exists", 400)
        for item in webdata:
            print(f"the item is {item}")
            revenue = item['revenue']
            customer_segment_list = item['customer_segment']
            print(f"item is {revenue}")
            print(f"item customer_segment is {customer_segment_list}")
            try:
                with transaction.atomic():
                    try:
                        revenue = RevenueStreams.objects.get(project=project,revenue=revenue)
                    except ObjectDoesNotExist:
                        revenue, created = RevenueStreams.objects.update_or_create(
                            project=project,
                            revenue=revenue
                        )
                        if created:
                            print("New Revenue Stream created")
                        else:
                            print("Revenue Stream updated")
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
        print(f"data is {data}")
        projectname= data['projectname']
        print(projectname)
        keysection_info = data['keysection_info']
        section = data['section']
        print(f"section is {section}")
        try:
            project = Project.objects.get(name=projectname, user=user)
        except Exception as e:
            message = "Project doesn't exist"
            print(message, e)
            return JsonResponse({"message": message , "error": e}, status=400)

        for item in keysection_info:
            keyvalue = item['keysectionvalue']
            print(f"keyvalue is {keyvalue}")
            keysection_description = item['keysection_description']
            print(f"keysection_description is {keysection_description}")
            keysection_data = item['data']
            print(f"keysection_data is {keysection_data}")
            if section == "keyresource":
                try:
                    created_model , created = KeyResources.objects.update_or_create(
                        project=project,
                        key_resource=keyvalue,
                        description=keysection_description,
                    )
                    if created:
                        print("New Key Resource created")
                    else:
                        print("Key resource updated")
                except Exception as e:
                    message = "couldn't create/update the Key Resource"
                    print(message)
                    print(f"the error is {e}")
                    return JsonResponse({message:message}, 400)
            elif section == "keyactivities":
                try:
                    created_model , created = KeyActivities.objects.update_or_create(
                        project=project,
                        key_activity=keyvalue,
                        description=keysection_description,
                    )
                    if created:
                        print("New Key Resource created")
                    else:
                        print("Key resource updated")
                except Exception as e:
                    message = "couldn't create/update the Key Resource"
                    print(message)
                    print(f"the error is {e}")
                    return JsonResponse({message:message}, 400)
            elif section == "keypartnership":
                try:
                    created_model , created = KeyPartnership.objects.update_or_create(
                        project=project,
                        key_partner=keyvalue,
                        description=keysection_description,
                    )
                    if created:
                        print("New Key Resource created")
                    else:
                        print("Key resource updated")
                except Exception as e:
                    message = "couldn't create/update the Key Resource"
                    print(message)
                    print(f"the error is {e}")
                    return JsonResponse({message:message}, 400)
            elif section == "coststructure":
                try:
                    created_model , created = CostStructure.objects.update_or_create(
                        project=project,
                        cost=keyvalue,
                        description=keysection_description,
                    )
                    if created:
                        print("New Key Resource created")
                    else:
                        print("Key resource updated")
                except Exception as e:
                    message = "couldn't create/update the Key Resource"
                    print(message)
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
                                print(f"successfully added {value} to key resource")
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
                                print(f"successfully added {value} to key resource")
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
                                print(f"successfully added {value} to key resource")
                            except Exception as e:
                                error(key)
                    elif key == "channel":
                        for value in keysection_data[key]:
                            try:
                                CH_retrival = Channel.objects.get(
                                    project=project,
                                    channels=value
                                )
                                print(f"the CH_retrival is {CH_retrival}")
                                created_model.channel.add(CH_retrival)
                                print(f"successfully added {value} to key resource")
                            except Exception as e:
                                error(key)
                    else:
                        message = "invalid request"
                        return JsonResponse({'message':message},400)
        
        export_data = Retrival(project,section)
        print("export data retrived")
        return JsonResponse(export_data, status=200)
    
    else:
        return Http404("Access Denied")
    
                    
def error(key):
    message = f"there is an error while adding {key}"
    print(message)
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
            print(all)


            value_propositions = [(vp.value, vp.description, vp.id) for vp in project.value_propositions.all()]
            customer_segments = [(cs.customer_segment, cs.id) for cs in project.customer_segments.all()]
            channels = [(ch.channels, ch.id) for ch in project.channel.all()]
            customer_relationships = [(cr.relationship,cr.description,cr.id) for cr in project.customer_relationship.all()]
            revenue_streams = [(rs.revenue,rs.id) for rs in project.revenue_stream.all()]
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
    print("the export data is")
    print(export_data)
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
                print("save completed")
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
        print(webdata)
        itemId = webdata['itemId']
        itemtype = webdata['type']
        if itemtype in handler_functions:
            try:
                item = handler_functions[itemtype](pk=itemId)
                item.delete()
                print("Item removed sucessfully")
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
    print(webdata['model'])
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
            print("inside customer_segment")
            model_to_add = webdata['customer-segment']
            for each in model_to_add:
                try:
                    foreignItem = CustomerSegment.objects.get(customer_segment=each,project=project)
                    getattr(instance, 'customer_segment').add(foreignItem)
                except Exception as e:
                    print(f"error in customer-segment {e}")

        if 'customer-relationship' in webdata and len(webdata['customer-relationship']) > 0:
            print("inside CustomerRelationship")
            model_to_add = webdata['customer-relationship']

            for each in model_to_add:
                print(each)
                try:
                    foreignItem = CustomerRelationship.objects.get(relationship=each,project=project)
                    getattr(instance, 'customer_relationship').add(foreignItem)
                except Exception as e:
                    print(e)

        if 'channels' in webdata:
            print("inside channels")
            model_to_add = webdata['channels']
            for each in model_to_add:
                print(each)
                try:
                    foreignItem = Channel.objects.get(channels=each,project=project)
                    getattr(instance, 'channel').add(foreignItem)
                    print("channel added")
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
            print(func)
            projectID = webdata['projectID']
            print(projectID)
            project = Project.objects.get(id=projectID)
            print(project)
            if func == 'channel' or func == 'revenue-stream' or func == 'customer-relationship':
                data = {'customer-segment': [cs.customer_segment for cs in project.customer_segments.all()]}
            elif func == 'key-resources' or func == 'key-activities' or func == 'key-partnerships' or func == 'cost-structure':
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
            print(data)
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
    print(section)
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
        data['key-resource']= [kr.id for kr in KeyResources.objects.filter(project=project,value_propositions=item)]
        data['key-activity']= [ka.id for ka in KeyActivities.objects.filter(project=project,value_propositions=item)]
        data['key-partner']= [kp.id for kp in KeyPartnership.objects.filter(project=project,value_propositions=item)]
        data['cost-structure']= [cost.id for cost in CostStructure.objects.filter(project=project,value_propositions=item)]

    if section == "customer-segment":
        print("data1")
        data['value-proposition']= [va.id for va in item.value_propositions.all()]
        data['channel']= [ch.id for ch in Channel.objects.filter(project=project,customer_segment=item)]
        data['customer-relation']= [cr.id for cr in CustomerRelationship.objects.filter(project=project,customer_segment=item)]
        data['revenue-stream']= [rev.id for rev in RevenueStreams.objects.filter(project=project,customer_segment=item)]
        data['key-resource']= [kr.id for kr in KeyResources.objects.filter(project=project,customer_segment=item)]
        data['key-activity']= [ka.id for ka in KeyActivities.objects.filter(project=project,customer_segment=item)]
        data['key-partner']= [kp.id for kp in KeyPartnership.objects.filter(project=project,customer_segment=item)]
        data['cost-structure']= [cost.id for cost in CostStructure.objects.filter(project=project,customer_segment=item)]

    print("data")
    print(data)


def handler404(request,exception):
    return render(request, "404.html")


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