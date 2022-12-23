const userPhotoDiv = document.querySelector(".user-photo")

if (userPhotoDiv){
    userPhotoDiv.addEventListener("click",  async (event) => {
        if ([...event.target.classList].includes("generate-link-btn")){
            const photo = event.target.dataset["photo"];
            let res = await fetch('http://192.168.0.136/exp-link/' + photo);
            data = await res.json();
            console.log(data["web_address"]);

        }
    })
}