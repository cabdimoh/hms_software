$(document).ready(function () {

  getSectionData()
  let insertType = "Insert";

  $('#Add_Section_button').on('click', function () {
    $(".add_Section_modal").modal("show");


    $("#depart_ID").val('');
    $("#section_name").val('');

    insertType = "Insert";

  });

  // saving and updating
  $("#Save_section").on("click", function (e) {
    // Prevent the page from loading or refreshing
    e.preventDefault();

    // Create form data
    let formData = new FormData();
    // Read user inputs

    formData.append("depart_ID", $("#depart_ID").val());
    formData.append("section_name", $("#section_name").val());




    let urls = ""

    if (insertType == "Insert") {
      urls = "/hrm/prerequirements/New_section";
    }
    else {
      urls = "/hrm/prerequirements/Update_section_data";
      let x = $("#section_detail_ids").val();

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
          $(".add_Section_modal").modal("hide");
          getSectionData()
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
  $("#Section_Table").on("click", ".Section_class_botton", function (e) {
    e.preventDefault();
    const ID = $(this).attr("section_detail_id");
    console.log(ID + "ayan wada")
    // Create form data
    let formData = new FormData();
    // Read user inputs
    formData.append("id", ID);



    $.ajax({
      method: "POST",
      url: "/hrm/prerequirements/get_single_section_Data",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {

          insertType = "Update";
          $(".add_Section_modal").modal("show");          
          $(".modal-title").text("Update " + response.Message.department_sections);
         
          $("#depart_ID").val(response.Message.department);
          $("#section_name").val(response.Message.department_sections);     
          $("#section_detail_ids").val(response.Message.id);




        } else {
          Swal.fire({
            title: response.title,
            text: response.Message,
            icon: response.type,
            confirmButtonClass: "btn btn-success w-xs mt-2",
            buttonsStyling: !1,
            showCloseButton: !0,
          });
        }
      },
      error: function (response) { },
    });

  });



  // Get all employee qualification data 
  function getSectionData() {
    // Create form data
    let formData = new FormData();
    // Read user inputs

    $.ajax({
      method: "POST",
      url: "/hrm/prerequirements/getSectionData",
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (!response.isError) {
          let table = $("#Section_Table").DataTable().clear().draw();

          for (let index = 0; index < response.Message.length; index++) {
            let temp = [

              response.Message[index].id,
              response.Message[index].department,
              response.Message[index].section_name,
           




              `<a href="#" class="Section_class_botton " section_detail_id=${response.Message[index].id}  style="color:white;" >
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

