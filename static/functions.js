function myFunction() {
  // Get the checkbox
  var checkBox = document.getElementById("Administrador");
  // Get the output text
  var passwordadmin = document.getElementById("passwordadmin");

  // If the checkbox is checked, display the output text
  if (checkBox.checked == true){
    passwordadmin.style.display = "block";
  } else {
    passwordadmin.style.display = "none";
  }
}
