$(document).ready(function () {

  getBankDetail()
  let insertType = "Insert";

  $('#Add_bank_button').on('click', function () {
    $(".add_banks_modal").modal("show");


    $("#Bank_name").val('');
    $("#Bank_descriptions").val('');
    insertType = "Insert";

  });

  // saving and updating
  $("#save_Bank").on("click", function (e) {
    // Prevent the page from loading or refreshing
    e.preventDefault();

    // Create form data
    let formData = new FormData();
    // Read user inputs

    formData.append("Bank_name", $("#Bank_name").val());
    formData.append("Bank_descriptions", $("#Bank_descriptions").val());



    let urls = ""

    if (insertType == "Insert") {
      urls = "/hrm/prerequirements/new_Banks";
    }
    else {
      urls = "/hrm/prerequirements/update_Bank_data";
      let x = $("#Bank_detail_ids").val();

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
          $(".add_banks_modal").modal("hide");
          getBankDetail()
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
  $("#Banks_table").on("click", ".bank_class_botton", function (e) {
    e.preventDefault();
    const ID = $(this).attr("Bank_detail_id");
    console.log(ID + "ayan wada")
    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("id", ID);



    $.ajax({
      method: "POST",
      url: "/hrm/prerequirements/get_single_banks_Data",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {

          insertType = "Update";
          $(".add_banks_modal").modal("show");
          $(".modal-title").text("Update Bank " + response.Message.Bank_name);
          $("#Bank_name").val(response.Message.Bank_name);
          $("#Bank_descriptions").val(response.Message.bank_discription);
          $("#Bank_detail_ids").val(response.Message.id);




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
  function getBankDetail() {
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
              <button type="button" class="btn btn-sm btn-info rounded" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-title="Tooltip on top">
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

