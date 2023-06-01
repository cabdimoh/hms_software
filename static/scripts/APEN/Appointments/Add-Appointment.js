$(document).ready(function() {
    const today = new Date().toISOString().split('T')[0];
  // Set the value of the input to today's date
    document.getElementById("AppointmentDate").value = today;
    let Speciality = "";
    $("#Speciality").on("change", () => {
        Speciality = $("#Speciality option:selected").val()
    })

    let Doctor = "";
    $("#Doctor").on("change", () => {
        Doctor = $("#Doctor option:selected").val()
    })

    $("#SubmitAppointments").on("click", function(e) {
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
        formData.append("PatientMarital", $("#PatientMarital").val());
        formData.append("PatientMobileNo", $("#PatientMobileNo").val());
        formData.append("PatientDistrict", $("#PatientDistrict").val());
        formData.append("Doctor", $("#Doctor_id").val());
        formData.append("hidden_btn", $("#hidden_btn").val());


        $.ajax({
            method: "POST",
            url: "/patient/manage-appointment/new_appointment",
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
                            $("#AppointmentForm")[0].reset();
                            window.location.replace("/patient/appointment-list");
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


    const PatientFirstName = $("#PatientFirstName")
    const PatientMiddleName = $("#PatientMiddleName")
    const PatientLastName = $("#PatientLastName")
    const PatientAge = $("#PatientAge")
    const PatientVillage = $("#PatientVillage")
    const PatientGender = $("#PatientGender")
    const PatientMobileNo = $("#PatientMobileNo")
    const PatientDistrict = $("#PatientDistrict")
    const hidden_btn = $("#hidden_btn")

    $("#SearchExistingPatient").on('input', function() {

        const value = $(this).val()
        if (value.length > 2) {
            PatientFirstName.val("")
            PatientMiddleName.val("")
            PatientLastName.val("")
            PatientAge.val("")
            PatientVillage.val("")
            PatientGender.val("")
            PatientMobileNo.val("")
            PatientDistrict.val("")

            $.ajax({
                type: "GET",
                url: "/patient/search-existing-patient/" + value,
                async: false,
                headers: { "X-CSRFToken": csrftoken },
                success: function(response) {
                    hidden_btn.val(response.Message[0].id);
                    PatientFirstName.val(response.Message[0].PatientFirstName);
                    PatientMiddleName.val(response.Message[0].PatientMiddleName);
                    PatientLastName.val(response.Message[0].PatientLastName);
                    PatientAge.val(response.Message[0].PatientAge);
                    PatientVillage.val(response.Message[0].PatientVillage);
                    PatientGender.val(response.Message[0].PatientGender);
                    PatientMobileNo.val(response.Message[0].PatientMobileNo);
                    PatientDistrict.val(response.Message[0].PatientDistrict);
                },
                error: function(err) {
                    alert(err)
                }


            })

        } else {
            PatientFirstName.val("")
            PatientMiddleName.val("")
            PatientLastName.val("")
            PatientAge.val("")
            PatientVillage.val("")
            PatientGender.val("")
            PatientMobileNo.val("")
            PatientDistrict.val("")
        }
    })

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
                minLength: 0,
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
                                `<option value="">Select Doctors </option>`
                            );
                        $("#Doctor_id").append(
                            `<option  value="${item.employe_id}">${item.name} ( ${item.status} )</option>`
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