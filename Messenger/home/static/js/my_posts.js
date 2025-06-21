const optionDivsList = document.querySelectorAll(".dots");

for (let optionDiv of optionDivsList){
    optionDiv.addEventListener("click", ()=> {
        let id = optionDiv.id;
        console.log("id =", id)
        let form = document.getElementById(`form-${id}`);
        console.log("form =", form)
        if (form.classList.contains("hidden-form")){
            form.classList.remove("hidden-form");
            form.classList.add("visible-form");
        }else if (form.classList.contains("visible-form")){
            form.classList.add("hidden-form");
            form.classList.remove("visible-form");
        }
    })
}