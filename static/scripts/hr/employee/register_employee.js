$(document).ready(function () {

  let photo = "";
  $("#lead-image-input").on("change", function (e) {
    photo = e.target.files[0];
    var reader = new FileReader();
    reader.onload = function(event) {
      var imageUrl = event.target.result;
      // console.log('Selected image URL:', imageUrl);
      $("#lead-img").attr("src", imageUrl);
    };
    reader.readAsDataURL(photo);
  });
  $("#btn_save").on("click", function (e) {
    // Prevent the page from loading or refreshing
    e.preventDefault();

    // Create form data
    let formData = new FormData();

    // Read user inputs
    formData.append("first_name", $("#first_name").val());
    formData.append("father_name", $("#father_name").val());
    formData.append("last_name", $("#last_name").val());
    formData.append("mother_name", $("#mother_name").val());
    formData.append("gender", $("#Gender").val());
    formData.append("marital", $("#maritial").val());
    formData.append("Blood_Group", $("#blood_group").val());
    formData.append("Dob", $("#Dob").val());
    formData.append("phone", $("#Phone").val());
    formData.append("emergency_contect", $("#Emer_contact").val());
    formData.append("email", $("#email").val());
    formData.append("speciality", $("#title").val());
    formData.append("address", $("#address").val());
    formData.append("photo", photo);




    $.ajax({
      method: "POST",
      url: "/hrm/manage_employees/new_employee",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {
          Swal.fire({
            title: "Successfully",
            text: response.Message,
            icon: "success",
            confirmButtonClass: "btn btn-primary w-xs mt-2",
            buttonsStyling: !1,
            showCloseButton: !0,
          }).then((e) => {
            if (e.value) {
              // hide the modal           
              $(".newEmployeeModal").modal("hide");
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
});

