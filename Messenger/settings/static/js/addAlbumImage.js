const addImageInputsList = document.getElementsByClassName("add-image-input");
console.log("addImageInputsList =", addImageInputsList);

for (let addImageInput of addImageInputsList){
    addImageInput.addEventListener("change", ()=>{
        let formData = new FormData();
        imageData = addImageInput.files[0];
        console.log("imageData", imageData);
        formData.append('image', imageData);
        const albumName = document.getElementById("albumName").textContent;
        formData.append('albumName', albumName);
        console.log("data =", formData, document.cookie.split("csrftoken=")[1].split(";")[0]);
        $.ajax({
            url: '/settings/save_album_image',
            type: "post",
            data: formData,
            contentType: false,
            processData: false,
            headers: {'X-CSRFToken': document.cookie.split("csrftoken=")[1].split(";")[0]},
            success: showImage(imageData)
        })
    })
}

function showImage(image) {
    const container = document.getElementsByClassName("album-images")[1];
    container.insertAdjacentHTML(
        "afterbegin",
        `<div style="background: url('http://127.0.0.1:8000/media/images/post/${image.name}');" class="image button-bottom">
            <button class="header-button round" type="button">
                <img class="header-image" src="{% static 'images/eye.png' %}" alt="">
            </button>
            <button class="header-button round" type="button">
                <img class="header-image" src="{% static 'images/trashcan.png' %}" alt="">
            </button>
        </div>`
    );
}