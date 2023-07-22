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
            if (fileName.includes(".pdf") || fileName.includes(".docx") || fileName.includes(".mp4") ||fileName.includes(".doc")){

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
            if (fileName.includes(".pdf") || fileName.includes(".docx") || fileName.includes(".mp4") || fileName.includes(".doc")){
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

// function validateForm() {
//     var fileUplaod = document.forms["formUpload"]["file"].value;
//     if (fileUplaod == null ) {
//       alert("hedaeade");
//       return false;
//     }
// }
function checkRequired(){
    const name = document.getElementById('inputName').value;
    const phone = document.getElementById('inputPhone').value;
    // const mail = document.getElementById('inputEmail').value;

    if (name.length == 0 || phone.length == 0){
        document.getElementById('error1').classList.remove('alert_star_hide');
        document.getElementById('error1').classList.add('alert_star');

        document.getElementById('error2').classList.remove('alert_star_hide');
        document.getElementById('error2').classList.add('alert_star');

    }
    else{
        document.getElementById('error1').classList.remove('alert_star');
        document.getElementById('error1').classList.add('alert_star_hide');
        document.getElementById('error2').classList.remove('alert_star');
        document.getElementById('error2').classList.add('alert_star_hide');

        document.getElementById('information_form').classList.add('information_form_hide');
    }
}

// submitForms = function(){
//     console.log('submitted');
//     document.getElementById("information_form").submit();
// }

// document.getElementById('submit-btn').addEventListener('click', function() {
//     // Get the form data
//     console.log('dsadsa');
//     var form1Data = new FormData(document.getElementById('form'));
//     var form2Data = new FormData(document.getElementById('information_form'));
    
//     // Merge the form data into a single object
//     var formData = {};
//     for (var pair of form1Data.entries()) {
//       formData[pair[0]] = pair[1];
//     }
//     for (var pair of form2Data.entries()) {
//       formData[pair[0]] = pair[1];
//     }
    
//     // Send the form data to the server
//     fetch('/upload', {
//       method: 'POST',
//       body: JSON.stringify(formData),
//       headers: {
//         'Content-Type': 'application/json'
//       }
//     }).then(response => {
//       // Handle the server response
//     }).catch(error => {
//       // Handle errors
//     });

//   });