$(document).ready(function () {

    let insertType = "Insert";
  
    $('#create_income_source').on('click', function () {
      $(".IncomeSource").modal("show");
  
  
      $("#name").val('');
     
      insertType = "Insert";
  
    });
  
    // saving and updating
    $("#save_income_source").on("click", function (e) {
      // Prevent the page from loading or refreshing
      e.preventDefault();
  
      // Create form data
      let formData = new FormData();
      // Read user inputs
  
      formData.append("name", $("#name").val());

  
  
  
      let urls = ""
  
      if (insertType == "Insert") {
        urls = "/finance/manage-income-source/new_income_source";
      }
      else {
        urls = "/finance/manage-income-source/update_income_source";
        let x = $("#incomeidHidden").val();  
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
            $(".IncomeSource").modal("hide");   

            Swal.fire({
              title: response.title,
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
  
    //Retrieving single data and display modal
    $("#income_source_table").on("click", "#incomesourceid", function (e) {
      e.preventDefault();
      const ID = $(this).attr("incomesourceids");
      console.log(ID + "ayan wada")
      // Create form data
      let formData = new FormData();
      // Read user inputs
      formData.append("id", ID);
  
  
  
      $.ajax({
        method: "POST",
        url: "/finance/manage-income-source/get_income_source_data",
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        async: false,
        success: function (response) {
          if (!response.isError) {
  
            insertType = "Update";
            $(".IncomeSource").modal("show");
            $(".modal-title").text("Update " + response.Message.name);
            $("#name").val(response.Message.name);           
            $("#incomeidHidden").val(response.Message.id);
  
  
  
  
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
  


  });
  
  