

// var resume = {{values | tojson}};

// //Create a HTML Table element.
// var table = document.querySelector(".table");


// //Add the data rows.
// for (var i = 1; i <= resume.length; i++) {
//     row = table.insertRow(-1);
//     for (var j = 0; j < 21; j++) {
//         var cell = row.insertCell(-1);
//         cell.innerHTML = resume[i][j];
//     }
// }




// var dvTable = document.getElementById("dvTable");
// dvTable.innerHTML = "";
// dvTable.appendChild(table);


function myFunction() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("fieldInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("table");
    tr = table.getElementsByTagName("tr");
    for (i = 2; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[3];
        txtValue = td.textContent || td.innerText;

        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
        }
    }
}

function personalityFunction() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("fieldInput");
    filter = input.value.toLowerCase();
    table = document.getElementById("table");
    tr = table.getElementsByTagName("tr");
    if ('active'.includes(filter)){

    }
    else if ('agreeableness'.includes(filter)) {

    }    
    else if ('cautiousness'.includes(filter)) {
    }
    else if ('compliant'.includes(filter)) {
    }
    else if ('confidence'.includes(filter)) {
    }
    else if ('conscientiousness'.includes(filter)) {
    }
    else if ('dominant'.includes(filter)) {
    }
    else if ('emotionality'.includes(filter)) {
    }
    else if ('extroversion'.includes(filter)) {
    }
    else if ('hard working'.includes(filter)) {
    }
    else if ('honest'.includes(filter)) {
    }
    else if ('influencing'.includes(filter)) {
    }
    else if ('knowledge-sharing'.includes(filter)) {
    }
    else if ('leadership'.includes(filter)) {
    }
    else if ('neuroticism'.includes(filter)) {
    }
    else if ('openness'.includes(filter)) {
    }
    else if ('punctual'.includes(filter)) {
    }
    else if ('responsible'.includes(filter)) {
    }
    else if ('steady'.includes(filter)) {
    }
    else if ('teamwork'.includes(filter)) {
    }
    // txtValue = td.textContent || td.innerText;

    // if (txtValue.toUpperCase().indexOf(filter) > -1) {
    //     tr[i].style.display = "";
    // } else {
    //     tr[i].style.display = "none";
    // }
    for (i = 2; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td");
        for (i = 0; i < td.length; i ++){

        }

    }
}