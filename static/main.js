
function show_alert(message){
    document.querySelector("#message").innerHTML = message;
    document.querySelector("#alert").style.display = "block";
}

function close_alert() {
    document.querySelector("#alert").style.display = "none";
}
