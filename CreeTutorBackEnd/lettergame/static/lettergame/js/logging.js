var start_time = undefined;
var end_time = undefined;

function testPrint(){
  document.getElementById("demo").innerHTML() = "NICE";
  return;
}


// window.onbeforeunload = function(e){
//   return false;
//   };

window.onload = function loadTime(){
  start_time = new Date();
  return;
};

// window.onbeforeunload = function unLoadTime(){
//   end_time = new Date();
//   window.alert("Got to unload")
//   timeSpentOnPage();
//   return;
// }

function timeSpentOnPage(){
  end_time = new Date();
  let total_time = start_time.getTime() - end_time.getTime();
  return total_time;
};

// function getRequestBody(id){
//   var form = document.getElementById(id)
//   values = [];
//   for (var i = 0, l = form.elements.length; i < l ; i += 1){
//     var el = form.elements[i];
//     //fieldName=value&fieldName2=value2&...
//       name = encodeURIComponent(el.name),
//       value = encodeURIComponent(el.value),
//       complete = name + "=" + value;
//       values.push(complete);
//
//   }
//   time = timeSpentOnPage();
//   var time_spent = "time_spent";
//   complete = time_spent + "=" + time;
//   values.push(complete);
//   return values.join("&");
// };

function postData() {
  $('.ajaxProgress').show();
  $.ajax({
    type: "POST",
    url: "{% url 'lettergame:whichgame' game %}",
    dataType: "json",
    async: true,
    data: {
      csfrmiddlewaretoken: '{{ csfr_token }}',
      user_r: $('#user_r').val(),
      correct_r: $('correct_r').val(),
      test: "test"
    },
    success: function(json){
      $('#output').html(json.message);
      $('.ajaxProgress').hide();
    }

  });
}
//
// function postData(id, url){
//   data = getRequestBody(id)
//   xhr = new XMLHttpRequest();
//   xhr.open("POST", url, true);
//   xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
//   xhr.send(data);
//   return;
// };
//
// function myFunction() {
//     document.getElementById("demo").innerHTML = "Iframe is loaded.";
// }
