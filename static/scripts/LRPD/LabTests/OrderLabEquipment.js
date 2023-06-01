$(document).ready(function() {
    insertType = "Insert";
    $("#SubmitOrder").on("click", function(e) {

        // Prevent the page from loading or refreshing
        e.preventDefault();
        // Create form data
        let formData = new FormData();

        // Read user 
        formData.append("ItemName", $("#ItemName").val());
        formData.append("Quantity", $("#Quantity").val());
        let urls = "";
        if (insertType == "Insert") {
            urls = "/prescription/manage-lab-equipment-order/new_lab_eq_order";
        } else {
            formData.append("TestID", $("#TestID").val());
            urls = "/prescription/manage-lab-test/edit_test";
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
                            $("#OrderForm")[0].reset();
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
            error: function(response) {},
        });
    });

    //Retrieving single data and display modal
    $("#TestTable tbody").on("click", "#editButtonTest", function(e) {
        e.preventDefault();
        const ID = $(this).attr("rowid");
        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("TestID", ID);


        $.ajax({
            method: "POST",
            url: "/prescription/manage-lab-test/get_test",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {

                    insertType = "Update";
                    $("#labTestModal").modal("show");
                    $("#myModalLabel").text("Update Test");

                    $("#TestName").val(response.Message.TestName);
                    $("#TestUnit").val(response.Message.TestUnit);
                    $("#TestDescription").val(response.Message.TestDescription);
                    $("#NormalRange").val(response.Message.NormalRange);
                    $("#TestID").val(response.Message.id);

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