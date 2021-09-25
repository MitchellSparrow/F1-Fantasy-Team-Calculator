
$(window).on('load', function(){ 
    $('#loading').hide();
});

function checkInp(){
    console.log("hello");
  var x=document.forms["budget_form"]["budget"].value;
  if (isNaN(x)) 
  {
    console.log("hello");
    alert("Your budget must be a number!");
    return false;
  }
  $('#loading').show();
}

$("form").submit(function (e) {
    var validationFailed = false;
    // validation
    if (isNaN( $("#search").val()  )|| $("#search").val() == null || $("#search").val() == "") {
        validationFailed = true;
    } 

    if (validationFailed) {
        $('#loading').hide();
        alert('Please enter your budget as a number!');
        e.preventDefault();
        return false;
    }
 }); 


 