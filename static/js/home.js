var pInd = 1;
function cycleThrough(){
    
    if(pInd > 4){
        pInd = 1;
        $("#landing > .post:nth-child(" + 4 + ")").removeClass("move");
    }else
        $("#landing > .post:nth-child(" + (pInd - 1) + ")").removeClass("move");

    $("#landing > .post:nth-child(" + pInd + ")").addClass("move");

    pInd++;
}

function checkIfFull(){
    if($("#landing > div").length >= 1)
        cycleThrough();
}

setInterval(checkIfFull, 6000);

$(document).ready(function () {

});