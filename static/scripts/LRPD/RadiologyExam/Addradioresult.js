$(document).ready(function() {
    insertType = "Insert";
    let ID = "";
    var id_increment = 1;

    $("#resultDocument").on("change", function(e) {
        documents = e.target.files[0];
    });

    $("#SubmitRadiologyResult").on("click", function(e) {
        // Prevent the page from loading or refreshing
        e.preventDefault();
        // Create form data
        let formData = new FormData();



        let findings = [];
        let impressions = [];
        let recommendations = [];
        let comments = [];
        let result_files = [];
        let exam_id = [];

        let id_s = []
        $('textarea[rdlogy = "rdlogy"]').each(function() {
            var id = $(this).attr('id');
            var matches = id.match(/(\D+)(\d+)/);
            var numberPart = parseInt(matches[2]);
            id_s.push(numberPart);
        });
        for (let i = 0; i < id_s.length; i++) {
            findings.push($("#findings" + id_s[i]).val());
            impressions.push($("#impressions" + id_s[i]).val());
            recommendations.push($("#recommendations" + id_s[i]).val());
            comments.push($("#comments" + id_s[i]).val());
            exam_id.push($("#exam_id" + id_s[i]).val());
            var files = $("#result_files" + id_s[i])[0].files;
            for (let j = 0; j < files.length; j++) {
                formData.append("result_files_" + id_s[i], files[j]);
            }
        }
        findings = findings.join(':');
        impressions = impressions.join(':');
        recommendations = recommendations.join(':');
        comments = comments.join(':');
        // Read user 
        // let examID = [];
        // // let findings = [];
        // // let impressions = [];
        // // let recommendations = [];
        // // let comments = [];
        // // let result_files = [];
        // for (let i = 2; i <= id_increment; i++) {
        //     examID.push($("#examID" + i).val());
        //     findings.push($("#findings" + i).val());
        //     impressions.push($("#impressions" + i).val());
        //     recommendations.push($("#recommendations" + i).val());
        //     comments.push($("#comments" + i).val());
        //     result_files.push($("#result_files" + i).val());
        // }
        formData.append("ID", $("#order_id").val());
        formData.append("examID", exam_id);
        formData.append("Collected_by", $("#Collected_by").val());
        formData.append("CollectionDate", $("#CollectionDate").val());

        formData.append("findings", findings);
        formData.append("impressions", impressions);
        formData.append("recommendations", recommendations);
        formData.append("comments", comments);
        formData.append("result_files", result_files);


        $.ajax({
            method: "POST",
            url: "/prescription/manage-radiology-result/new_radiologyresult",
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
                            $("#radioresult")[0].reset();
                            window.location.replace("/prescription/radiology-exam-orders");
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

    
    $("#UpdateRadiologyResult").on("click", function(e) {
        // Prevent the page from loading or refreshing
        e.preventDefault();
        // Create form data
        let formData = new FormData();



        let findings = [];
        let impressions = [];
        let recommendations = [];
        let comments = [];
        let result_files = [];
        let exam_id = [];

        let id_s = []
        $('textarea[rdlogy = "rdlogy"]').each(function() {
            var id = $(this).attr('id');
            var matches = id.match(/(\D+)(\d+)/);
            var numberPart = parseInt(matches[2]);
            id_s.push(numberPart);
        });
        for (let i = 0; i < id_s.length; i++) {
            findings.push($("#findings" + id_s[i]).val());
            impressions.push($("#impressions" + id_s[i]).val());
            recommendations.push($("#recommendations" + id_s[i]).val());
            comments.push($("#comments" + id_s[i]).val());
            exam_id.push($("#exam_id" + id_s[i]).val());
            var files = $("#result_files" + id_s[i])[0].files;
            for (let j = 0; j < files.length; j++) {
                formData.append("result_files", files[j]);
            }

        }
        findings = findings.join(':');
        impressions = impressions.join(':');
        recommendations = recommendations.join(':');
        comments = comments.join(':');
        // Read user 
        // let examID = [];
        // // let findings = [];
        // // let impressions = [];
        // // let recommendations = [];
        // // let comments = [];
        // // let result_files = [];
        // for (let i = 2; i <= id_increment; i++) {
        //     examID.push($("#examID" + i).val());
        //     findings.push($("#findings" + i).val());
        //     impressions.push($("#impressions" + i).val());
        //     recommendations.push($("#recommendations" + i).val());
        //     comments.push($("#comments" + i).val());
        //     result_files.push($("#result_files" + i).val());
        // }
        formData.append("ID", $("#order_id").val());
        formData.append("examID", exam_id);
        formData.append("Collected_by", $("#Collected_by").val());
        formData.append("CollectionDate", $("#CollectionDate").val());

        formData.append("findings", findings);
        formData.append("impressions", impressions);
        formData.append("recommendations", recommendations);
        formData.append("comments", comments);
        formData.append("result_files", result_files);

       
        $.ajax({
            method: "POST",
            url:"/prescription/manage-radiology-result/edit_radiologyresult",

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
                            $("#radioresult")[0].reset();
                            window.location.replace("/prescription/radiology-result");
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
});