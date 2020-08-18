
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
