const form = document.querySelector(".new-group-form");
const saveGroupButton = document.querySelector(".continue");

saveGroupButton.addEventListener('click', ()=>{
    document.querySelector(".search2").remove();
    const formData = new FormData(form);
    $.ajax({
        url: '/chats/create_group/',
        type: "post",
        data: formData,
        contentType: false,
        processData: false,
        headers: {'X-CSRFToken': document.cookie.split("csrftoken=")[1].split(";")[0]},
        error: function(){
            document.querySelector('.active-dark-background').style.display = 'none';
        }
    })
})