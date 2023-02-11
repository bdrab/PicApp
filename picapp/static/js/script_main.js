const dropDIV = document.querySelector("#drop_zone")
const fileField = document.querySelector("#file")
const chosenFilesList = document.querySelector(".chosen-files-list")
const submitBTN = document.querySelector(".btn-submit")
const FILE_SIZE = 4194304

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');


if(fileField){
    fileField.addEventListener("change", event => {
        chosenFilesList.textContent = "";
        [...fileField.files].forEach(item =>{
            if (item.size <= FILE_SIZE){
                const li = document.createElement("li");
                chosenFilesList.append(li);
                li.textContent = item["name"];
            }
        })
    })
}
if(dropDIV){
    dropDIV.addEventListener("drop", event => {
        event.preventDefault();
        let formData = new FormData();
        let dataTransfer = new DataTransfer();
        if (event.dataTransfer.items) {
            [...event.dataTransfer.items].forEach(item => {
                const file = item.getAsFile();
                if ((file.type === "image/png" ||
                    file.type === "image/gif" ||
                    file.type === "image/jpeg") && file.size <= FILE_SIZE){
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
}
if(submitBTN){
    submitBTN.addEventListener("click", async event => {
        let filesCounter = Array.from(fileField.files).length
        if(filesCounter != 0){
            let data = new FormData()

            Array.from(fileField.files).forEach(element => {
                data.append('photo', element)
            })

            let response = await fetch('http://192.168.0.136/api/v1/', {
                            method: "POST",
                            headers: {'X-CSRFToken': csrftoken},
                            body: data
                            });

            responseData = await response.json();
            responseStatus = await response.status

            if(responseStatus === 201){
                chosenFilesList.textContent = "Uploaded successfully!";
                fileField.files = (new DataTransfer()).files;

            }else{
                chosenFilesList.textContent = "Uploaded failed!";
                fileField.files = (new DataTransfer()).files;
            }
        }
    })
}