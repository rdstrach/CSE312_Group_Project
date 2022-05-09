
socket = new WebSocket('ws://' + window.location.host + '/DM_websocket');
socket.onmessage = function (ws_message) {

    const jsonData = JSON.parse(ws_message.data);

}
function inputdata(username, comment) {
    socket.send(JSON.stringify({ 'username':username,'message': comment}));
}
function sendMessage() {

    const sendto = document.getElementById("chat-username");
    const username = sendto.value;
    const chatBox = document.getElementById("chat-comment");
    const comment = chatBox.value;
    chatBox.value = "";
    chatBox.focus();
    if (comment !== "") {
        /*
        username:  username of recipient
        comment: message to send to username
        */
        inputdata(username,comment)
    }
}
function request_data(){
    socket.send("")//send blank message periodically to receive messages

    }
function page() {
setInterval(request_data,200)
}

