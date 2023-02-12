const userPhotoDiv = document.querySelector(".user-photo")



if (userPhotoDiv){
    userPhotoDiv.addEventListener("click",  async (event) => {
        if ([...event.target.classList].includes("generate-link-btn")){
            const photoNumber = event.target.dataset["photo"];
            const linkTime = Number(document.getElementById("generate-link-time-" + photoNumber).value);
            if(linkTime){
            const data = { image: photoNumber,
                            time: linkTime};
            let res = await fetch('http://192.168.0.136/api/v1/createExpiresLink/', {
              method: 'POST',
              headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(data),
            })
            const response = await res.json();
            const link = "http://192.168.0.136/e/" + response["link"]
            console.log(response)
            document.querySelector(".generate-link-p-"+photoNumber).textContent = link
            console.log(link);
            }
        }

        if ([...event.target.classList].includes("show-thumbnails-link")){
            photo_number = event.originalTarget.dataset['photo'];
            const value2 = document.querySelector(`.thumbnails-div-${photo_number}`)
            value2.classList.toggle("hide")
        }

    })
}