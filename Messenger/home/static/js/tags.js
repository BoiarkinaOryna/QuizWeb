const tagList = document.getElementsByTagName("input[type='checkbox']");
const textArea = document.querySelector("textarea");

for (let tag of tagList){
    tag.addEventListener("checked", ()=>{
        let currentTags = textArea.textContent.split("\n")[1];
        if (currentTags != ""){
            currentTags += ` ${tag.textContent}`;
        } else{
            currentTags = `\n ${tag.textContent}`;
        }
        textArea.textContent = textArea.textContent.split("\n")[0] + currentTags;
    })
}