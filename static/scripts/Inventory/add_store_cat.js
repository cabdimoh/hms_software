$(document).ready(function() {
    insertType = "Insert"
    $("#btnn_submit").on("click", function(e) {




        // Prevent the page from loading or refreshing
        e.preventDefault();

        // Create form data
        let formData = new FormData();

        // Read user 
        formData.append("Category_Name", $("#Category_Name").val());
        formData.append("Description", $("#Description").val());
        let urls = "";
        if (insertType == "Insert") {
            urls = "/inventory/manage-equipment-cat/new_equipment_category"
        } else {
            formData.append("CategoryID", $("#CategoryID").val());
            urls = "/inventory/manage-equipment-cat/update_equipmen_category"

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
                            $("#store_category")[0].reset();
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

$("#store_cat_table tbody").on("click", "#editbuttonequipment", function(e) {
    e.preventDefault();
    const ID = $(this).attr("rowid");

    let formData = new FormData();

    formData.append("category_id", ID);

    $.ajax({
        method: "POST",
        url: "/inventory/manage-equipment-cat/getequipmentcat",
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        async: false,
        success: function(response) {
            if (!response.isError) {

                insertType = "Update";
                $("#myModal").modal("show");
                $("#myModalLabel").text("Update Equipmentcat");

                $("#Category_Name").val(response.Message.category_name);
                $("#Description").val(response.Message.Description);
                $("#CategoryID").val(response.Message.id);
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

})