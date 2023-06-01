$(document).ready(function () {

    let insertType = "Insert";
    $('#newShift').on('click', function () {
      $(".Assigning_Employee_show").modal("show");
      $("#search").val('');
      $("#userIDs").val('');
      $("#getDepartment").val('');
      $("#getshiftName").val('');
      insertType = "Insert";
    console.log($('#departments_id').val(), 'ayan wada');
  
    });
  
    // saving and updating
    $("#save_workshift").on("click", function (e) {
      // Prevent the page from loading or refreshing
      e.preventDefault();
      
      // Create form data
      let formData = new FormData();
      // Read user inputs
      // formData.append("employee_id", employee_id);
      formData.append("search", $("#search").val());        
      formData.append("description", $("#description").val());        
      formData.append("job_detail_id", $("#job_detail_id").val());   
      formData.append("getshiftNames", $("#getshiftNames").val());   

  
      let urls = ""
  
      if (insertType == "Insert") {
        urls = "/hrm/manages_shifts/new_assigning_shift";
      }
      else {
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
        success: function (response) {
          if (!response.isError) {
            $(".Assigning_Employee_show").modal("hide");          
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
                window.location.reload(urls);
  
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
  

    $("#search").on("input", function (e) {
  
      var listUsers = [];
      if ($(this).val() != "" && $(this).val().length > 0) {
        listUsers = SearchEngine($(this).val());
  
        $("#search").autocomplete({
          source: listUsers,
          select: function (event, ui) {
            const item = ui.item.userid;
            const value = ui.item.value;
  
            if (value != "") {
              $("#search").attr("userid", item);
              getDepartments($("#search").attr("userid"));    
              getShift($("#departments_id").val());                    
              
            }
          },
          response: function (event, ui) {
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
        url: "/hrm/search_employee/",
        processData: false,
        contentType: false,
        data: formData,
        headers: { "X-CSRFToken": csrftoken },
        async: false,
  
        success: function (data) {
          data.Message.forEach((user) => {
            list.push(user);
          });
        },
      });
  
      return list;
    }
  
    function getDepartments(ID) {
  
      let formData = new FormData();
  
      formData.append("employee_id", ID);
     
      $.ajax({
        method: "POST",
        url: "/hrm/manages_shifts/get_employee_department",
        processData: false,
        contentType: false,
        data: formData,
        headers: { "X-CSRFToken": csrftoken },
        async: false,
        success: function (response) {
          if (!response.isError) {
            $("#departments_id").val(response.Message[0].id);
            $("#getDepartment").val(response.Message[0].name);
            $("#job_detail_id").val(response.Message[0].Jobid);
          
           
       
          } else {
          }
          response.Message;
        },
        error: function (response) { },
      });
    }
    



    
function getShift(department_id) {
  let formData = new FormData();
 
  formData.append("depart_id", department_id);
  $.ajax({
      method: "POST",
      url: "/hrm/manages_shifts/get_department_shift",
      async: false,
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      success: function (response) {
          if (!response.isError) {

              $("#getshiftNames").html("");

              if (response.Message.length == 0) {

                  $("#getshiftNames").append(
                      `<option value="Not available">No Departments</option>`
                  );
                
              } else {
                 
              }

              response.Message.forEach((item, index) => {
                  index == 0 &&
                      $("#getshiftNames").append(
                          `<option value="">Select Department</option>`
                      );
                  $("#getshiftNames").append(
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

$("#save_days").on("click", function (e) {
  // Prevent the page from loading or refreshing
  e.preventDefault();

  // Create form data
  let formData = new FormData();
  let shift_days = []

  $('.days .col-4 .form-check input:checked').each(function (item, index) {
    shift_days.push($(this).attr('id'));
  });

  // Read user inputs
  formData.append("shift_day", shift_days);
    let x = $("#IDshift").val();
    console.log('kani shift id' ,x);
    formData.append("id", x);
  
  $.ajax({
    method: "POST",
    url: "/hrm/manages_shifts/update_days",
    headers: { "X-CSRFToken": csrftoken },
    processData: false,
    contentType: false,
    data: formData,
    async: false,
    success: function (response) {
      if (!response.isError) {
        $('.EditDays_modal').modal('hide')
        Swal.fire({
          title: "Successfully",
          text: response.Message,
          icon: "success",
          confirmButtonClass: "btn btn-primary w-xs mt-2",
          buttonsStyling: !1,
          showCloseButton: !0,
        }).then((e) => {
          if (e.value) {
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
    error: function (response) { },
  });
});

$('#Shift_management_table').on('click', '#Editdays_btn', function(e){
  $('.EditDays_modal').modal('show')

    const ID = $(this).attr("shifID");
    // console.log(ID + "ayan wada")
    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("id", ID);
    $.ajax({
      method: "POST",
      url: "/hrm/manages_shifts/get_schedule_days",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {
            console.log();
          $(".days").val(response.Message[0].days);
          $("#IDshift").val(response.Message[0].id);

          let days = $(".days").val()
          console.log(days, 'ayan wada');
          days = days.split(',')
          $('.days .col-4 .form-check input').each(function (index, item) {

            if (days.includes($(item).attr('id'))) {
              $(item).prop('checked', true)
            }
            else {
              
              $(item).prop('checked', false)

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



  });
  
  