let groupPk = 1

const webSocket = new WebSocket(`ws://${window.location.host}/chat/${groupPk}`)

let messageForm = document.querySelector('#message')
// Додаємо подію до форми
messageForm.addEventListener(
    type = 'submit',
    (event) =>{
        // Прибираэмо стан форми за замовчуванням, щоб вона не відправлялась
        event.preventDefault();
        // Отримуємо значення повідомлення
        let data_message = event.target.message.value;
        // Відправляємо повідомлення на сервер у форматі json
        webSocket.send(JSON.stringify({
            'message': data_message
        }));
        event.target.message.value = '';
    }
)


webSocket.onmessage = function(event){
    // Парсимо дані в javascript об єкт
    let data = JSON.parse(event.data)
    console.log('Data: ', data)
    if (data.type === 'chat' ){
        let messages = document.getElementById('messagesBlock')
        // Створюємо обєкт дати з отриманої дати
        let date_time = new Date(data.date_time)
        // Локалізумо дату 
        date_time = date_time.toLocaleString()
        // Додаємо повідомлення в кінець messages
        messages.insertAdjacentHTML(
            'beforeend',
            // `<div><p><b>${data.username}: </b>${data.message} (${date_time})</p></div>`
            `<div class="message">
                <div class="avatar"></div>
                <div class="message-content">
                    <span class="message-text">
                        <h4 class="sender">
                            ${data.username}
                        </h4>
                        ${data.message}
                    </span>
                    <div class="message-time">
                        ${date_time}
                        <img src="" alt="" class="small-img">
                    </div>
                </div>
            </div>`
        )
    }
}

// let dateTimeList = document.getElementsByClassName("message-time");
// // 
// for (let dateTime of dateTimeList){
//     // 
//     let currentDate = new Date(dateTime.textContent);
//     // 
//     console.log("c date =", currentDate);
//     currentDate = currentDate.toLocaleString();
    
//     currentDate = currentDate.split(" ")[3];
//     // 
//     dateTime.textContent = currentDate;
// }