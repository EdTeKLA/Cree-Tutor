// body.on("load", loadTime);
// body.on("unload", unLoadTime);
document.addEventListener("load", testPrint);

var start_time = undefined;
var end_time = undefined;

function testPrint(){
  document.getElementById("demo").innerHTML() = "NICE";
  return;
}

function testPnt(){
  window.alert("Oh bye")
  return;
}

function loadTime(){
  start_time = new Date();
  window.alert("Got time")
  return;
}

function unLoadTime(){
  end_time = new Date();
  timeSpentOnPage();
  return;
}

function timeSpentOnPage(){
  let total_time = start_time.getTime() - end_time.getTime();
  window.alert(total_time);
  return;
}

function myFunction() {
    document.getElementById("demo").innerHTML = "Iframe is loaded.";
}
