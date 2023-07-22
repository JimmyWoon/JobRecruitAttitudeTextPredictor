
function checkAns() {
}
var radioGroups = document.querySelectorAll('input[type="radio"]');
var submitButton = document.getElementById('submit_question');
// submitButton.disabled = true;

var form = document.getElementById('question_form');

// Check if any radio button is unchecked
function checkRadioButtons() {
    var checked = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
    for (var i = 1; i < 22; i++){
        var x= "q"+i;
        var radioBtn = document.getElementsByName(x);
        checked_question = 0
        for (var i = 0; i < radioBtn.length; i++) {
            if (radioBtn[i].checked) {
                checked_question = 1;
                break;
                // submitButton.disabled = true;
                // return;
            }
        }
        if (checked_question == 1){
            checked[(i-1)] = 1;
        }
        else{
            checked[(i-1)] = 0;
        }
    }
    if (arr.includes(0)) {
        submitButton.disabled = true;
    }
    else{
        submitButton.disabled = false;
    }

    // for (var i = 0; i < radioGroups.length; i++) {
    //   if (!radioGroups[i].checked) {
    //     submitButton.disabled = true;
    //     return;
    //   }
    // }
    // submitButton.disabled = false;
  }
  
  // Add an event listener to each radio button group
//   radioGroups.forEach(function(radioGroup) {
//     radioGroup.addEventListener('change', checkRadioButtons);
//   });
