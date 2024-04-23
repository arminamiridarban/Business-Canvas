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
        
        # Call the appropriate handler function based on model_to_submit
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
    model_to_submit = webdata['model']
    value = webdata['value']
    projectname = webdata['projectname']

    if value == "":
        return JsonResponse({"message": "The 'value' field cannot be empty"}, status=400)
    if 'description' in webdata:
        description = webdata['description']
        print(f"description is {description}")
    if 'select' in webdata:
        select = webdata['select']
        if select == "":
            return JsonResponse({"message":"The 'value' field cannot be empty"}, status=400)
        print(f"select is {select}")

    try:
        project = Project.objects.get(user=user, name=projectname)
        print("Project Found")
    except ObjectDoesNotExist:
        print("Project doesn't exists")
        return JsonResponse({"message":"Project Doesn't Exists"}, status=500)
    except Exception as e:
        return JsonResponse({"message": e}, status=400)
    
    if model_to_submit == "value-proposition":
        print("value-description")
        try:
            create_value, created = ValueProposition.objects.update_or_create(
                project=project,
                value=value,
                description=description
            )
            if created:
                print("New Value Proposition Created")
            else:
                print("Value Proposition Found and Updated")
            data = {'value':create_value.value,'description': create_value.description,'id': create_value.id,'message': f"{model_to_submit} is added successfully"}
            # Return a success response with a 200 status code
            return JsonResponse({"data": data, "section": "value-proposition"}, status=200)
        
        except IntegrityError:
            return JsonResponse({"message": "Error: Value Proposition already exists for this project"}, status=400)

        except Exception as e:
            print("Error:", e)
            return JsonResponse({"message": "Error occurred while adding new Value Proposition"}, status=500)

    elif model_to_submit == "customer-segment":
        pass


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
            if func == 'customer-segment':
                data = [(vp.value,vp.id) for vp in project.value_propositions.all()]
            elif func == 'channels':
                data = [(ch.channels, ch.id) for ch in project.channel.all()]
            elif func == 'customer-relationship':
                data = [(cr.relationship, cr.description, cr.id) for cr in project.customer_relationship.all()]
            elif func == 'revenue-stream':
                data = [(rs.revenue, rs.id) for rs in project.revenue_stream.all()]
            elif func == 'key-resources':
                data = [(kr.key_resource, kr.description, kr.id) for kr in project.key_resources.all()]
            elif func == 'key-activities':
                data = [(ka.key_activity, ka.description, ka.id) for ka in project.key_activity.all()]
            elif func == 'key-partnerships':
                data = [(kp.key_partner, kp.description, kp.id) for kp in project.key_partner.all()]
            elif func == 'cost-structure':
                data = [(cs.cost, cs.description, cs.id) for cs in project.cost_structure.all()]
            else:
                key= "invalid function"
                error(key)
            
            return JsonResponse(data, safe=False)
        
        else:
            return Http404("Access Denied")


def handler404(request,exception):
    return render(request, "404.html")