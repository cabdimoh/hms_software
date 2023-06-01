$(document).ready(function () {

  GetJobtitleDatas()
  let insertType = "Insert";

  $('#add_Secretary').on('click', function () {
    $(".newSecretary").modal("show");
    $("#director_name").val('');
    $("#secretary_name").val('');
    $("#descriptions_director ").val('');
    insertType = "Insert";

  });

  // saving and updating
  $("#save_secretary").on("click", function (e) {
    // Prevent the page from loading or refreshing
    e.preventDefault();

    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("director_name", $("#director_name").val());
    formData.append("secretary_name", $("#secretary_name").val());
    formData.append("descriptions_director", $("#descriptions_director").val());



    let urls = ""

    if (insertType == "Insert") {
      urls = "/hrm/prerequirements/new_secretory";
    }
    else {
      urls = "/hrm/prerequirements/update_secretary";
      let x = $("#SecretoryIDS").val();
     
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
          $(".newSecretary").modal("hide");
          GetJobtitleDatas();
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
  $("#Secretary_table").on("click", ".secretary_botton_class", function (e) {
    e.preventDefault();
    const ID = $(this).attr("secretaryID");
    console.log(ID + "ayan wada")
    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("id", ID);



    $.ajax({
      method: "POST",
      url: "/hrm/prerequirements/get_secretary_data",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {

          insertType = "Update";
          $(".newSecretary").modal("show");
          $(".modal-title").text("Update Secretary ");
          $("#director_name").val(response.Message.director);
          $("#secretary_name").val(response.Message.secretory);
          $("#descriptions_director").val(response.Message.discription);
          $("#SecretoryIDS").val(response.Message.id);

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
  function GetJobtitleDatas() {
    // Create form data
    let formData = new FormData();
    // Read user inputs

    $.ajax({
      method: "POST",
      url: "/hrm/prerequirements/getSecretaryData",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {
          let table = $("#Secretary_table").DataTable().clear().draw();

          for (let index = 0; index < response.Message.length; index++) {
            let temp = [

              response.Message[index].id,
              response.Message[index].director,
              response.Message[index].secretary,
              response.Message[index].discription,




              `<a href="#" class="secretary_botton_class" secretaryID=${response.Message[index].id}  style="color:white;" >
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

