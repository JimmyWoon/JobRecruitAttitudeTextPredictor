const form = document.querySelector("form"),
browse = document.getElementById("browseBtn"),
fileInput = form.querySelector(".file-input"),
// uplaodFile = form.querySelector(".submit"),
progressArea = document.querySelector(".progress-area.name"),
uploadedArea = document.querySelector(".upload-area");

// cannot use form to activate the browse button because information form is under form 
// form.addEventListener("click", ()=>{  
//     fileInput.click();
// });

browse.addEventListener("click", ()=>{
    fileInput.click();

});
window.addEventListener("dragover",function(e){
    e = e || event;
    e.preventDefault();
},false);
window.addEventListener("drop",function(e){
    e = e || event;
    e.preventDefault();
},false);

form.addEventListener("drop", e => {
    e.preventDefault();
    if(e.dataTransfer.files.length){
        target = e.dataTransfer.files;
        // target = e.dataTransfer.files[0];
        // updateFile(uploadedArea,e.dataTransfer.files[0]);
        uploadedArea.innerHTML = null;

        for (let i = 0; i < target.length; i++) {   
            let fileName = target[i].name;
            var shortFileName;
            // const reader = new FileReader();
            if (fileName.length >=12){
                let splitName = fileName.split('.');
                shortFileName = splitName[0].substring(0,10) + "... ." + splitName[1];
            }else{
                shortFileName = fileName;
            }
            // console.log(reader.readAsDataURL(target));
            if (fileName.includes(".pdf") || fileName.includes(".jpeg") || fileName.includes(".jpg") || fileName.includes(".png")){

                let uploadFileHTML = `<li class="row">
                <i class="fas fa-file-alt"></i>
    
                <div class="content">
                    <div class="details">
                        <span class="name">${shortFileName}</span>
                    </div>
                </div>
                <i class="fas fa-check"></i>
                </li>`;
                // uploadedArea.insertAdjacentHTML('afterbegin',uploadFileHTML);
                uploadedArea.innerHTML += uploadFileHTML;
            }else{
                alert("Wrong file type");
            }
        }
        fileInput.files = e.dataTransfer.files;

    }
});


fileInput.onchange = ({target}) =>{
    // let file = target.files[0] //getting file and [0] this means if user has selected multiple files then will only get the first one only
    let file = target.files
    if (file){ // if file is selected
        // console.log(file.read());
        uploadedArea.innerHTML = null;

        for (let i = 0; i < file.length; i++) {   
            let fileName = file[i].name;
            var shortFileName;
            if (fileName.includes(".pdf") || fileName.includes(".jpeg") || fileName.includes(".jpg") || fileName.includes(".png")){
                if (fileName.length >=12){
                    let splitName = fileName.split('.');
                    shortFileName = splitName[0].substring(0,10) + "... ." + splitName[1];
                }else{
                    shortFileName = fileName;
                }

                let uploadFileHTML = `<li class="row">
                <i class="fas fa-file-alt"></i>
    
                <div class="content">
                    <div class="details">
                        <span class="name">${shortFileName}</span>
                    </div>
                </div>
                <i class="fas fa-check"></i>
                </li>`;
                // uploadedArea.insertAdjacentHTML('afterbegin',uploadFileHTML);
                uploadedArea.innerHTML += uploadFileHTML;
    
            }else{
                alert("Wrong file type");
            }
        }     

    }
}
function confirm(){
    
    document.getElementById('exampleModalCenter').classList.add('exampleModalCenter_hide');
    
}
