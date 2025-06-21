document.addEventListener("click", ()=>{

    let buttonList = document.getElementsByClassName("confirm-button");
    let decButtonList = document.getElementsByClassName("decline-button");
    const mainBlock = document.querySelector(".main-block");

    for(let button of buttonList){
        addListener(button);
    }

    for (let decButton of decButtonList){
        addListener(decButton);
    }

    function addListener(button){
        button.addEventListener("click", ()=>{
            let formData = new FormData();
            formData.append('user_id', button.id);
            let type = button.value;
            $.ajax({
                url: `/friends/${type}/`,
                type: "post",
                data: formData,
                contentType: false,
                processData: false,
                headers: {'X-CSRFToken': document.cookie.split("csrftoken=")[1].split(";")[0]},
                success: function(){$(".main-block").load(window.location.href + " .main-block > *")}
            })
        })
    }

})