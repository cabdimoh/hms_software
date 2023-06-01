$(document).ready(function() {
    insertType = "Insert";

    r_counter = 1
    l_counter = 1

    // ------------------------------Start Prescription form--------------------------------------------------------- 
    counter = 1
    var available_medicines = get_available_medicines(); // Number of items to add to the DOM
    var available_med_category = get_available_med_category(); // Number of items to add to the DOM

    // a function to get available medicines
    function get_available_medicines() {
        let medicineList = "";
        $.ajax({
            method: "POST",
            url: "/patient/manage-prescription/get_option_data",
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
            url: "/patient/manage-prescription/get_option_data",
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




        $("#show_item").append(` <div class="row" id="row${counter}">
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
                url: "/patient/manage-prescription/get_category_medicine",
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
                url: "/patient/manage-prescription/get_available_medicine",
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

                            $("#available_qty"+counter).append(
                                `
                                <input type="number" class="form-control" value="${item.total_quantity}" id="av_qty${counter}" disabled>`
                            );
                            $("#hidden_available_qty"+counter).append(
                                `<span>${item.total_quantity}</span>`
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
            url: "/patient/manage-prescription/get_category_medicine",
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
            url: "/patient/manage-prescription/get_available_medicine",
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
                            `<input type="number" class="form-control" value="${item.total_quantity}" id="av_qty1" disabled>`
                        );
                        $("#hidden_available_qty1").append(
                            `<span>${item.total_quantity}</span>`
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
        formData.append("appointmentId", appointmentId);
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
            urls = "/patient/manage-prescription/new_prescription"
        } else {
            // formData.append("AppointmentID", $("#AppointmentID").val());
            urls = "/patient/manage-prescription/edit_prescription"
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



  



    // ------------------------------Start- Operation form--------------------------------------------------------- 

    // submit the operation form
    $("#operation_btn").on("click", function(e) {

        // Prevent the page from loading or refreshing
        e.preventDefault();
        // Create form data
        let formData = new FormData();

        // Read user 
        formData.append("appointmentId", appointmentId);
        formData.append("OperationCategory", $("#OperationCategory").val());
        formData.append("OperationDate", $("#OperationDate").val());
        formData.append("Operation", $("#Operation").val());
     
        let urls = "";
        if (insertType == "Insert") {
            urls = "/patient/manage-patient-operation/new_patient_operation"

        } else {
            formData.append("OperationID", $("#OperationID").val());
            urls = "/patient/manage-patient-operation/update_patient_operation"
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
            url: "/patient/manage-patient-operation/get_category_operation",
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
                        
                        $("#Operation").append(
                            `<option value="Not available">Not available</option>`
                        );
                       
                    } else {
                        
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

    //-------------------------------Start Approve patient-------------------------------------------------------
    
  $(".approval_list").on("click", "#approve", function () {

    ApproveAppointment(
      "Approved",
      appointmentId
    );
  });
  
  $(".approval_list").on("click", "#reject", function () {

    ApproveAppointment(
      "Cancelled",
      appointmentId
    );
  });



  // Finction to handle job approval
  function ApproveAppointment(status, appointment) {
    // Prepare the form data
    let formData = new FormData();
    // Append data to form data

    formData.append("status", status);
    formData.append("appointmentId", appointment);
    Swal.fire({
      title: "Are you sure",
      text: "Are you sure to " + status + " ?",
      icon: "warning",
      showCancelButton: !0,
      confirmButtonColor: "#2ab57d",
      cancelButtonColor: "#fd625e",
      confirmButtonText: "Yes, " + status + " it",
    }).then(function (e) {
      if (e.value) {
        $.ajax({
          method: "POST",
          url: "/patient/approve-appointment/approve_appointment",
          headers: { "X-CSRFToken": csrftoken },
          processData: false,
          contentType: false,
          data: formData,
          async: false,
          success: function (data) {
            if (!data.isError) {
              Swal.fire({
                title: data.title,
                text: data.Message,
                icon: data.type,
                confirmButtonColor: "#2ab57d",
                cancelButtonColor: "#fd625e",
                confirmButtonText: "Ok it!",
              }).then((e) => {
                if (e.value) {
                  // hide the modal and resret the form
                  if (status == "Cancelled"){
                    window.location.replace("/patient/appointment-list");
                  }
                  else{
                    window.location.reload()
                  }
                 
      
                }
              });

            }

           
          
          },
          error: function (error) {
            //(error);
          },
        
        });
     
      }
    
    }   
    )
  }
  //-----------------------------------------end Approve/Reject Patients-----------------------------


  // ---------------------------------------start ORder admission -------------
  $("#submit_order_admission").on("click", function(e) {

    // Prevent the page from loading or refreshing
    e.preventDefault();
    // Create form data
    let formData = new FormData();

    // Read user 
    formData.append("appointmentId", appointmentId);
    formData.append("admission_date", $("#admission_date").val());
    formData.append("bedType", $("#bedType").val());
    formData.append("admission_reason", $("#admission_reason").val());
    formData.append("admission_note", $("#admission_note").val());
    formData.append("patient_priority", $("#patient_priority").val());
   
    let urls = "";
    if (insertType == "Insert") {
        urls = "/patient/order-admission/new_order_admission"

    } else {
        formData.append("OperationID", $("#OperationID").val());
        urls = "/patient/order-admission/edit_order_admission"
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
                        window.location.replace("/patient/appointment-list");
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
  // ---------------------------------------end order admission -----------------

    // ----------------------------edit prescription----------------------
   // depedent chained dropdowns medicine and medicine category without the plus button
   $("#MedicineCategory_edit1").on("change", function() {

    // Clear all other fields
    $("#Medicine_edit1").html("");


    // if the data selected is not empty
    if ($(this).val() != "") {
        get_category_medicine_edit($("#MedicineCategory_edit1").val());
    }
    });

    //..... depedent chained dropdowns medicine and medicine category without the plus button
    function get_category_medicine_edit(MedicineCategory1) {
        let formData = new FormData();
        formData.append("MedicineCategory1", MedicineCategory1);
        console.log(MedicineCategory1)

        $.ajax({
            method: "POST",
            url: "/patient/manage-prescription/get_category_medicine",
            async: false,
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            success: function(response) {
                if (!response.isError) {

                    $("#Medicine_edit1").html("");

                    // if the data length is 0
                    if (response.Message.length == 0) {
                        // Add disabled attribute from directorate
                        // $("#job_directorate").attr("disabled", true);
                        $("#Medicine_edit1").append(
                            `<option value="Not available">Not available</option>`
                        );

                    } else {

                    }

                    response.Message.forEach((item, index) => {
                        index == 0 &&
                            $("#Medicine_edit1").append(
                                `<option value="">Select Medicine</option>`
                            );
                        $("#Medicine_edit1").append(
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
    prescriped_medicine_ids=[]
    $('input[data-prescribed-medicine]').each(function() {
        var id = $(this).attr('id');
        var matches = id.match(/(\D+)(\d+)/);
        var numberPart = parseInt(matches[2]);
        console.log(matches);
    
        prescriped_medicine_ids.push(numberPart);
    });
    console.log(prescriped_medicine_ids, '...');

    // for (let i = 0; i < report.length; i++) {
    //     TestNumber.push($("#TestNumber" + report[i]).val());
    //     ResultValue.push($("#ResultValue" + report[i]).val());
    //     flagvalue.push($("#flagvalue" + report[i]).val());
    //     console.log(prescriped_medicine_ids[i]);

    // }
    counter_edit = 4;
     // add elements button
     $(".add_item_btn_edit5").click(function(e) {
        counter_edit += 1
        e.preventDefault();




        $("#show_item_edit5").append(` <div class="row" id="row_edit${counter_edit}">
        <div class="col-lg-2">
            <div class="mb-3">
                <label class="form-label">Medicine Category</label>
                <select class="form-select" name="MedicineCategory_edit1${counter_edit}" id="MedicineCategory_edit1${counter_edit}">
                <option selected value="">Select</option>
                ${med_category_option_elements()}
                </select>
            </div>                                                       
        </div>

        <div class="col-lg-2">
            <div class="mb-3">
                <label class="form-label">Medicine</label>
                <select class="form-select" name="Medicine${counter_edit}" id="Medicine_edit1${counter_edit}">
                   
                </select>
            </div>                                                       
        </div>
        <div class="col-md-2">
            <div class="mb-3">
                <label class="form-label">Dose</label>
                <input type="text" class="form-control" name="Dose${counter_edit}"  id="Dosee${counter_edit}" placeholder="1 tablet at a time">
            </div>                                                       
        </div>
        <div class="col-md-2">
            <div class="mb-3">
                <label class="form-label">Dose Interval</label>
                <input type="text" class="form-control" name="DoseInterval${counter_edit}"  id="DoseIntervale${counter_edit}" placeholder="1 tablet at a time">
            </div>                                                       
         </div>
        
        <div class="col-lg-2">
            <div class="mb-3">
                <label class="form-label">Dose Duration</label>
                <select class="form-select" name="DoseDuration${counter_edit}"  id="DoseDuratione${counter_edit}">
                    <option selected value="">Select</option>
                    <option value="3 maalmood">3 maalmood</option>
                    <option value="1 isbuuc">1 isbuuc</option>
                    <option value="2 isbuuc">2 isbuuc</option>
                    <option value="3 isbuuc">3 isbuuc</option>
                    <option value="1 bil">1 bil</option>
                    <option value="2 bil">2 bil</option>
                    <option value="3 bil">3 bil</option>
                    <option value="6 bil">6 bil</option>
                </select>
            </div>                                                       
        </div>
        <div class="col-lg-1">
            <div class="mb-3">
                <label class="form-label">Qty</label>
                <input type="number" class="form-control" name="Qtye${counter_edit}" id="Qty${counter_edit}">
                <div class="text-muted" style="color:#001022;" id="available_qty${counter_edit}">*</div>
  
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

        // $("#MedicineCategory" + counter).on("change", function() {

        //     // Clear all other fields
        //     $("#Medicine" + counter).html("");


        //     // if the data selected is not empty
        //     if ($(this).val() != "") {
        //         get_category_medicine($("#MedicineCategory" + counter).val());
        //     }
        // });


        // function get_category_medicine(MedicineCategory1) {
        //     let formData = new FormData();
        //     formData.append("MedicineCategory1", MedicineCategory1);
        //     $.ajax({
        //         method: "POST",
        //         url: "/patient/manage-prescription/get_category_medicine",
        //         async: false,
        //         headers: { "X-CSRFToken": csrftoken },
        //         processData: false,
        //         contentType: false,
        //         data: formData,
        //         success: function(response) {
        //             if (!response.isError) {

        //                 $("#Medicine" + counter).html("");

        //                 // if the data length is 0
        //                 if (response.Message.length == 0) {
        //                     // Add disabled attribute from directorate
        //                     // $("#job_directorate").attr("disabled", true);
        //                     $("#Medicine" + counter).append(
        //                         `<option value="Not available">Not available</option>`
        //                     );

        //                 } else {

        //                 }

        //                 response.Message.forEach((item, index) => {
        //                     index == 0 &&
        //                         $("#Medicine" + counter).append(
        //                             `<option value="">Select Medicine</option>`
        //                         );
        //                     $("#Medicine" + counter).append(
        //                         `<option value="${item.id}">${item.name}</option>`
        //                     );

        //                 });
        //             } else {
        //                 Swal.fire("Something Wrong!!", data.Message, "error");
        //             }
        //         },
        //         error: function(error) {},
        //     });
        // }
        // $("#Medicine" + counter).on("change", function() {

        //     // Clear all other fields
        //     $("#available_qty" + counter).html("");


        //     // if the data selected is not empty
        //     if ($(this).val() != "") {
        //         get_available_medicine_qty($("#Medicine" + counter).val());
        //     }
        // });


        // function get_available_medicine_qty(Medicine) {
        //     let formData = new FormData();
        //     formData.append("Medicine", Medicine);
        //     $.ajax({
        //         method: "POST",
        //         url: "/patient/manage-prescription/get_available_medicine",
        //         async: false,
        //         headers: { "X-CSRFToken": csrftoken },
        //         processData: false,
        //         contentType: false,
        //         data: formData,
        //         success: function(response) {
        //             if (!response.isError) {

        //                 $("#available_qty" + counter).html("");

        //                 // if the data length is 0
        //                 if (response.Message.length == 0) {
        //                     // Add disabled attribute from directorate
        //                     // $("#job_directorate").attr("disabled", true);
        //                     $("#available_qty" + counter).append(
        //                         `<span>*</span>`
        //                     );

        //                 } else {

        //                 }

        //                 response.Message.forEach((item, index) => {
        //                     index == 0 &&

        //                         $("#available_qty" + counter).append(
        //                             `<span>${item.total_quantity}</span>`
        //                         );
        //                     $("#available_qty" + counter).append(
        //                         `<input type="hidden" value="${item.total_quantity}" id="av_qty${counter}">`
        //                     );
        //                 });
        //             } else {
        //                 Swal.fire("Something Wrong!!", data.Message, "error");
        //             }
        //         },
        //         error: function(error) {},
        //     });
        // }


    });
    //------------------------------edit prescription to be continued later---------------------

    //-----------------------------check if the order has blood result ordered or urine or stool ---------
    
    $(".view-order-btn").on("click", function(e) {
        // Prevent the page from loading or refreshing
        e.preventDefault();
    
        // Get the ID of the clicked element
        let id = $(this).attr('id');
        var matches = id.match(/(\D+)(\d+)/);
        var numberPart = parseInt(matches[2]);
        // Create form data
        let formData = new FormData();
        
        // Add the ID to the form data
        formData.append("clicked_order", numberPart);

        console.log(numberPart)
        $.ajax({
            method: "POST",
            url: "/patient/manage-patient-diagnosis/view_lab_order",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {
                    if (response.Message.has_urine_tests === true) {
                        var urine_result_div = document.getElementById("urine_result");
                        urine_result_div.style.display = "block";
                        var blood_result_div = document.getElementById("blood_result");
                        blood_result_div.style.display = "none";
                        var stool_result_div = document.getElementById("stool_result");
                        stool_result_div.style.display = "none";
                    } else if (response.Message.has_stool_tests === true) {
                        var urine_result_div = document.getElementById("urine_result");
                        urine_result_div.style.display = "none";
                        var blood_result_div = document.getElementById("blood_result");
                        blood_result_div.style.display = "none";
                        var stool_result_div = document.getElementById("stool_result");
                        stool_result_div.style.display = "block";
                    } else if (response.Message.has_blood_tests === true) {
                        var urine_result_div = document.getElementById("urine_result");
                        urine_result_div.style.display = "none";
                        var blood_result_div = document.getElementById("blood_result");
                        blood_result_div.style.display = "block";
                        var stool_result_div = document.getElementById("stool_result");
                        stool_result_div.style.display = "none";
                    } else {
                        // None of the conditions are true, so show all the elements
                        var urine_result_div = document.getElementById("urine_result");
                        urine_result_div.style.display = "block";
                        var blood_result_div = document.getElementById("blood_result");
                        blood_result_div.style.display = "block";
                        var stool_result_div = document.getElementById("stool_result");
                        stool_result_div.style.display = "block";
                    }
                  
                } else {
                   
                }
            },
            error: function(response) {},
        });
    });
    //-----------------------------end check if the order has either blood, urine, stool ordered in it------------
//     const printModalBtn = document.querySelector('#print-modal-btn');

//   printModalBtn.addEventListener('click', () => {
//     const modalContent = document.querySelector('.view-presription-modal');
//     const printWindow = window.open('', 'Print Window');
//     printWindow.document.write(`
//       <html>
//         <head>
//           <title>Print Window</title>
//           <style>
//             table {
//               border-collapse: collapse;
//               width: 100%;
//             }
//             th, td {
//               border: 1px solid black;
//               padding: 8px;
//               text-align: left;
//             }
//             th {
//               background-color: #f2f2f2;
//               color: black;
//             }
//             .second-table {
//                 margin-top: 32px;
//               }
//           </style>
//         </head>
//         <body>
//         <div id="invoice" class="modal fade view-modal"  tabindex="-1" role="dialog" id="#" aria-labelledby="myLargeModalLabel1" aria-hidden="true">
//         <div class="modal-dialog modal-lg">
//             <div class="modal-content">
//                 <div class="modal-header">
//                     <h5 class="modal-title" id="myLargeModalLabel1">Invoice</h5>
                    
//                 </div>
//                 <div class="modal-body">
//                     <div class="row justify-content-center">
//                         <div class="col-xxl-9">
                           
//                                 <div class="row">
                                
//                                     <div class="col-lg-12">
//                                         <div class="card-header border-bottom-dashed p-4">
//                                             <div class="d-flex">
//                                                 <div class="flex-grow-1">
//                                                     <img src="/assets/images/logo2-removebg-preview.png" style="width: 30%;" alt="" height="60" class="card-logo card-logo-dark" alt="logo dark" height="17">
//                                                     <!-- <img src="/assets/images/images.jpeg" style="width: 100%;" class="card-logo card-logo-light" alt="logo light" height="17"> -->
//                                                     <div class="mt-sm-5 mt-4">
//                                                         <h6 class="text-muted text-uppercase fw-semibold">Address</h6>
//                                                         <p class="text-muted mb-1" id="address-details">Mugadishu , Somalia</p>
//                                                         <p class="text-muted mb-0" id="zip-code"><span>Zone:</span> Maka al mukarama</p>
//                                                     </div>
//                                                 </div>
//                                                 <div class="flex-shrink-0 mt-sm-0 mt-3">
//                                                     </span><span id="legal-register-no">GOVERMENT HOSPITAL </span></h6>
//                                                     <h6><span class="text-muted fw-normal">Email:</span><span id="email">velzon@themesbrand.com</span></h6>
//                                                     <h6><span class="text-muted fw-normal">Website:</span> <a href="https://themesbrand.com/" class="link-primary" target="_blank" id="website">www.themesbrand.com</a></h6>
//                                                     <h6 class="mb-0"><span class="text-muted fw-normal">Contact No: </span><span id="contact-no"> +252 0615667788</span></h6>
//                                                 </div>
//                                             </div>
//                                         </div>
//                                         <!--end card-header-->
//                                     </div><!--end col-->
//                                     <div class="col-lg-12">
//                                     ${modalContent.innerHTML}
    
//                                     </div>
    
    
    
                                         
                                      
//                                 </div><!--end row-->
                           
//                             <!--end card-->
//                         </div>
//                         <!--end col-->
//                     </div>
//                 </div>
//             </div><!-- /.modal-content -->
//         </div><!-- /.modal-dialog -->
//     </div>
//         </body>
//       </html>
//     `);
//     printWindow.document.close();
//     printWindow.focus();
//     printWindow.print();
//     printWindow.close();
//   });
});