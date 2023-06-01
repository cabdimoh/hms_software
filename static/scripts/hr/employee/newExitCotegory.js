$(document).ready(function () {

  getexitCotorgryData()
  let insertType = "Insert";


  $('#New_Exit_Cotegory_id').on('click', function () {
    $(".add_exit_cat_modal").modal("show");
   
   

    // $("#Bank_name").val('');
    // $("#Bank_descriptions").val('');
    insertType = "Insert";

  });

  // saving and updating
  $("#save_exit_cat").on("click", function (e) {
    // Prevent the page from loading or refreshing
    e.preventDefault();

    // Create form data
    let formData = new FormData();
    // Read user inputs

    formData.append("Exit_Cotegory_name", $("#Exit_Cotegory_name").val());
  



    let urls = ""

    if (insertType == "Insert") {
      urls = "/hrm/exit_cotegory_all/new_Category";
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
          $(".add_exit_cat_modal").modal("hide");
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
              // hide the modal and resret the form
            
                // hide the modal and resret the form
              
                window.location.reload();
                // $(".CategoryModal").modal("hide");



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
      url: "/hrm/exit_cotegory_all/get_exit_cotegory",
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
         
          $("#itemID").val(response.Message.id);
          $("#ItemName").val(response.Message.category_name);

  




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

