$(document).ready(function () {

  gethospitaldepartmentdata()
  let insertType = "Insert";

  $('#add_department_button_modal').on('click', function () {
    $(".add_Department_modal").modal("show");


    $("#Department_name").val('');
    $("#director_id").val('');
    $("#department_descriptions").val('');
    insertType = "Insert";
  });

  // saving and updating
  $("#save_department").on("click", function (e) {
    // Prevent the page from loading or refreshing
    e.preventDefault();

    // Create form data
    let formData = new FormData();
    // Read user inputs

    formData.append("Department_name", $("#Department_name").val());
    formData.append("department_descriptions", $("#department_descriptions").val());
    formData.append("director_id", $("#director_id").val());



    let urls = ""

    if (insertType == "Insert") {
      urls = "/hrm/prerequirements/new_Department";
    }
    else {
      urls = "/hrm/prerequirements/update_departments";
      let x = $("#departments_id").val();

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
          $(".add_Department_modal").modal("hide");
          gethospitaldepartmentdata();
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
              // $("#job_t")[0].reset();

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
  $("#hospital_department_table").on("click", ".department_botton", function (e) {
    e.preventDefault();
    const ID = $(this).attr("departments_id");
    console.log(ID + "ayan wada")
    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("id", ID);



    $.ajax({
      method: "POST",
      url: "/hrm/prerequirements/get_Department_single_Data",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {

          insertType = "Update";
          $(".add_Department_modal").modal("show");
          $(".modal-title").text("Update Department Data");
          $("#director_id").val(response.Message.director);
          $("#Department_name").val(response.Message.department_name);
          $("#department_descriptions").val(response.Message.department_discription);
          $("#departments_id").val(response.Message.id);




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



  // Get all employee qualification data 
  function gethospitaldepartmentdata() {
    // Create form data
    let formData = new FormData();
    // Read user inputs

    $.ajax({
      method: "POST",
      url: "/hrm/prerequirements/getDepartmentData",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {
          let table = $("#hospital_department_table").DataTable().clear().draw();

          for (let index = 0; index < response.Message.length; index++) {
            let temp = [

              response.Message[index].id,
              response.Message[index].director_name,
              response.Message[index].department_name,
              response.Message[index].department_discription,




              ` <a href="#" class="department_botton text-end" departments_id=${response.Message[index].id}  style="color:white;" >
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

