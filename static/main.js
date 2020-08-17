
function show_alert(message){
    document.querySelector("#message").innerHTML = message;
    document.querySelector("#alert").style.display = "block";
}

function close_alert() {
    document.querySelector("#alert").style.display = "none";
}

function slider_label(element) {
    let lables = ["minimalist", "simple", "elaborate","quite specific","extreemly bossy"];
    let lable = lables[element.value];
    let href = "/?level=" + element.value;
    document.querySelector("#slider_label").innerHTML = lable;
    document.querySelector("#change_level").href = href;
}

function display_options() {
    options = document.querySelector("#options")
    if (options.style.display === "none") {
        options.style.display = "block";
    } else {
        options.style.display = "none";
    }
}
