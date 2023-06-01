$(document).ready(function () {

  getDoctorSpecializations()
  let insertType = "Insert";

  $('#Add_Specialization_button').on('click', function () {
    $(".add_specialization_modal").modal("show");
    $("#spec_name").val('');
    $("#description_spec").val('');
    insertType == "Insert"

  });

  // saving and updating
  $("#save_specialization").on("click", function (e) {
    // Prevent the page from loading or refreshing
    e.preventDefault();

    // Create form data
    let formData = new FormData();
    // Read user inputs

    formData.append("spec_name", $("#spec_name").val());
    formData.append("description_spec", $("#description_spec").val());
 



    let urls = ""

    if (insertType == "Insert") {
      urls = "/hrm/prerequirements/new_administarator";
    }
    else {
      urls = "/hrm/prerequirements/Update_specialization_data";
      let x = $("#speci_detail_ids").val();
      formData.append("id", x);

    }
    $.ajax({
      method: "POST",
      url: urls,
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {
          $(".add_specialization_modal").modal("hide");
          getDoctorSpecializations()
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
              $("#job_t")[0].reset();
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

  //Retrieving single data and display modal
  $("#Specialition_table").on("click", ".specializaiton_class_botton", function (e) {
    e.preventDefault();
    const ID = $(this).attr("specializations_detail_id");
    console.log(ID + "ayan wada")
    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("id", ID);



    $.ajax({
      method: "POST",
      url: "/hrm/prerequirements/get_single_specialization_Data",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {

          insertType = "Update";
          $(".add_specialization_modal").modal("show");
          $(".modal-title").text("Edit " + response.Message.specialization_name);

          $("#spec_name").val(response.Message.specialization_name);
          $("#description_spec").val(response.Message.description);

          $("#speci_detail_ids").val(response.Message.id);


          // formData.append("spec_name", $("#spec_name").val());
          // formData.append("description_spec", $("#description_spec").val());
       

        } else {
          Swal.fire({
            title: response.title,
            text: response.Message,
            icon: response.type,
            confirmButtonClass: "btn btn-success w-xs mt-2",
            buttonsStyling: !1,
            showCloseButton: !0,
          });
        }
      },
      error: function (response) { },
    });

  });



  // Get all employee qualification data 
  function getDoctorSpecializations() {
    // Create form data
    let formData = new FormData();
    // Read user inputs

    $.ajax({
      method: "POST",
      url: "/hrm/prerequirements/get_doctor_Specialization",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {
          let table = $("#Specialition_table").DataTable().clear().draw();

          for (let index = 0; index < response.Message.length; index++) {
            let temp = [

              response.Message[index].id,
              response.Message[index].specialization_name,
              response.Message[index].description,





              `<a href="#" class="specializaiton_class_botton " specializations_detail_id=${response.Message[index].id}  style="color:white;" >
              <button type="button" class="btn btn-sm btn-info rounded">
                  
                  <i class="mdi mdi-file-document-edit" ></i>
                 
                  </button>
                  </a>
    
              
            `
            ];
            table.row.add(temp).draw();
          }

        }
      },
      error: function (response) { },
    });
  }
});

