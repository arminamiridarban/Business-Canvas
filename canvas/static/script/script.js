document.addEventListener("DOMContentLoaded", () => {
    if (window.location.pathname != "/"){

        // GPT modal
        var modal = document.getElementById("modal");
        var btn = document.getElementById("chatgpt_logo");
        var span = document.getElementsByClassName("close")[0];
    
        btn.onclick = function() {
            modal.style.display = "block";
        }
            
        span.onclick = function() {
        modal.style.display = "none";
        }
        
        window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }}
        if (window.location.pathname === "/") {
    }


    } else if (window.location.pathname.startsWith("/login") ){
        
    }
    else if (window.location.pathname.startsWith("/samplecanvas")){
        
        let select = document.querySelector('#samplecanvas');
        select.addEventListener('change', () => {
            let csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
            fetch('/samplecanvas',{
                method: 'POST',
                headers:{
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({
                    project_id: select.value,
                })
            })
            .then(response => response.json())
            .then(data =>{
                let canvas_info = data.data;
                values = {
                    "value_propositions":"value",
                    "customer_segments":"customer_segment",
                    "channels":"channels",
                    "revenue_streams":"revenue",
                    "key_partners":"key_partner",
                    "key_resources":"key_resource",
                    "key_activities":"key_activity",
                    "customer_relationships":"relationship",
                    "cost_structures":"cost"
                }
                document.querySelectorAll('.XX').forEach((div) => {
                    div.remove();
                });                
                for (item in canvas_info){
                    let element = document.querySelector(`#${item}`);
                    if (item in values){
                        console.log(canvas_info[item]);
                        for (each in canvas_info[item]){
                            let tempDiv = document.createElement('div');
                            tempDiv.classList.add('XX');
                            let tempInput = document.createElement('input');
                            tempInput.type = "text";
                            tempInput.setAttribute('readonly','true');
                            tempInput.value = canvas_info[item][each][`${values[item]}`];
                            let temptextarea = document.createElement('textarea');
                            temptextarea.textContent = canvas_info[item][each]['description'];
                            temptextarea.setAttribute('readonly','true');
                            tempDiv.append(tempInput);
                            tempDiv.append(temptextarea);
                            element.append(tempDiv);
                        }

                    } 
                }
                
            })
            .catch(error =>{
                console.log(error);
            })
        });
    }
    else if (window.location.pathname.startsWith("/comparecanvas")){

        document.querySelectorAll('.a').forEach(select => {
            select.addEventListener('change', () => {
                let section = select;
                console.log(section);
                let csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
            fetch('/comparecanvas',{
                method: 'POST',
                headers:{
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({
                    project_id: section.value,
                })
            })
            .then(response => response.json())
            .then(data => {
                values = {
                    "value_propositions":"value",
                    "customer_segments":"customer_segment",
                    "channels":"channels",
                    "revenue_streams":"revenue",
                    "key_partners":"key_partner",
                    "key_resources":"key_resource",
                    "key_activities":"key_activity",
                    "customer_relationships":"relationship",
                    "cost_structures":"cost"
                }
                document.querySelector(`#${section.name}`).style.display = "block";
                let main_div = document.querySelector(`#${section.name}`);
                data = data['data'];
                for (item in data){
                    if (item === "project"){
                        main_div.querySelector('.project').textContent = data[item];
                    }
                    else{
                        let div = main_div.querySelector(`.${item}`);
                        for (let eachvalue in data[item]) {
                            if (data[item].hasOwnProperty(eachvalue)) {
                                console.log(values[item]);
                                let temp_div = document.createElement('div');
                                temp_div.classList.add('show-comparison-created-div');
                                let temp_p_tag = document.createElement('p');
                                temp_p_tag.textContent = data[item][eachvalue][values[item]];
                                let temp_textarea_tag = document.createElement('textarea');
                                temp_textarea_tag.disabled = true;
                                temp_textarea_tag.textContent = data[item][eachvalue]['description'];
                                temp_div.append(temp_p_tag);
                                temp_div.append(temp_textarea_tag);
                                console.log(temp_div);
                                div.append(temp_div);
                            }
                        }
                    }
                }
            })
            .catch(error => {
                console.log(error);
            })
            });
        });
    }
    else if (window.location.pathname.startsWith("/buildcanvas")) {
        document.querySelectorAll('.buildCanvasTextarea').forEach(item =>{
            item.style.display = 'none';
        });

        let textareas = document.querySelectorAll('textarea');
        textareas.forEach(textarea => {
            textarea.style.height = "auto";
            textarea.style.height = textarea.scrollHeight + "px";
        });
        document.querySelectorAll(".BuildCanvasEditID").forEach(button => {
            button.addEventListener("click", (event) => { 
                editInCanvas(event);
            });
        });
        document.querySelectorAll(".BuildCanvasRemoveID").forEach(button =>{
            button.addEventListener("click",(event)=>{
                removeInCanvas(event);
            })
        });
        document.querySelectorAll(".buildCanvasAddButton").forEach(button =>{
            button.addEventListener('click', (event) =>{
                console.log("clicked");
                addInCanvas(event);
            })
        });
        document.querySelectorAll(".expandable").forEach(item => {
            item.addEventListener('click', (event) => {
                if (event.target.tagName === 'SPAN' || event.target.tagName === 'INPUT') {
                    expandDiscription(event);
                }
            });
        });
        document.querySelectorAll(".BuildCanvasViewID").forEach(item =>{
            item.addEventListener('click',(event)=>{
                console.log("View Clicked");
                ViewInCanvas(event);
            })
        });
        

    } else if (window.location.pathname.startsWith("/canvas")) {
        document.querySelectorAll(".infobutton").forEach(button => {
            button.addEventListener("click", (event) => {
                let form = event.target.closest('form');
                let infoParagraph = form.querySelector('.info');
                
                if (infoParagraph.style.display === "none"){
                    infoParagraph.style.display = 'block';
                } else {
                    infoParagraph.style.display = 'none';
                }
            });
        });
    }    
});

function ViewInCanvas(event){
    console.log("inside View In Canvas Function");
    action = event.target;
    section = action.dataset.type;
    itemID = action.value;

    let csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    let projectname = document.querySelector('#projectname').value;
    fetch('/ViewInCanvas',{
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            projectname: projectname,
            section: section,
            itemID:itemID,
        })
    })
    .then(response => response.json())
    .then(data => {
        var datadic = data.data;
        document.querySelectorAll("input[data-viewID]").forEach(item =>{
            item.style.backgroundColor = "transparent";
        });
        for (let key in datadic) {
            let maindiv = document.querySelector(`.${key}`);
            console.log(maindiv);
            let x = datadic[key];
            for (let i = 0; i < x.length; i++) {
                let value = x[i];
                let dummyitem = maindiv.querySelector(`input[data-viewId="${value}"]`);
                dummyitem.style.backgroundColor = "#DC6B19";
            }
        }
    })    
    .catch(error =>{
        console.log("error happened");
        console.log(error);
    })
}


function addValueField() {
    let valueNumbers = document.querySelector('#fieldcreator').value;
    let valuePropositionForm = document.querySelector('#valuePropositionForm');
    valuePropositionForm.style.display = 'block';
    let valuePropositionDiv = document.createElement('div');
    valuePropositionDiv.id = "valuePropositionDiv";
    valuePropositionDiv.classList.add('d-flex','flex-column',);
    valuePropositionForm.append(valuePropositionDiv);

    for (let i = 0; i < valueNumbers; i++) {
        let tempDiv = document.createElement('div');
        tempDiv.classList.add('valueProposition');
        let tempValue = document.createElement('input');
        tempValue.placeholder = `Enter Value number ${i + 1}`;
        tempValue.classList.add('mx-2', 'value');
        let tempValueDescription = document.createElement('textarea');
        tempValueDescription.placeholder = `Enter Description for Value number ${i + 1}`;
        tempValueDescription.classList.add('mx-2', 'desc');
        tempDiv.append(tempValue);
        tempDiv.append(tempValueDescription);
        valuePropositionDiv.append(tempDiv);
    }

    if (document.querySelector('#tempvaluePropositionSubmit') !== null) {
        document.querySelector('#tempvaluePropositionSubmit').remove();
    }
    let tempvaluePropositionSubmit = document.createElement('button');
    tempvaluePropositionSubmit.type = "button";
    tempvaluePropositionSubmit.id = "tempvaluePropositionSubmit";
    tempvaluePropositionSubmit.textContent = "Submit Values";
    tempvaluePropositionSubmit.classList.add('canvasbutton');
    tempvaluePropositionSubmit.addEventListener('click', () => {
        fetchaddValueFields();
    });
    valuePropositionDiv.append(tempvaluePropositionSubmit);
}


function fetchaddValueFields(){
    let data = [];
    let valuePropositionList = document.querySelectorAll('.valueProposition');
    let csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    valuePropositionList.forEach(item =>{
        var input = item.querySelector('.value').value;
        var description = item.querySelector('.desc').value;
        data.push({input,description});
    })
    let projectname = document.querySelector('#projectname').value;
    fetch('/valueproposition',{
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            projectname: projectname,
            data: data,
        })
    })
    .then(response => response.json())
    .then(data => {
        let tempInputDiv= document.querySelectorAll(".tempInputDiv");
        if (tempInputDiv.length > 0){
            document.querySelector('#submitCustomerSegment').remove();
            tempInputDiv.forEach(element=>{
                element.remove();
            });   
        }
        let passingform = document.querySelector('#customerSegmentForm');
        document.querySelector("#valuePropositionForm").style.display = "none";
        document.querySelector('#collapseValueProposition').style.display = "block";
        segmentaddbutton(data,passingform);
    })
    .catch(error =>{
        console.log(`the error is ${error}`);
    });
}

function saveCustomerSegment(customerSegmentForm){
    let form = customerSegmentForm;
    console.log("this is the form");
    console.log(form);
    let allCustomerSegmentsList = [];
    let allCustomerSegments = form.querySelectorAll('.tempInputDiv');
    allCustomerSegments.forEach(element =>{
        if (element.classList.contains("tempInputDiv")) {
            console.log("this is item we want");
            console.log(element);
            let customerSegmentinput = element.querySelector('input').value;
            console.log(customerSegmentinput);
            let customerSegmentselect = element.querySelector('select');
            let selectValues = customerSegmentselect.selectedOptions;
            let description = element.querySelector('textarea').value;
            console.log(description);
            let values = [];
            for (let i=0; i<selectValues.length;i++){
                values.push(selectValues[i].value);
            }
            console.log(values);
            allCustomerSegmentsList.push({ customersegment: customerSegmentinput, valueproposition: values, description: description });
        }
    });
    console.log(allCustomerSegmentsList);
    for (let i=0; i<allCustomerSegmentsList.length; i++){
        console.log(allCustomerSegmentsList);
        console.log(allCustomerSegmentsList[i]);
    }
    let csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;
    let projectname = document.querySelector('#projectname').value;
    fetch("/customersegment",{
        method: "POST",
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            projectname: projectname,
            customersegment: allCustomerSegmentsList,
        })
    })
    .then(response => response.json())
    .then(data =>{
        let form = document.querySelector('#channelsForm');
        form.style.display = 'block';
        segmentaddbutton(data,form);
        addInput(form,data);
    })
    .catch(error =>{
        console.log(`the error is ${error}`)
    })
}



function saveChannels(channelForm){
    form = channelForm;
    console.log('channel');
    console.log(form);
    let formDivs = form.querySelectorAll('div');
    let allChannelsList = [];
    formDivs.forEach(element=>{
        if (element.classList.contains("tempInputDiv")) {
            let channel = element.querySelector('input').value;
            let description = element.querySelector('textarea').value;
            let channelSelect = element.querySelector('select');
            let channelOptions = channelSelect.selectedOptions;
            let values = [];
            for (let i=0; i<channelOptions.length; i++){
                values.push(channelOptions[i].value);
            }
            allChannelsList.push({channel: channel, customersegment:values, description:description});
        }
    })
    let csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;
    let projectname = document.querySelector('#projectname').value;
    console.log(allChannelsList);
    fetch("/channels",{
        method : "POST",
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            projectname : projectname,
            channel : allChannelsList,

        })
    })
    .then(response=>response.json())
    .then(data=>{
        let form = document.querySelector('#relationshipForm');
        form.style.display = 'block';
        console.log(data);
        segmentaddbutton(data,form);
        addInput(form,data);
    })
    .catch(error =>{
        console.log(`the error is ${error}`)
    })
}

function saveRelationship(relationshipForm){
    form = relationshipForm;
    console.log(form);
    let formDivs = form.querySelectorAll('div');
    let relation_final = []
    formDivs.forEach(element =>{
        console.log(element)
        if (!element.classList.contains("not")) {
            let relation = element.querySelector('input').value;
            let relation_description = element.querySelector('textarea').value;
            let relation_select_element= element.querySelector('select');
            let customer_segment = relation_select_element.selectedOptions;
            let customer_segment_list = [];
            for (let i=0; i<customer_segment.length;i++){
                customer_segment_list.push(customer_segment[i].value);
                console.log(customer_segment[i].value);
            }
            relation_final.push({relation:relation,relation_description:relation_description,customer_segment:customer_segment_list});
        }
    });
    let csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;
    let projectname = document.querySelector('#projectname').value;
    fetch("/customerrelationship", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            projectname: projectname,
            data: relation_final,
        })
    })
    .then(response => response.json())
    .then(data => {
        let form = document.querySelector('#revenueForm');
        form.style.display = 'block';
        console.log(data);
        segmentaddbutton(data,form);
        addInput(form,data);
    })
    .catch(error => {
        console.log(`the error is ${error}`)
    });
}
function saveRevenueStream(Formid){
    form = Formid;
    console.log("Inside the saveRevenueStream function");
    let formDivs = form.querySelectorAll('div');
    let revenue_final = []
    formDivs.forEach(element =>{
        console.log(element)
        if (!element.classList.contains("not")){
            let revenue = element.querySelector('input').value;
            let revenue_select_element= element.querySelector('select');
            let description = element.querySelector('textarea').value;
            let customer_segment = revenue_select_element.selectedOptions;
            let customer_segment_list = [];
            for (let i=0; i<customer_segment.length;i++){
                customer_segment_list.push(customer_segment[i].value);
                console.log(customer_segment[i].value);
            }
            revenue_final.push({revenue:revenue,customer_segment:customer_segment_list, description:description});
        }
    });
    let csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;
    let projectname = document.querySelector('#projectname').value;
    fetch("/revenuestream", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            projectname: projectname,
            data: revenue_final,
        })
    })
    .then(response => response.json())
    .then(data => {
        let form = document.querySelector('#keyresourceForm');
        form.style.display = 'block';
        console.log(data);
        segmentaddbutton(data,form);
        addInput(form,data);
    })
    .catch(error => {
        console.log(`the error is ${error}`)
    });
}



function saveKeysection(Formid,name) {
    section_name=name;
    console.log(section_name);
    console.log("Inside the saveKeySection");
    let formDivs = Formid.querySelectorAll('div');
    let keysection_final = [];

    formDivs.forEach(element => {
        console.log(element);
        if (!element.classList.contains("not")){
            
            let keysectionvalue = element.querySelector('input').value;
            let keysection_description = element.querySelector('textarea').value;
            let keysection_select = element.querySelector('select');
            let selectedOptions = Array.from(keysection_select.selectedOptions);
            let mappeddata = {};
    
            selectedOptions.forEach(selectedOption => {
                console.log("check here");
                let selectedGroup = selectedOption.parentElement.label;
                let selectedValue = selectedOption.value;
                if (!mappeddata[selectedGroup]) {
                    mappeddata[selectedGroup] = [];
                }
                mappeddata[selectedGroup].push(selectedValue);
            });
            console.log("the mappeddata is");
            console.log(mappeddata);
            keysection_final.push({ keysectionvalue: keysectionvalue, keysection_description: keysection_description, data: mappeddata });
        }
    });
    console.log(keysection_final);
    console.log(`The keysection_final is ${keysection_final}`);
    let csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;
    let projectname = document.querySelector('#projectname').value;
    fetch("/keysection", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            projectname: projectname,
            section:section_name,
            keysection_info: keysection_final,
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Inside then of saveKeysection function");
        let form = document.getElementById(`${section_name}Form`);
        form.style.display = "none";
        if (section_name === "keyresource"){
            section_name = "keyactivities";
            form = document.querySelector("#keyactivitiesForm");
            form.style.display = "block";
            segmentaddbutton(data,form);
            addInput(form,data);
        } else if (section_name === "keyactivities"){
            section_name = "keypartnership";
            form = document.querySelector("#keypartnershipForm");
            form.style.display = "block";
            segmentaddbutton(data,form);
            addInput(form,data);
        } else if (section_name === "keypartnership"){
            section_name = "coststructure";
            form = document.querySelector("#coststructureForm");
            form.style.display = "block";
            segmentaddbutton(data,form);
            addInput(form,data);
        }
        else {
            var submitform = document.createElement("form");
            submitform.method = "POST";
            submitform.action = "/buildcanvas"; 

            var input1 = document.createElement("input");
            input1.type = "hidden";
            input1.name = "project";
            input1.value = projectname;

            var input2 = document.createElement("input");
            input2.type = "hidden";
            input2.name = "csrfmiddlewaretoken";
            input2.value = csrfToken;

            var input3 = document.createElement("input");
            input3.type = "hidden";
            input3.name = "direct";
            input3.value = "direct";

            submitform.appendChild(input1);
            submitform.appendChild(input2);
            submitform.appendChild(input3);
            document.body.appendChild(submitform);
            submitform.submit();
        }
        
    })
    .catch(error => {
        console.log(`the error is ${error}`)
    });
}


function collapse(formid){
    let form = document.querySelector(`#${formid}`);
    let style = form.style.display;
    if (style === "none"){
        form.style.display = "block"
    } else {
        form.style.display = "none";
    }
}

function segmentaddbutton(data,passingform){
    form = passingform;
    console.log("segmentaddbutton");
    console.log(form);
    let name = form.name;
    let customerSegmentForm = document.querySelector(`#${form.id}`);
    customerSegmentForm.style.display = "block";
    customerSegmentForm.classList.add('ssss');
    let customerSegmentCount = 0
    let checkAddButton = document.querySelector("#customerSegmentAddButton");
    if (checkAddButton){
        checkAddButton.remove()
    }
    let AddButton = document.createElement('button');
    AddButton.textContent = `Add ${name}`;
    AddButton.classList.add('canvasbutton');
    AddButton['type']='button';
    AddButton['id'] = 'customerSegmentAddButton';
    AddButton.addEventListener('click',function(){
        addInput(customerSegmentForm,data);
        customerSegmentCount += 1;
    });
    customerSegmentForm.append(AddButton);
}

function addInput(idOfForm,data){
    let different = ["keyresource","keyactivities","keypartnership","coststructure"]
    form = idOfForm;
    let name = form.name;
    let tempInputDiv = document.createElement('div');
    tempInputDiv.classList.add('tempInputDiv');
    let tempInput = document.createElement('input');
    tempInput.classList.add(`${name}`);
    tempInput['placeholder'] = `Enter ${form.name}`;
    tempInput['autofocus']= true;
    tempInputDiv.append(tempInput);
    if (!different.includes(name)){
        console.log("not key resource");
        let tempSelect = document.createElement('select');
        tempSelect.classList.add();
        tempSelect['multiple'] = true;
        for (let i=0; i< data.length; i++){
            let tempOption = document.createElement('option');
            tempOption['value'] = data[i];
            tempOption.textContent = data[i];
            tempSelect.append(tempOption);
        }
        tempInputDiv.append(tempSelect);
    }


    let temptextarea= document.createElement('textarea');
    temptextarea['placeholder']= "Enter Description";
    temptextarea.classList.add('tempTextarea');
    tempInputDiv.append(temptextarea);

    if (different.includes(name)){
        console.log("not key resource create group select");
        let tempSelect = document.createElement('select');
        tempSelect.classList.add('tempSelect');
        tempSelect['multiple'] = true;
        console.log(data);
        for (let key in data){
            console.log(`the key is ${key}`);
            console.log(data[key]);
            let Optgroup = document.createElement('optgroup');
            Optgroup.label = key;
            for (let i in data[key]){
                let opt = document.createElement('option');
                opt.textContent = data[key][i];
                opt['value'] = data[key][i];
                Optgroup.append(opt);
            }
            tempSelect.append(Optgroup)
        }
        tempInputDiv.append(tempSelect);
    }
    form.append(tempInputDiv);

    let submitbutton = document.querySelector(`#submit${name}`);
    if (submitbutton !== null){
        submitbutton.remove();
    }
    let tempsubmitbutton = document.createElement('button');
    tempsubmitbutton['type'] = 'button';
    tempsubmitbutton.textContent = `Submit ${name}`;
    tempsubmitbutton['id'] = `submit${name}`;
    tempsubmitbutton.classList.add('canvasbutton');
    tempsubmitbutton.dataset.condition =name;
    tempsubmitbutton.addEventListener('click', function(event){
        let tempname = name;
        let tohidden = event.target.dataset.condition;
        let x = document.querySelector(`#${tohidden}Form`);
        console.log(x);
        if (x.classList.contains('d-flex')){
            x.classList.remove('d-flex');
        }
        x.style.display = 'none';
        let temp = document.querySelector(`#collapse${tempname}`);
        temp.style.display = "block";
        temp.style.margin = "1% 0 1% 0";
        console.log(`the temp name is ${tempname}`);
        switch (tempname){
            case "customerSegment":
                console.log('customerSegment save');
                saveCustomerSegment(form);
                break;
            case "channels":
                console.log('channels save');
                saveChannels(form);
                break;
            case "relationship":
                console.log("relationship");
                saveRelationship(form);
                break;
            case "revenue":
                console.log("revenue");
                saveRevenueStream(form);
                break;
            case "keyresource":
                console.log("keyresource");
                saveKeysection(form,tempname);
                break;
            case "keyactivities":
                console.log("keyresource");
                saveKeysection(form,tempname);
                break;
            case "keypartnership":
                console.log("keyresource");
                saveKeysection(form,tempname);
                break;
            case "coststructure":
                console.log("Cost Structure");
                saveKeysection(form,tempname);
                break;

        }
        
    });
    form.append(tempsubmitbutton);
}


function editInCanvas(event) {
    let action = event.target;
    console.log(action);
    console.log("in the editInCanvas function");
    let project_id = document.querySelector('#projectname').dataset['id'];
    let number = action.value;
    let div = action.closest('[data-id]');
    let elements = div.querySelectorAll('input, textarea, select');
    let csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    if (action.classList.contains("fa-pen") ){
        let temptextarea = div.querySelector('textarea');
        let data = {func: action.dataset['type'],projectID: project_id,}
        if (temptextarea.style.display === "none"){
            temptextarea.style.display = "block";
        }
        action.classList.remove('fa-pen');
        action.classList.add('fa-check');
        elements.forEach(item => {
            console.log(item);
            if (item.disabled || item.hasAttribute('readonly')) {
                item.disabled = false;
                item.style.backgroundColor = "white";
                item.removeAttribute('readonly');
            }

        });
        fetch('/fetchforcanvas', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            let temp_select = document.createElement('select');
            temp_select.setAttribute('data-type', 'select');            
            temp_select['multiple'] = true;
            temp_select.classList.add('editCanvasSelect');
            if (Object.keys(data).length !== 0){
                for (item in data){
                    let temp_groupdata = document.createElement('optgroup');
                    temp_groupdata.label = item.replace("_"," ").toUpperCase();
                    temp_select.append(temp_groupdata);
                    for (value in data[item]){
                        console.log("here");
                        let group_value = document.createElement('option');
                        group_value.value = data[item][value][1];
                        group_value.textContent = data[item][value][0];
                        temp_groupdata.append(group_value);                        
                    }
                    temp_select.append(temp_groupdata);
                }
                div.append(temp_select);
            }
        })
        .catch(error => {
            console.log(error);
        });
        
    } else {
        let data = {};
        elements.forEach(item => {
            let dataset = item.dataset.type;
            switch (dataset) {
                case "value":
                    data.value = item.value;
                    break;
                case "description":
                    data.description = item.value;
                    break;
                case "select":
                    let selectedOptions = [];
                    item.querySelectorAll('optgroup').forEach(optgroup => {
                        let item_list = [];
                        optgroup.querySelectorAll('option:checked').forEach(option =>{
                            item_list.push(option.value);
                        });
                        let dummy = optgroup.label.replace(" ","_").toLowerCase();
                        selectedOptions.push({[dummy]:item_list});
                    });
                    data.section = selectedOptions;
                    break;
            }
        });
        data.pk = number;
        data.func = action.dataset.type;
        console.log(data);
        let csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        fetch('/editcanvas', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            action.classList.add('fa-pen');
            action.classList.remove("fa-check");
            if (div.querySelector('textarea')){
                expandDiscription(event);
            }
            elements.forEach(element =>{
                if (element.tagName === "SELECT"){
                    console.log(element);
                    element.remove();
                }
                element.setAttribute('readonly','true');
                element.style.backgroundColor = "transparent";
            });

            showNotification(data.message);
        })
        .catch(error => {
            console.log(error);
        });
    }
}

function removeInCanvas(event) {
    if (confirm("Are You Sure?\nItems are Cascade so if its relevant to other items, they would be deleted as well.")){
        let action = event.target;
        console.log("in the removeInCanvas function");
        let itemid = action.value;
        let type = action.dataset.type;
        data = {itemId:itemid, type:type};
        console.log(type);
        let div = action.closest('[data-id]');
        console.log(div)
        let csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        fetch('/removeincanvas',{
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data =>{
            console.log(data);
            showNotification(data.message);
            div.remove();
        }).catch(error =>{  
            console.log(error);
        });
    }
}

function addInCanvas(event){
    console.log("Inside addInCanvas function");
    let functionsWithDescription = ["value-proposition","key-resources","customer-relationship","key-activities","key-partnership","cost-structure"]
    let func = event.target.value;
    console.log(`the func  is ${func}`);
    let funcDiv = event.target;
    funcDiv.style.display = 'none';
    let funcOuterDiv =event.target.closest("div");
    let tempDiv = document.createElement('div');
    tempDiv.classList.add('buildCanvasAddContent');

    let tempInputLabel = document.createElement('label');

    let tempInput = document.createElement("input");
    tempInput.dataset.func = func ;
    tempInput.dataset.value = 'value';
    let closeButton = document.createElement('span');
    closeButton.innerHTML = '';
    closeButton.classList.add('close-button', 'fa-solid', 'fa-xmark');

    let projectID = document.querySelector('#projectname').dataset['id'];
    let csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    fetch('/fetchforcanvas', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            func: func,
            projectID: projectID,
        }),
    })
    .then(response => response.json())
    .then(data => {
        const keys = Object.keys(data);
        if (keys.length > 0 ){
            let tempSelect = document.createElement('select');
            tempSelect.setAttribute('data-value', 'select');            
            tempSelect['multiple'] = true;
    
            keys.forEach(key =>{
                const values = data[key];
                let tempoptgroup = document.createElement('optgroup');
                tempoptgroup.label = key;
                values.forEach(value => {
                    let tempOption = document.createElement('option');
                    tempOption['value'] = value[0];
                    tempOption.textContent = value[0];
                    tempoptgroup.appendChild(tempOption);
                });
                tempSelect.appendChild(tempoptgroup);
            });

            if (functionsWithDescription.includes(func)){
                let temptextarea = document.createElement("textarea");
                temptextarea.dataset.value = "description";
                let tempTextareaLabel = document.createElement('label');
                
                tempTextareaLabel.textContent = 'Description:';
                tempDiv.append(tempTextareaLabel,temptextarea);
            }
            tempDiv.append(tempSelect);
            let tempAddButton = document.createElement('button');
            tempAddButton['type'] = 'button';
            tempAddButton['value'] = func;
            tempAddButton.classList.add('canvasbutton','text-dark');
            tempAddButton.textContent = "Add Item";
            tempAddButton.addEventListener('click', (event)=>{
                submitAddIncanvas(event);
            });
            tempDiv.append(tempAddButton);
        }
    })    
    .catch(error => {
        console.log(error);
    });    
    switch (func){
        case "value-proposition":
            tempInputLabel.textContent = 'Value Proposition:';
            closeButton.dataset.addButton = 'value-proposition-add-button';
            break;
        case "key-resources":
            tempInputLabel.textContent = 'Key Resources:';
            closeButton.dataset.addButton = 'key-resources-add-button';
            break;
        case "customer-relationship":
            tempInputLabel.textContent = 'Customer Relationship:';
            closeButton.dataset.addButton = 'customer-relationship-add-button';
            break;
        case "key-activities":
            tempInputLabel.textContent = 'Key Activities:';
            closeButton.dataset.addButton = 'key-activities-add-button';
            break;
        case "key-partnership":
            tempInputLabel.textContent = 'Key Partnership:';
            closeButton.dataset.addButton = 'key-partnership-add-button';
            break;
        case "cost-structure":
            tempInputLabel.textContent = 'Cost Structure:';
            closeButton.dataset.addButton = 'cost-structure-add-button';
            break;
        case "customer-segment":
            tempInputLabel.textContent = 'Customer Segment:';
            closeButton.dataset.addButton = 'customer-segment-add-button';
            break;
        case "channel":
            console.log("here");
            tempInputLabel.textContent = 'Channels:';
            closeButton.dataset.addButton = 'channel-add-button';
            break;
        case "revenue-stream":
            tempInputLabel.textContent = 'Revenue Streams:';
            closeButton.dataset.addButton = 'revenue-stream-add-button';
            break;
    }

    closeButton.onclick = function() {
        console.log(closeButton);
        let y = closeButton.closest('div');
        console.log(y);
        let x = closeButton.dataset.addButton;
        console.log(x);
        y.remove();
        console.log(document.querySelector(`#${x}`));
        document.querySelector(`#${x}`).style.display = 'block';
        
    };

    tempDiv.append(closeButton,tempInputLabel,tempInput);
    if (func === "value-proposition"){
        let temptextarea = document.createElement("textarea");
        temptextarea.dataset.value = "description";
        let tempTextareaLabel = document.createElement('label');
        
        tempTextareaLabel.textContent = 'Description:';
        tempDiv.append(tempTextareaLabel,temptextarea);

        let tempAddButton = document.createElement('button');
        tempAddButton['type'] = 'button';
        tempAddButton['value'] = func;
        tempAddButton.classList.add('canvasbutton','text-dark');
        tempAddButton.textContent = "Add Item";
        tempAddButton.addEventListener('click', (event)=>{
            submitAddIncanvas(event);
        });
        tempDiv.append(tempAddButton);
    }
    funcOuterDiv.insertAdjacentElement('afterend', tempDiv);
}

function submitAddIncanvas(event){
    action = event.target;
    let div = action.closest('div');
    console.log(div);
    let projectname = document.querySelector("#projectname").value;
    let data = {}
    data.model = action.value;
    data.projectname = projectname;
    div.querySelectorAll('input, textarea , select').forEach(element =>{
        console.log("element");
        console.log(element);
        let type = element.dataset.value;
        switch (type) {
            case "value":
                console.log("value")
                let value = element.value;
                console.log(value);
                data.value = value;
                break;
            case "description":
                let description = element.value;
                console.log(description);
                data.description = description;
                break;
            case "select":
                console.log("select");
                element.querySelectorAll('optgroup').forEach(optgroup => {
                    console.log("select2");
                    let groupName = optgroup.label;
                    let selectedOptions = [];
                    optgroup.querySelectorAll('option:checked').forEach(option => {
                        selectedOptions.push(option.value);
                    });
                    data[groupName] = selectedOptions;
                });
                break;
                
        }
    });
    console.log("The data gathered is : ");
    console.log(data);
    let csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    fetch('/addincanvas',{
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body : JSON.stringify(data),
    })
    .then(response => {
        if (response.ok){
            return response.json();
        } else {
            throw new Error('Network response were not OK');
        }
    })
    .then(data =>{
        console.log("the div is this div");
        console.log(div);
        div.remove()
        addNewItemDivInCanvas(data);
        showNotification(`${data.section} added successfully`);
    })
    .catch(error => {
        console.log(error);
    });
}

function addNewItemDivInCanvas (divdata){
    console.log("here to add new item");
    console.log(divdata);
    let maindiv = document.querySelector(`#${divdata.section}-main-div`);
    let data = divdata.data;
    console.log(data);
    let instance = maindiv.querySelector('[data-id]').cloneNode(true);
    console.log("the maindiv is");
    console.log(maindiv);

    instance.setAttribute('data-id', `${data.id}`);
    instance.querySelector('[data-type=value]').setAttribute('value',`${data.value}`);
    instance.querySelector('[data-type=value]').onclick = expandDiscription;
    instance.querySelector('[data-mode="edit"]').setAttribute('value',`${data.id}`);
    instance.querySelector('[data-mode="edit"]').onclick = editInCanvas;
    instance.querySelector('[data-mode="remove"]').setAttribute('value',`${data.id}`);
    instance.querySelector('[data-mode="remove"]').onclick = removeInCanvas;
    if (instance.querySelector('[data-type="description"]')){
        instance.querySelector('[data-type="description"]').textContent = data.description;
    }
    instance.querySelector('input').setAttribute('data-viewid',`${data.id}`);
    maindiv.append(instance);

    console.log(`data.section is ${divdata.section}`);
    let addbutton = document.querySelector(`#${divdata.section}-add-button`);
    addbutton.style.display = "block";
}

function showNotification(text) {
    var notification = document.querySelector('#notification');
    console.log(text);
    if (text.includes("removed")){
        console.log("yes");
        notification.style.backgroundColor = "red";
    } else if (text.includes("added")){
        notification.style.backgroundColor = "green";
    } else if (text.includes("updated")){
        notification.style.backgroundColor = "orange";
    }
    notification.textContent = ` ${text.replace(/-/g, " ")}`;
    notification.style.display = 'block';
    setTimeout(function() {
        notification.style.display = 'none';
    }, 2000);
}

function expandDiscription(event){
    console.log(event);
    let x = (event.target).parentNode;
    let div = x.parentNode.parentNode;
    console.log(div);
    let textarea = div.querySelector(".buildCanvasTextarea");
    if (textarea.style.display === "block"){
        textarea.style.display = "none"
    } else {
        textarea.style.display = "block";
        textarea.style.height = "auto";
        textarea.style.height = textarea.scrollHeight + "px";
    }
}