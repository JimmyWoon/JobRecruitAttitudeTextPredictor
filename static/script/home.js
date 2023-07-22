
// $(function(){
//     $("input[type='checkBox']").change(function(){
//       var len = $("input[type='checkBox']:checked").length;
//       if(len == 0)
//         $("input[type='submit']").prop("disabled", true);
//       else
//         $("input[type='submit']").removeAttr("disabled");
//     });
//     $("input[type='checkBox']").trigger('change');
// });

function deleteFunction() {
    var input, filter, table, tr, td, i, txtValue;
    var checked = [];
    container = document.getElementById("displayContainer");

     // One-Liner version to loop through each input element and check the first checkbox element
    for(x=0;x<document.getElementsByTagName('input').length;x++){
        if(document.getElementsByTagName('input').item(x).type=='checkbox'){
            if (document.getElementsByTagName('input').item(x).checked == true){
                checked.push(document.getElementsByTagName('input').item(x).value);
            }
        }
    };
    if (checked.length == 0){
        alert("No file selected!");
    }
    else{
        // function x(){
        //     $.ajax({
        //         type: "POST",
        //         url: "/home",
        //         contentType: "application/json",
        //         data: JSON.stringify({checked: checked}),
        //         dataType: "json",
        //         success: function(response) {
        //             console.log(response);
        //         },
        //         error: function(err) {
        //             console.log(err);
        //         }
        //     });
        // }


        // const s = JSON.stringify(checked);
        // console.log(s);
        // $.ajax({
        //     url:"/hello",
        //     type:"POST",
        //     dataType: "json",
        //     contentType:"application/json",
        //     data: JSON.stringify(s)
        // });
        var entry = {checked};
        // var xml = new XMLHttpRequest();
        // xml.open("POST", "{{url_for('test')}}",true);
        // xml.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        // xml.onload = function(){
        //     var dataReply = JSON.parse(this.responseText)
        //     alert(dataReply)
        // }
        // dataSend = JSON.stringify({
        //     'selected':checked
        // })
        // xml.send(dataSend)
        // $.ajax({
        //     type:"POST",
        //     url:"{{url_for('test')}}",
        //     data:{"selected": checked}
        // })

        // fetch(`${window.origin}/hello`,{
        //     method: "POST",
        //     credentials: "include",
        //     cache: "no-cache",
        //     headers: {
        //         "Content-type": "text/html",
        //     },
        //     body: JSON.stringify(entry),

        // })
        // console.log(checked)
        // W
        // window.document.location = "/hello";

        // console.log(entry);
//original
        // const request = new XMLHttpRequest();
        // request.open('POST',`/home/${JSON.stringify(checked)}`); // send the checked item to the webpage
        // request.send();
        // request.onload = () => {
        //     if (request.response != null){
        //         request.abort(); // need to stop the post request because the no response will get from the home.html post reqeust 
        //         window.location.reload(); // then refresh the page to reload the page without the deleted item
        //     }
        // };

    }

}
//--------------------------------------------delay function for auto subtmit
        // //setup before functions
        // var typingTimer;                //timer identifier
        // var doneTypingInterval = 1000;  //time in ms, 5 seconds for example
        // var $input = $('#fieldInput');

        // //on keyup, start the countdown
        // $input.on('keyup', function () {
        // clearTimeout(typingTimer);
        // typingTimer = setTimeout(doneTyping, doneTypingInterval);
        // });

        // //on keydown, clear the countdown 
        // $input.on('keydown', function () {
        // clearTimeout(typingTimer);
        // });

        // //user is "finished typing," do something
        // function doneTyping () {
        // //do something
        //     var input, filter, container, btn, name, i, txtValue;
        //         hiddenField = document.getElementById('field');
        //         input = document.getElementById("fieldInput");
        //         console.log(hiddenField.value);
        //         if (hiddenField.value != ""){
        //             input.value = hiddenField.value;
        //         }
        //         filter = input.value.toLowerCase();
        //         container = document.getElementById("displayContainer");
        //         btn = container.getElementsByTagName("button");
        //         for (i = 1; i < btn.length; i++) {
        //             // console.log(btn[i].getAttribute('name'));
        //             name = (btn[i].getAttribute('name')).split(",");
        //             name = name[0];
        //             // console.log(name);
        //             if (name.indexOf(filter) > -1) {
        //                 btn[i].style.display = "";
        //             } else {
        //                 btn[i].style.display = "none";
        //             }
        //         }
        //             document.filterForm.submit();

        // }



function myFunction() {

    // var Fieldinput, Fieldfilter, container, btn, field, i, Persoanlityinput,Personalityfilter;
    // // hiddenField = document.getElementById('field');
    // Fieldinput = document.getElementById("fieldInput");
    // Persoanlityinput = document.getElementById("PersonalityInput");

    // // console.log(hiddenField.value);
    // // if (hiddenField.value != ""){
    // //     input.value = hiddenField.value;
    // // }
    // Fieldfilter = Fieldinput.value.toLowerCase();
    // Personalityfilter = Persoanlityinput.value.toLowerCase();
    // Personalityfilter = Personalityfilter.split(' ');

    // container = document.getElementById("displayContainer");
    // btn = container.getElementsByTagName("button");
    // for (i = 1; i < btn.length; i++) {
    //     // console.log(btn[i].getAttribute('name'));
    //     field = (btn[i].getAttribute('name')).split(",");
    //     field = field[0];
    //     // console.log(name);
    //     if (field.indexOf(Fieldfilter) > -1) {
    //         btn[i].style.display = "";
    //         personality = (btn[i].getAttribute('name')).split(",");
    //         personality.shift();
    //         nextResume:
    //         for (z = 0; z < personality.length; z++){
    //             // console.log(name2[z]);
    //             // console.log(filter2);
    //             for (j = 0; j < Personalityfilter.length; j++){
    //                 if (personality[z].indexOf(Personalityfilter[j]) > -1) {
    //                     btn[i].style.display = "";
    //                     break nextResume; // break nested loop
    //                 } else {
    //                     btn[i].style.display = "none";
    //                 }
    //             }
    //         }
    //     } else {
    //         btn[i].style.display = "none";
    //     }
    // }
}




function personalityFunction() {

    // var input, filter, container, btn, name, i, txtValue;
    // // hiddenField = document.getElementById('field');
    // input = document.getElementById("PersonalityInput");
    // // console.log(hiddenField.value);
    // // if (hiddenField.value != ""){
    // //     input.value = hiddenField.value;
    // // }
    // filter = input.value.toLowerCase();
    // container = document.getElementById("displayContainer");
    // btn = container.getElementsByTagName("button");
    // for (i = 1; i < btn.length; i++) {
    //     // console.log(btn[i].getAttribute('name'));
    //     name = (btn[i].getAttribute('name')).split(",");
    //     name.shift();
    //     for (z = 0; z < name.length; z++){
    //         console.log(name[z]);
    //         console.log(filter);
    //         if (name[z].indexOf(filter) > -1) {
    //             btn[i].style.display = "";
    //             break;
    //         } else {
    //             btn[i].style.display = "none";
    //         }
    //     }
    // }
}

// const fieldHidden = document.getElementById("field");
// const personalityHidden = document.getElementById("personality");
// if (fieldHidden.value != ""){
//     console.log(fieldHidden);
//     document.getElementById("fieldInput").value = fieldHidden;
// }
// if (personalityHidden.value != ""){
//     document.getElementById("PersonalityInput").value = personalityHidden;
// }

