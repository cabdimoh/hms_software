$(document).ready(function () {
    getBankDetail()
    
    let insertType = "Insert";
  
    $('#AddAccounts').on('click', function () {
      $(".HospitalAccount").modal("show");
  
  
      $("#Bank_name").val('');
      $("#Bank_descriptions").val('');
      insertType = "Insert";
  
    });
  
    // saving and updating
    $("#save_account").on("click", function (e) {
      // Prevent the page from loading or refreshing
      e.preventDefault();
  
      // Create form data
      let formData = new FormData();
      // Read user inputs
  
      formData.append("name", $("#name").val());
      formData.append("account", $("#Acc_number").val());
  
  
  
      let urls = ""
  
      if (insertType == "Insert") {
        urls = "/finance/manage-mainAccounts/New_account";
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
            $(".HospitalAccount").modal("hide");   

            Swal.fire({
              title: "Successfully",
              text: response.Message,
              icon: "success",
              confirmButtonClass: "btn btn-primary w-xs mt-2",
              buttonsStyling: !1,
              showCloseButton: !0,
            }).then((e) => {
              if (e.value) {
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
  
  