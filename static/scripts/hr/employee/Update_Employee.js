$(document).ready(function () {
  getAllEmployeDatas()
  getAbsentData()
  leaveHistoryFunc()
  let insertType = "Insert";
  img_profile = ''


  // show img profile modal changer
  $('#change_profile_picture').on('click', function () {
    $(".ProfilePicture").modal("show");
    $(".hide_doc").removeClass("d-none");
    $("#specialization").val('');
    $("#qualifcationIDs").val('');
    $("#updatedprofile").val('');
    insertType = "Insert";

    img_profile = $(this).attr('imgUrls')
    $("#lead-img").attr("src", img_profile);


  });


  $("#lead-image-input").on("change", function (e) {
    img_profile = e.target.files[0];
    var reader = new FileReader();
    reader.onload = function(event) {
      var imageUrl = event.target.result;   
      $("#lead-img").attr("src", imageUrl);
    };
    reader.readAsDataURL(img_profile);
  });


  // $("#updatedprofile").on("change", function (e) {
  //   img_profile = e.target.files[0];

  // });

  // saving and updating

  $("#update_profile_picture").on("click", function (e) {
    // Prevent the page from loading or refreshing
    e.preventDefault();

    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append('image', img_profile);

      formData.append("employee_id", employee_id);




    $.ajax({
      method: "POST",
      url: "/hrm/manage_employees/update_profile_picture",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {
          getAllEmployeDatas();
          $(".ProfilePicture").modal("hide");
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
              window.location.reload();


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
          $("#Phone").val(response.Message.phone);
          $("#address").val(response.Message.address);
          $("#email").val(response.Message.email);
          $("#Emer_contact").val(response.Message.emergency_contact);
          $("#title").val(response.Message.title);




          let x = response.Message.id;
          console.log("waxan wada  " + x);
          $("#empoyee_bank_id").val(x);
          
        

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
          $("#d_Phone").val(response.Message.d_Phone);
          $("#d_address").val(response.Message.address);
          $("#d_email").val(response.Message.email);
          $("#d_Emer_contact").val(response.Message.Emargency_contact);
          $("#d_title").val(response.Message.title);

          $("#d_Fullname").text(response.Message.fullname);    
          $("#d_person_email").text(response.Message.email);
          $("#d_mytitles").text(response.Message.titlename);
          $("#empl_states").text(response.Message.emp_approve);





        }
      },
      error: function (response) { },
    });
  }

  $(".approval_list").on("click", "#approve", function () {

    handleEmployeeApprovel(
      "Approved",
      employee_id
    );
  });
  
  $(".approval_list").on("click", "#reject", function () {

    handleEmployeeApprovel(
      "Rejected",
      employee_id
    );
  });



  // Finction to handle job approval
  function handleEmployeeApprovel(status, employee) {
    // Prepare the form data
    let formData = new FormData();
    // Append data to form data

    formData.append("status", status);
    formData.append("employee_id", employee);
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
          url: "/hrm/manage_employees/approve_reject_employee",
          headers: { "X-CSRFToken": csrftoken },
          processData: false,
          contentType: false,
          data: formData,
          async: false,
          success: function (data) {
            if (!data.isError) {
              getAllEmployeDatas()
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
                  window.location.reload()
      
                }
              });

              // Display all budgeting  by filtering year and month
              // if ($("#SelectYear").val() != "" && $("#SelectMonth").val()) {
              //   GetAllBudget($("#SelectYear").val(), $("#SelectMonth").val());
              // }
            }

            //  else {
            //   Swal.fire(data.title, data.Message, data.type);
            // }
          
          },
          error: function (error) {
            //(error);
          },
        
        });
     
      }
    
    }   
    )
  }



  LeaveHistory


  function getAbsentData() {
    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("id", employee_id);
    $.ajax({
      method: "POST",
      url: "/hrm/manage_employees/getemployeAbsentdata",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {
          let table = $("#AbsentDay").DataTable().clear().draw();

          for (let index = 0; index < response.Message.length; index++) {
            let temp = [
              response.Message[index].shift_name,
              response.Message[index].shift_type,
              response.Message[index].shift_start,
              response.Message[index].end_shift,
              response.Message[index].stateday,
              response.Message[index].dayname,
              response.Message[index].state,

        
            ];
            table.row.add(temp).draw();
          }

        }
      },
      error: function (response) { },
    });
  }

  function leaveHistoryFunc() {
    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("id", employee_id);
    $.ajax({
      method: "POST",
      url: "/hrm/manage_employees/getleaveHistory",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {
          let table = $("#LeaveHistory").DataTable().clear().draw();

          for (let index = 0; index < response.Message.length; index++) {
            let temp = [

              response.Message[index].leaveType,
              response.Message[index].leaveTypenumber,         
              response.Message[index].startDay,
              response.Message[index].Endday,
              response.Message[index].remaindays,         
              response.Message[index].leaveState,
              response.Message[index].approvedWho,

        
            ];
            table.row.add(temp).draw();
          }

        }
      },
      error: function (response) { },
    });
  }
  
});

