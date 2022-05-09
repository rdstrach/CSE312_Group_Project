// https://bulma.io/documentation/elements/notification/#javascript-example
document.addEventListener('DOMContentLoaded', () => {
    (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
        const $notification = $delete.parentNode;

        $delete.addEventListener('click', () => {
            $notification.parentNode.removeChild($notification);
        });
    });
});

socket = new WebSocket('ws://' + window.location.host + '/DM_websocket');
var chatmsgId=1;
function addMessage(chatMessage) {
    let chat = document.getElementById('chat');
    // chat.innerHTML += "<b>" + chatMessage['username'] + "</b>: " + chatMessage["message"] + "<br/>";
    let msgId="msg_"+chatmsgId.toString();

    chat.innerHTML += "<div class=\"notification\" id=\""+msgId+"\"><button class=\"delete\" onclick=\"delete_message("+chatmsgId.toString()+")\"></button><b>" + chatMessage['username']
        + " says:</b><br>" + chatMessage["message"] + "<br><br></div>"
    chatmsgId++;
}
function delete_message(id){
let msgId="msg_"+id.toString();
document.getElementById(msgId).style.display = "none";
}
function show_dm() {
    let chat = document.getElementById('chat');
    chat.innerHTML += "<div class=\"notification\"><button class=\"delete\"></button><b>Send message to:</b><br>" +
        "<input class=\"input\" id=\"chat-username\" type=\"text\" placeholder=\"username\"><br>" +
        "<input class=\"input\" id=\"chat-comment\" type=\"text\" placeholder=\"Message\">" +
        "<br><br><button onClick=\"sendMessage()\">send</button></div>"
}

socket.onmessage = function (ws_message) {
    console.log(ws_message['data'])

    const jsonData = JSON.parse(ws_message.data);
    const chatBox = document.getElementById("chat-comment");
    const comment = chatBox.value;
    addMessage(jsonData);

}

function inputdata(username, comment) {
    socket.send(JSON.stringify({'username': username, 'message': comment}));
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
        inputdata(username, comment)
    }
}

function request_data() {
    socket.send("")//send blank message periodically to receive messages

}


function page() {
    setInterval(request_data, 200)
}

const socket_upvote = new WebSocket('ws://' + location.host + '/upvote');

socket_upvote.addEventListener('message', event => {
    const json_obj = JSON.parse(event.data)
    document.getElementById('upvotes' + json_obj.id).innerHTML = "Votes: " + json_obj.votes;
});

function upvote_button(tm_id) {
    socket_upvote.send('{"messageType": "upvote", "id": "' + tm_id + '"}');
}

socket.onopen = function (msg) {
    console.log("WS connection has been opened" + msg)

}
socket.onclose = function () {
    console.log("WS connection has been closed")
}
