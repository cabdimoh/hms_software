$(document).ready(function () {

  gethospitaldepartmentdata()
  let insertType = "Insert";

  $('#add_workshift_button_modal').on('click', function () {
    $(".add_workshift_modal").modal("show");

    let id_shifts = $("#work_shift_id").val('');
    // console.log(id_shifts[0]);
    $("#departments_all").val('');
    $("#shift_name").val('');
    $("#shift_name").val('');
    $("#shiftType").val('');
    let days = $('.days').val();
    // console.log(days + 'wada');
    days = days.split(',')
    $('.days .col-4 .form-check input').each(function (index, item) {
      $(item).prop('checked', false)


    });
    days = []

    $(".days", days);
    $("#shift_start_time").val('');
    $("#shift_end_time").val('');
    insertType = "Insert";

  });

  $("#shiftType").on("change", function () {
    if ($("#shiftType").val() != "") {
      if ($("option:selected", "#shiftType").text() == "Fulltime") {
        $('.days .col-4 .form-check input').each(function (index, item) {

          $(item).prop('checked', true)
          if (index == 6) {
            $(".fridayclass").addClass('d-none')
            $(item).prop('checked', false)
          }


        });
      }
      else {
        $('.days .col-4 .form-check input').each(function (index, item) {
          $(item).prop('checked', false)
          if (index == 6) {
            $(".fridayclass").removeClass('d-none')
           
          }
        });

      }
    } else {
      $('.days .col-4 .form-check input').each(function (index, item) {
        $(item).prop('checked', false)
        if (index == 6) {
          $(".fridayclass").removeClass('d-none')
         
        }
      });
    }
  });

  // saving and updating
  $("#save_workshift").on("click", function (e) {
    // Prevent the page from loading or refreshing
    e.preventDefault();

    // Create form data
    let formData = new FormData();
    let shift_days = []

    $('.days .col-4 .form-check input:checked').each(function (item, index) {
      shift_days.push($(this).attr('id'));
    });

    // Read user inputs

    formData.append("departments", $("#departments_all").val());
    formData.append("shift_name", $("#shift_name").val());
    formData.append("shiftType", $("#shiftType").val());
    formData.append("shift_day", shift_days);
    formData.append("shift_start_time", $("#shift_start_time").val());
    formData.append("shift_end_time", $("#shift_end_time").val());



    let urls = ""

    if (insertType == "Insert") {
      urls = "/hrm/prerequirements/new_workshift";
    }
    else {
      urls = "/hrm/prerequirements/update_workshift";
      let x = $("#work_shift_id").val();
      formData.append("id", x);










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
          $(".add_workshift_modal").modal("hide");
          gethospitaldepartmentdata();
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
              // $("#job_t")[0].reset();

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

  //Retrieving single data and display modal
  $("#work_shift_table").on("click", ".work_shift_botton", function (e) {
    e.preventDefault();
    const ID = $(this).attr("work_shift_id");
    // console.log(ID + "ayan wada")
    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("id", ID);
    $.ajax({
      method: "POST",
      url: "/hrm/prerequirements/get_workshift_single_Data",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {

          insertType = "Update";

          $(".add_workshift_modal").modal("show");
          $(".modal-title").text("Update work shift");

          $("#work_shift_id").val(response.Message.id);
          $("#departments_all").val(response.Message.departments);
          $("#shift_name").val(response.Message.shift_name);
          $(".days").val(response.Message.shift_days);

          let days = $(".days").val()
          days = days.split(',')
          $('.days .col-4 .form-check input').each(function (index, item) {

            if (days.includes($(item).attr('id'))) {
              $(item).prop('checked', true)
            }
            else {
              
              $(item).prop('checked', false)

            }

          });

          $("#shiftType").val(response.Message.shifttype);
          $("#shift_start_time").val(response.Message.shift_start_time);
          $("#shift_end_time").val(response.Message.shift_end_time);





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



  // Get all employee qualification data 
  function gethospitaldepartmentdata() {
    // Create form data
    let formData = new FormData();
    // Read user inputs

    $.ajax({
      method: "POST",
      url: "/hrm/prerequirements/getworkshifttData",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {          
          let table = $("#work_shift_table").DataTable().clear().draw();

          for (let index = 0; index < response.Message.length; index++) {

            let temp = [
            
              response.Message[index].id,
              response.Message[index].departments,
              response.Message[index].shift_name,
              response.Message[index].shift_type,
              response.Message[index].shift_days,
              response.Message[index].shift_start_day,
              response.Message[index].shift_end_day,
              
              `<a href="#" class="work_shift_botton" work_shift_id=${response.Message[index].id}  style="color:white;" >
                <button type="button" class="btn  btn-soft-info  rounded" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-title="Tooltip on top">
                  <i class="mdi mdi-file-document-edit" ></i>
                  </button>
                  </a>

                  <a href="${response.Message[index].url}"  style="color:white;" >
                  <button type="button" class="btn btn-soft-danger  rounded" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-title="Tooltip on top">
                    <i class="mdi mdi-account-multiple-plus-outline" ></i>
                    </button>
                    </a>
              
            `,
            
            
            ];
            table.row.add(temp).draw();
          }

        }
      },
      error: function (response) { },
    });

    
  }
});

