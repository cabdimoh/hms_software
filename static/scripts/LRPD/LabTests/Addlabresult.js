$(document).ready(function() {
    let insertType = "Insert";
    var id_increment = 1;
    let ID = "";
    $("#resultDocument").on("change", function(e) {
        documents = e.target.files[0];
    });

    $("#SubmitLabbTest").on("click", function(e) {
        // Prevent the page from loading or refreshing
        e.preventDefault();
        // Create form data
        let formData = new FormData();
        // Read user 
        let ResultValue = [];
        let flagvalue = [];
        let TestNumber = [];


        let report = []
        $('input[resultFlag = "resultFlag"]').each(function() {
            var id = $(this).attr('id');
            var matches = id.match(/(\D+)(\d+)/);
            var numberPart = parseInt(matches[2]);
            report.push(numberPart);
        });
        for (let i = 0; i < report.length; i++) {
            TestNumber.push($("#TestNumber" + report[i]).val());
            ResultValue.push($("#ResultValue" + report[i]).val());
            flagvalue.push($("#flagvalue" + report[i]).val());
            console.log(report[i]);

        }
        let stool_test_ids = []
        let stool_test = []
        let stool_test_id = []
        $('input[stool_test = "stool_test"]').each(function() {
            var id = $(this).attr('id');
            var matches = id.match(/(\D+)(\d+)/);
            var numberPart = parseInt(matches[2]);
            console.log('marki qoralka laga saaro', numberPart)
            stool_test_ids.push(numberPart);
        });
        for (let i = 0; i < stool_test_ids.length; i++) {
            stool_test.push($("#stool_test" + stool_test_ids[i]).val());
            stool_test_id.push($("#stool_test_id" + stool_test_ids[i]).val());


        }
        let urine_test_ids = []
        let urine_test = []
        let urine_test_id = []
        $('input[urine_test = "urine_test"]').each(function() {
            var id = $(this).attr('id');
            var matches = id.match(/(\D+)(\d+)/);
            var numberPart = parseInt(matches[2]);
            console.log('marki qoralka laga saaro', numberPart)
            urine_test_ids.push(numberPart);
        });
        for (let i = 0; i < urine_test_ids.length; i++) {
            urine_test.push($("#urine_test" + urine_test_ids[i]).val());
            urine_test_id.push($("#urine_test_id" + urine_test_ids[i]).val());


        }


        // urine
        // physical
        let physical_urine_ids = []
        let physical_urine = []
        let physical_urine_id = []
        $('input[physical_urine = "Physical_Urine"]').each(function() {
            var id = $(this).attr('id');
            var matches = id.match(/(\D+)(\d+)/);
            var numberPart = parseInt(matches[2]);
            physical_urine_ids.push(numberPart);
            console.log(numberPart)

        });

        for (let i = 0; i < physical_urine_ids.length; i++) {
            physical_urine.push($("#Physical_Urine" + physical_urine_ids[i]).val());
            physical_urine_id.push($("#Physical_Urine_id" + physical_urine_ids[i]).val());
        }
        console.log(physical_urine_ids)

        // chemical
        let chemical_urine_ids = []
        let chemical_urine = []
        let chemical_urine_id = []
        $('input[chemical_urine = "Chemical_Urine"]').each(function() {
            var id = $(this).attr('id');
            var matches = id.match(/(\D+)(\d+)/);
            var numberPart = parseInt(matches[2]);
            chemical_urine_ids.push(numberPart);
        });

        for (let i = 0; i < chemical_urine_ids.length; i++) {
            chemical_urine.push($("#Chemical_Urine" + chemical_urine_ids[i]).val());
            chemical_urine_id.push($("#Chemical_Urine_id" + chemical_urine_ids[i]).val());
        }

        // micro
        let micro_urine_ids = []
        let micro_urine = []
        let micro_urine_id = []
        $('input[microscopic_Urine = "Microscopic_Urine"]').each(function() {
            var id = $(this).attr('id');
            var matches = id.match(/(\D+)(\d+)/);
            var numberPart = parseInt(matches[2]);
            micro_urine_ids.push(numberPart);
        });

        for (let i = 0; i < micro_urine_ids.length; i++) {
            micro_urine.push($("#Microscopic_Urine" + micro_urine_ids[i]).val());
            micro_urine_id.push($("#Microscopic_Urine_id" + micro_urine_ids[i]).val());
        }
        // stool
        // physical
        let physical_stool_ids = []
        let physical_stool = []
        let physical_stool_id = []
        $('input[physical_Stool = "Physical_Stool"]').each(function() {
            var id = $(this).attr('id');
            var matches = id.match(/(\D+)(\d+)/);
            var numberPart = parseInt(matches[2]);
            physical_stool_ids.push(numberPart);
        });

        for (let i = 0; i < physical_stool_ids.length; i++) {
            physical_stool.push($("#Physical_Stool" + physical_stool_ids[i]).val());
            physical_stool_id.push($("#Physical_Stool_id" + physical_stool_ids[i]).val());
        }

        // chemical
        let chemical_stool_ids = []
        let chemical_stool = []
        let chemical_stool_id = []
        $('input[chemical_Stool = "Chemical_Stool"]').each(function() {
            var id = $(this).attr('id');
            var matches = id.match(/(\D+)(\d+)/);
            var numberPart = parseInt(matches[2]);
            chemical_stool_ids.push(numberPart);
        });

        for (let i = 0; i < chemical_stool_ids.length; i++) {
            chemical_stool.push($("#Chemical_Stool" + chemical_stool_ids[i]).val());
            chemical_stool_id.push($("#Chemical_Stool_id" + chemical_stool_ids[i]).val());
        }

        // micro
        let micro_stool_ids = []
        let micro_stool = []
        let micro_stool_id = []
        $('input[microscopic_stool = "Microscopic_Stool"]').each(function() {
            var id = $(this).attr('id');
            var matches = id.match(/(\D+)(\d+)/);
            var numberPart = parseInt(matches[2]);
            micro_stool_ids.push(numberPart);
        });

        for (let i = 0; i < micro_stool_ids.length; i++) {
            micro_stool.push($("#Microscopic_Stool" + micro_stool_ids[i]).val());
            micro_stool_id.push($("#Microscopic_Stool_id" + micro_stool_ids[i]).val());
        }

        formData.append("Comment", $("#lab_comment").val());
        formData.append("Collected_by", $("#Collected_by").val());
        formData.append("CollectionDate", $("#CollectionDate").val());

        formData.append("order_id", $("#order_id").val());

        formData.append("stool_test", stool_test);
        formData.append("stool_test_id", stool_test_id);

        formData.append("urine_test", urine_test);
        formData.append("urine_test_id", urine_test_id);

        formData.append("TestNumber", TestNumber);
        formData.append("ResultValue", ResultValue);
        formData.append("flagvalue", flagvalue);

        formData.append("physical_stool", physical_stool);
        formData.append("chemical_stool", chemical_stool);
        formData.append("micro_stool", micro_stool);
        formData.append("physical_stool_id", physical_stool_id);
        formData.append("chemical_stool_id", chemical_stool_id);
        formData.append("micro_stool_id", micro_stool_id);

        formData.append("physical_urine", physical_urine);
        formData.append("chemical_urine", chemical_urine);
        formData.append("micro_urine", micro_urine);
        formData.append("physical_urine_id", physical_urine_id);
        formData.append("chemical_urine_id", chemical_urine_id);
        formData.append("micro_urine_id", micro_urine_id);



        let urls = "";
        if (insertType == "Insert") {
            urls = "/prescription/manage-labresult/new_labResult";
        } else {
            formData.append("labResultId", $("#labResultId").val());
            urls = "/prescription/manage-labresult/edit_labResult";
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
                            $("#AddResultform")[0].reset();
                            window.location.replace("/prescription/lab-test-orders");
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
    $("#LabOrderTable tbody").on("click", "#viewLabResult", function(e) {
        e.preventDefault();
        ID = $(this).attr("rowid");
        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("orderid", ID);

        let Tests = "";
        $.ajax({
            method: "POST",
            url: "/prescription/manage-labresult/get_labResult_info",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {
                    // insertType = "Update";
                    $("#AddLabResult").modal("show");
                    $("#myModalLabel").text("Update Test");
                    var address = response.Message.PatientVillage + ', ' + response.Message.PatientDistrict
                    $("#order_id").text(response.Message.OrderId);
                    $("#result_id").text(response.Message.LabResultID);
                    $("#Appoint_id").text(response.Message.AppointId);
                    $("#patient").text(response.Message.PatientName);
                    $("#doctor").text(response.Message.Doctor);
                    $("#age").text(response.Message.PatientAge);
                    $("#gender").text(response.Message.PatientGender);
                    $("#mobileNo").text(response.Message.PatientMobileNo);
                    $("#address").text(address);
                    $("#result_date").text(response.Message.ResultDate);
                    $("#collection_date").text(response.Message.CollectionDate);
                    $("#collected_by").text(response.Message.Collected_by);
                    $("#Comment").text(response.Message.Comment)
                        // 'name': result.TestID.TestName,
                        //     'normalRange': result.TestID.NormalRange,
                        //     'TestUnit': result.TestID.TestUnit,
                        //     'ReportValue': result.ReportValue,
                        //     'flag': result.flag,

                    const tbody_blood = $('#tbody_blood')
                    const tbody = $('#tbody')
                    response.Message.blood_results.map(result => {
                        tbody_blood.append('<tr></tr>').append(`<td>${result.group}</td><td>${result.subgroup}</td><td><span>${result.name}</span></td>
                        <td><span>${result.ReportValue}</span></td>
                        <td><span>${result.flag}</span></td>
                        <td><span>${result.normalRange}</span></td>
                        <td><span>${result.TestUnit}</span></td>
                       `)
                    })
                    response.Message.other_results.map(other_result => {
                        tbody.append('<tr></tr>').append(`<td><span>${other_result.name}</span></td>
                        <td><span>${other_result.Type}</span></td>
                        <td><span>${other_result.Parameter}</span></td>
                        <td><span>${other_result.ReportValue}</span></td>
                       `)

                    })



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