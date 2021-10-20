const socket = io.connect();

// DOM variables:
const message = document.getElementById('message'),
    name = document.getElementById('name'),
    btn = document.getElementById('send'),
    output = document.getElementById('output'),
    answer = document.getElementById('answer');

//event listener for when a button is clicked
btn.addEventListener('click', () => {
    socket.emit('message', {
        message: message.value,
        name: name.value
    })
    message.value = '';
})
//event listener for when a message is being typed (it sends the type and the person who is typing)
message.addEventListener('keypress', () => {
    socket.emit('typing', name.value);
})

//display message from the server in the chat
socket.on('message', (data) => {
    answer.innerHTML = '';
    output.innerHTML += `<p><strong> ${data.name} : </strong> ${data.message} </p>`;
})

//display the typing from the server in chat
socket.on('typing', (data) => {
    answer.innerHTML = `<p><em> ${data} is typing..</em></p>`;
})