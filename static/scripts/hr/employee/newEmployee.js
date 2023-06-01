$(document).ready(function () {
  getAllEmployeDatas()
  let insertType = "Insert";


// approve employee
  $('#Aprove_employee').on('click', function () {
    $(".ApproveModel").modal("show");

    insertType == 'approve_reject_employee'

  
  });
// approve employee



  // saving and updating

  $("#btn_save").on("click", function (e) {
    // Prevent the page from loading or refreshing
    e.preventDefault();

    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("first_name", $("#first_name").val());
    formData.append("father_name", $("#father_name").val());
    formData.append("last_name", $("#last_name").val());
    formData.append("mother_name", $("#mother_name").val());
    formData.append("gender", $("#gender").val());
    formData.append("marital", $("#maritial").val());
    formData.append("Blood_Group", $("#Blood_Group").val());
    formData.append("Dob", $("#Dob").val());    
    formData.append("phone", $("#Phone").val());
    formData.append("emergency_contect", $("#Emer_contact").val());
    formData.append("email", $("#email").val());
    formData.append("speciality", $("#title").val());
    formData.append("address", $("#address").val());
    formData.append("photo", photo);
    formData.append("employee_id", employee_id);




    $.ajax({
      method: "POST",
      url: "/hrm/manage_employees/update_employee_data",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {
          getAllEmployeDatas();
          $(".editBasicEmpInfo").modal("hide");
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
              $("#Employee_form")[0].reset();

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
      error: function (response) { },
    });
  });


  $("#save_state").on("click", function (e) {
    // Prevent the page from loading or refreshing
    e.preventDefault();

    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("app_re_employee", $("#app_re_employee").val());
  

    formData.append("employee_id", employee_id);




    $.ajax({
      method: "POST",
      url: "/hrm/manage_employees/approve_reject_employee",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {
          getAllEmployeDatas();
          $(".ApproveModel").modal("hide");
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
              $("#Employee_form")[0].reset();

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
      error: function (response) { },
    });
  });


  // Retrieving single data and display modal

  $("#editButtonEmplDate").on("click", function (e) {

    e.preventDefault();
    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("employee_id", employee_id);


    $.ajax({
      method: "POST",
      url: "/hrm/manage_employees/getEmployeeData",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {

        if (!response.isError) {
          insertType = "Update";
          $(".editBasicEmpInfo").modal("show");
          $("#modaeltitle").text("Update Employee Basic information");
          $(".hidephoto").addClass("d-none");

          $("#first_name").val(response.Message.employee_firstname);
          $("#father_name").val(response.Message.employee_father_name);
          $("#last_name").val(response.Message.employee_last_name);
          $("#mother_name").val(response.Message.employee_mother_name);
          $("#Dob").val(response.Message.dob);
          $("#Blood_Group").val(response.Message.blood_group);
          $("#gender").val(response.Message.gender);
          $("#maritial").val(response.Message.maritial);
          $("#Join_date").val(response.Message.date_join);
          $("#Phone").val(response.Message.phone);
          $("#address").val(response.Message.address);
          $("#email").val(response.Message.email);
          $("#Emer_contact").val(response.Message.emergency_contact);
          $("#title").val(response.Message.title);




          let x = response.Message.id;
          console.log("waxan wada  " + x);
          $("#empoyee_bank_id").val(x);
          // getEmployeDataform()

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
      error: function (response) { },
    });

  });

// approve employee

  // Get all employee  data 

  function getAllEmployeDatas() {
    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("id", employee_id);
    $.ajax({
      method: "POST",
      url: "/hrm/manage_employees/getAllEmployeData",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {

          $("#d_first_name").val(response.Message.first_name);
          $("#d_father_name").val(response.Message.father_name);
          $("#d_last_name").val(response.Message.last_name);
          $("#d_mother_name").val(response.Message.mother_name);
          $("#d_Dob").val(response.Message.dob);
          $("#d_Blood_Group").val(response.Message.blood_group);
          $("#d_gender").val(response.Message.gender);
          $("#d_maritial").val(response.Message.maritial);
          $("#d_Join_date").val(response.Message.date_join);
          $("#d_Phone").val(response.Message.d_Phone);
          $("#d_address").val(response.Message.address);
          $("#d_email").val(response.Message.email);
          $("#d_Emer_contact").val(response.Message.Emargency_contact);
          $("#d_title").val(response.Message.title);

          $("#d_Fullname").text(response.Message.fullname);
          $("#d_mytitle").text(response.Message.d_title);
          $("#d_person_email").text(response.Message.email);
          



        }
      },
      error: function (response) { },
    });
  }












});

