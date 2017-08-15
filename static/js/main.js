function goToUser(userId){
    localStorage.setItem("userId", userId);
    window.location.assign("profile.html");
}

function goToPhotos(){
    localStorage.removeItem("albumId");
    window.location.assign("photos.html");
}

function goToAlbum(albumId){
    localStorage.setItem("albumId", albumId);
    window.location.assign("photos.html");
}

$(document).ready(function () {
   
    $("#photosLink").click(function (evt){
        evt.preventDefault();
        goToPhotos();
    });
    
    $("#imageView #close").click(function (){
       $("#imageView").fadeOut(300);
    });

    $(".post img").on('click', function(event){
        window.open(this.src)
    });

    $("#offers").on('click', '.acceptOffer',function(event){
        event.preventDefault();
        var obj = $(this);
        $.ajax({
            url: '/showItem/acceptOffer/',
            method: 'GET',
            data: {
                offer: obj.data('offer')
            }, success: function(data){
                if(data.success === false){
                    alert("Cannot accept this offer at the moment.");
                }else{
                    document.location.href = obj.href;
                }
            }
        })
    });

    $("#offers").on('click', '.rejectOffer',function(event){
        event.preventDefault();
        var obj = $(this);
        $.ajax({
            url: '/showItem/rejectOffer/',
            method: 'GET',
            data: {
                offer: obj.data('offer')
            }, success: function(data){
                if(data.success === false){
                    alert("Cannot reject this offer at the moment.");
                }else{
                    document.location.href = obj.href;
                }
            }
        })
    });


    $("#form_p").on('change', "#id_offerType", function (event){

        var type = $("#id_offerType").val();
        var post = $("#id_post").val();

       $.ajax({
           url: '/showItem/changeForm/',
           method: 'GET',
           data: {
               post: post,
               type: type
           }, success: function(data){
               console.log(data);
               $("#form_p").empty();
               $("#form_p").append(data);
           }
       })
    });

});