$(document).ready(function () {


    $("#btn_submit").on("click", function (e) {
        // Prevent the page from loading or refreshing
        e.preventDefault();

        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("CurrentPassword", $('#CurrentPassword').val());
        formData.append("newPassword", $('#newPassword').val());
        formData.append("CormfirmPassword", $('#CormfirmPassword').val());

        $.ajax({
            method: "POST",
            url: "/users/users-management/ChangeUserPassword",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function (response) {
                if (!response.isError) {                   
                   Swal.fire({
                        title: "Successfully changed",
                        text: response.Message,
                        icon: "success",
                        confirmButtonClass: "btn btn-primary w-xs mt-2",
                        buttonsStyling: !1,
                        showCloseButton: !0,
                    }).then((e) => {
                        if (e.value) {
                            // hide the modal and resret the form
                            window.location.reload()

                        }
                    });
                } else {
                    Swal.fire({
                        title: response.title,
                        text: response.Message,
                        icon: response.type,
                        confirmButtonClass: "btn btn-primary w-xs mt-2",
                        buttonsStyling: !1,
                        showCloseButton: !0,
                    });
                }
            },
            error: function (response) { },
        });
    });







     img_profile = ''
  // show img profile modal changer
  $('#change_profile_picture').on('click', function () {
    $(".ProfilePicture").modal("show");
    img_profile = $(this).attr('imgurls ')
  
    $("#lead-img").attr("src", img_profile);
  });


  $("#lead-image-input").on("change", function (e) {

    img_profile = e.target.files[0];
    var reader = new FileReader();
    reader.onload = function(event) {
      var imageUrl = event.target.result;   
      $("#lead-img").attr("src", imageUrl);
    };
    reader.readAsDataURL(img_profile);
  });



  $("#update_profile_picture").on("click", function (e) {
    // Prevent the page from loading or refreshing
    e.preventDefault();

    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append('photo', img_profile);
    $.ajax({
      method: "POST",
      url: "/users/users-management/change_profile_picture",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {   
          $(".ProfilePicture").modal("hide");
          Swal.fire({
            title: "Successfully",
            text: response.Message,
            icon: "success",
            confirmButtonClass: "btn btn-primary w-xs mt-2",
            buttonsStyling: !1,
            showCloseButton: !0,
          }).then((e) => {
            if (e.value) {
              // hide the modal and resret the form
              window.location.reload();


            }
          });
        } else {
          Swal.fire({
            title: response.title,
            text: response.Message,
            icon: response.type,
            confirmButtonClass: "btn btn-primary w-xs mt-2",
            buttonsStyling: !1,
            showCloseButton: !0,
          });
        }
      },
      error: function (response) { },
    });
  });

  $("#CurrentUser").on("click", function (e) {  
    // Prevent the page from loading or refreshing
    e.preventDefault();
    

    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("user_username", $('#user_username').val());
    formData.append("user_firstname", $('#user_firstname').val());
    formData.append("user_lastname", $('#user_lastname').val());
    formData.append("user_gender", $('#user_gender').val());
    formData.append("user_email", $('#user_email').val());
   

    $.ajax({
        method: "POST",
        url: "/users/users-management/Edit_user_data",
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        async: false,
        success: function (response) {
            if (!response.isError) {                   
               Swal.fire({
                    title: "Successfully changed",
                    text: response.Message,
                    icon: "success",
                    confirmButtonClass: "btn btn-primary w-xs mt-2",
                    buttonsStyling: !1,
                    showCloseButton: !0,
                }).then((e) => {
                    if (e.value) {
                        // hide the modal and resret the form
                        window.location.reload()

                    }
                });
            } else {
                Swal.fire({
                    title: response.title,
                    text: response.Message,
                    icon: response.type,
                    confirmButtonClass: "btn btn-primary w-xs mt-2",
                    buttonsStyling: !1,
                    showCloseButton: !0,
                });
            }
        },
        error: function (response) { },
    });
});

$("#edituserdata").on("click", function (e) {
    e.preventDefault();
$(".EditUserData_modal").modal("show");
})

})

