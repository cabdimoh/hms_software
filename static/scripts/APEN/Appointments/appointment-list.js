$(document).ready(function() {

    $("#DataNumber").val($("#DataNumber").attr("DataNumber"));

    $("#dataDate").val($("#dataDate").attr("dataDate"));

    $("#DataNumber").on("change", function() {
        RefreshPage();
    });
    $("#dataDate").on("change", function() {
        RefreshPage();
    });
    $("#SearchQuery").on("change", function() {
        RefreshPage();
    });

    $("#SearchQueryBTN").on("click", function() {
        RefreshPage();
    });

    $(".pagination .page-item").on("click", function() {
        const pageNumber = $(this).attr("page");
        $(".activePage").attr("activePage", pageNumber);
        RefreshPage();
    });

    function RefreshPage() {

        let page = $(".activePage").attr("activePage");
        let search = $("#SearchQuery").val();
        let entries = $("#DataNumber").val();
        let dataDate = $("#dataDate").val();

        let url = `/patient/appointment-list?DataNumber=${entries}&dataDate=${dataDate}&page=${page}`;

        if (search != "") {
            url += `&SearchQuery=${search}`;
        }

        window.location.replace(url);
    }
    //Retrieving single data and display modal
    $("#AppointmentTable tbody").on("click", "#viewAppointment", function(e) {
        e.preventDefault();
        ID = $(this).attr("rowid");
        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("appointId", ID);

        $.ajax({
            method: "POST",
            url: "/patient/manage-appointment/get_appointment_info ",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {
                    // insertType = "Update";
                    $("#ViewAppointment").modal("show");
                    $("#myModalLabel").text("Update Test");
                    var address = response.Message.PatientVillage + ', ' + response.Message.PatientDistrict
                    var Receptionist_fullname = response.Message.Receptionist_first + ' ' + response.Message.Receptionist_last
                    $("#Appoint_id").text(response.Message.AppointmentID);
                    $("#patient").text(response.Message.PatientName);
                    $("#doctor").text(response.Message.Doctor);
                    $("#age").text(response.Message.PatientAge);
                    $("#gender").text(response.Message.PatientGender);
                    $("#mobileNo").text(response.Message.PatientMobileNo);
                    $("#Status").text(response.Message.Status);
                    $("#AppointmentDate").text(response.Message.AppointmentDate);
                    $("#Queue_no").text(response.Message.Queue_no);
                    $("#Receptionist").text(Receptionist_fullname);
                    $("#address").text(address);


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