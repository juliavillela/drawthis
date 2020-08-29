
function show_alert(message){
    document.querySelector("#message").innerHTML = message;
    document.querySelector("#alert").style.display = "block";
}

function close_alert() {
    document.querySelector("#alert").style.display = "none";
}

function update_slider() {
    let input = document.querySelector("#slider_input")
    let lables = ["minimalist", "basic", "fairly detailed", "quite specific", "elaborate", "a tad overdone", "extreemly bossy"];
    let lable = lables[input.value];
    let href = "/?level=" + input.value;
    document.querySelector("#slider_label").innerHTML = lable;
    document.querySelector("#change_level").href = href;
}

function display_options() {
    let options = document.getElementById("options");
    let background = document.getElementById("pop-up-background");
    update_slider();
    background.style.display = "block";
    background.className += " active";
    options.style.display = "block";
}

function close_popup(popup_id){
    let options = document.getElementById(popup_id);
    let background = document.getElementById("pop-up-background");
    options.style.display = "none";
    background.className.replace("active", "");
    background.style.display = "none";
}

function search_regex() {
    let string = document.querySelector("#search_input").value;
    let table = document.querySelector("#table").children[2];
    let table_row = table.children;
    for (let i = 0; i < table_row.length ; i++) {

        table_row[i].className = "search-hidden";
        let table_data = table_row[i].children;

        for (let j = 1; j < table_data.length - 1 ; j++) {
            let data_string = table_data[j].innerHTML;
            if (data_string.match(string)) {
                table_row[i].className = "search-found";
            }
        }
    }
    document.querySelector("#search-box").className = "active";
}

function end_search() {
    let table = document.querySelector("#table").children[2];
    let table_row = table.children;
    for (let i = 0; i < table_row.length ; i++) {

        table_row[i].className = null;
    }
    document.querySelector("#search_input").value = "";
    document.querySelector("#search-box").className = null;
}

function open_dialogue(id){
    document.getElementById("pop-up-background").style.display = "block"
    document.getElementById(id).style.display = "grid";

}

function close_dialogue(id) {
    document.getElementById(id).style.display = "none";
    document.getElementById("pop-up-background").style.display = "none"
}


function edit_mode(element_id) {
    let element = document.getElementById(element_id);
    let parent = document.getElementById('user-stuff');
    let siblings = parent.children
    for (let i = 0; i < siblings.length ; i++) {
        if (siblings[i] !== element) {
            siblings.open = false;
        }
    }
    element.open = true;
    element.style.height = "100%"
}

function image_form(form_id, item_id){
    let form = document.getElementById(form_id);
    let item = document.getElementById(item_id);
    form.innerHTML = item.cloneNode(true);
    open_dialogue(form_id);
}

function alert() {
    document.getElementById("alert").className += " active";
}

function close_alert() {
    document.getElementById("alert").style.padding=0;
}
