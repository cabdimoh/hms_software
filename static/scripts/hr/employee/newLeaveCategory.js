$(document).ready(function () {
  getexitCotorgryData()
  let insertType = "Insert";

  $('#New_Leave_Cotegory_id').on('click', function () {
    $(".add_leave_cat_modal").modal("show");
    $('#name_leave').val('')
    $("#leavedays").val('');


    insertType = "Insert";
  });

  // saving and updating
  $("#save_leave_cat").on("click", function (e) {
    // Prevent the page from loading or refreshing
    e.preventDefault();

    // Create form data
    let formData = new FormData();
    // Read user inputs

    formData.append("name", $("#name_leave").val());
    formData.append("leavedays", $("#leavedays").val());
  



    let urls = ""

    if (insertType == "Insert") {
      urls = "/hrm/Leave_cotegory_all/new_leave_Category";
    }
    else {
      urls = "/hrm/Leave_cotegory_all/update_leave_Category";
      let x = $("#Leaveid").val();

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
          $(".add_leave_cat_modal").modal("hide");
          getexitCotorgryData()
          Swal.fire({
            title: "Successfully",
            text: response.Message,
            icon: "success",
            confirmButtonClass: "btn btn-primary w-xs mt-2",
            buttonsStyling: !1,
            showCloseButton: !0,
          }).then((e) => {
            if (e.value) {
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

  //Retrieving single data and display modal
  $("#Leave_cotegory_table").on("click", ".leaveEditbtn", function (e) {
    const ID = $(this).attr("LeaveID");
    let formData = new FormData();
        // Read user inputs
    formData.append("id", ID);



    $.ajax({
      method: "POST",
      url: "/hrm/Leave_cotegory_all/get_leave_Category",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {

          insertType = "Update";
          $(".add_leave_cat_modal").modal("show");
          $(".modal-title").text("Update  " + response.Message.name);
         
          $("#Leaveid").val(response.Message[0].id);
          $("#name_leave").val(response.Message[0].name);
          $("#leavedays").val(response.Message[0].day);

  




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
  function getexitCotorgryData() {
    // Create form data
    let formData = new FormData();
    // Read user inputs

    $.ajax({
      method: "POST",
      url: "/hrm/prerequirements/getAllBanksData",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {
          let table = $("#Banks_table").DataTable().clear().draw();

          for (let index = 0; index < response.Message.length; index++) {
            let temp = [

              response.Message[index].id,
              response.Message[index].Bank_name,
              response.Message[index].Banks_descriptions,




              `<a href="#" class="bank_class_botton" Bank_detail_id=${response.Message[index].id}  style="color:white;" >
                  <button type="button" class=" btn-primary rounded">
                  
                      <i class="las la-pen"></i>
                 
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

