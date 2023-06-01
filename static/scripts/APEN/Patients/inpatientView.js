$(document).ready(function() {
    insertType = "Insert";


 

    // ------------------------------Start Prescription form--------------------------------------------------------- 
    counter = 1
    var available_medicines = get_available_medicines(); // Number of items to add to the DOM
    var available_med_category = get_available_med_category(); // Number of items to add to the DOM

    // a function to get available medicines
    function get_available_medicines() {
        let medicineList = "";
        $.ajax({
            method: "POST",
            url: "/patient/manage-inpatient-prescription/get_option_data",
            headers: { "X-CSRFToken": csrftoken },
            async: false,
            success: function(response) {
                console.log(response)
                if (!response.isError) {
                    medicineList = response.Message.medicines;
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

        return medicineList;
    }

    // a function to get all medicine category
    function get_available_med_category() {
        let medicine_category_list = "";
        $.ajax({
            method: "POST",
            url: "/patient/manage-inpatient-prescription/get_option_data",
            headers: { "X-CSRFToken": csrftoken },
            async: false,
            success: function(response) {
                console.log(response)
                if (!response.isError) {
                    medicine_category_list = response.Message.medicines_category;
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

        return medicine_category_list;
    }


    // function medicine_option_elements() {
    //     let options = "";
    //     available_medicines.forEach((item, index) => {
    //         options += `<option value="${item.id}">${item.name}</option>`;
    //     });

    //     return options;
    // }

    function med_category_option_elements() {
        let options = "";
        available_med_category.forEach((item, index) => {
            options += `<option value="${item.id}">${item.name}</option>`;
        });

        return options;
    }
    // add elements button
    $(".add_item_btn").click(function(e) {
        counter += 1
        e.preventDefault();




        $("#show_item").append(`  <div class="row" id="row${counter}">
        <div class="col-lg-2">
            <div class="mb-3">
                <label class="form-label">Medicine Category</label>
                <select class="form-select" name="MedicineCategory${counter}" id="MedicineCategory${counter}">
                <option selected value="">Select</option>
                ${med_category_option_elements()}
                </select>
            </div>                                                       
        </div>

        <div class="col-lg-3">
            <div class="mb-3">
                <label class="form-label">Medicine</label>
                <select class="form-select" name="Medicine${counter}" id="Medicine${counter}">
                </select>
            </div>                                                       
        </div>
        <div class="col-md-1">
            <div class="mb-3">
                <label class="form-label">Frequency(1</label>
                <input type="text" class="form-control" id="Dose${counter}" placeholder="1">
            </div>                                                       
        </div>
        
        <div class="col-md-1">
            <div class="mb-3">
                <label class="form-label">x  2)</label>
                <input type="text" class="form-control" id="DoseInterval${counter}" placeholder="2">
            </div>                                                       
        </div>
        <div class="col-md-2">
            <div class="mb-3">
                <label class="form-label">Route/Instructions</label>
                <input type="text" class="form-control" id="DoseDuration${counter}" placeholder="Oral After Meal">
            </div>                                                       
        </div>
        
        <div class="col-lg-1">
            <div class="mb-3">
                <label class="form-label">Qty</label>
                <input type="number" class="form-control" id="Qty${counter}">
                
            </div>                                                       
        </div>
        <div class="col-lg-1">
            <div class="mb-3">
                <label class="form-label">In Stock</label>
                <div class="div" id="available_qty${counter}">
                    <input type="number" class="form-control"  disabled>
                </div>
                
                
                <input type="hidden" id="hidden_available_qty${counter}">

            </div>                                                       
        </div>

       
       
        <div class="col-lg-1">
            <div class="mb-3">
                <label class="form-label">Remove</label>
                <button type="button" class="btn btn-danger remove_item_btn" >
                    <i class="las la-trash"></i> 
                </button>
            </div>                                                       
        </div>
    </div>`);
        // depedent chained dropdowns medicine and medicine category with the plus button

        $("#MedicineCategory" + counter).on("change", function() {

            // Clear all other fields
            $("#Medicine" + counter).html("");


            // if the data selected is not empty
            if ($(this).val() != "") {
                get_category_medicine($("#MedicineCategory" + counter).val());
            }
        });


        function get_category_medicine(MedicineCategory1) {
            let formData = new FormData();
            formData.append("MedicineCategory1", MedicineCategory1);
            $.ajax({
                method: "POST",
                url: "/patient/manage-inpatient-prescription/get_category_medicine",
                async: false,
                headers: { "X-CSRFToken": csrftoken },
                processData: false,
                contentType: false,
                data: formData,
                success: function(response) {
                    if (!response.isError) {

                        $("#Medicine" + counter).html("");

                        // if the data length is 0
                        if (response.Message.length == 0) {
                            // Add disabled attribute from directorate
                            // $("#job_directorate").attr("disabled", true);
                            $("#Medicine" + counter).append(
                                `<option value="Not available">Not available</option>`
                            );

                        } else {

                        }

                        response.Message.forEach((item, index) => {
                            index == 0 &&
                                $("#Medicine" + counter).append(
                                    `<option value="">Select Medicine</option>`
                                );
                            $("#Medicine" + counter).append(
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
        $("#Medicine" + counter).on("change", function() {

            // Clear all other fields
            $("#available_qty" + counter).html("");


            // if the data selected is not empty
            if ($(this).val() != "") {
                get_available_medicine_qty($("#Medicine" + counter).val());
            }
        });


        function get_available_medicine_qty(Medicine) {
            let formData = new FormData();
            formData.append("Medicine", Medicine);
            $.ajax({
                method: "POST",
                url: "/patient/manage-inpatient-prescription/get_available_medicine",
                async: false,
                headers: { "X-CSRFToken": csrftoken },
                processData: false,
                contentType: false,
                data: formData,
                success: function(response) {
                    if (!response.isError) {

                        $("#available_qty" + counter).html("");

                        // if the data length is 0
                        if (response.Message.length == 0) {
                            // Add disabled attribute from directorate
                            // $("#job_directorate").attr("disabled", true);
                            $("#available_qty" + counter).append(
                                `<span>*</span>`
                            );

                        } else {

                        }

                        response.Message.forEach((item, index) => {
                            index == 0 &&

                                $("#available_qty" + counter).append(
                                    `<span>${item.total_quantity}</span>`
                                );
                            $("#available_qty" + counter).append(
                                `<input type="hidden" value="${item.total_quantity}" id="av_qty${counter}">`
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
    $(document).on('click', '.remove_item_btn', function(e) {
        e.preventDefault();
        let row_item = $(this).parent().parent().parent();
        $(row_item).remove();
        counter -= 1;
    })

    // depedent chained dropdowns medicine and medicine category without the plus button
    $("#MedicineCategory1").on("change", function() {

        // Clear all other fields
        $("#Medicine1").html("");


        // if the data selected is not empty
        if ($(this).val() != "") {
            get_category_medicine($("#MedicineCategory1").val());
        }
    });

    //..... depedent chained dropdowns medicine and medicine category without the plus button
    function get_category_medicine(MedicineCategory1) {
        let formData = new FormData();
        formData.append("MedicineCategory1", MedicineCategory1);
        $.ajax({
            method: "POST",
            url: "/patient/manage-inpatient-prescription/get_category_medicine",
            async: false,
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            success: function(response) {
                if (!response.isError) {

                    $("#Medicine1").html("");

                    // if the data length is 0
                    if (response.Message.length == 0) {
                        // Add disabled attribute from directorate
                        // $("#job_directorate").attr("disabled", true);
                        $("#Medicine1").append(
                            `<option value="Not available">Not available</option>`
                        );

                    } else {

                    }

                    response.Message.forEach((item, index) => {
                        index == 0 &&
                            $("#Medicine1").append(
                                `<option value="">Select Medicine</option>`
                            );
                        $("#Medicine1").append(
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

    // get total available quantity of a medicine
    $("#Medicine1").on("change", function() {

        // Clear all other fields
        $("#available_qty1").html("");


        // if the data selected is not empty
        if ($(this).val() != "") {
            get_available_medicine_qty($("#Medicine1").val());
        }
    });

    //....get total available quantity of a medicine
    function get_available_medicine_qty(Medicine) {
        let formData = new FormData();
        formData.append("Medicine", Medicine);
        $.ajax({
            method: "POST",
            url: "/patient/manage-inpatient-prescription/get_available_medicine",
            async: false,
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            success: function(response) {
                if (!response.isError) {

                    $("#available_qty1").html("");

                    // if the data length is 0
                    if (response.Message.length == 0) {
                        // Add disabled attribute from directorate
                        // $("#job_directorate").attr("disabled", true);
                        $("#available_qty1").append(
                            `<span>*</span>`
                        );

                    } else {

                    }

                    response.Message.forEach((item, index) => {
                        index == 0 &&

                            $("#available_qty1").append(
                                `<span>${item.total_quantity}</span>`
                            );
                        $("#available_qty1").append(
                            `<input type="hidden" value="${item.total_quantity}" id="av_qty1">`
                        );
                    });
                } else {
                    Swal.fire("Something Wrong!!", data.Message, "error");
                }
            },
            error: function(error) {},
        });
    }

    // submit button for prescription form
    $("#btn_submit").on("click", function(e) {
        e.preventDefault();
        // Create form data
        let formData = new FormData();
        let MedicineCategory = [];
        let Medicine = [];
        let Dose = [];
        let DoseInterval = [];
        let DoseDuration = [];
        let Qty = [];
        let AVQty = [];
        // loop through tracke elements
        for (let i = 1; i <= counter; i++) {
            MedicineCategory.push($("#MedicineCategory" + i).val());
            Medicine.push($("#Medicine" + i).val());
            Dose.push($("#Dose" + i).val());
            DoseInterval.push($("#DoseInterval" + i).val());
            DoseDuration.push($("#DoseDuration" + i).val());
            Qty.push($("#Qty" + i).val());
            AVQty.push($("#av_qty" + i).val());
        }
        // Read user 
        formData.append("admission_id", admission_id);
        formData.append("MedicineCategory1", MedicineCategory);
        formData.append("Medicine1", Medicine);
        formData.append("Dose1", Dose);
        formData.append("DoseInterval1", DoseInterval);
        formData.append("DoseDuration1", DoseDuration);
        formData.append("Qty1", Qty);
        formData.append("AvailableQty1", AVQty);
        formData.append("Instructions", $("#Instructions").val());

        let urls = "";
        if (insertType == "Insert") {
            urls = "/patient/manage-inpatient-prescription/new_prescription"
        } else {
            // formData.append("AppointmentID", $("#AppointmentID").val());
            urls = "/patient/manage-inpatient-prescription/edit_prescription"
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
                            // $("#PrescriptionForm")[0].reset();
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
    // ------------------------------End Prescription form--------------------------------------------------------- 

    // ------------------------------Start- Diagnosis form--------------------------------------------------------- 
    r_counter = 1
    l_counter = 1
    // ------------------------------Start- Radioloy part of the diagnosis form--------------------------------------------------------- 

    var radiology = get_radiology(); // Number of items to add to the DOM
    var radiologycategory = get_radio_category(); // Number of items to add to the DOM

    // a function to get radiology
    function get_radiology() {
        let radiology_list = "";
        $.ajax({
            method: "POST",
            url: "/patient/manage-inpatient-diagnosis/get_radiology_option_data",
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
            url: "/patient/manage-inpatient-diagnosis/get_radiology_option_data",
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
                url: "/patient/manage-inpatient-diagnosis/get_category_radiology",
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
            url: "/patient/manage-inpatient-diagnosis/get_category_radiology",
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
                url: "/patient/manage-inpatient-diagnosis/get_category_lab",
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
                url: "/patient/manage-inpatient-diagnosis/get_blood_test",
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
            url: "/patient/manage-inpatient-diagnosis/get_category_lab",
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
        $.ajax({
            method: "POST",
            url: "/patient/manage-inpatient-diagnosis/get_blood_test",
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
        formData.append("admission_id", admission_id);
        formData.append("laboratory", laboratory);
        formData.append("radiology", radiology);
        let urls = "";
        if (insertType == "Insert") {
            urls = "/patient/manage-inpatient-diagnosis/new_diagnosis"

        } else {
            // formData.append("CategoryID", $("#CategoryID").val());
            urls = "/patient/manage-inpatient-diagnosis/update_diagnosis"
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
    
    // ------------------------------Start- Operation form--------------------------------------------------------- 

    // submit the operation form
    $("#operation_btn").on("click", function(e) {

        // Prevent the page from loading or refreshing
        e.preventDefault();
        // Create form data
        let formData = new FormData();

        // Read user 
        formData.append("admission_id", admission_id);
        formData.append("OperationCategory", $("#OperationCategory").val());
        formData.append("OperationDate", $("#OperationDate").val());
        formData.append("Operation", $("#Operation").val());
     
        let urls = "";
        if (insertType == "Insert") {
            urls = "/patient/manage-inpatient-operation/new_patient_operation"

        } else {
            formData.append("OperationID", $("#OperationID").val());
            urls = "/patient/manage-inpatient-operation/update_patient_operation"
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
                            $("#operationForm")[0].reset();
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


    // chained dropdown for operation and operation category
    $("#OperationCategory").on("change", function() {

        // Clear all other fields
        $("#Operation").html("");


        // if the data selected is not empty
        if ($(this).val() != "") {
            get_category_operation($("#OperationCategory").val());
        }
    });
    // chained dropdown for operation and operation category
    function get_category_operation(operationCategory) {
        let formData = new FormData();
        formData.append("operationCategory", operationCategory);
        $.ajax({
            method: "POST",
            url: "/patient/manage-inpatient-operation/get_category_operation",
            async: false,
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            success: function(response) {
                if (!response.isError) {

                    $("#Operation").html("");

                    // if the data length is 0
                    if (response.Message.length == 0) {
                        // Add disabled attribute from directorate
                        // $("#job_directorate").attr("disabled", true);
                        $("#Operation").append(
                            `<option value="Not available">Not available</option>`
                        );
                        
                    } else {
                        // Remove disabled attribute from directorate
                        // $("#job_directorate").attr("disabled", false);
                    }

                    response.Message.forEach((item, index) => {
                        index == 0 &&
                            $("#Operation").append(
                                `<option value="">Select Operation</option>`
                            );
                        $("#Operation").append(
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
    // ------------------------------End- Operation form--------------------------------------------------------- 
    
    // --------------------------------start medication dose form ----------------------------------
    $("#medications_btn").on("click", function(e) {
        // Prevent the page from loading or refreshing
        e.preventDefault();

        // Create form data
        let formData = new FormData();

        // Read user inputs
        formData.append("admission_id", admission_id);
        formData.append("MedicationsDose_date", $("#med_date").val());
        formData.append("MedicationsName", $("#medicine").val());
        formData.append("MedicationsDose_time", $("#med_time").val());
        formData.append("MedicationDose", $("#med_dose").val());
        formData.append("Remarks", $("#Remarks").val());
    
        $.ajax({
            method: "POST",
            url: "/patient/manage-inpatient-profile/new_medicine_dose",
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
                            $("#medicationsform")[0].reset();
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
     
    // ---------------------------------end medication dose form-----------------------------------

      // --------------------------------start Nurse Notes form ----------------------------------
      $("#submit_nurseNote").on("click", function(e) {
        // Prevent the page from loading or refreshing
        e.preventDefault();

        // Create form data
        let formData = new FormData();

        // Read user inputs
        formData.append("admission_id", admission_id);
        formData.append("note_dateTime", $("#note_dateTime").val());
        formData.append("Nurse", $("#Nurse").val());
        formData.append("Note", $("#Note").val());
        formData.append("Comment", $("#Comment").val());
    
        $.ajax({
            method: "POST",
            url: "/patient/manage-inpatient-profile/new_NurseNotes",
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
                            $("#medicationsform")[0].reset();
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

    
    // ---------------------------------end Notes Note form-----------------------------------

    //--------------------------------start discharge form ----------------------
    // modify form according discharge status
    $("#dischargeStatus").on("change", function() { // for-admission  for-normal-referel-death for-referrel for-death
        if ($("#dischargeStatus").val() != "") {
            $(".for-admission").addClass("d-none");
            $(".for-normal-referel-death").addClass("d-none");
            $(".for-referrel").addClass("d-none");
            $(".for-death").addClass("d-none");
            if ($("option:selected", "#dischargeStatus").text() == "Normal" ){

                $(".for-referrel").removeClass("d-none");
                $(".referrell").addClass("d-none");

                $(".for-death").removeClass("d-none");
                $(".death").addClass("d-none");

                $(".for-normal-referel-death").removeClass("d-none");
                $(".for-normal-referel-death").removeClass("d-none");
            } else if ($("option:selected", "#dischargeStatus").text() == "Death" ) {
                $(".for-referrel").removeClass("d-none");
                $(".referrell").addClass("d-none");

                $(".for-normal-referel-death").removeClass("d-none");
                $(".for-normal-referel-death").removeClass("d-none");

                $(".for-death").removeClass("d-none");
                $(".death").removeClass("d-none");
            } else if ($("option:selected", "#dischargeStatus").text() == "Referrel" ) {
               
                $(".for-normal-referel-death").removeClass("d-none");
                $(".for-normal-referel-death").removeClass("d-none");

                $(".for-death").removeClass("d-none");
                $(".death").addClass("d-none");

                $(".for-referrel").removeClass("d-none");
                $(".referrell").removeClass("d-none");
            } else {
                $(".for-normal-referel-death").removeClass("d-none");
                $(".for-normal-referel-death").removeClass("d-none");

             
            }
        } else {
            $(".for-normal-referel-death").removeClass("d-none");
                $(".for-normal-referel-death").removeClass("d-none");

              
        }
    });

    // submit discharge form
    $("#submit_discharge").on("click", function(e) {
        // Prevent the page from loading or refreshing
        e.preventDefault();

        // Create form data
        let formData = new FormData();

        // Read user inputs
        formData.append("admission_id", admission_id);

        formData.append("discharge_date", $("#discharge_date").val());
        formData.append("dischargeStatus", $("#dischargeStatus").val());
     
        formData.append("diagnosis_result", $("#diagnosis_result").val());
        formData.append("surgery_operations", $("#surgery_operations").val());
        formData.append("discharge_note", $("#discharge_note").val());

        formData.append("referel_date", $("#referel_date").val());
        formData.append("hospital_name", $("#hospital_name").val());
        formData.append("referel_reason", $("#referel_reason").val());

        formData.append("death_date", $("#death_date").val());
        formData.append("death_reason", $("#death_reason").val());
    
        $.ajax({
            method: "POST",
            url: "/patient/manage-inpatient-profile/new_discharge",
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
                            $("#dischargeform")[0].reset();
                            window.location.replace("/patient/inpatient-list");
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
    //----------------------------------finish discharge form---------------------

});