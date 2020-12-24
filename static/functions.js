function myFunction() {
  // Get the checkbox
  var checkBox = document.getElementById("IsAdmin");
  // Get the output text
  var passwordadmin = document.getElementById("admin");

  // If the checkbox is checked, display the output text
  if (checkBox.checked == true){
    passwordadmin.style.display = "block";
  } else {
    passwordadmin.style.display = "none";
  }
}
