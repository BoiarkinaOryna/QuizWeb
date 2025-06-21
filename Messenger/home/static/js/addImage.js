const imageDivList = document.getElementsByClassName("add-image");
// const sendImageButtonList = document.getElementsByClassName("addImageButton");
const addImageInputList = document.getElementsByClassName("addImageInput");

const showImageDivList = document.getElementsByClassName("post-image");
const tempContainer = document.getElementsByClassName("temp-image-container")[0];

for (let addImageInput of addImageInputList){
    addImageInput.addEventListener("change", ()=>{
        let formData = new FormData();
        imageData = addImageInput.files[0];
        console.log("imageData", imageData);
        formData.append('image', imageData);
        console.log("data =", formData, document.cookie.split("csrftoken=")[1].split(";")[0]);
        $.ajax({
            url: '/load_image/',
            type: "post",
            data: formData,
            contentType: false,
            processData: false,
            headers: {'X-CSRFToken': document.cookie.split("csrftoken=")[1].split(";")[0]},
            success: function(response){showImage(imageData, response.width, response.height, response.email)}
        })
    })
}

function showImage(image, width, height, email) {
    const container = document.getElementsByClassName("temp-image-container")[0];

    if (typeof staticBase === "undefined") {
        console.error("staticBase is undefined");
        return;
    }

    const fullPath = `${staticBase}${email}/${image.name}`;
    console.log("Inserting image at path:", fullPath);

    console.log(width, height);
    let imgClass;
    if (width > height){
        imgClass = 'horizontal-image';
    } else{
        imgClass = 'vertical-image';
    }

    container.insertAdjacentHTML(
        "afterbegin",
        `<img src="${fullPath}" class=${imgClass}>`
    );
}