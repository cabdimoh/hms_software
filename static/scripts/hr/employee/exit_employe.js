$(document).ready(function() {

    let insertType = "Insert";
    let documents = "";
    let updatedocuments = "";

    $("#exit_Documents").on("change", function(e) {
        documents = e.target.files[0];
    });


    $("#exit_cotegory_id").on("change", function() {
        if ($("#exit_cotegory_id").val() != "") {
            $(".Classify-exit").addClass("d-none");
            if ($("option:selected", "#exit_cotegory_id").text() == "Death") {
                $(".Classify-exit").removeClass("d-none");
                $(".death").removeClass("d-none");
            } else {
                $(".Classify-exit").removeClass("d-none");
                $(".death").addClass("d-none");
            }
        } else {
            $(".Classify-exit").addClass("d-none");
            $(".death").addClass("d-none");
        }
    });

    // $("#updatedocuments").on("change", function (e) {
    //   updatedocuments = e.target.files[0];
    // });

    $('#New_Exit_employee_id').on('click', function() {
        $(".add_exit_Employee_modal").modal("show");
        $("#exited_employee_id").val('');
        $("#exit_reason").val('');
        $("#search").val('');
        $("#save_exit_employe").removeClass('d-none');
        $("#exit_cotegory_id").val('');
        $("#exit_Documents").val('');
        $(".CreatedClass").addClass('d-none');
        $('.modal-title').removeClass('d-none')
        $('.fileClass').removeClass('col-lg-6')
        $('.fileClass').addClass('col-lg-12')
        $('.fileClass').removeClass('d-none')
        $('.ApprovedClass').addClass('d-none')
        insertType = "Insert";

    });

    // saving and updating
    $("#save_exit_employe").on("click", function(e) {
        // Prevent the page from loading or refreshing
        e.preventDefault();

        // Create form data
        let formData = new FormData();
        // Read user inputs
        // formData.append("employee_id", employee_id);
        formData.append("exited_employee_id", $("#exited_employee_id").val());
        formData.append("exit_cotegory_id", $("#exit_cotegory_id").val());
        formData.append("exit_reason", $("#exit_reason").val());
        formData.append("date_death", $("#date_death").val());
        formData.append("time_death", $("#time_death").val());
        formData.append("userIDs", $("#userIDs").val());
        formData.append("documents", documents);

        let urls = ""

        if (insertType == "Insert") {
            urls = "/hrm/exit_employee_all/new_exit_employee";
        } else {
            urls = "/hrm/manage_qualification/update_qualification";
            formData.append("id", $("#qualifcationIDs").val());
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
                    $(".AddQualification").modal("hide");
                    getexitemployeedata()
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



    // Get all employee qualification data 
    function getexitemployeedata() {
        // Create form data
        let formData = new FormData();
        // Read user inputs
        // formData.append("id", employee_id);
        $.ajax({
            method: "POST",
            url: "/hrm/manage_qualification/getAllData",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {
                    let table = $("#qualification_table").DataTable().clear().draw();

                    for (let index = 0; index < response.Message.length; index++) {
                        let temp = [
                            response.Message[index].name,
                            response.Message[index].specialization,


                            `
              <table class="table align-middle table-nowrap table-borderless">
                <tbody>
                    <tr>
                        <td style="width: 50px;">
                            <div class="font-size-22 text-${response.Message[index].document.color}">
                                <i class="bx bx-down-arrow-${response.Message[index].document.icon} d-block"></i>
                            </div>
                        </td>

                        <td>
                            <div>
                              <a  target="_blank" href='${response.Message[index].document.url}'>${response.Message[index].document.name} ${response.Message[index].document.extension}</a>
                                <p class="text-muted mb-0 font-size-12">${response.Message[index].document.size}</p>
                            </div>
                        </td>   
                </tr>
                </tbody>
                </table>
              `,

                            `<a href="#" class="edit_qualification" qualification_id=${response.Message[index].id} style="color:white;" >
              <button type="button" class=" btn-primary rounded">
              
                  <i class="las la-pen"></i>
             
              </button>
              </a>
              </a> <a href="#" class="edit_document" qualification_id=${response.Message[index].id} style="color:white;" >
              <button type="button" class=" btn-danger rounded">
              
                  <i class="las la-file-alt"></i>
            
              </button>
            </a> 

          
        `
                        ];
                        table.row.add(temp).draw();
                    }

                }
            },
            error: function(response) {},
        });
    }


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