$(document).ready(function() {

    // ------------------------------Start- Diagnosis form--------------------------------------------------------- 

    // ------------------------------Start- Radioloy part of the diagnosis form--------------------------------------------------------- 

    var radiology = get_radiology(); // Number of items to add to the DOM
    var radiologycategory = get_radio_category(); // Number of items to add to the DOM

    // a function to get radiology
    function get_radiology() {
        let radiology_list = "";
        $.ajax({
            method: "POST",
            url: "/patient/manage-patient-diagnosis/get_radiology_option_data",
            headers: { "X-CSRFToken": csrftoken },
            async: false,
            success: function(response) {
                console.log(response)
                if (!response.isError) {
                    radiology_list = response.Message.radiology;
                } else {
                    Swal.fire({
                        title: "Something Wrong!!",
                        text: response.Message,
                        icon: "error",
                        confirmButtonClass: "btn btn-primary w-xs mt-2",
                        buttonsStyling: !1,
                        showCloseButton: !0,
                    });
                }
            },
            error: function(response) {},
        });

        return radiology_list;
    }

    // a function to get all radiology category
    function get_radio_category() {
        let radiology_category_list = "";
        $.ajax({
            method: "POST",
            url: "/patient/manage-patient-diagnosis/get_radiology_option_data",
            headers: { "X-CSRFToken": csrftoken },
            async: false,
            success: function(response) {
                console.log(response)
                if (!response.isError) {
                    radiology_category_list = response.Message.radiology_category;
                } else {
                    Swal.fire({
                        title: "Something Wrong!!",
                        text: response.Message,
                        icon: "error",
                        confirmButtonClass: "btn btn-primary w-xs mt-2",
                        buttonsStyling: !1,
                        showCloseButton: !0,
                    });
                }
            },
            error: function(response) {},
        });

        return radiology_category_list;
    }

    function radiologycategory_option_elements() {
        let options = "";
        radiologycategory.forEach((item, index) => {
            options += `<option value="${item.id}">${item.name}</option>`;
        });

        return options;
    }
    // add elements button
    $(".add_radio_btn").click(function(e) {
        r_counter += 1
        e.preventDefault();




        $("#show_radio").append(` <div class="row" id="row${counter}">
        <div class="col-md-4">
        <div class="mb-3">
            <label class="form-label">Radiology Exam Category</label>
            <select class="form-select" id="radiologyCategory${r_counter}">
                <option selected value="">Select</option>
                ${radiologycategory_option_elements()}
            </select>
        </div>                                                       
        </div>

    <div class="col-md-4">
        <div class="mb-3">
            <label class="form-label">Radiology Exam Name</label>
            <select class="form-select " id="radiology${r_counter}" multiple >
                
            </select>
        </div>                                                       
    </div>
       
        <div class="col-lg-1">
            <div class="mb-3">
                <label class="form-label">Remove</label>
                <button type="button" class="btn btn-danger remove_radio_btn" >
                    <i class="las la-trash"></i> 
                </button>
            </div>                                                       
        </div>
        </div>`);

        $("#radiologyCategory" + r_counter).on("change", function() {

            // Clear all other fields
            $("#radiology").html("");


            // if the data selected is not empty
            if ($(this).val() != "") {
                get_category_radiology($("#radiologyCategory" + r_counter).val());
            }
        });

        var multipleCancelButton_r_loop = new Choices('#radiology' + r_counter, {
            removeItemButton: true,
            choices: []
        });

        function get_category_radiology(radiologyCategory) {
            let formData = new FormData();
            formData.append("radiologyCategory", radiologyCategory);
            $.ajax({
                method: "POST",
                url: "/patient/manage-patient-diagnosis/get_category_radiology",
                async: false,
                headers: { "X-CSRFToken": csrftoken },
                processData: false,
                contentType: false,
                data: formData,
                success: function(response) {
                    if (!response.isError) {

                        $("#radiology").html("");

                        // if the data length is 0
                        if (response.Message.length == 0) {
                            // Add disabled attribute from directorate
                            // $("#job_directorate").attr("disabled", true);
                            $("#radiology" + r_counter).append(
                                `<option value="Not available">Not available</option>`
                            );

                        } else {
                            // Remove disabled attribute from directorate
                            // $("#job_directorate").attr("disabled", false);
                        }

                        const options = response.Message.map(item => ({
                            value: item.id,
                            label: item.name
                        }));

                        // Check if a Choices instance exists on the labTest1 element
                        if (multipleCancelButton_r_loop) {
                            // If it exists, update the options of the existing Choices instance on the labTest1 element
                            multipleCancelButton_r_loop.setChoices(options, "value", "label", true);
                        } else {
                            // If it doesn't exist, create a new Choices instance on the labTest1 element with the updated options
                            multipleCancelButton = new Choices('#radiology' + r_counter, {
                                removeItemButton: true,
                                choices: options
                            });
                        }

                        response.Message.forEach((item, index) => {

                            index == 0 &&
                                $("#radiology" + r_counter).append(
                                    `<option value="">Select Radiology Exam</option>`
                                );
                            $("#radiology" + r_counter).append(
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
    // remove elements button
    $(document).on('click', '.remove_radio_btn', function(e) {
        e.preventDefault();
        let row_item = $(this).parent().parent().parent();
        $(row_item).remove();
        r_counter -= 1;
    })

    // depenedent chained dropdowns between radiology and radiology category without plus button
    $("#radiologyCategory1").on("change", function() {

        // Clear all other fields
        $("#radiology1").html("");


        // if the data selected is not empty
        if ($(this).val() != "") {
            get_category_radiology($("#radiologyCategory1").val());
        }
    });
    var multipleCancellButton_r = new Choices('#radiology1', {
        removeItemButton: true,
        choices: []
    });
    // depenedent chained dropdowns between radiology and radiology category without plus button
    function get_category_radiology(radiologyCategory) {
        let formData = new FormData();
        formData.append("radiologyCategory", radiologyCategory);
        $.ajax({
            method: "POST",
            url: "/patient/manage-patient-diagnosis/get_category_radiology",
            async: false,
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            success: function(response) {
                if (!response.isError) {

                    $("#radiology1").html("");

                    // if the data length is 0
                    if (response.Message.length == 0) {
                        // Add disabled attribute from directorate
                        // $("#job_directorate").attr("disabled", true);
                        $("#radiology1").append(
                            `<option value="Not available">Not available</option>`
                        );

                    } else {
                        // Remove disabled attribute from directorate
                        // $("#job_directorate").attr("disabled", false);
                    }

                    const options = response.Message.map(item => ({
                        value: item.id,
                        label: item.name
                    }));

                    // Check if a Choices instance exists on the labTest1 element
                    if (multipleCancellButton_r) {
                        // If it exists, update the options of the existing Choices instance on the labTest1 element
                        multipleCancellButton_r.setChoices(options, "value", "label", true);
                    } else {
                        // If it doesn't exist, create a new Choices instance on the labTest1 element with the updated options
                        multipleCancelButton = new Choices('#radiology1', {
                            removeItemButton: true,
                            choices: options
                        });
                    }


                } else {
                    Swal.fire("Something Wrong!!", data.Message, "error");
                }
            },
            error: function(error) {},
        });
    }
    // ------------------------------End- Radioloy part of the diagnosis form--------------------------------------------------------- 



    // ------------------------------Start- Laboratory part of the diagnosis form--------------------------------------------------------- 

    // if select blood get group dropdown , if not just get test dropdown
    $("#Sample1").on("change", function() {
        if ($("#Sample1").val() != "") {
            $(".if-blood1").addClass("d-none");
            if ($("option:selected", "#Sample1").text() == "Blood") {
                $(".if-blood1").removeClass("d-none");
                $(".blood1").removeClass("d-none");
            } else {
                $(".if-blood1").removeClass("d-none");
                $(".blood1").addClass("d-none");
            }
        } else {
            $(".if-blood1").addClass("d-none");
            $(".blood1").addClass("d-none");
        }
    });

    // add elements btn
    $(".add_lab_btn").click(function(e) {
        l_counter += 1
        e.preventDefault();




        $("#show_lab").append(` <div class="row" id="row${l_counter}">
        <div class="col-md-4">
        <div class="mb-3">
            <label class="form-label">Sample Type</label>
            <select class="form-select"  id="Sample${l_counter}">
            <option value="">Select Sample Type</option>
            <option value="Blood">Blood</option>
            <option value="Urine">Urine</option>
            <option value="Stool">Stool</option>
            </select>
        </div>                                                       
    </div>

    <div class="col-md-3 if-blood${l_counter} d-none blood${l_counter}">
        <div class="mb-3">
            <label class="form-label">Group Name</label>

            <select class="form-select"  id="Group${l_counter}">
              
            </select>
        </div>
    </div>
           
    
        
      
    <div class="col-md-4  ">
        <div class="mb-3">
            <label class="form-label">Test Name</label>
            <select class="form-select" id="labTest${l_counter}" multiple>
              
        
            </select>
        </div>                                                       
    </div>


    <div class="col-lg-1">
            <div class="mb-3">
                <label class="form-label">Remove</label>
                <button type="button" class="btn btn-danger remove_lab_btn" >
                    <i class="las la-trash"></i> 
                </button>
            </div>                                                       
        </div>
    </div>`);
        $("#Sample" + l_counter).on("change", function() {
            if ($("#Sample" + l_counter).val() != "") {
                $(".if-blood" + l_counter).addClass("d-none");
                if ($("option:selected", "#Sample" + l_counter).text() == "Blood") {
                    $(".if-blood" + l_counter).removeClass("d-none");
                    $(".blood" + l_counter).removeClass("d-none");
                } else {
                    $(".if-blood" + l_counter).removeClass("d-none");
                    $(".blood" + l_counter).addClass("d-none");
                }
            } else {
                $(".if-blood" + l_counter).addClass("d-none");
                $(".blood" + l_counter).addClass("d-none");
            }
        });
        $("#Sample" + l_counter).on("change", function() {

            // Clear all other fields
            $("#labTest" + l_counter).html("");
            $("#Group" + l_counter).html("");


            // if the data selected is not empty
            if ($(this).val() != "") {
                get_sample_type($("#Sample" + l_counter).val());
            }
        });

        function get_sample_type(Sample) {
            let formData = new FormData();
            formData.append("Sample1", Sample);
            $.ajax({
                method: "POST",
                url: "/patient/manage-patient-diagnosis/get_category_lab",
                async: false,
                headers: { "X-CSRFToken": csrftoken },
                processData: false,
                contentType: false,
                data: formData,
                success: function(response) {
                    if (!response.isError) {

                        $("#labTest").html("");

                        // if the data length is 0
                        if (response.Message.length == 0) {
                            // Add disabled attribute from directorate
                            // $("#job_directorate").attr("disabled", true);
                            $("#labTest" + l_counter).append(
                                `<option value="Not available">Not available</option>`
                            );

                        } else {
                            // Remove disabled attribute from directorate
                            // $("#job_directorate").attr("disabled", false);
                        }

                        const options = response.Message.map(item => ({
                            value: item.id,
                            label: item.name
                        }));

                        // Check if a Choices instance exists on the labTest1 element
                        if (multipleCancellButton) {
                            multipleCancellButton.removeActiveItems();
                            // If it exists, update the options of the existing Choices instance on the labTest1 element
                            multipleCancellButton.setChoices(options, "value", "label", true);
                        } else {
                            // If it doesn't exist, create a new Choices instance on the labTest1 element with the updated options
                            multipleCancelButton = new Choices('#labTest' + l_counter, {
                                removeItemButton: true,
                                choices: options
                            });
                        }

                        response.Groups.forEach((item, index) => {

                            index == 0 &&
                                $("#Group" + l_counter).append(
                                    `<option value="">Select Test Name</option>`
                                );
                            $("#Group" + l_counter).append(
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

        $("#Group" + l_counter).on("change", function() {

            // Clear all other fields
            $("#labTest" + l_counter).html("");


            // if the data selected is not empty
            if ($(this).val() != "") {
                get_blood_test($("#Group" + l_counter).val());
            }
        });
        var multipleCancellButton = new Choices('#labTest' + l_counter, {
            removeItemButton: true,
            choices: []
        });

        function get_blood_test(Group) {
            let formData = new FormData();
            formData.append("Group", Group);
            $.ajax({
                method: "POST",
                url: "/patient/manage-patient-diagnosis/get_blood_test",
                async: false,
                headers: { "X-CSRFToken": csrftoken },
                processData: false,
                contentType: false,
                data: formData,
                success: function(response) {
                    if (!response.isError) {

                        $("#labTest" + l_counter).html("");

                        // if the data length is 0
                        if (response.Message.length == 0) {
                            // Add disabled attribute from directorate
                            // $("#job_directorate").attr("disabled", true);
                            $("#labTest" + l_counter).append(
                                `<option value="Not available">Not available</option>`
                            );

                        } else {
                            // Remove disabled attribute from directorate
                            // $("#job_directorate").attr("disabled", false);
                        }
                        const options = response.Message.map(item => ({
                            value: item.id,
                            label: item.name
                        }));

                        // Check if a Choices instance exists on the labTest1 element
                        if (multipleCancellButton) {
                            multipleCancellButton.removeActiveItems();
                            // If it exists, update the options of the existing Choices instance on the labTest1 element
                            multipleCancellButton.setChoices(options, "value", "label", true);
                        } else {
                            // If it doesn't exist, create a new Choices instance on the labTest1 element with the updated options
                            multipleCancelButton = new Choices('#labTest' + l_counter, {
                                removeItemButton: true,
                                choices: options
                            });
                        }


                    } else {
                        Swal.fire("Something Wrong!!", data.Message, "error");
                    }
                },
                error: function(error) {},
            });
        }
    });
    // remove elements btn
    $(document).on('click', '.remove_lab_btn', function(e) {
        e.preventDefault();
        let row_item = $(this).parent().parent().parent();
        $(row_item).remove();
        l_counter -= 1;
    })

    // if select blood get chained dependent dropdown for blood and group, if not get for urine and stool
    $("#Sample1").on("change", function() {

        // Clear all other fields

        $("#Group1").val();


        // if the data selected is not empty
        if ($(this).val() != "") {
            get_sample_type($("#Sample1").val());
        }
    });


    // if select blood get chained dependent dropdown for blood and group
    function get_sample_type(Sample1) {
        let formData = new FormData();
        formData.append("Sample1", Sample1);
        $.ajax({
            method: "POST",
            url: "/patient/manage-patient-diagnosis/get_category_lab",
            async: false,
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            success: function(response) {
                if (!response.isError) {

                    $("#labTest1").html("");
                    $("#Group1").html("");

                    // if the data length is 0
                    if (response.Message.length == 0) {
                        // Add disabled attribute from directorate
                        // $("#job_directorate").attr("disabled", true);
                        $("#labTest1").append(
                            `<option value="Not available">Not available</option>`
                        );

                    } else {

                    }

                    const options = response.Message.map(item => ({
                        value: item.id,
                        label: item.name
                    }));

                    // Check if a Choices instance exists on the labTest1 element
                    if (multipleCancellButton) {
                        // If it exists, make it empty
                        multipleCancellButton.removeActiveItems();
                        // Then update the options of the existing Choices instance on the labTest1 element
                        multipleCancellButton.setChoices(options, "value", "label", true);
                    } else {
                        // If it doesn't exist, create a new Choices instance on the labTest1 element with the updated options
                        multipleCancelButton = new Choices('#labTest1', {
                            removeItemButton: true,
                            choices: options
                        });
                    }
                    response.Groups.forEach((item, index) => {

                        index == 0 &&
                            $("#Group1").append(
                                `<option value="">Select Test Name</option>`
                            );
                        $("#Group1").append(
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
    // chained dependent dropdown for group and tests
    $("#Group1").on("change", function() {

        // Clear all other fields

        $("#labTest1").val("");


        // if the data selected is not empty
        if ($(this).val() != "") {
            get_blood_test($("#Group1").val());
        }
    });
    // multiple select 
    var multipleCancellButton = new Choices('#labTest1', {
        removeItemButton: true,
        choices: []
    });
    // chained dependent dropdown for group and tests

    function get_blood_test(Group) {
        let formData = new FormData();
        formData.append("Group", Group);
        console.log(Group)
        $.ajax({
            method: "POST",
            url: "/patient/manage-patient-diagnosis/get_blood_test",
            async: false,
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            success: function(response) {
                if (!response.isError) {


                    $("#labTest1").html("");


                    // if the data length is 0
                    if (response.Message.length == 0) {
                        // Add disabled attribute from directorate
                        // $("#job_directorate").attr("disabled", true);
                        $("#labTest1").append(
                            `<option value="Not available">Not available</option>`
                        );

                    } else {
                        // Remove disabled attribute from directorate
                        // $("#job_directorate").attr("disabled", false);
                    }
                    const options = response.Message.map(item => ({
                        value: item.id,
                        label: item.name
                    }));

                    // Check if a Choices instance exists on the labTest1 element
                    if (multipleCancellButton) {
                        multipleCancellButton.removeActiveItems();
                        // If it exists, update the options of the existing Choices instance on the labTest1 element
                        multipleCancellButton.setChoices(options, "value", "label", true);
                    } else {
                        // If it doesn't exist, create a new Choices instance on the labTest1 element with the updated options
                        multipleCancelButton = new Choices('#labTest1', {
                            removeItemButton: true,
                            choices: options
                        });
                    }




                } else {
                    Swal.fire("Something Wrong!!", data.Message, "error");
                }
            },
            error: function(error) {},
        });
    }

    $("#LabTable tbody").on("click", "#view_lab_order", function(e) {
        e.preventDefault();
        ID = $(this).attr("rowid");
        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("order_id", ID);
        console.log(ID)
        $.ajax({
            method: "POST",
            url: "/patient/manage-patient-diagnosis/get_lab_order_info",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {  
                    var pending_orders_html = '';
                    var approved_orders_html = '';
                    response.Message.pending_order_details.forEach((order, index) => {
                        if (order.order_status === "Pending") {
                            if (order.group === 'null') {
                                pending_orders_html +=
                                    `<tr>
                                        <td>${order.testNumber}</td>
                                        <td>${order.sampleType}</td>
                                        <td>${order.sampleType}</td>
                                         <td>${order.testName}</td>
                                    </tr>`;
                            } else {
                                pending_orders_html +=
                                    `<tr>
                                        <td>${order.testNumber}</td>
                                        <td>${order.sampleType}</td>
                                        <td>${order.group}</td>
                                        <td>${order.testName}</td>
                                    </tr>`;
                            }
                        }
                    });

                  

                    var approved_orders_html = '';
                    var prevGroup = null;

                    var prevSubGroup = null;

                    response.Message.approved_order_details.forEach((order, index) => {
                        if (order.order_status === "Approved") {
                            if(order.blood_result === "empty"){
                                var blood_result_cat = document.getElementById("blood_result")
                                blood_result_cat.style.display = 'none'
                            }
                            else{
                                var blood_result_cat = document.getElementById("blood_result")
                                blood_result_cat.style.display = 'block'
                                var urine_stool_result_cat = document.getElementById("urine_stool_result")
                                urine_stool_result_cat.style.display = 'none'
                                for (const unique_group of order.Group) {
                                    for (const subgroup of order.subGroup) {
                                        if (unique_group !== prevGroup && subgroup !== prevSubGroup) {
                                          
                                            approved_orders_html += `
                                            <caption style="caption-side: top;font-size: 14px;padding: 1px;margin-bottom: 0em;font-weight: 600;margin-top:3px">${unique_group}</caption>
                                            <tr><td colspan='8'><span style="font-weight:600;">${subgroup}</span></td></tr>
                                                <tr>
                                                   
                                                    <td>${order.testNumber}</td>
                                                    <td>${order.testName}</td>
                                                    <td>${order.resultValue} (${order.flag})</td>
                                                    <td>${order.normalRange}</td>
                                                    <td>${order.testUnit}</td>
                                                </tr>`;
                                            prevGroup = unique_group;
                                            prevSubGroup = subgroup;
                                        }
                                        else if (unique_group === prevGroup && subgroup !== prevSubGroup){
                                            approved_orders_html += `
                                            <tr><td colspan='8'><span style="font-weight:600;">${subgroup}</span></td></tr>
                                                <tr>
                                                   
                                                    <td>${order.testNumber}</td>
                                                    <td>${order.testName}</td>
                                                    <td>${order.resultValue} (${order.flag})</td>
                                                    <td>${order.normalRange}</td>
                                                    <td>${order.testUnit}</td>
                                                </tr>`;
                                            prevGroup = unique_group;
                                            prevSubGroup = subgroup;
                                        }
                                        
                                        else{
                                            approved_orders_html += `
                                                <tr>
                                                 
                                                    <td>${order.testNumber}</td>
                                                    <td>${order.testName}</td>
                                                    <td>${order.resultValue} (${order.flag})</td>
                                                    <td>${order.normalRange}</td>
                                                    <td>${order.testUnit}</td>
                                                </tr>`;
                                        }
                                    }
                                }
                            }
                        }
                    });
                 
                    console.log(prevGroup)
                    var approved_orders_html_comment = '';
                  
                                           
                            if (response.Message.Comment !== null) {
                                var comment = document.getElementById("comment")
                                comment.style.display = 'block'
                                approved_orders_html_comment +=
                                    `<tr>
                                        <td>${response.Message.Comment}</td>
                                        
                                    </tr>`;
                            }  else{
                                var comment = document.getElementById("comment")
                                comment.style.display = 'none'
                            }
                   
                  
                    if (pending_orders_html !== '') {
                        var lab_status_pending = document.getElementById('lab_status_pending');
                        lab_status_pending.style.display = 'block';
                        var lab_status_approved = document.getElementById('lab_status_approved');
                        lab_status_approved.style.display = 'none';

                        var pending_orders_table = document.getElementById('pending_orders_table');
                        pending_orders_table.innerHTML = pending_orders_html;
                    } else {
                        var lab_status_pending = document.getElementById('lab_status_pending');
                        lab_status_pending.style.display = 'none';
                        var lab_status_approved = document.getElementById('lab_status_approved');
                        lab_status_approved.style.display = 'block';
                        var approved_orders_table = document.getElementById('approved_orders_table');
                        approved_orders_table.innerHTML = approved_orders_html;

                        var comment_table = document.getElementById('comment_table');
                        comment_table.innerHTML = approved_orders_html_comment;
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
    // ------------------------------End- laboratory part of the diagnosis form--------------------------------------------------------- 

    // submit the daignosis form 
    $("#diagnosis_btn_submit").on("click", function(e) {

        // Prevent the page from loading or refreshing
        e.preventDefault();
        // Create form data
        let formData = new FormData();
        let laboratory = [];
        let radiology = [];

        // loop through tracke elements
        for (let i = 1; i <= l_counter; i++) {
            laboratory.push($("#labTest" + i).val());

        }
        for (let i = 1; i <= r_counter; i++) {
            radiology.push($("#radiology" + i).val());

        }
        // Read user 
        formData.append("appointmentId", appointmentId);
        formData.append("laboratory", laboratory);
        formData.append("radiology", radiology);
        let urls = "";
        if (insertType == "Insert") {
            urls = "/patient/manage-patient-diagnosis/new_diagnosis"

        } else {
            // formData.append("CategoryID", $("#CategoryID").val());
            urls = "/patient/manage-patient-diagnosis/update_diagnosis"
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
                            $("#DiagnosisForm")[0].reset();
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

    // ------------------------------End- Diagnosis form--------------------------------------------------------- 
});