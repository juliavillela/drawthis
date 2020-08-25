
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
    options = document.querySelector("#options")
    if (options.style.display === "none") {
        update_slider();
        options.style.display = "block";
    } else {
        options.style.display = "none";
    }
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

function create_form() {
    document.querySelector("#create_form").style.display = "grid";
}

function close_create_form() {
    document.querySelector("#create_form").style.display= "none";
    document.querySelector("#create_form").value = "";
}

function open_dialogue(id){
    document.getElementById(id).style.display = "grid";
}

function close_dialogue(id) {
    document.getElementById(id).style.display = "none";
}
