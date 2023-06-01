$(document).ready(function() {
    insertType = "Insert";
    counter = 1

    var available_medicines = get_available_medicines(); // Number of items to add to the DOM
    var available_med_category = get_available_med_category(); // Number of items to add to the DOM

    // a function to get available medicines
    function get_available_medicines() {
        let medicineList = "";
        $.ajax({
            method: "POST",
            url: "/prescription/manage-medicine-order/manage_medicine_order_data",
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
            url: "/prescription/manage-medicine-order/manage_medicine_order_data",
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


    function medicine_option_elements() {
        let options = "";
        available_medicines.forEach((item, index) => {
            options += `<option value="${item.id}">${item.name}</option>`;
        });

        return options;
    }

    function med_category_option_elements() {
        let options = "";
        available_med_category.forEach((item, index) => {
            options += `<option value="${item.id}">${item.name}</option>`;
        });

        return options;
    }
    $(".add_item_btn").click(function(e) {
        counter += 1
        e.preventDefault();




        $("#show_item").append(` <div class="row" id="row${counter}">
        <div class="col-lg-3">
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
                    <option selected value="">Select</option>
                    ${medicine_option_elements()}
                </select>
            </div>                                                       
        </div>
        
        <div class="col-lg-3">
            <div class="mb-3">
                <label class="form-label">Box</label>
                <input type="number" class="form-control" name="Box${counter}" id="Qty${counter}">
                    
            </div>                                                       
        </div>
        <div class="col-lg-2">
            <div>
                <div class="mb-3">
                    <label class="form-label">Av.Qty</label>
                   
                    <div class="div" id="available_qty${counter}">
                    <input type="number" class="form-control"  disabled>
                </div>
                </div>                                                       
            </div>
        </div>
        <div class="col-lg-1">
            <div class="mb-3">
                <label class="form-label">Remove</label>
                <button type="button" class="btn btn-danger remove_item_btn" >
                <i class="ri-chat-delete-fill"></i>
                </button>
            </div>                                                       
        </div>
    </div>`);
    $("#Medicine"+counter).on("change", function() {

        // Clear all other fields
        $("#available_qty"+counter).html("");


        // if the data selected is not empty
        if ($(this).val() != "") {
            get_available_medicine($("#Medicine"+counter).val());
        }
    });
    function get_available_medicine(Medicine) {
        let formData = new FormData();
        formData.append("Medicine", Medicine);
        $.ajax({
            method: "POST",
            url: "/prescription/manage-medicine-order/get_available_medicine",
            async: false,
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            success: function(response) {
                if (!response.isError) {

                    $("#available_qty"+counter).html("");

                    // if the data length is 0
                    if (response.Message.length == 0) {
                        // Add disabled attribute from directorate
                        // $("#job_directorate").attr("disabled", true);
                        $("#available_qty"+counter).append(
                            `<span>*</span>`
                        );

                    } else {

                    }

                    response.Message.forEach((item, index) => {
                        index == 0 &&

                            $("#available_qty"+counter).append(
                                `<input type="number" class="form-control" value="${item.box}" name="AvailableQty" disabled>`
                            );
                        $("#hidden_available_qty"+counter).append(
                            `<span>${item.box}</span>`
                        );
                    });
                } else {
                    Swal.fire("Something Wrong!!", data.Message, "error");
                }
            },
            error: function(error) {},
        });
    }
    

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
            url: "/prescription/manage-medicine-order/get_category_medicine",
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


    });
    $(document).on('click', '.remove_item_btn', function(e) {
        e.preventDefault();
        let row_item = $(this).parent().parent().parent();
        $(row_item).remove();
        counter -= 1;
    })

    $("#MedicineCategory1").on("change", function() {

        // Clear all other fields
        $("#Medicine1").html("");


        // if the data selected is not empty
        if ($(this).val() != "") {
            get_category_medicine($("#MedicineCategory1").val());
        }
    });


    function get_category_medicine(MedicineCategory1) {
        let formData = new FormData();
        formData.append("MedicineCategory1", MedicineCategory1);
        $.ajax({
            method: "POST",
            url: "/prescription/manage-medicine-order/get_category_medicine",
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
    $("#Medicine1").on("change", function() {

        // Clear all other fields
        $("#available_qty1").html("");


        // if the data selected is not empty
        if ($(this).val() != "") {
            get_available_medicine($("#Medicine1").val());
        }
    });
    function get_available_medicine(Medicine) {
        let formData = new FormData();
        formData.append("Medicine", Medicine);
        $.ajax({
            method: "POST",
            url: "/prescription/manage-medicine-order/get_available_medicine",
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
                                `<input type="number" class="form-control" value="${item.box}" id="AvailableQty" disabled>`
                            );
                        $("#hidden_available_qty1").append(
                            `<span>${item.box}</span>`
                        );
                    });
                } else {
                    Swal.fire("Something Wrong!!", data.Message, "error");
                }
            },
            error: function(error) {},
        });
    }


    $("#btn_submit").on("click", function(e) {
        e.preventDefault();
        // Create form data
        let formData = new FormData();
        let MedicineCategory = [];
        let Medicine = [];
       
        
        let Qty = [];

        // loop through tracke elements
        for (let i = 1; i <= counter; i++) {
            MedicineCategory.push($("#MedicineCategory" + i).val());
            Medicine.push($("#Medicine" + i).val());
          
            Qty.push($("#Qty" + i).val());
        }


        // Prevent the page from loading or refreshing


        // Read user 
        
        formData.append("MedicineCategory1", MedicineCategory);
        formData.append("Medicine1", Medicine);
        formData.append("Qty1", Qty);
       
        formData.append("available_qty1", $("#AvailableQty").val());
        
        let urls = "";
        if (insertType == "Insert") {
            urls = "/prescription/manage-medicine-order/new_medicine_order"
        } else {
            formData.append("AppointmentID", $("#AppointmentID").val());
            urls = "/prescription/manage-medicine-order/edit_prescription"
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
                            $("#PrescriptionForm")[0].reset();
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
    $("#PrescriptionTable tbody").on("click", "#editbuttonPrescription", function(e) {
        e.preventDefault();
        const ID = $(this).attr("rowid");
        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("AppointmentId", ID);


        $.ajax({
            method: "POST",
            url: "/patient/manage_prescription/getPrescription",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {
                    insertType = "Update";
                    $("#PrescriptionModal").modal("show");
                    $("#myExtraLargeModalLabel").text("Update Prescription");

                    // $("#medicineId").val(response.Message.medicinePrescriptionId);
                    // $("#radiologyId").val(response.Message.radiologyId);
                    // $("#labId").val(response.Message.labId);

                    $("#AppointmentID").val(response.Message.appointmentId);

                    $("#Medicine1").val(response.Message.medicineName);
                    $("#MedicineCategory1").val(response.Message.medicineCategory);
                    $("#Dose1").val(response.Message.dose);
                    $("#DoseInterval1").val(response.Message.doseInterval);
                    $("#DoseDuration1").val(response.Message.doseDuration);
                    $("#Qty1").val(response.Message.quantity);
                    $("#laboratory").val(response.Message.labTest);
                    $("#radiology").val(response.Message.radiologyExam);



                    // formData.append("Qty1", $("#Qty1").val());
                    // formData.append("AvailableQty1", $("#AvailableQty1").val());
                    // formData.append("laboratory", $("#laboratory").val());
                    // formData.append("radiology", $("#radiology").val());
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






    
    $("#MedicineOrder tbody").on("click", "#orderview", function(e) {
        e.preventDefault();
        const ID = $(this).attr("rowid");
        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("order_id", ID);

        let Tests = "";
        $.ajax({
            method: "POST",
            url: "/prescription/manage-medicine-order/MedicineOderView",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {

                    // insertType = "Update";
                    $("#addapprove").modal("show");
                    

                    
                    $("#OrderId").val(response.Message.OrderId);
                    
                    
                    const tbody = $('#tbody')
                    response.Message.medicineOrder.map(Order => {
                        tbody.append('<tr></tr>').append(`<td>${Order.MedicineName}</td>
                        
                        <td>${Order.Quantity} </td>
                        
                        
                        
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
