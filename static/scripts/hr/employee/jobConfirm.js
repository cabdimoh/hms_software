$(document).ready(function () {


  $("#pending_job_table").on("click", "#Approved", function () {
    const id = $(this).attr('jobID')
    const employeeid = $(this).attr('employeeId')


    handleEmployeeApprovel(
      "Approved",
      id,
      employeeid

    );
  });


  $("#pending_job_table").on("click", "#Rejected", function () {
    const id = $(this).attr('jobID')
    const employeeid = $(this).attr('employeeId')


    handleEmployeeApprovel(
      "Rejected",
      id,
      employeeid

    );
  });


  $("#pending_job_table").on("click", "#Pending", function () {
    const id = $(this).attr('jobID')
    const employeeid = $(this).attr('employeeId')

    handleEmployeeApprovel(
      "Pending",
      id,
      employeeid
    );
  });

  function handleEmployeeApprovel(status, jobDetID, employee_id) {
    // Prepare the form data
    let formData = new FormData();
    // Append data to form data

    formData.append("status", status);
    formData.append("jobDetID", jobDetID);
    formData.append("employee_id", employee_id);
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
          url: "/hrm/manage_pending_jobs/approve_reject_jobs",
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
            (error);
          },

        });

      }

    }
    )
  }

  $("#pending_job_table").on("click", "#pendingjobView", function () {
    $('.ViewJobDetail_modal').modal('show')
    GetAllJobDetail($(this).attr('jobdetailID'))
  });


  function GetAllJobDetail(id) {

    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("id", id);

    $.ajax({
      method: "POST",
      url: "/hrm/manage_pending_jobs/get_job_detail_all",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {

          if(response.Message[0].employee_type == 'General-Director'){                       
              $(".directorClass").removeClass("col-lg-6");
              $(".directorClass").addClass("col-lg-12");
              $(".secretoryClass").addClass("d-none");
              $(".departmentClass").addClass("d-none");
              $(".sections").addClass("d-none");
              $(".netpayClass").removeClass("col-lg-12");
              $(".netpayClass").addClass("col-lg-6");            
          } 
          else if(response.Message[0].employee_type == 'Director-Secretory'){
              $(".directorClass").removeClass("col-lg-12");
              $(".directorClass").addClass("col-lg-6");
              $(".secretoryClass").removeClass("d-none");
              $(".departmentClass").addClass("d-none");
              $(".sections").addClass("d-none");
              $(".netpayClass").removeClass("col-lg-12");
              $(".netpayClass").addClass("col-lg-6");
     
          }            
          else if(response.Message[0].employee_type == 'Department-Head'){
              $(".directorClass").removeClass("col-lg-12");
              $(".directorClass").addClass("col-lg-6");
              $(".departmentClass").addClass("col-lg-6");
              $(".departmentClass").removeClass("col-lg-12");
              $(".secretoryClass").addClass("d-none");
              $(".departmentClass").removeClass("d-none");
              $(".sections").addClass("d-none");
              $(".netpayClass").removeClass("col-lg-12");
              $(".netpayClass").addClass("col-lg-6");                 
          }            
          else if(response.Message[0].employee_type == 'Section-Head'){

              $(".directorClass").removeClass("col-lg-12");
              $(".directorClass").addClass("col-lg-6");
              $(".directorClass").removeClass("d-none");
              
              $(".secretoryClass").addClass("d-none");
              $(".departmentClass").removeClass("d-none");
              $(".departmentClass").removeClass("col-lg-12");

              $(".departmentClass").addClass("col-lg-6");
              $(".sections").removeClass("d-none");
              $(".netpayClass").addClass("col-lg-12");         
          }     
          else{
              $(".directorClass").removeClass("col-lg-12");
              $(".directorClass").addClass("col-lg-6");
              $(".directorClass").removeClass("d-none");

              $(".secretoryClass").addClass("d-none");
              $(".departmentClass").removeClass("d-none");
              $(".departmentClass").removeClass("col-lg-12");

              $(".departmentClass").addClass("col-lg-6");
              $(".sections").removeClass("d-none");
              $(".netpayClass").addClass("col-lg-12");                     
          }            
        
          $('#empl_type').val(response.Message[0].employee_type)
          $('#job_type').val(response.Message[0].job_type)
          $('#directorate_id').val(response.Message[0].Director)
          
          console.log('yaan wada', response.Message[0].Director);

          get_department_name(response.Message[0].Director)
          $('#depart_id').val(response.Message[0].department_name)

          get_department_section(response.Message[0].department_name)          
          $('#section_id').val(response.Message[0].section_department)

          get_salary(response.Message[0].job_type)         
          $('#Jobtype_Salary').val(response.Message[0].jobytpesalary)
          $('#salary').val(response.Message[0].base_salary)
          get_secretory_name(response.Message[0].Director)
          $('#secretory_id').val(response.Message[0].secretary)
          $('#fix_alowence').val(response.Message[0].fixed_allow)
          $('#netpay').val(response.Message[0].base_pay)


        }


      },
      error: function (response) { },
    });
  }


  function get_secretory_name(secretary) {
    let formData = new FormData();
   
    formData.append("secretary", secretary);
    $.ajax({
        method: "POST",
        url: "/hrm/manage_Job_Detail/get_director_assistance_func",
        async: false,
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        success: function (response) {
            if (!response.isError) {

                $("#secretory_id").html("");

                // if the data length is 0
                if (response.Message.length == 0) {
                    // Add disabled attribute from directorate
                    // $("#job_directorate").attr("disabled", true);
                    $("#secretory_id").append(
                        `<option value="Not available">Not available</option>`
                    );
                    // $("#job_department").append(
                    //   `<option value="Not available">Not available</option>`
                    // );
                    // $("#job_section").append(
                    //   `<option value="Not available">Not available</option>`
                    // );
                    // $("#job_branch").append(
                    //   `<option value="Not available">Not available</option>`
                    // );
                    // $("#job_sub_branch").append(
                    //   `<option value="Not available">Not available</option>`
                    // );
                } else {
                    // Remove disabled attribute from directorate
                    // $("#job_directorate").attr("disabled", false);
                }

                response.Message.forEach((item, index) => {
                    index == 0 &&
                        $("#secretory_id").append(
                            `<option value="">Select Section</option>`
                        );
                    $("#secretory_id").append(
                        `<option value="${item.id}">${item.name}</option>`
                    );
                });
            } else {
                Swal.fire("Something Wrong!!", data.Message, "error");
            }
        },
        error: function (error) { },
    });
}

function get_department_section(section) {
    let formData = new FormData();
    
    formData.append("department", section);
    $.ajax({
        method: "POST",
        url: "/hrm/manage_Job_Detail/get_deb_section_func",
        async: false,
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        success: function (response) {
            if (!response.isError) {

                $("#section_id").html("");

                // if the data length is 0
                if (response.Message.length == 0) {
                    // Add disabled attribute from directorate
                    // $("#job_directorate").attr("disabled", true);
                    $("#section_id").append(
                        `<option value="Not available">Not available</option>`
                    );
                    // $("#job_department").append(
                    //   `<option value="Not available">Not available</option>`
                    // );
                    // $("#job_section").append(
                    //   `<option value="Not available">Not available</option>`
                    // );
                    // $("#job_branch").append(
                    //   `<option value="Not available">Not available</option>`
                    // );
                    // $("#job_sub_branch").append(
                    //   `<option value="Not available">Not available</option>`
                    // );
                } else {
                    // Remove disabled attribute from directorate
                    // $("#job_directorate").attr("disabled", false);
                }

                response.Message.forEach((item, index) => {
                    index == 0 &&
                        $("#section_id").append(
                            `<option value="">Select Section</option>`
                        );
                    $("#section_id").append(
                        `<option value="${item.id}">${item.name}</option>`
                    );
                });
            } else {
                Swal.fire("Something Wrong!!", data.Message, "error");
            }
        },
        error: function (error) { },
    });
}

function get_salary(salary) {
    let formData = new FormData();
  
    formData.append("department", salary);
    $.ajax({
        method: "POST",
        url: "/hrm/manage_Job_Detail/get_salary_func",
        async: false,
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        success: function (response) {
            if (!response.isError) {



                $("#Jobtype_Salary").html("");
                if (response.Message.length == 0) {
                    $("#Jobtype_Salary").append(
                        `<option value="Not available">Not available</option>`
                    );

                } else {

                }


                response.Message.forEach((item, index) => {
                    index == 0 &&
                        $("#Jobtype_Salary").append(
                            `<option value="">Select Salary Type</option>`
                        );
                    $("#Jobtype_Salary").append(
                        `<option value="${item.id}">${item.name}</option>`
                    );
                });



            } else {
              Swal.fire("Something Wrong!!", data.Message, "error");
            }
        },
        error: function (error) { },
    });
}


function get_subcategory_salary(subsalary) {
    let formData = new FormData();
   
    formData.append("subsalary", subsalary);
    $.ajax({
        method: "POST",
        url: "/hrm/manage_Job_Detail/get_sub_category_salary_func",
        async: false,
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        success: function (response) {
            if (!response.isError) {

                $("#salary").val(response.Message[0].base_salary);
                $("#salary_id").val(response.Message[0].id);

                let salary = $("#salary").val();
                let fix_alowence = $("#fix_alowence").val();
                salary = salary == "" ? 0 : salary;
                fix_alowence = fix_alowence == "" ? 0 : fix_alowence;
                let total_amount = parseFloat(salary) + parseFloat(fix_alowence);
                $("#netpay").val(total_amount);


            } else {
                Swal.fire("Something Wrong!!", response.Message, "error");
            }
        },
        error: function (error) { },
    });
}

function get_department_name(department_id) {
    let formData = new FormData();
   
    formData.append("department_id", department_id);
    $.ajax({
        method: "POST",
        url: "/hrm/manage_Job_Detail/get_departments_func",
        async: false,
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        success: function (response) {
            if (!response.isError) {

                $("#depart_id").html("");

                if (response.Message.length == 0) {

                    $("#depart_id").append(
                        `<option value="Not available">No Departments</option>`
                    );
                  
                } else {
                   
                }

                response.Message.forEach((item, index) => {
                    index == 0 &&
                        $("#depart_id").append(
                            `<option value="">Select Section</option>`
                        );
                    $("#depart_id").append(
                        `<option value="${item.id}">${item.name}</option>`
                    );
                });
            } else {
                Swal.fire("Something Wrong!!", response.Message, "error");
            }
        },
        error: function (error) { },
    });
}
});

