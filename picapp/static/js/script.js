const dropDIV = document.querySelector("#drop_zone")
const fileField = document.querySelector("#file")

dropDIV.addEventListener("drop", event => {
  event.preventDefault();
  console.log('File(s) dropped');

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
  }
})

dropDIV.addEventListener("dragover", event => {
  console.log('File(s) in drop zone');
  event.preventDefault();
})
