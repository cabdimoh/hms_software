$(document).ready(function() {

    $('#add_radiology_exam').on('click', function() {
        $(".add_radiology_exam").modal("show");


        $("#ExamName").val('');
        $("#ExamDescription").val('');
        $("#category").val('');
        insertType = "Insert";


    });


     $("#SubmitRadiologyTest").on("click", function(e) {

        // Prevent the page from loading or refreshing
        e.preventDefault();
        // Create form data
        let formData = new FormData();

        // Read user 
        formData.append("ExamName", $("#ExamName").val());
        formData.append("ExamDescription", $("#ExamDescription").val());
        formData.append("category", $("#category").val());
        let urls = "";
        if (insertType == "Insert") {
            urls = "/prescription/manage-radiology-exam/new_radiologyExam";
        } else {
            formData.append("ExamID", $("#ExamID").val());
            urls = "/prescription/manage-radiology-exam/edit_radiologyExam";
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
                            $("#RadiologyExamForm")[0].reset();
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
    $("#RadiologyTable tbody").on("click", "#edit_exam", function(e) {
        e.preventDefault();
        const ID = $(this).attr("rowid");
        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("ExamID", ID);


        $.ajax({
            method: "POST",
            url: "/prescription/manage-radiology-exam/get_radiologyExam",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {

                    insertType = "Update";
                    $("#RadiologyExamModal").modal("show");
                    $("#myModalLabel").text("Update Radiology Exam");

                    $("#ExamName").val(response.Message.ExamName);
                    $("#ExamDescription").val(response.Message.ExamDescription);
                    $("#ExamID").val(response.Message.id);
                    $("#category").val(response.Message.category);

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