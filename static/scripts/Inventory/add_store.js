$(document).ready(function() {
    insertType = "Insert"
    let category = "";
    $("#select_store_cat").on("change", () => {
        category = $("#select_store_cat option:selected").val()
    })
    $("#btn_submit").on("click", function(e) {




        // Prevent the page from loading or refreshing
        e.preventDefault();

        // Create form data
        let formData = new FormData();

        // Read user 
        formData.append("ItemName", $("#ItemName").val());
        formData.append("select_store_cat", category);
        formData.append("quantity", $("#quantity").val());
        formData.append("Lost_and_damage", $("#Lost_and_damage").val());
        formData.append("manufaturing", $("#manufaturing").val());
        formData.append("supplier_price", $("#supplier_price").val());

        formData.append("select_employe", $("#select_employe").val());
        let urls = "";
        if (insertType == "Insert") {
            urls = "/inventory/manage-equipment/new_equipment"
        } else {
            formData.append("EquipmentID", $("#EquipmentID").val());
            urls = "/inventory/manage-equipment/update_equipment"

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
                            $("#itemsForm")[0].reset();
                            window.location.replace("/inventory/equipment");
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

$("#EquipmentTable tbody").on("click", "#EditEquipmentButton", function(e) {
    e.preventDefault();
    const ID = $(this).attr("rowid");

    let formData = new FormData();

    formData.append("EquipmentID", ID);

    $.ajax({
        method: "POST",
        url: "/inventory/manage-equipment/getEquipment",
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        async: false,
        success: function(response) {
            if (!response.isError) {

                insertType = "Update";
                $("#myModal").modal("show");
                $("#myModalLabel").text("Update Equipmemnt");

                $("#ItemName").val(response.Message.ItemName);
                $("#select_store_cat").val(response.Message.select_store_cat);
                $("#quantity").val(response.Message.quantity);
                $("#Lost_and_damage").val(response.Message.Lost_and_damage);

                $("#manufaturing").val(response.Message.manufaturing);

                $("#supplier_price").val(response.Message.supplier_price);
                $("#select_employe").val(response.Message.select_employe);
                $("#EquipmentID").val(response.Message.id);
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

$("#btn_submit_refill_equipment").on("click", function(e) {
    // Prevent the page from loading or refreshing
    e.preventDefault();

    // Create form data
    let formData = new FormData();

    // Read user inputs
    formData.append("EquipmenCat", $("#EquipmenCat").val());
    formData.append("SelectStoreCat", $("#SelectStoreCat").val());
    formData.append("Lost_and_damage2", $("#Lost_and_damage2").val());
    formData.append("quantity2", $("#quantity2").val());
    formData.append("manufaturing2", $("#manufaturing2").val());
    formData.append("supplier_price2", $("#supplier_price2").val());

    formData.append("EquipmentID", $("#EquipmentID").val());

    // $("#MedicineID").val(response.Message.id);
    


    $.ajax({
        method: "POST",
        url: "/inventory/manage-equipment/new_refill_equipment",
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
                        $("#itemsForm")[0].reset();
                        window.location.reload();
                    }
                });
            } else {
                Swal.fire({
                    title: response.title,
                    text: response.Message,
                    icon: response.type,
                    confirmButtonClass: "btn btn-danger w-xs mt-2",
                    buttonsStyling: !1,
                    showCloseButton: !0,
                });
            }
        },
        error: function(response) {},
    });


});


$("#EquipmentTable tbody").on("click", "#Refill", function(e) {
    e.preventDefault();
    const ID = $(this).attr("rowid");

    let formData = new FormData();

    formData.append("Equipment_id", ID);

    $.ajax({
        method: "POST",
        url: "/inventory/manage-equipment/refillEquipment",
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        async: false,
        success: function(response) {
            if (!response.isError) {
                // insertType = "Update";
                $("#refillequipment").modal("show");
                $("#myModalLabel").text("refill equipment");
                
                $("#EquipmentID").val(response.Message.id);
               
                $("#EquipmenCat").val(response.Message.EquipmenCat);
                $("#SelectStoreCat").val(response.Message.SelectStoreCat);
                
                
    
                // $("#report").attr({ target: '_blank', href: document_url });
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