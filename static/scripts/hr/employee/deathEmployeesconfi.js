$(document).ready(function () {

  $('#exit_employee_table').on('click', "#Confirmed", function() {
    const ID = $(this).attr('exitID')      
            handleEmployeeApprovel( "Confirmed",  ID );
    });
  
  $('#exit_employee_table').on('click', "#Returned", function() {
    const ID = $(this).attr('exitID')
    handleEmployeeApprovel( "Returned",  ID );
    });

$('#exit_employee_table').on('click', "#Rejected", function() {
    const ID = $(this).attr('exitID')
    handleEmployeeApprovel( "Rejected",  ID );
});

  // Finction to handle job approval
  function handleEmployeeApprovel(status, ID) {
    // Prepare the form data
    let formData = new FormData();
    // Append data to form data

    formData.append("status", status);
    formData.append("ID", ID);
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
          url: "/hrm/exit_employee_all/approve_reject_exit",
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
            //(error);
          },
        
        });
     
      }
    
    }   
    )
  }



  $("#exit_employee_table").on("click", "#pendingjobView", function () {
    $(".add_view_Employee_modal").modal("show");   
    $(".CreatedClass").removeClass('d-none');
    $("#save_exit_employe").addClass('d-none');
    $('.fileClass').addClass('d-none')
    $('.ApprovedClass').removeClass('d-none')
    
    const ID = $(this).attr('jobdetailID')      
    GetAllJobDetail(ID)
  });

  


  function GetAllJobDetail(id) {

    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("id", id);

    $.ajax({
      method: "POST",
      url: "/hrm/exit_employee_all/get_exit_detail",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {
          $('#dsearch').val(response.Message[0].employe_name)
          $('#dexit_cotegory_id').val(response.Message[0].category)
          $('#dexit_reason').val(response.Message[0].reason)
          $('#ddate_death').val(response.Message[0].dayhappen)
          $('#dtime_death').val(response.Message[0].timeHappen)
          $('#dApprovedBy').val(response.Message[0].approvedWho)
          $('#dExistState').val(response.Message[0].exitstate)
          $('#dCreated').val(response.Message[0].Created)
        }


      },
      error: function (response) { },
    });
  }


});

