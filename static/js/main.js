
function show_alert(message){
    document.querySelector("#message").innerHTML = message;
    document.querySelector("#alert").style.display = "block";
}

//options form:

function update_slider() {
    let input = document.querySelector("#slider_input");
    let lables = ["minimalist", "basic", "fairly detailed", "quite specific", "elaborate", "a tad overdone", "extreemly bossy"];
    let lable = lables[input.value]
    document.querySelector("#slider_label").innerHTML = lable;
}

function custom_deck() {
    let input = document.getElementById("toggle-decks");
    let lang = document.getElementById("language-block");
    let deck = document.getElementById("deck-block");
    let input_area = deck.children[1];
    let level = document.getElementById("slider_input");
    if (input.checked === true) {
        // if uses picks custom deck, disable language and display deck-list
        lang.style.display = "none";
        input_area.style.display = "grid";
        level.max = 2;
    } else {
        // else, enable language choice and hide list
        level.max = "initial";
        lang.style.display = "grid";
        input_area.style.display = "none";
    }
}

function update_checks() {
    let lang = document.getElementById("language-block");
    check_curr_value(lang);
    let deck = document.getElementById("deck-block");
    if (deck) {
        let custom = check_curr_value(deck);
        let input_title = deck.children[0];
        if (custom) {
            input_title.children[0].checked = true;
            custom_deck();
        }
    }
}

function check_curr_value(input_block) {
    let input_area = input_block.children[1];
    let inputs = input_area.children;
    let curr = inputs[0].value;
    for(let i = 1; i < inputs.length; i++) {
        if (inputs[i].children[0].value === curr) {
            inputs[i].children[0].checked = true;
            return true;
        }
    }
    return false;
}

function display_options() {
    let options = document.getElementById("options");
    let background = document.getElementById("pop-up-background");
    update_slider();
    update_checks();
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
    // let table = document.querySelector("#table").children[2];
    // let table_row = table.children;
    let table_row = document.querySelector("#table-content").children
    for (let i = 0; i < table_row.length ; i++) {

        table_row[i].className = "search-hidden";
        let table_data = table_row[i].children;

        for (let j = 0; j < table_data.length - 1 ; j++) {
            let data_string = table_data[j].innerHTML;
            if (data_string.match(string)) {
                table_row[i].className = "search-found";
            }
        }
    }
    document.querySelector("#search-box").className = "active";
}

function end_search() {
    // let table = document.querySelector("#table").children[2];
    // let table_row = table.children;
    let table_row = document.querySelector("#table-content").children
    for (let i = 0; i < table_row.length ; i++) {

        table_row[i].className = null;
    }
    document.querySelector("#search_input").value = "";
    document.querySelector("#search-box").className = null;
}


function upload_with_cards(bookmark_id, dialogue_id) {
    document.getElementById('bookmark_id').value = bookmark_id;
    open_dialogue(dialogue_id);
}

function open_dialogue(id){
    document.getElementById("pop-up-background").style.display = "block"
    document.getElementById(id).style.display = "grid";
}

function close_dialogue(id) {
    document.getElementById(id).style.display = "none";
    document.getElementById("pop-up-background").style.display = "none"
}



function alert() {
    document.getElementById("alert").style.padding = "2em";
}

function close_alert() {
    document.getElementById("alert").style.display = "none";
}



// function add_card_input(){
// // on key up create another input slot
//     let template = document.getElementById("card_input");
//     let parent = document.getElementById("cards_section");
//     let count = parent.children.length-1;
//     let clone = template.cloneNode(true);
//     clone.id = "unset";
//     clone.name = "card_" + count;
//     clone.value = "";
//     parent.insertBefore(clone, parent.children[count]);
// }

function display(element_id) {
    element = document.getElementById(element_id);
    if (element.style.display === "none") {
        element.style.display = "block";
    } else {
        element.style.display = "none";
    }
}


function collapse_ui() {
    let ui_block  = document.getElementById("user-info");
    if (ui_block.style.marginLeft !== "-262px") {
        ui_block.style.marginLeft = "-262px";
    }
    document.getElementById("invisible-collapse").style.display="none";
}

function open_ui() {
    let ui_block  = document.getElementById("user-info");
    if (ui_block.style.marginLeft === "-262px") {
        ui_block.style.marginLeft = 0;
    }
    document.getElementById("invisible-collapse").style.display="block";
}


function edit_cards() {
    document.getElementById("static-cards").style.display = "none";
    document.getElementById("static-buttons").style.display = "none";
    document.getElementById("edit-cards").style.display = "block";
    document.getElementById("edit-buttons").style.display = "block";
}

function cancel_edit_cards() {
    document.getElementById("static-cards").style.display = "block";
    document.getElementById("static-buttons").style.display = "block";
    document.getElementById("edit-cards").style.display = "none";
    document.getElementById("edit-buttons").style.display = "none";
}
