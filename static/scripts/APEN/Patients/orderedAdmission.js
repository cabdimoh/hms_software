$(document).ready(function() {
    insertType = "Insert";

    

    //Retrieving patient info in admission form
    $("#ordered_admission tbody").on("click", "#admitpatient", function(e) {
        e.preventDefault();
        ID = $(this).attr("rowid");
        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("orderid", ID);

        let Tests = "";
        $.ajax({
            method: "POST",
            url: "/patient/manage-ordered-admission/get_ordered_admission",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {
                    // insertType = "Update";
                    $("#admitPatient").modal("show");
                    $("#myModalLabel").val("Update Test");
                    var address = response.Message.PatientVillage + ', ' + response.Message.PatientDistrict
                    $("#hidden_admission_order").val(response.Message.OrderId);
                    $("#patient").val(response.Message.patientFullname);
                    $("#doctor").val(response.Message.Doctor);
                    $("#age").val(response.Message.PatientAge);
                    $("#gender").val(response.Message.PatientGender);
                    $("#mobileNo").val(response.Message.PatientMobileNo);
                    $("#address").val(address);
                    $("#admissionDate").val(response.Message.admissionDate);
                 



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
    //Retrieving patient info in admission form
    $("#ordered_admission tbody").on("click", "#viewOrderedAdmisson", function(e) {
        e.preventDefault();
        ID = $(this).attr("rowid");
        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("orderid", ID);

        let Tests = "";
        $.ajax({
            method: "POST",
            url: "/patient/manage-ordered-admission/get_ordered_admission",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {
                    // insertType = "Update";
                    $("#viewOrderedadmisson").modal("show");
                    $("#myModalLabel").val("Admisson Order Letter");
                    var address = response.Message.PatientVillage + ', ' + response.Message.PatientDistrict
                    $("#hidden_admission_order_view").val(response.Message.OrderId);
                    $("#patient_view").val(response.Message.patientFullname);
                    $("#doctor_view").val(response.Message.Doctor);
                    $("#age_view").val(response.Message.PatientAge);
                    $("#gender_view").val(response.Message.PatientGender);
                    $("#mobileNo_view").val(response.Message.PatientMobileNo);
                    $("#address_view").val(address);
                    $("#admissionDate_view").val(response.Message.admissionDate);
                    $("#orderedBy_view").val(response.Message.orderedBy);
                    $("#Note_view").text(response.Message.Note);
                    $("#admissonReason_view").text(response.Message.admissonReason);
                    $("#patientPriority_view").val(response.Message.patientPriority);
                
                


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
    //--------------------- get room and beds-------
    // chained dropdown for departments and rooms
    $("#Room_category").on("change", function() {

        // Clear all other fields
        $("#room").html("");


        // if the data selected is not empty
        if ($(this).val() != "") {
            get_category_room($("#Room_category").val());
        }
    });
    // chained dropdown for Room_category and rooms
    function get_category_room(Room_category) {
        let formData = new FormData();
        formData.append("Room_category", Room_category);
        $.ajax({
            method: "POST",
            url: "/patient/manage-ordered-admission/get_room_category",
            async: false,
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            success: function(response) {
                if (!response.isError) {

                    $("#room").html("");

                    // if the data length is 0
                    if (response.Message.length == 0) {
                        // Add disabled attribute from directorate
                        // $("#job_directorate").attr("disabled", true);
                        $("#room").append(
                            `<option value="Not available">Not available</option>`
                        );
                        
                    } else {
                    
                    }

                    response.Message.forEach((item, index) => {
                        index == 0 &&
                            $("#room").append(
                                `<option value="">Select room</option>`
                            );
                        $("#room").append(
                            `<option value="${item.id}">${item.name}</option>`
                        );
                    });
                } else {
                    Swal.fire("Something Wrong!!", data.Message, "error");
                }
            },
            error: function(error) {},
        });
    }
    // chained dropdown for rooms and beds
    $("#room").on("change", function() {

        // Clear all other fields
        $("#bed").html("");


        // if the data selected is not empty
        if ($(this).val() != "") {
            get_room_bed($("#room").val());
        }
    });
    // chained dropdown for rooms and beds
    function get_room_bed(room) {
        let formData = new FormData();
        formData.append("room", room);
        $.ajax({
            method: "POST",
            url: "/patient/manage-emergency-profile/get_bed_room",
            async: false,
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            success: function(response) {
                if (!response.isError) {

                    $("#bed").html("");

                    // if the data length is 0
                    if (response.Message.length == 0) {
                        // Add disabled attribute from directorate
                        // $("#job_directorate").attr("disabled", true);
                        $("#bed").append(
                            `<option value="Not available">Not available</option>`
                        );
                        
                    } else {
                    
                    }

                    response.Message.forEach((item, index) => {
                        index == 0 &&
                            $("#bed").append(
                                `<option value="">Select bed</option>`
                            );
                        $("#bed").append(
                            `<option value="${item.id}">${item.name}</option>`
                        );
                    });
                } else {
                    Swal.fire("Something Wrong!!", data.Message, "error");
                }
            },
            error: function(error) {},
        });
    }

    //---------------------finish get room and beds-----

    // ------submit admission Form---------
    $("#submit_admission").on("click", function(e) {
        // Prevent the page from loading or refreshing
        e.preventDefault();

        // Create form data
        let formData = new FormData();

        // Read user inputs
        formData.append("hidden_admission_order", $("#hidden_admission_order").val());
        formData.append("bed", $("#bed").val());
        formData.append("room", $("#room").val());
        formData.append("guardianName", $("#guardianName").val());
        formData.append("guardianrelation", $("#guardianrelation").val());
        formData.append("guardianMobileNo", $("#guardianMobileNo").val());
        formData.append("guardianAddress", $("#guardianAddress").val());
    
        $.ajax({
            method: "POST",
            url: "/patient/manage-ordered-admission/new_admission_form",
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
    //-------finish submitting admission Form------
});