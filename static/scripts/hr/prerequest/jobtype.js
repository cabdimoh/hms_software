$(document).ready(function () {
  GetAllJobType()
  let insertType = "Insert";
  $('#add_Jobtype').on('click', function () {
    $(".add_job_type_modal").modal("show");
    $("#job_type_name").val('');
    $("#descriptions").val('');
    $('#relateAppoint').val('')
    insertType = "Insert";
  });

  // saving and updating
  $("#save_job_type").on("click", function (e) {
    // Prevent the page from loading or refreshing
    e.preventDefault();

    // Create form data
    let formData = new FormData();
    // Read user inputs

    formData.append("job_type_name", $("#job_type_name").val());
    formData.append("descriptions", $("#descriptions").val());
    formData.append("relateAppoint", $("#relateAppoint").val());



    let urls = ""

    if (insertType == "Insert") {
      urls = "/hrm/prerequirements/new_jobtype";
    }
    else {
      urls = "/hrm/prerequirements/update_job_types";
      let x = $("#job_type_id").val();
     
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
         
          
          $(".add_job_type_modal").modal("hide");
          GetAllJobType();
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
              $("#job_t")[0].reset();

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
  $("#Jobtype_table").on("click", ".jobtype_bottn", function (e) {
    e.preventDefault();
    const ID = $(this).attr("job_type_id");
    console.log(ID + "ayan wada")
    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("id", ID);



    $.ajax({
      method: "POST",
      url: "/hrm/prerequirements/get_job_single_Data",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {

          insertType = "Update";
          $(".add_job_type_modal").modal("show");
          $(".modal-title").text("Update job type");
          $("#job_type_name").val(response.Message.name);
          $("#descriptions").val(response.Message.discription);
          $("#job_type_id").val(response.Message.id);
          $("#relateAppoint").val(response.Message.is_related);

          $('.relateAppointClass input').each(function (index, item) {
            
           

            if ($("#relateAppoint").val() == "relate_appointment") {
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



  // Get all employee qualification data 
  function GetAllJobType() {
    // Create form data
    let formData = new FormData();
    // Read user inputs

    $.ajax({
      method: "POST",
      url: "/hrm/prerequirements/getjobtypeData",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {
          let table = $("#Jobtype_table").DataTable().clear().draw();

          for (let index = 0; index < response.Message.length; index++) {
            let temp = [

              response.Message[index].id,
              response.Message[index].name,
              response.Message[index].discription,




              `<a href="#" class="jobtype_bottn" job_type_id=${response.Message[index].id}  style="color:white;" >
                 <button type="button" class="btn btn-sm btn-info rounded">
                  
                 <i class="mdi mdi-file-document-edit" ></i>
                 
                  </button>
                  </a>
    
              
            `
            ];
            table.row.add(temp).draw();
          }

        }
      },
      error: function (response) { },
    });
  }
 
  

$('#relateAppoint').on('click', function(){
  if ($("#relateAppoint").is(":checked")) {
    Swal.fire({
      title: "by checking this checkbox you sure:",
      text: "this job relate with Appointment and patient can make appoitment behalf of this job",
      icon: "warning",
      showCancelButton: !0,
      confirmButtonColor: "#2ab57d",
      cancelButtonColor: "#fd625e",
      confirmButtonText: "Yes, ",
    }).then(function (e) {
     

      if(e.isDismissed == true && e.isConfirmed == false && e.isDenied == false){
        $('.relateAppointClass input').each(function(index, item){
          $(item).prop('checked', false)
         
          
        })
      }
      else{
        $('#relateAppoint').val('relate_appointment')
      
      }



      
    });
  
  

  } else {
    // $("#relateAppoint").val('non-spaciality')
  }

})
  

});

