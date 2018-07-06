$(window).on("load", loadTime);
$(window).on("unload", unLoadTime);

var start_time = undefined;
var end_time = undefined;

function loadTime(){
  start_time = new Date();
  return;
}

function unLoadTime(){
  end_time = new Date();
  timeSpentOnPage();
  return;
}

function timeSpentOnPage(){
  let total_time = start_time.getTime() - end_time.getTime();
  return total_time;
}

function myFunction() {
    document.getElementById("demo").innerHTML = "Iframe is loaded.";
}
