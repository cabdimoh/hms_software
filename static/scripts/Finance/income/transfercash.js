$(document).ready(function () {   

    $("#DataNumber").val($("#DataNumber").attr("DataNumber"));
    $("#DataNumber").change(function () {
        RefreshPage();
    });

    $("#SearchQuery").on("change", function () {
        RefreshPage();
    });



    $(".pagination .page-item").on("click", function () {
        const pageNumber = $(this).attr("page");
        $(".activePage").attr("activePage", pageNumber);
        RefreshPage();
    });


    function RefreshPage() {
        let page = $(".activePage").attr("activePage");
        let search = $("#SearchQuery").val();
        let entries = $("#DataNumber").val();
  


        let url = `/finance/income-transfer?DataNumber=${entries}&page=${page}`;

        if (search != "") {
            url += `&SearchQuery=${search}`;
        }
        

        window.location.replace(url);
       
    }

});


$('#transfer_cash').on('click', function () {
    $(".transfer_modal").modal("show");

  
    insertType = "Insert";

  });


// save cash transfer

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







//   edit cash transfe r
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


// type of cash transfer
$("#transfer_cash_type").on("change", function () {
    $("#fromAccount").html("");
    $("#toAccount").html("");
    const transfer_cash_type=$("#transfer_cash_type").val()
    if(transfer_cash_type!="" && transfer_cash_type !=undefined){
        if(transfer_cash_type=="form-income-source"){
            get_income_source()
        }
        else{
            get_Main_Account()
        }}
        
    // if ($("#transfer_cash_type").val() != "") {     
    //     if ($("option:selected", "#transfer_cash_type").text() == "Transfer to Account") {          
          
    //         get_Main_Account()
   

    //     }
    //     else if ($("option:selected", "#transfer_cash_type").text() == "Transfer from Source") {
    //         $("#toAccount").html("");
    //         get_income_source()



    //     }
    //     else if ($("option:selected", "#transfer_cash_type").text() == "Director Secretory") {
    //         get_Main_Account()
    //         $(".directorClass").removeClass("col-lg-12");

    //         $(".directorClass").addClass("col-lg-6");
    //         $(".secretoryClass").removeClass("d-none");
    //         $(".departmentClass").addClass("d-none");


    //     }
    //     else if ($("option:selected", "#empl_type").text() == "Section Head") {
    //         $(".directorClass").removeClass("col-lg-12");
    //         $(".directorClass").addClass("col-lg-6");
    //         $(".directorClass").removeClass("d-none");

    //         $(".secretoryClass").addClass("d-none");
    //         $(".departmentClass").removeClass("d-none");
    //         $(".departmentClass").removeClass("col-lg-12");

    //         $(".departmentClass").addClass("col-lg-6");
    //         $(".sections").removeClass("d-none");
    //         $(".netpayClass").addClass("col-lg-12");

    //     }
    //     else {

    //         $(".directorClass").removeClass("col-lg-12");
    //         $(".directorClass").addClass("col-lg-6");

    //         $(".departmentClass").removeClass("col-lg-12");
    //         $(".departmentClass").addClass("col-lg-6");

    //         $(".secretoryClass").addClass("d-none");
    //         $(".departmentClass").removeClass("d-none");

    //         $(".sections").removeClass("d-none");
    //         $(".netpayClass").removeClass("col-lg-6");
    //         $(".netpayClass").addClass("col-lg-12");



    //     }
    // } else {

    //     $(".directorClass").removeClass("col-lg-12");
    //     $(".directorClass").addClass("col-lg-6");
    //     $(".departmentClass").removeClass("col-lg-12");
    //     $(".departmentClass").addClass("col-lg-6");
    //     $(".secretoryClass").addClass("d-none");
    //     $(".departmentClass").removeClass("d-none");
    //     $(".sections").removeClass("d-none");
    //     $(".sections").removeClass("col-lg-12");
    //     $(".sections").addClass("col-lg-6");
    //     $(".netpayClass").removeClass("col-lg-6");
    //     $(".netpayClass").addClass("col-lg-12");

    // }
});

$("#fromAccount").on("change", function (e) {
    $("#toAccount").html("");
    const id = $("#fromAccount").val() 
    const transfer_cash_type=$("#transfer_cash_type").val()
  
    if(id!="" && id !=undefined){
        if(transfer_cash_type=="form-income-source"){
            get_Main_Accountto('All')
        }
        else{
            get_Main_Accountto(id)
        }


       
    }





    

})


function get_Main_Account() {
    // let formData = new FormData();
   

    $.ajax({
        method: "POST",
        url: "/finance/manage-transfer-income-source/get_all_main_banks",
        async: false,
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        // data: formData,
        success: function (response) {
            if (!response.isError) {
                
                $("#fromAccount").html("");
                // if the data length is 0
               
                if (response.Message.length == 0) {
                    $("#fromAccount").append(
                        `<option value="Not available">Not available</option>`
                    );                   
                }
                response.Message.forEach((item, index) => {
                    index == 0 &&
                        $("#fromAccount").append(
                            `<option value="">Select Account</option>`
                        );
                    $("#fromAccount").append(
                        `<option value="${item.id}">${item.name}</option>`
                    );
                });
            } else {
                Swal.fire("Something Wrong!!", response.Message, "error");
            }
        },
        error: function (error) { },
    });
}
function get_Main_Accountto(id) {
    let formData = new FormData();
    formData.append("ID", id);


   

    $.ajax({
        method: "POST",
        url: "/finance/manage-transfer-income-source/get_all_main_banks",
        async: false,
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        success: function (response) {
            if (!response.isError) {
               
                $("#toAccount").html("");
                // if the data length is 0
                
                if (response.Message.length == 0) {
                    $("#toAccount").append(
                        `<option value="Not available">Not available</option>`
                    );                   
                }
                response.Message.forEach((item, index) => {
                    index == 0 &&
                        $("#toAccount").append(
                            `<option value="">Select Account</option>`
                        );
                    $("#toAccount").append(
                        `<option value="${item.id}">${item.name}</option>`
                    );
                });
            } else {
                Swal.fire("Something Wrong!!", response.Message, "error");
            }
        },
        error: function (error) { },
    });
}

function get_income_source() {
    // let formData = new FormData();
   

    $.ajax({
        method: "POST",
        url: "/finance/manage-transfer-income-source/get_all_income_source",
        async: false,
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        // data: formData,
        success: function (response) {
            if (!response.isError) {
                $("#fromAccount").html("");
                // if the data length is 0
                
                if (response.Message.length == 0) {
                    $("#fromAccount").append(
                        `<option value="Not available">Not available</option>`
                    );                   
                }
                response.Message.forEach((item, index) => {
                    index == 0 &&
                        $("#fromAccount").append(
                            `<option value="">Select income sources</option>`
                        );
                    $("#fromAccount").append(
                        `<option value="${item.id}">${item.name}</option>`
                    );
                });
            } else {
                Swal.fire("Something Wrong!!", response.Message, "error");
            }
        },
        error: function (error) { },
    });
}
