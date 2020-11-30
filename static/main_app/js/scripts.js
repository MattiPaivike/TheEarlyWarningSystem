$(document).ready(function() {
  //this function is used to activate checkbox when menu item is clicked
     $(".clickselect").click(function () {
      var $checks = $(this).find('input');
      $checks.prop("checked", !$checks.is(":checked"));
  });

});

//this function is used for mobile navbar
function NavBar() {
  var x = document.getElementById("navbar");
  if (x.className === "menu_items") {
    x.className += " responsive";
  } else {
    x.className = "menu_items";
  }
};
