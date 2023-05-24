$(document).ready(function() {
  $("#feedback-form").submit(function(e) {
    e.preventDefault();
    // Serialize the form data
    var formdata = $(this).serialize();
    // Send the request
    $.ajax({
      type: "POST",
      url: ".",
      data: formdata,
      success: function(response) {
        console.log(response);
        // Find the id
        var inputid = $("#feedback-form input[name='detail']").attr("id");
        // Clear the input field
        $("#" + inputid).val("");
        // Append the submitted data to the form
        $("#feedback-form").append("<p>" + response.detail + "</p>");
      },
      error: function(xhr, status, error) {
        console.log(xhr.responseText);
      }
    });
  });


$("#rating-form").submit(function(e){
  e.preventDefault();

  formdata = $(this).serialize();

$.ajax({
  type: "POST",
  url: ".",
  data:formdata,
  success: function(response){
    console.log(response)
  },
  error: function(xhr, status, error){
    console.log(xhr.response)
  },
});

});

$("#chat-form").submit(function(e) {
  e.preventDefault();
  var form = $(this);

  $.ajax({
    type: "POST",
    url: ".",
    data: form.serialize(),
    dataType: "json",
    success: function(response) {
      console.log(response);

      // Clear the input field
      form.find("textarea[name='content']").val("");

      // Display the response content in a separate element
      if (response.content) {
        $("#chat-form").append("<p>" + response.content + "</p>");
      }
    },
    error: function(xhr, status, error) {
      console.log(xhr.response);
    }
  });


});



// $(document).ready(function() {
//   console.log("Document ready function is executing");

//   $("#chat-form").submit(function(e) {
//     e.preventDefault();
//     var form = $(this);

//     $.ajax({
//       type: "POST",
//       url: ".",
//       data: form.serialize(),
//       dataType: "json",
//       success: function(response) {
//         console.log(response);

//         // Clear the input field
//         console.log("Executing clear textarea code");

//         form.find("textarea[name='content']").val("");

//         // Display the response content in a separate element
//         if (response.content) {
//           $("#chat-container").append("<p>" + response.content + "</p>");
//         }
//       },
//       error: function(xhr, status, error) {
//         console.log(xhr.response);
//       }
//     });
//   });

//   $("#toggle-button").click(function(e) {
//     e.preventDefault();
//     $("#hidden-messages").toggle();
//     if ($("#hidden-messages").is(":visible")) {
//       $(this).text("Hide messages");
//     } else {
//       $(this).text("Show all messages");
//     }
//   });
// });




// $("#chat-form").submit(function(e) {
//   e.preventDefault();
//   var form = $(this);

//   $.ajax({
//     type: "POST",
//     url: ".",
//     data: form.serialize(),
//     dataType: "json",
//     success: function(response) {
//       console.log(response);

//       // Clear the input field
//       var inputid = $("#id_content").attr("id");
//       $("#" + inputid).val("");

//       // Display the response content in a separate element
//       if (response.content) {
//         $("#chat-form").append("<p>" + response.content + "</p>");
//       }
//     },
//     error: function(xhr, status, error) {
//       console.log(xhr.response);
//     }
//   });
// });



// $("#chat-form").submit(function(e) {
//   e.preventDefault();
//   var form = $(this);
//   var formData = form.serialize();

//   $.ajax({
//     type: "POST",
//     url: ".",
//     data: formData,
//     dataType: "json",
//     success: function(response) {
//       console.log(response);

//       // Clear the input field
//       form.find("textarea[name='content']").val("");

//       // Display the response content in a separate element
//       if (response.content) {
//         $("#chat-form").append("<p>" + response.content + "</p>");
//       }
//     },
//     error: function(xhr, status, error) {
//       console.log(xhr.response);
//     }
//   });
// });

 
// $("#chat-form").submit(function(e) {
//   e.preventDefault();
//   var form = $(this);
//   var formData = form.serialize();

//   $.ajax({
//     type: "POST",
//     url: ".",
//     data: formData,
//     dataType: "json",
//     success: function(response) {
//       console.log(response);

//       // Clear the input field
//       form.find("textarea[name='content']").val("");

//       // Display the response content in a separate element
//       if (response.content) {
//         $("#chat-form").append("<p>" + response.content + "</p>");
//       }
//     },
//     error: function(xhr, status, error) {
//       console.log(xhr.response);
//     }
//   });
// });
});


// $(document).ready(function() {
//   $("#chat-form").submit(function(e) {
//     e.preventDefault();
//     var form = $(this);

//     $.ajax({
//       type: "POST",
//       url: ".",
//       data: form.serialize(),
//       dataType: "json",
//       success: function(response) {
//         console.log(response);

//         // Clear the input field
//         form.find("textarea[name='content']").val("");

//         // Display the response content in a separate element
//         if (response.content) {
//           $("#chat-container").append("<p>" + response.content + "</p>");
//         }
//       },
//       error: function(xhr, status, error) {
//         console.log(xhr.response);
//       }
//     });
//   });

 

