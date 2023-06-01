// $(document).ready(function(){

//     $("#btn-save").on("click", function (e) {
//         console.log('btn clicked');
//         // Prevent the page from loading or refreshing
//         e.preventDefault();

//         // Create form data
//         let formData = new FormData();
//         // Read user inputs
//         formData.append("Email", $('#email').val());
//         formData.append("Password", $('#password').val());

//         $.ajax({
//             method: "POST",
//             url: "/users/Login_user",
//             headers: { "X-CSRFToken": csrftoken },
//             processData: false,
//             contentType: false,
//             data: formData,
//             async: false,
//             success: function (response) {
//                 console.log(response);
//             },

//             error: function (response , status, error) {alert(xhr.responseText); },
//         });
//     });
// })