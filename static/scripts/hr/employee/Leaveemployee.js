$(document).ready(function() {

    let insertType = "Insert";
    let documents = "";
    let updatedocuments = "";

    $("#exit_Documents").on("change", function(e) {
        documents = e.target.files[0];
    });


    $('#leave_employee_btn').on('click', function() {
        $(".Leave_emp_modal").modal("show");
        $("#exited_employee_id").val('');
        $("#exit_reason").val('');
        $("#search").val('');
        $("#date_ended").val('');
        $("#date_started").val('');
        $("#exit_cotegory_id").val('');
        $("#exit_Documents").val('');
        $("#save_leave_employe").removeClass('d-none');
        $('.fileClass').removeClass('d-none')
        $('.CreatedClass').addClass('d-none')
        $('.UpdatedClass').addClass('d-none')
        $('.updsentDaty').addClass('d-none')
        $('#save_print_employe').addClass('d-none')
       
        insertType = "Insert";

    });

    // saving and updating
    $("#save_leave_employe").on("click", function(e) {
        // Prevent the page from loading or refreshing
        e.preventDefault();

        // Create form data
        let formData = new FormData();
        // Read user inputs
        // formData.append("employee_id", employee_id);
        if(insertType == 'update'){
            formData.append("exited_employee_id", $('#userIDs').val());
            formData.append("exit_cotegory_id", $("#exit_cotegory_id").val());
            formData.append("exit_reason", $("#exit_reason").val());
            formData.append("date_started", $("#date_started").val());
            formData.append("date_ended", $("#date_ended").val());
            formData.append("userIDs", $("#userIDs").val());
            formData.append("documents", documents);
        }
        else{            
            formData.append("exited_employee_id", $("#exited_employee_id").val());
            formData.append("exit_cotegory_id", $("#exit_cotegory_id").val());
            formData.append("exit_reason", $("#exit_reason").val());
            formData.append("date_started", $("#date_started").val());
            formData.append("date_ended", $("#date_ended").val());
            formData.append("userIDs", $("#userIDs").val());
            formData.append("documents", documents);
        }


        let urls = ""

        if (insertType == "Insert") {
            urls = "/hrm/leave_employee_all/new_leave_employee";
        } else {
            urls = "/hrm/leave_employee_all/update_leave_employee";
            formData.append("id", $("#IDleave").val());
          
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
                    $(".Leave_emp_modal").modal("hide");                
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
            error: function(response) {},
        });
    });

    //Retrieving single data and display modal






    $('#exit_employee_table').on('click', '#confirmExit', function() {


        let confirm = 'approved'
        let formData = new FormData();
        const ID = $(this).attr("employeeid");
        const cotegoryID = $(this).attr("exitcotegroID");
        console.log(ID + "ayan wada libax");
        console.log(cotegoryID + "ayan wada libax");

        formData.append('confirm', confirm)
        formData.append('employeeID', ID)
        formData.append('cotegroryID', cotegoryID)



        Swal.fire({
            title: "Are you sure ?",
            text: "This Employee Will Blocked ",
            icon: "warning",
            showCancelButton: !0,
            confirmButtonColor: "#2ab57d",
            cancelButtonColor: "#fd625e",
            confirmButtonText: "Yes, ",
        }).then(function(e) {
            if (e.value) {
                $.ajax({
                    method: "POST",
                    url: "/hrm/exit_employee_all/confirm_employe_removal",
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
                                    window.location.reload()

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
                    error: function(response) { error },
                });

            }
        });



    })


    $("#search").on("input", function(e) {

        var listUsers = [];
        if ($(this).val() != "" && $(this).val().length > 0) {
            listUsers = SearchEngine($(this).val());

            $("#search").autocomplete({
                source: listUsers,
                select: function(event, ui) {
                    const item = ui.item.userid;
                    const value = ui.item.value;

                    if (value != "") {
                        $("#search").attr("userid", item);
                        getEmployee($("#search").attr("userid"));
                    }
                },
                response: function(event, ui) {
                    if (!ui.content.length) {
                        var noResult = { value: "", label: "No result found" };
                        ui.content.push(noResult);
                    }
                },
                minLength: 1,
            });
        }
    });

    function SearchEngine(letter) {
        let formData = new FormData();
        formData.append("employee", letter);
        var list = [];
        $.ajax({
            method: "POST",
            url: "/hrm/search_engine/",
            processData: false,
            contentType: false,
            data: formData,
            headers: { "X-CSRFToken": csrftoken },
            async: false,

            success: function(data) {
                data.Message.forEach((user) => {
                    list.push(user);
                });
            },
        });

        return list;
    }

    function getEmployee(ID) {

        let formData = new FormData();

        formData.append("employee_id", ID);

        $.ajax({
            method: "POST",
            url: "/hrm/exit_employee_all/get_employee_name",
            processData: false,
            contentType: false,
            data: formData,
            headers: { "X-CSRFToken": csrftoken },
            async: false,
            success: function(response) {
                if (!response.isError) {
                    $("#userIDs").val(response.Message[0].id);



                } else {}
                response.Message;
            },
            error: function(response) {},
        });
    }








$('#leave_employee_table').on('click', "#Confirmed", function() {
    const ID = $(this).attr('exitID')      
            handleEmployeeApprovel( "Confirmed",  ID );
    });
  
  $('#leave_employee_table').on('click', "#Returned", function() {
    const ID = $(this).attr('exitID')
    handleEmployeeApprovel( "Returned",  ID );
    });

$('#leave_employee_table').on('click', "#Rejected", function() {
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
          url: "/hrm/leave_employee_all/approve_reject_exit",
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



  $("#leave_employee_table").on("click", "#viewLeavs", function () {
    $(".view_Leave_emp_modal").modal("show");
    $('.modal-title').addClass('d-none')
    $(".CreatedClass").removeClass('d-none');
    $("#save_leave_employe").addClass('d-none');
    $('.fileClass').addClass('d-none')
    $('.CreatedClass').removeClass('d-none')
    $('.UpdatedClass').removeClass('d-none')
    $('#save_print_employe').removeClass('d-none')
    $('.updsentDaty').removeClass('d-none')
    $('.ApprovedClass').removeClass('d-none')
    
    const ID = $(this).attr('jobdetailID')      
    GetAllJobDetailscond(ID)
  });


  $("#leave_employee_table").on("click", "#LeaveEdit", function () {
    $(".Leave_emp_modal").modal("show");
    $(".CreatedClass").removeClass('d-none');
    $("#save_leave_employe").removeClass('d-none');
    $('.fileClass').removeClass('d-none')
    $('.CreatedClass').addClass('d-none')
    $('.UpdatedClass').addClass('d-none')
    $('.updsentDaty').addClass('d-none')
    $('#save_print_employe').addClass('d-none')
    $('.ApprovedClass').removeClass('d-none')
    $("#exit_Documents").val('')
    
    const ID = $(this).attr('LeaveID')      
    GetAllJobDetail(ID)
  });


  function GetAllJobDetail(id) {

    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("id", id);

    $.ajax({
      method: "POST",
      url: "/hrm/leave_employee_all/get_leave_detail",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {
            insertType = 'update'
          $('#search').val(response.Message[0].employe_name)
          $('#exit_cotegory_id').val(response.Message[0].category)
          $('#exit_reason').val(response.Message[0].reason)
          $('#date_started').val(response.Message[0].start)
          $('#date_ended').val(response.Message[0].end)
          $('#approvedby').val(response.Message[0].approvedWho)
          $('#created').val(response.Message[0].Created)
          $('#updated').val(response.Message[0].update)
          $('#leave_days').val(response.Message[0].leaveday)
          $('#IDleave').val(response.Message[0].id),
          $('#userIDs').val(response.Message[0].empIDss)
        
        }


      },
      error: function (response) { },
    });
  }



  function GetAllJobDetailscond(id) {

    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("id", id);

    $.ajax({
      method: "POST",
      url: "/hrm/leave_employee_all/get_leave_detail",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {
            insertType = 'update'
          $('#dsearch').val(response.Message[0].employe_name)
          $('#dexit_cotegory_id').val(response.Message[0].category)
          $('#dexit_reason').val(response.Message[0].reason)
          $('#ddate_started').val(response.Message[0].start)
          $('#ddate_ended').val(response.Message[0].end)
          $('#dapprovedby').val(response.Message[0].approvedWho)
          $('#dcreated').val(response.Message[0].Created)
          $('#dupdated').val(response.Message[0].update)
          $('#dleave_days').val(response.Message[0].leaveday)
          $('#dIDleave').val(response.Message[0].id),
          $('#duserIDs').val(response.Message[0].empIDss)
        
        }


      },
      error: function (response) { },
    });
  }


});