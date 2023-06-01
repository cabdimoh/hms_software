$(document).ready(function() {
    insertType = "Insert"
    $("#btn_submit_edit_transacrion_refill").on("click", function(e) {




        // Prevent the page from loading or refreshing
        e.preventDefault();

        // Create form data
        let formData = new FormData();

        // Read user 
        formData.append("bach_no3", $("#bach_no3").val());
        formData.append("ExpireDate3", $("#ExpireDate3").val());
        formData.append("supplierPrice3", $("#supplierPrice3").val());

        formData.append("box3", $("#box3").val());

        formData.append("quantity3", $("#quantity3").val());
        formData.append("manufacturingdate3", $("#manufacturingdate3").val());
        formData.append("Medicinerefilid", $("#medid").val());

        


        let urls = "";
        if (insertType == "Insert") {
            urls = "/inventory/manage-medicine/edit_refill_med_transaction"
        } else {
            formData.append("CategoryID", $("#CategoryID").val());
            urls = "/inventory/manage-medicine/update_equipmen_category1"

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
                            $("#medicineForm1")[0].reset();
                            window.location.reload();
                            // $(".bank_modal").modal("hide");

                            // Read all spouses information
                            // getBanks(employeeID);
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



    insertType = "Insert"
    $("#btn_submit_transection2").on("click", function(e) {




        // Prevent the page from loading or refreshing
        e.preventDefault();

        // Create form data
        let formData = new FormData();

        // Read user 
        formData.append("bach_no2", $("#bach_no2").val());
        formData.append("ExpireDate2", $("#ExpireDate2").val());
        formData.append("supplierPrice2", $("#supplierPrice2").val());

        formData.append("box2", $("#box2").val());

        formData.append("quantity2", $("#quantity2").val());
        formData.append("manufacturingdate2", $("#manufacturingdate2").val());
        formData.append("medicineid", $("#medid1").val());

        


        let urls = "";
        if (insertType == "Insert") {
            urls = "/inventory/manage-medicine/edit_purchase_medicine_transaction"
        } else {
            formData.append("CategoryID", $("#CategoryID").val());
            urls = "/inventory/manage-medicine/update_equipmen_category2"

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
                            $("#medicinedit")[0].reset();
                            window.location.reload();
                            // $(".bank_modal").modal("hide");

                            // Read all spouses information
                            // getBanks(employeeID);
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
});

