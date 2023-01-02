const userPhotoDiv = document.querySelector(".user-photo")



if (userPhotoDiv){
    userPhotoDiv.addEventListener("click",  async (event) => {
        if ([...event.target.classList].includes("generate-link-btn")){
            const photo = event.target.dataset["photo"];
            const linkTime = Number(document.getElementById("generate-link-time-" + photo).value);
            if(linkTime){
            const data = { time: linkTime};
            let res = await fetch('http://192.168.0.136/exp-link/' + photo, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(data),
            })
            const response = await res.json();
            const link = response["web_address"]
            document.querySelector(".generate-link-p-"+photo).textContent = link
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