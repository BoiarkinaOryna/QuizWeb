const addAvatarButton = document.getElementById("addAvatarButton");
const addAvatarInput = document.getElementById("addAvatarInput");

addAvatarButton.addEventListener("click", ()=>{
    addAvatarInput.click();
})

addAvatarInput.addEventListener("input", ()=>{
    let formData = new FormData();
    imageData = addAvatarInput.files[0];
    console.log("imageData", imageData);
    formData.append('image', imageData);
    console.log("data =", formData, document.cookie.split("csrftoken=")[1].split(";")[0]);
    $.ajax({
        url: '/settings/save_image',
        type: "post",
        data: formData,
        contentType: false,
        processData: false,
        headers: {'X-CSRFToken': document.cookie.split("csrftoken=")[1].split(";")[0]},
        success: hideDefaultAvatar()
    })
})

function hideDefaultAvatar(){
    showImage(imageData, addAvatarInput.id);
    document.getElementById("defaultAvatar").style.display = "none";
}