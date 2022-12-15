const dropDIV = document.querySelector("#drop_zone")
const fileField = document.querySelector("#file")
const chosenFilesList = document.querySelector(".chosen-files-list")



fileField.addEventListener("change", event => {
    chosenFilesList.textContent = "";
    [...fileField.files].forEach(item =>{
        const li = document.createElement("li");
        chosenFilesList.append(li);
        li.textContent = item["name"];
    })
})

dropDIV.addEventListener("drop", event => {
  event.preventDefault();
  let formData = new FormData();
  let dataTransfer = new DataTransfer();

  if (event.dataTransfer.items) {
    [...event.dataTransfer.items].forEach(item => {
        const file = item.getAsFile();
        if ((file.type === "image/png" ||
            file.type === "image/gif" ||
            file.type === "image/jpeg") && file.size <= 3000000){
                dataTransfer.items.add(file);
        }
    })
    fileField.files = dataTransfer.files;
    fileField.dispatchEvent(new Event("change"))
  }
})

dropDIV.addEventListener("dragover", event => {
  event.preventDefault();
})
