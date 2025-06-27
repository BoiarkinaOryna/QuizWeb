const groupObjects = document.getElementsByClassName("group-item");

for (let group of groupObjects){
    group.addEventListener("click", ()=>{
        let formData = new FormData();
        formData.append('group_id', group.id);
        $.ajax({
            url: `/chats/`,
            type: "post",
            data: formData,
            contentType: false,
            processData: false,
            headers: {
                'X-CSRFToken': document.cookie.split("csrftoken=")[1].split(";")[0],
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(response){
                $(".main-s").html(response);
                document.querySelector(".main-s").style.justifyContent = "space-between";
            }
        })
    })
}