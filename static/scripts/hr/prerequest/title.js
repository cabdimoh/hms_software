$(document).ready(function () {

  GetAllJobType()
  let insertType = "Insert";
  $('#add_title').on('click', function () {
    $(".Title_modal").modal("show");
    $("#title_names").val('');
    $("#title_dis").val('');    
    insertType = "Insert";
  });

  // saving and updating
  $("#save_title").on("click", function (e) {
    // Prevent the page from loading or refreshing
    e.preventDefault();

    // Create form data
    let formData = new FormData();
    // Read user inputs

    formData.append("title_names", $("#title_names").val());
    formData.append("title_dis", $("#title_dis").val());




    let urls = ""

    if (insertType == "Insert") {
      urls = "/hrm/prerequirements/new_title";
    }
    else {
      urls = "/hrm/prerequirements/update_title";
      let x = $("#job_title_id").val();
     
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
                window.location.reload(urls)

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
  $("#Title_table").on("click", ".title_botton_class", function (e) {
    e.preventDefault();
    const ID = $(this).attr("job_title_id");
    console.log(ID + "ayan wada")
    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("id", ID);



    $.ajax({
      method: "POST",
      url: "/hrm/prerequirements/get_single_title",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {

          insertType = "Update";
          $(".Title_modal").modal("show");
          $(".modal-title").text("Update job type");
          $("#title_names").val(response.Message.name);
          $("#title_dis").val(response.Message.discription);
          $("#job_title_id").val(response.Message.id);
 






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
      url: "/hrm/prerequirements/get_all_titles",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {
          let table = $("#Title_table").DataTable().clear().draw();

          for (let index = 0; index < response.Message.length; index++) {
            let temp = [

              response.Message[index].id,
              response.Message[index].name,
              response.Message[index].discription,




              `<a href="#" class="title_botton_class" job_title_id=${response.Message[index].id}  style="color:white;" >
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
 
  

  

});

