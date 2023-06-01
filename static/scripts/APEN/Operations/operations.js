$(document).ready(function() {
    insertType = "Insert";
    $("#btn_submit").on("click", function(e) {

        // Prevent the page from loading or refreshing
        e.preventDefault();
        // Create form data
        let formData = new FormData();

        // Read user 
        formData.append("OperationName", $("#OperationName").val());
        formData.append("CategoryName", $("#CategoryName").val());
        formData.append("Description", $("#Description").val());
        let urls = "";
        if (insertType == "Insert") {
            urls = "/patient/manage-operations/new_operations"

        } else {
            formData.append("id", $("#id").val());
            urls = "/patient/manage-operations/update_operations"
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
                            $("#operationForm")[0].reset();
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
    $("#operationTable tbody").on("click", "#editButtonOperations", function(e) {
        e.preventDefault();
        const ID = $(this).attr("rowid");
        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("id", ID);


        $.ajax({
            method: "POST",
            url: "/patient/manage-operations/getOperations",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {

                    insertType = "Update";
                    $("#OperationModal").modal("show");
                    $("#myModalLabel").text("Update Operations");
                    $("#OperationName").val(response.Message.Operation);
                    $("#CategoryName").val(response.Message.CategoryName);
                    $("#Description").val(response.Message.Description);
                    $("#id").val(response.Message.id);
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