document.addEventListener('DOMContentLoaded', () => {
        var socket = io.connect('http://' + document.domain + ':' + location.port + '/_chat_app');
        socket.on('connected', () =>{
            socket.send('iam connected')
        });
        socket.on('message', data => {
            console.log(`message recieved : ${data}`)

        });
});