$(document).ready(function() {
    $('#add_test').on('click', function() {
        $(".add_labtest").modal("show");


        $("#TestName").val('');
        $("#TestUnit").val('');
        $("#ShortName").val('');
        $("#TestDescription").val('');
        $("#Physical").val('');
        $("#Chemical").val('');
        $("#Microscopic").val('');
        $("#Group").val('');
        $("#SubGroup").val('');
        $("#sampleType").val('');
        $("#NormalRange").val('');
        $("#ResultType").val('');
       
        insertType = "Insert";


    });
    chemical_counter = 1
    micro_counter = 1
    physical_counter = 1
    $("#ResultType").on("change", function() {
        if ($("#sampleType").val() != "") {
            $(".for-blood").addClass("d-none");
            if ($("option:selected", "#ResultType").text() == "Quantitative" && $("option:selected", "#sampleType").text() == "Blood") {
                $(".for-blood").removeClass("d-none");
                $(".blood").removeClass("d-none");
                $(".for-blood-result").removeClass("d-none");
                $(".blood_result").removeClass("d-none");
                $(".for-others").removeClass("d-none");
                $(".others").addClass("d-none");
            } else if ($("option:selected", "#ResultType").text() == "Qualitative" && $("option:selected", "#sampleType").text() == "Blood") {
                $(".for-blood").removeClass("d-none");
                $(".blood").removeClass("d-none");
                $(".for-blood-result").removeClass("d-none");
                $(".blood_result").addClass("d-none");
                $(".for-others").removeClass("d-none");
                $(".others").addClass("d-none");
            } else if (($("option:selected", "#sampleType").text() == "Urine" || $("option:selected", "#sampleType").text() == "Stool") && $("option:selected", "#ResultType").text() == "Qualitative") {
                $(".for-blood").removeClass("d-none");
                $(".blood").addClass("d-none");
                $(".for-others").removeClass("d-none");
                $(".others").addClass("d-none");
            } else if (($("option:selected", "#sampleType").text() == "Urine" || $("option:selected", "#sampleType").text() == "Stool") && $("option:selected", "#ResultType").text() == "MultiComponent") {
                $(".for-blood").removeClass("d-none");
                $(".blood").addClass("d-none");
                $(".for-others").removeClass("d-none");
                $(".others").removeClass("d-none");
            } else {
                $(".for-blood").removeClass("d-none");
                $(".blood").addClass("d-none");
                $(".for-others").removeClass("d-none");
                $(".others").addClass("d-none");
            }
        } else {
            $(".for-blood").addClass("d-none");
            $(".blood").addClass("d-none");
        }
    });
    let Group = "";
    $("#Group").on("change", () => {
        Group = $("#Group option:selected").val()
    })
    let SubGroup = "";
    $("#SubGroup").on("change", () => {
        SubGroup = $("#SubGroup option:selected").val()
    })
    let sampleType = "";
    $("#sampleType").on("change", () => {
        sampleType = $("#sampleType option:selected").val()
    })
    $("#SubmitLabTest").on("click", function(e) {

        // Prevent the page from loading or refreshing
        e.preventDefault();
        // Create form data
        let formData = new FormData();
        let Physical = [];
        let Chemical = [];
        let Microscopic = [];


        // loop through tracke elements
        for (let i = 1; i <= physical_counter; i++) {
            Physical.push($("#Physical" + i).val());
        }
        for (let i = 1; i <= chemical_counter; i++) {
            Chemical.push($("#Chemical" + i).val());
        }
        for (let i = 1; i <= micro_counter; i++) {
            Microscopic.push($("#Microscopic" + i).val());
        }

        // Read user 

        
        formData.append("TestName", $("#TestName").val());
        formData.append("TestUnit", $("#TestUnit").val());
        formData.append("ShortName", $("#ShortName").val());
        formData.append("TestDescription", $("#TestDescription").val());
        formData.append("Physical", Physical);
        formData.append("Chemical", Chemical);
        formData.append("Microscopic", Microscopic);
        formData.append("Group", Group);
        formData.append("SubGroup", SubGroup);
        formData.append("sampleType", sampleType);
        formData.append("NormalRange", $("#NormalRange").val());
        formData.append("ResultType", $("#ResultType").val());
        let urls = "";
        if (insertType == "Insert") {
            urls = "/prescription/manage-lab-test/new_test";
        } else {
            formData.append("TestID", $("#TestID").val());
            urls = "/prescription/manage-lab-test/edit_test";
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
                            $("#TestForm")[0].reset();
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
    $("#TestTable tbody").on("click", "#editButtonTest", function(e) {
        e.preventDefault();
        const ID = $(this).attr("rowid");
        console.log(ID);

        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("TestID", ID);

        $.ajax({
            method: "POST",
            url: "/prescription/manage-lab-test/get_test",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {

                    insertType = "Update";
                    $("#labTestModal").modal("show");
                    $("#myLargeModalLabel").text("Update Test");

                    $("#TestName").val(response.Message.TestName);
                    $("#ShortName").val(response.Message.ShortName);
                    $("#TestDescription").val(response.Message.TestDescription);
                    $("#sampleType").val(response.Message.sampleType);
                    $("#TestID").val(response.Message.id);
                    $("#NormalRange").val(response.Message.normalrange);
                    $("#TestUnit").val(response.Message.testUnit);
                    $("#ResultType").val(response.Message.resultType);

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
    $("#TestTable tbody").on("click", "#viewLabTests", function(e) {
        e.preventDefault();
        ID = $(this).attr("rowid");
        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("testID", ID);

        $.ajax({
            method: "POST",
            url: "/prescription/manage-lab-test/get_test_info",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {
                    // insertType = "Update";
                    if(response.Message.sampleType == "Blood"){
                        $("#ViewbloodTests").modal("show");
                    
                        $("#testID").text(response.Message.id);
                        $("#testName").text(response.Message.TestName);
                        $("#shortName").text(response.Message.ShortName);
                         $("#test_category").text(response.Message.sampleType);
                         $("#normalrange").text(response.Message.normalrange);
                        $("#testUnit").text(response.Message.testUnit);
                        $("#group").text(response.Message.group);
                        $("#subgroup").text(response.Message.subgroup);
                     }
                    else{
                        $("#ViewparameterTests").modal("show");
                    
                        $("#testID_").text(response.Message.id);
                        $("#testName_").text(response.Message.TestName);
                        $("#test_category_").text(response.Message.sampleType);
                        $("#shortName_").text(response.Message.ShortName);
                        if(response.Message.resultType == "Qualitative"){
                            document.querySelector("#examination").style.display = "none";
                        }else{
                            var physical_parameter = document.createElement("ul");
                            for (var i = 0; i < response.Message.physical_parameters.length; i++) {
                                var listItem = document.createElement("li");
                                var listItemText = document.createTextNode(response.Message.physical_parameters[i]);
                                listItem.appendChild(listItemText);
                                physical_parameter.appendChild(listItem);
                            }
                            document.getElementById("physical_parameters").appendChild(physical_parameter);

                            var chemical_parameter = document.createElement("ul");
                            for (var i = 0; i < response.Message.chemical_parameters.length; i++) {
                                var listItem = document.createElement("li");
                                var listItemText = document.createTextNode(response.Message.chemical_parameters[i]);
                                listItem.appendChild(listItemText);
                                chemical_parameter.appendChild(listItem);
                            }
                            document.getElementById("chemical_parameters").appendChild(chemical_parameter);

                            var microscopic_parameter = document.createElement("ul");
                            for (var i = 0; i < response.Message.microscopic_parameters.length; i++) {
                                var listItem = document.createElement("li");
                                var listItemText = document.createTextNode(response.Message.microscopic_parameters[i]);
                                listItem.appendChild(listItemText);
                                microscopic_parameter.appendChild(listItem);
                            }
                            document.getElementById("microscopic_parameters").appendChild(microscopic_parameter);
                        
                        }
                     }
                    
 
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
  



    $(".add_item_btn").click(function(e) {
        physical_counter += 1
        e.preventDefault();




        $("#show_physical").append(`<div class="row" id="row${physical_counter}">
                                                    
        <div class="col-md-10">
            <div class="mb-3">
                <input class="form-control" type="text" id="Physical${physical_counter}">
            </div>                                                       
        </div>
        <div class="col-md-2">
            <div class="mb-3">
                <label class="form-label"></label>
                <button type="button" class="btn btn-sm btn-danger remove_item_btn" >
                    <i class="las la-trash"></i> 
                </button>
            </div>                                                       
        </div>
        </div>
    `);


    });
    $(document).on('click', '.remove_item_btn', function(e) {
        e.preventDefault();
        let row_item = $(this).parent().parent().parent();
        $(row_item).remove();
        physical_counter -= 1;
    })
    $(".add_chemical_btn").click(function(e) {
        chemical_counter += 1
        e.preventDefault();




        $("#show_chemical").append(`<div class="row" id="row${chemical_counter}">
                                                    
        <div class="col-md-10">
            <div class="mb-3">
                <input class="form-control" type="text" id="Chemical${chemical_counter}">
            </div>                                                       
        </div>
        <div class="col-md-2">
            <div class="mb-3">
                <label class="form-label"></label>
                <button type="button" class="btn btn-danger btn-sm remove_chemical_btn" >
                    <i class="las la-trash"></i> 
                </button>
            </div>                                                       
        </div>
        </div>
    `);


    });
    $(document).on('click', '.remove_chemical_btn', function(e) {
        e.preventDefault();
        let row_item = $(this).parent().parent().parent();
        $(row_item).remove();
        chemical_counter -= 1;
    })

    $(".add_micro_btn").click(function(e) {
        micro_counter += 1
        e.preventDefault();
        $("#show_micro").append(`<div class="row" id="row${micro_counter}">
                                                    
        <div class="col-md-10">
            <div class="mb-3">
                <input class="form-control" type="text" id="Microscopic${micro_counter}">
            </div>                                                       
        </div>
        <div class="col-md-2">
            <div class="mb-3">
                <label class="form-label"></label>
                <button type="button" class="btn btn-danger btn-sm remove_micro_btn" >
                    <i class="las la-trash"></i> 
                </button>
            </div>                                                       
        </div>
        </div>
    `);


    });
    $(document).on('click', '.remove_micro_btn', function(e) {
        e.preventDefault();
        let row_item = $(this).parent().parent().parent();
        $(row_item).remove();
        micro_counter -= 1;
    })

     // chained dropdown for rooms and beds
    $("#sampleType").on("change", function() {

        // Clear all other fields
        $("#ResultType").html("");


        // if the data selected is not empty
        if ($(this).val() != "") {
            get_sample_resultType($("#sampleType").val());
        }
    });
    // chained dropdown for rooms and beds
    function get_sample_resultType(sampleType) {
        if (sampleType == "Blood"){
            $("#ResultType").append(
                '<option value="">Select Result Type</option>' +
                '<option value="Quantitative">Quantitative</option>' +
                '<option value="Qualitative">Qualitative</option>'
            );
        }
        else {
            $("#ResultType").append(
                '<option value="">Select Result Type</option>' +
                '<option value="Qualitative">Qualitative</option>' +
                '<option value="Multi">MultiComponent</option>'
            );
        }
    }


   // chained dependent dropdown for group and tests
    $("#Group").on("change", function() {

        // Clear all other fields

        $("#SubGroup").val("");


        // if the data selected is not empty
        if ($(this).val() != "") {
            get_blood_test($("#Group").val());
        }
    });
  
    // chained dependent dropdown for group and tests
    function get_blood_test(Group) {
        let formData = new FormData();
        formData.append("Group", Group);
        $.ajax({
            method: "POST",
            url: "/prescription/manage-lab-test/get_group_subgroup",
            async: false,
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            success: function(response) {
                if (!response.isError) {

                    $("#SubGroup").html("");

                    // if the data length is 0
                    if (response.Message.length == 0) {
                        
                        $("#SubGroup").append(
                            `<option value="Not available">Not available</option>`
                        );
                       
                    } else {
                        
                    }

                    response.Message.forEach((item, index) => {
                        index == 0 &&
                            $("#SubGroup").append(
                                `<option value="">Select SubGroup</option>`
                            );
                        $("#SubGroup").append(
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
});