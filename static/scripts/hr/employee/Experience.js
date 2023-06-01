$(document).ready(function () {
  getExperienceData();
  let insertType = "Insert";
  let documents = "";
  let updatedocuments = "";

  $("#documents_exp").on("change", function (e) {
    documents = e.target.files[0];
  });

  $("#updatedocuments_emp").on("change", function (e) {
    updatedocuments = e.target.files[0];
  });

  $('#add_Experience').on('click', function () {
    $(".newExperience").modal("show");
    $(".hide_doc").removeClass("d-none");
    $("#name_exp").val('');
    $("#place_exp").val('');
    $("#start_time_exp").val('');
    $("#end_time_exp").val('');
    $("#Experience_ID").val('');
    insertType = "Insert";

  });

  // saving and updating
  $("#exp_save").on("click", function (e) {
    // Prevent the page from loading or refreshing
    e.preventDefault();

    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("employee_id", employee_id);
    formData.append("name_exp", $("#name_exp").val());
    formData.append("place_exp", $("#place_exp").val());
    formData.append("start_time_exp", $("#start_time_exp").val());
    formData.append("end_time_exp", $("#end_time_exp").val());
    formData.append("documents", documents);
    let urls = ""

    if (insertType == "Insert") {
      urls = "/hrm/manage_Experience/new_Experience";
    }
    else {
      urls = "/hrm/manage_Experience/update_Experience";
      formData.append("id", $("#Experience_ID").val());
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
          $(".newExperience").modal("hide");
          getExperienceData()
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
              $("#Employee_form")[0].reset();

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
  $("#Experience_table").on("click", ".edit_experience", function (e) {
    e.preventDefault();
    const ID = $(this).attr("experienceID");
    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("id", ID);

    $.ajax({
      method: "POST",
      url: "/hrm/manage_Experience/getSingleExpirience",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {

          insertType = "Update";
          $(".newExperience").modal("show");
          $("#modaltitle").text("Update Experience");
          $(".hide_doc").addClass("d-none");
          $("#name_exp").val(response.Message.name);
          $("#place_exp").val(response.Message.place);
          $("#start_time_exp").val(response.Message.start);
          $("#end_time_exp").val(response.Message.end);
          $("#Experience_ID").val(response.Message.id);
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
  //Retrieving qualification document
  $("#Experience_table").on("click", ".edit_document", function (e) {
    e.preventDefault();
    const ID = $(this).attr("experienceID");
    $("#ExpdocIDs").val(ID);
    $(".experience_document").modal("show");
  });

  $("#update_document_exp").on("click", function (e) {
    // Prevent the page from loading or refreshing
    e.preventDefault();

    // Create form data
    let formData = new FormData();
    // Read user inputs

    formData.append("id", $("#ExpdocIDs").val());
    formData.append("documents", updatedocuments);
   
    $.ajax({
      method: "POST",
      url: "/hrm/manage_Experience/update_Experience_document",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {
          $(".experience_document").modal("hide");
          getExperienceData()
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
      error: function (response) { },
    });
  });

  // Get all employee qualification data 
  function getExperienceData() {
    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("id", employee_id);
    $.ajax({
      method: "POST",
      url: "/hrm/manage_Experience/getExperienceData",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {
          let table = $("#Experience_table").DataTable().clear().draw();

          for (let index = 0; index < response.Message.length; index++) {
            let temp = [
              response.Message[index].name,
              response.Message[index].place,
              response.Message[index].start,
              response.Message[index].end,




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

              `<a href="#" class="edit_experience" experienceID=${response.Message[index].id} style="color:white;" >
              <button type="button" class="btn btn-sm btn-info rounded">
                  
              <i class="mdi mdi-file-document-edit" ></i>
             
              </button>
              </a>
              </a> <a href="#" class="edit_document" experienceID=${response.Message[index].id} style="color:white;" >
              <button type="button" class="btn btn-sm btn-success rounded">
                  
              <i class="mdi mdi-file-image-plus-outline" ></i>
              </button>
            </a> 

          
        `
            ];
            table.row.add(temp).draw();
          }

        }
        else {
          Swal.fire(
            response.title, response.Message, response.type
          );
        }
      },
      error: function (response) { },
    });
  }
});

