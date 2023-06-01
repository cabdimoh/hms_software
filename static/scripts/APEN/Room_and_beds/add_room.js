$(document).ready(function() {
    insertType = "Insert";
    $("#btn_submit").on("click", function(e) {

        // Prevent the page from loading or refreshing
        e.preventDefault();
        // Create form data
        let formData = new FormData();

        // Read user 
        formData.append("RoomCtategory", $("#RoomCtategory").val());
        formData.append("RoomNo", $("#RoomNo").val());
        
        let urls = "";
        if (insertType == "Insert") {
            urls = "/patient/manage-room/new_room"

        } else {
            formData.append("id", $("#id").val());
            urls = "/patient/manage-room/update_room"
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
                            $("#categoryForm")[0].reset();
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

    // Retrieving single data and display modal
    $("#Category_Table tbody").on("click", "#editButtonCat", function(e) {
        e.preventDefault();
        const ID = $(this).attr("rowid");
        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("id", ID);


        $.ajax({
            method: "POST",
            url: "/patient/manage-room/getroom",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {

                    insertType = "Update";
                    $("#CategoryModal").modal("show");
                    $("#myModalLabel").text("Update room cat");
                    $("#RoomCtategory").val(response.Message.RoomCtategory);
                    $("#RoomNo").val(response.Message.RoomNo);
                   
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

    $("#Category_Table tbody").on("click", "#Refeil", function(e) {
        e.preventDefault();
        const ID = $(this).attr("rowid");
    
        let formData = new FormData();
    
        formData.append("id", ID);
    
        $.ajax({
            method: "POST",
            url: "/patient/manage-room/add_bed",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {
                    // insertType = "Update";
                    $("#Aaddbed").modal("show");
                    $("#myModalLabel").text("add bed");
                    
                    $("#roomno").val(response.Message.id);
                   
                    $("#RoomNomber").val(response.Message.RoomNomber);
                   
                    
                    
        
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
    $("#btn_submit_bed").on("click", function(e) {
        // Prevent the page from loading or refreshing
        e.preventDefault();
    
        // Create form data
        let formData = new FormData();
    
        // Read user inputs
        formData.append("RoomNomber", $("#RoomNomber").val());
        formData.append("BedNo", $("#BedNo").val());
        
    
        formData.append("roomno", $("#roomno").val());
    
        // $("#MedicineID").val(response.Message.id);
        
    
    
        $.ajax({
            method: "POST",
            url: "/patient/manage-room/new_bed",
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
                            $("#categoryForm")[0].reset();
                            window.location.replace("/patient/add-room");
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

    
});

