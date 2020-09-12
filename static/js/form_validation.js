let current_form = null;
let input_array = []

function none_empty() {
    let complete = true;
    let inputs = [];
    let button = document.getElementById('submit');
    if (current_form === null) {
        inputs = document.getElementsByTagName('input');
    } else {
        inputs = input_array;
        button = input_array[input_array.length - 1];
    }
    for(let i = 0; i < inputs.length; i++) {
        let error = inputs[i].className.search("issue")
        if( inputs[i].value === "" || error !== -1){
            complete = false;
        }
    }
    if(complete){
        button.disabled = false;
        button.focus();
    }else {
        button.disabled = true;
    }
}

function username_unique(input, usernames) {
    let username_div = document.getElementById('username')
    let unique = true;
    for(let i = 0; i < usernames.length; i++) {

        if (input.value === usernames[i]){
            if (input.className.search("issue") === -1){
                unique = false;
                input.className += " issue";
                username_div.children[2].innerHTML="this username is already taken";
                document.getElementById('submit').disabled = true;
            }
        }
    }
    if (unique){
        none_empty();
    }
}

function clear_issues(id) {
    let element = document.getElementById(id);
    element.children[2].innerHTML = "";
    element.children[1].className = element.children[1].className.replace(" issue", "");
}


function password_match() {
    let password_div = document.getElementById('password');
    let confirmation_div = document.getElementById('password-confirmation');
    let input = confirmation_div.children[1]
    if (input.value !== "" && input.value !== password_div.children[1].value){
        if (input.className.search("issue") === -1){
            input.className += " issue";
            confirmation_div.children[2].innerHTML="passwords don't match!";
            document.getElementById('submit').disabled = true;
        }
    } else {
        none_empty()
    }
}

function toggle_edit(id) {
    let element = document.getElementById(id);
    element.style.display ="table-row"
}

function set_form(form_id) {
    current_form = document.getElementById(form_id);
    input_array = [];
    let children = current_form.children;
    for(let i = 0; i < children.length; i++){
        let tag = children[i].tagName;
        if (tag === 'INPUT'){
            input_array.push(children[i]);
        }else{
            let inner_children = children[i].children;
            for (let j=0; j < inner_children.length; j++) {
                let tag = inner_children[j].tagName;
                if (tag === 'INPUT') {
                    inner_children[j].value = "";
                    input_array.push(inner_children[j]);
                }
            }
        }
    }
}

function open_form_dialogue(dialogue_id, form_id) {
    document.getElementById("pop-up-background").style.display = "block"
    document.getElementById(dialogue_id).style.display = "grid";
    set_form(form_id);
}
