$(document).ready(function () {
  GetAllQualification();
  let insertType = "Insert";
  let documents = "";
  let updatedocuments = "";
  $("#documents").on("change", function (e) {
    documents = e.target.files[0];
  });

  $("#updatedocuments").on("change", function (e) {
    updatedocuments = e.target.files[0];
  });

  $('#add_qualification').on('click', function () {
    $(".AddQualification").modal("show");
    $(".hide_doc").removeClass("d-none");
    $("#specialization").val('');
    $("#qualifcationIDs").val('');
    $("#name").val('');
    insertType = "Insert";

  });

  // saving and updating
  $("#quali_save").on("click", function (e) {
    // Prevent the page from loading or refreshing
    e.preventDefault();

    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("employee_id", employee_id);
    formData.append("name", $("#name").val());
    formData.append("specialization", $("#specialization").val());
    formData.append("documents", documents);
    let urls = ""

    if (insertType == "Insert") {
      urls = "/hrm/manage_qualification/new_qualification";
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
          $(".AddQualification").modal("hide");
          GetAllQualification()
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
  $("#qualification_table").on("click", ".edit_qualification", function (e) {
    e.preventDefault();
    const ID = $(this).attr("qualification_id");
    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("id", ID);

    $.ajax({
      method: "POST",
      url: "/hrm/manage_qualification/getData",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {

          insertType = "Update";
          $(".AddQualification").modal("show");
          $("#modaltitle").text("Update Qualification");
          $(".hide_doc").addClass("d-none");
          $("#name").val(response.Message.name);

          $("#specialization").val(response.Message.specialization);
          $("#qualifcationIDs").val(response.Message.id);
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
  $("#qualification_table").on("click", ".edit_document", function (e) {
    e.preventDefault();
    const ID = $(this).attr("qualification_id");
    $("#docIDs").val(ID);
    $(".updateDocoment").modal("show");
  });

  $("#update_document").on("click", function (e) {
    // Prevent the page from loading or refreshing
    e.preventDefault();

    // Create form data
    let formData = new FormData();
    // Read user inputs

    formData.append("id", $("#docIDs").val());
    formData.append("documents", updatedocuments);
    let urls = ""
    $.ajax({
      method: "POST",
      url: "/hrm/manage_qualification/update_qualification_document",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {
          $(".updateDocoment").modal("hide");
          GetAllQualification()
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

  // Get all employee qualification data 
  function GetAllQualification() {
    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("id", employee_id);
    $.ajax({
      method: "POST",
      url: "/hrm/manage_qualification/getAllData",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
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
              <button type="button" class="btn btn-sm btn-info rounded">
                  
              <i class="mdi mdi-file-document-edit" ></i>
              </button>
              </a>
              </a> <a href="#" class="edit_document" qualification_id=${response.Message[index].id} style="color:white;" >
              <button type="button" class="btn btn-sm btn-success rounded">
                  
              <i class="mdi mdi-file-image-plus-outline" ></i>
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

