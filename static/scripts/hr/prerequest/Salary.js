$(document).ready(function () {

  getbasesalarydata()
  let insertType = "Insert";

  $('#Add_Salary_button').on('click', function () {
    $(".add_Salary_modal").modal("show");


    $("#jobtype_salary").val('');
    $("#base_salary").val('');
    $("#name").val('');
    insertType = "Insert";

  });

  // saving and updating
  $("#save_salary").on("click", function (e) {
    // Prevent the page from loading or refreshing
    e.preventDefault();

    // Create form data
    let formData = new FormData();
    // Read user inputs

    formData.append("jobtype_salary", $("#jobtype_salary").val());
    formData.append("name", $("#name").val());
    formData.append("base_salary", $("#base_salary").val());
    formData.append("fixed_allowance", $("#fixed_allowance").val());



    let urls = ""

    if (insertType == "Insert") {
      urls = "/hrm/prerequirements/New_Salary";
    }
    else {
      urls = "/hrm/prerequirements/Update_Salary_data";
      let x = $("#Base_Salar_detail_ids").val();

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
          $(".add_Salary_modal").modal("hide");
          getbasesalarydata()
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
  $("#Salary_table").on("click", ".Salar_class_botton", function (e) {
    e.preventDefault();
    const ID = $(this).attr("salary_detail_id");
    console.log(ID + "ayan wada")
    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("id", ID);



    $.ajax({
      method: "POST",
      url: "/hrm/prerequirements/get_single_Salary_Data",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {

          insertType = "Update";
          $(".add_Salary_modal").modal("show");
          $(".modal-title").text("Update " + response.Message.jobtype_salary_name);
          $("#jobtype_salary").val(response.Message.jobtype_salary);
          $("#base_salary").val(response.Message.base_salry);        
          $("#name").val(response.Message.name);
          $("#Base_Salar_detail_ids").val(response.Message.id);




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
  function getbasesalarydata() {
    // Create form data
    let formData = new FormData();
    // Read user inputs

    $.ajax({
      method: "POST",
      url: "/hrm/prerequirements/getAllSalaryData",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {
          let table = $("#Salary_table").DataTable().clear().draw();

          for (let index = 0; index < response.Message.length; index++) {
            let temp = [

              response.Message[index].id,
              response.Message[index].jobtype,
              response.Message[index].name,
              response.Message[index].base_salary,




              `<a href="#" class="Salar_class_botton " salary_detail_id=${response.Message[index].id}  style="color:white;" >
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

