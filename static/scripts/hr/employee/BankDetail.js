$(document).ready(function () {
    GetAllEmpoBanks()
    let insertType = "Insert";
  
    $('#new_Employee_bank').on('click', function () {
      $(".AddBankDetail").modal("show");
      
      $("#banks").val('');
      $("#Account").val('');
 
      insertType = "Insert";

     
    });
  
    // saving and updating
    $("#save_banks").on("click", function (e) {
      // Prevent the page from loading or refreshing
      e.preventDefault();
  
      // Create form data
      let formData = new FormData();
      // Read user inputs
      formData.append("employee_id", employee_id);
      formData.append("banks", $("#banks").val());
      formData.append("Account", $("#Account").val());
     
  
  
      let urls = ""
   
      if (insertType == "Insert") {
        urls = "/hrm/manage_EmployeeAccountk/new_Employe_Bank";
      }
      else {
        urls = "/hrm/manage_EmployeeAccountk/update_Bank";
    
        let x = $("#empoyee_bank_id").val();
        formData.append("id", $("#empoyee_bank_id").val());
  
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
            $(".AddBankDetail").modal("hide");
            GetAllEmpoBanks();
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
                $("#Employee_form")[0].reset();
  
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
    $("#employee_bank_table").on("click", ".editBankButton", function (e) {
      e.preventDefault();
      const ID = $(this).attr("employe_bank_id");
      // Create form data
      let formData = new FormData();
      // Read user inputs
      formData.append("id", ID);
  
  
      $.ajax({
        method: "POST",
        url: "/hrm/manage_EmployeeAccountk/getBankData",
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        async: false,
        success: function (response) {
          if (!response.isError) {
         
            insertType = "Update";
            $(".AddBankDetail").modal("show");
            $(".modal-title").text("Update Employee Banks");
            $("#banks").val(response.Message.bank);
            $("#Account").val(response.Message.Account);
            $("#expire_date").val(response.Message.expire_date);
            

            // formData.append("employee_id", employee_id);
            // formData.append("banks", $("#banks").val());
            // formData.append("Account", $("#Account").val());
            // formData.append("expire_date", $("#expire_date").val());

            let x = response.Message.id;
            console.log("waxan wada  " + x);
            $("#empoyee_bank_id").val(x);
         
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
    function GetAllEmpoBanks() {
      // Create form data
      let formData = new FormData();
      // Read user inputs
      formData.append("id", employee_id);
      $.ajax({
        method: "POST",
        url: "/hrm/manage_EmployeeAccountk/getAllBankData",
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        async: false,
        success: function (response) {
          if (!response.isError) {
            let table = $("#employee_bank_table").DataTable().clear().draw();
  
            for (let index = 0; index < response.Message.length; index++) {
              let temp = [
            //     'id': getemployeBankDetail[xjobdetail].id,
            //     'banks': getemployeBankDetail[xjobdetail].banks.name,
            //     'EmployeeName': getemployeBankDetail[xjobdetail].employee.get_full_name,
            //     'account_number': getemployeBankDetail[xjobdetail].account_number,
            //     'expire_date': getemployeBankDetail[xjobdetail].Expire_date,

                response.Message[index].banks,
                response.Message[index].EmployeeName,
                response.Message[index].account_number,
             
              
  
  
                `<a href="#" class="editBankButton" employe_bank_id=${response.Message[index].id}  style="color:white;" >
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
  
  