$(document).ready(function() {


    // saving and updating

    $("#btn_submit1").on("click", function(e) {
        // Prevent the page from loading or refreshing
        e.preventDefault();

        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("CategoryName", $("#CategoryName").val());
        formData.append("Description", $("#Description").val());




        let urls = ""

        if (insertType == "Insert") {
            // urls = "/hrm/manage_EmployeeAccountk/new_Employe_Banksd";
            console.log("PASSED");
        } else {
            urls = "/Inventory/manage-category/update_category";

            // let x = $("#empoyee_bank_id").val();
            // formData.append("id", $("#empoyee_bank_id").val());

        }
        $.ajax({
            method: "POST",
            url: urls,
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
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
                            // hide the modal and resret the form
                            $("#categoryForm1")[0].reset();

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
            error: function(response) {},
        });
    });

    // Retrieving single data and display modal

    $("#editButtonCat").on("click", function(e) {

        e.preventDefault();
        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("Medicine_categories_id", Medicine_categories_id);


        $.ajax({
            method: "POST",
            url: "/hrm/manage-category/getMedicineeCategories",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {

                    insertType = "Update";
                    $(".editBasicEmpInfo").modal("show");
                    $("#modaeltitle").text("Update Employee Basic information");
                    $(".hidephoto").addClass("d-none");

                    $("#CategoryName").val(response.Message.CategoryName);
                    $("#Description").val(response.Message.Description);

                    let x = response.Message.id;
                    console.log("waxan wada  " + x);


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
            error: function(response) {},
        });

    });



    // Get all employee qualification data 
    // function GetAllEmpoBanks() {
    //     // Create form data
    //     let formData = new FormData();
    //     // Read user inputs
    //     formData.append("id", employee_id);

    //     $.ajax({
    //         method: "POST",
    //         url: "/hrm/manage_employees/getAllEmployeData",
    //         headers: { "X-CSRFToken": csrftoken },
    //         processData: false,
    //         contentType: false,
    //         data: formData,
    //         async: false,
    //         success: function (response) {
    //             if (!response.isError) {
    //                 let table = $("#employe_basic_data_table").DataTable().clear().draw();

    //                 for (let index = 0; index < response.Message.length; index++) {
    //                     let temp = [

    //                         response.Message[index].fullname,
    //                         response.Message[index].mother_name,
    //                         response.Message[index].dob,
    //                         response.Message[index].gender,
    //                         response.Message[index].maritial,
    //                         response.Message[index].blood_group,
    //                         response.Message[index].date_join,
    //                         response.Message[index].title_name,



    //                         `<a href="#" class="editBankButton" employe_bank_id=${response.Message[index].id}  style="color:white;" >
    //               <button type="button" class=" btn-primary rounded">

    //                   <i class="las la-pen"></i>

    //               </button>
    //               </a>


    //         `
    //                     ];
    //                     table.row.add(temp).draw();
    //                 }

    //             }
    //         },
    //         error: function (response) { },
    //     });
    // }
});