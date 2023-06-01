$(document).ready(function() {
    getdata(AppointmentId)

    $("#UpdateSaveBtn").on("click", function(e) {
        // Prevent the page from loading or refreshing

        e.preventDefault();
        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("PatientFirstName", $("#PatientFirstName").val());
        formData.append("PatientMiddleName", $("#PatientMiddleName").val());
        formData.append("PatientLastName", $("#PatientLastName").val());
        formData.append("PatientAge", $("#PatientAge").val());
        formData.append("PatientVillage", $("#PatientVillage").val());
        formData.append("jobtype_ids", $("#userIDs").val());        
        formData.append("AppointmentDate", $("#AppointmentDate").val());
        formData.append("PatientGender", $("#PatientGender").val());
        formData.append("PatientMobileNo", $("#PatientMobileNo").val());
        formData.append("PatientDistrict", $("#PatientDistrict").val());
        formData.append("Doctor", $("#Doctor_id").val());
        formData.append("AppointmentId", AppointmentId);
        $.ajax({
            method: "POST",
            url: "/patient/manage-appointment/update_appointment",
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
                            window.location.replace("/patient/appointment-list")
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
    //Retrieving single data and display modal
    function getdata(id) {

        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("AppointmentId", id);
        $.ajax({
            method: "POST",
            url: "/patient/manage-appointment/getAppointmentData",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {

                    $("#PatientFirstName").val(response.Message.PatientFirstName);
                    $("#PatientMiddleName").val(response.Message.PatientMiddleName);
                    $("#PatientLastName").val(response.Message.PatientLastName);
                    $("#PatientAge").val(response.Message.PatientAge);
                    $("#PatientVillage").val(response.Message.PatientVillage);
                    $("#search").val(response.Message.Speciality);
                    $("#AppointmentDate").val(response.Message.AppointmentDate);
                    $("#PatientGender").val(response.Message.PatientGender);
                    $("#PatientMobileNo").val(response.Message.PatientMobileNo);
                    $("#PatientDistrict").val(response.Message.PatientDistrict);
                    $("#userIDs").val(response.Message.Speciality_id);
                    
                      GetJobDetails(response.Message.Speciality_id)
                    $("#Doctor_id").val(response.Message.doctorid);


                    console.log(response.Message.Doctors);

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

    }

    $("#search").on("input", function(e) {
        $('#Doctor_id').html('')
        $('#userIDs').val('')
        var listUsers = [];
        if ($(this).val() != "" && $(this).val().length > 0) {
            listUsers = SearchEngine($(this).val());
            $("#search").autocomplete({
                source: listUsers,
                select: function(event, ui) {
                    const item = ui.item.userid;
                    const employe_id = ui.item
                    const value = ui.item.value;

                    if (value != "") {
                        $("#userIDs").val(item);
                        GetJobDetails(item);
                        getjobtype(item);
                    }
                },
                response: function(event, ui) {
                    if (!ui.content.length) {
                        var noResult = { value: "", label: "No result found" };
                        ui.content.push(noResult);
                    }
                },
                minLength: 1,
            });
        }
    });

    function SearchEngine(letter) {
        let formData = new FormData();
        formData.append("employee", letter);
        var list = [];
        $.ajax({
            method: "POST",
            url: "/patient/search_speciality/",
            processData: false,
            contentType: false,
            data: formData,
            headers: { "X-CSRFToken": csrftoken },
            async: false,

            success: function(data) {
                data.Message.forEach((user) => {
                    list.push(user);
                });
            },
        });

        return list;
    }

    function getjobtype(ID) {

        let formData = new FormData();

        formData.append("jobtypeid", ID);

        $.ajax({
            method: "POST",
            url: "/patient/manage-appointment/get_jobtype_name",
            processData: false,
            contentType: false,
            data: formData,
            headers: { "X-CSRFToken": csrftoken },
            async: false,
            success: function(response) {
                if (!response.isError) {
                    $("#userIDs").val(response.Message[0].id);



                } else {}
                response.Message;
            },
            error: function(response) {},
        });
    }


    function GetJobDetails(ID) {

        let formData = new FormData();

        formData.append("jobtype_ids", ID);

        $.ajax({
            method: "POST",
            url: "/patient/manage-appointment/get_Doctors_name",
            processData: false,
            contentType: false,
            data: formData,
            headers: { "X-CSRFToken": csrftoken },
            async: false,
            success: function(response) {
                if (!response.isError) {



                    $("#Doctor_id").html("");
                    if (response.Message.length == 0) {
                        $("#Doctor_id").append(
                            `<option value="Not available">Not available Doctors</option>`
                        );

                    } else {
                        // Remove disabled attribute from directorate
                        // $("#job_directorate").attr("disabled", false);
                    }


                    response.Message.forEach((item, index) => {
                        index == 0 &&
                            $("#Doctor_id").append(
                                `<option value="">Select Doctors </option>`                            );
                        $("#Doctor_id").append(
                            `<option value="${item.employe_id}">${item.name}</option>`
                        );
                    });



                } else {
                    Swal.fire("Something Wrong!!", response.Message, "error");
                }
            },
            error: function(response) {},
        });
    }
});