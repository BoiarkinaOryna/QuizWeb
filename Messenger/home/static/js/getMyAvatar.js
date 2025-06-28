const my_avatar = document.querySelector(".my-avatar");

try{
    let avatar = document.cookie.split("my_avatar=")[1].split(";")[0];
    avatar = avatar.replace(/"/g, ''); 
    console.log(1, `http://127.0.0.1:8000/media/${avatar}`);
    my_avatar.style.backgroundImage = `url("http://127.0.0.1:8000/media/${avatar}")`;
} catch{
    $.ajax({
        url: '/get_avatar/',
        type: "post",
        contentType: false,
        processData: false,
        headers: {'X-CSRFToken': document.cookie.split("csrftoken=")[1].split(";")[0]},
        success: function(){
            let avatar = document.cookie.split("my_avatar=")[1].split(";")[0];
            avatar = avatar.replace(/"/g, ''); 
            console.log(2, `http://127.0.0.1:8000/media/${avatar}`);
            my_avatar.style.backgroundImage = `url("http://127.0.0.1:8000/media/${avatar}")`;
        },
        error: function(){
            my_avatar.style.backgroundImage = `url("https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small_2x/default-avatar-icon-of-social-media-user-vector.jpg")`;
        }
    })
}