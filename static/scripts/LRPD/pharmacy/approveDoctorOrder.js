$(document).ready(function() {
    $("#approvebutton").on("click", function (e) {
      
        e.preventDefault();
    
        // Create form data
        let formData = new FormData();
        
        // Read user inputs
        formData.append("OrderId", $("#OrderId").val());
        
    
        $.ajax({
          method: "POST",
          url: "/prescription/manage-doctor-order/get_approvers",
          headers: { "X-CSRFToken": csrftoken },
          processData: false,
          contentType: false,
          data: formData,
          async: false,
          success: function (response) {
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
                  $("#AddResultForm")[0].reset();
                  window.location.reload()
                }
              });
            } else {
              Swal.fire({
                title: response.title,
                text: response.Message,
                icon: response.type,
                confirmButtonClass: "btn btn-danger w-xs mt-2",
                buttonsStyling: !1,
                showCloseButton: !0,
              });
            }
          },
          error: function (response) { },
        });
    
      
      });
    // insertType = "Insert";
    // $("#SubmitLabTest").on("click", function(e) {
    //     // Prevent the page from loading or refreshing
    //     e.preventDefault();
    //     // Create form data
    //     let formData = new FormData();

    //     // Read user 
    //     formData.append("TestName", $("#TestName").val());
    //     formData.append("TestUnit", $("#TestUnit").val());
    //     formData.append("TestDescription", $("#TestDescription").val());
    //     formData.append("NormalRange", $("#NormalRange").val());
    //     let urls = "";
    //     if (insertType == "Insert") {
    //         urls = "/prescription/manage-labresult/add_labOrder_info";
    //     } else {
    //         formData.append("TestID", $("#TestID").val());
    //         urls = "/prescription/manage-labresult/get_labOrder_info";
    //     }
    //     $.ajax({
    //         method: "POST",
    //         url: urls,
    //         headers: { "X-CSRFToken": csrftoken },
    //         processData: false,
    //         contentType: false,
    //         data: formData,
    //         async: false,
    //         success: function(response) {
    //             if (!response.isError) {
    //                 Swal.fire({
    //                     title: "Successfully",
    //                     text: response.Message,
    //                     icon: "success",
    //                     confirmButtonClass: "btn btn-primary w-xs mt-2",
    //                     buttonsStyling: !1,
    //                     showCloseButton: !0,
    //                 }).then((e) => {
    //                     if (e.value) {
    //                         // hide the modal and resret the form
    //                         $("#TestForm")[0].reset();
    //                         window.location.reload();
    //                         // $(".CategoryModal").modal("hide");


    //                     }
    //                 });
    //             } else {
    //                 Swal.fire({
    //                     title: response.title,
    //                     text: response.Message,
    //                     icon: response.type,
    //                     confirmButtonClass: "btn btn-primary w-xs mt-2",
    //                     buttonsStyling: !1,
    //                     showCloseButton: !0,
    //                 });
    //             }
    //         },
    //         error: function(response) {},
    //     });
    // });

    //Retrieving single data and display modal
    $("#doctororder tbody").on("click", "#approveoder", function(e) {
        e.preventDefault();
        const ID = $(this).attr("rowid");
        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("order_id", ID);

        let Tests = "";
        $.ajax({
            method: "POST",
            url: "/prescription/manage-doctor-order/get_doctor_order",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {

                    // insertType = "Update";
                    $("#addapprove").modal("show");
                    $("#myModalLabel").text("uprove");

                    var address = response.Message.PatientVillage + ', ' + response.Message.PatientDistrict
                    $("#OrderId").val(response.Message.OrderId);
                    $("#AppointId").val(response.Message.AppointId);
                    $("#PatientFullname").val(response.Message.PatientName);
                    $("#Doctor").val(response.Message.Doctor);
                    $("#PatientAge").val(response.Message.PatientAge);
                    $("#PatientGender").val(response.Message.PatientGender);
                    $("#MobileNo").val(response.Message.PatientMobileNo);
                    $("#address").val(address);
                    $("#Instructions").text(response.Message.Instructions);

                    const tbody = $('#tbody')
                    response.Message.doctor_orders.map(Order => {
                        tbody.append('<tr></tr>').append(`<td>${Order.MedicineName}</td>
                        
                        <td>${Order.Quantity} </td>
                        <td>${Order.Dose}</td>
                        <td>${Order.DoseInterval}</td>
                        <td>${Order.DoseDuration}</td>
                      
                        
                        
                        `)
                    })
                    if(response.Message.Status=='Approved'){
                      var button = document.getElementById("approvebutton");
                      button.style.display = "none";

                    }
                    
                    

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

    $("#doctororder tbody").on("click", "#printorder", function(e) {
      e.preventDefault();
      const ID = $(this).attr("rowid");
      // Create form data
      let formData = new FormData();
      // Read user inputs
      formData.append("order_id", ID);

      let Tests = "";
      $.ajax({
          method: "POST",
          url: "/prescription/manage-doctor-order/get_doctor_order",
          headers: { "X-CSRFToken": csrftoken },
          processData: false,
          contentType: false,
          data: formData,
          async: false,
          success: function(response) {
              if (!response.isError) {

                  // insertType = "Update";
                  $("#invoice").modal("show");
                  $("#myModalLabel1").text("uprove");

                  var address = response.Message.PatientVillage + ', ' + response.Message.PatientDistrict
                  $("#OrderId1").text(response.Message.OrderId);
                  $("#AppointId1").text(response.Message.AppointId);
                  $("#PatientFullname1").text(response.Message.PatientName);
                  $("#Doctor1").text(response.Message.Doctor);
                  $("#PatientAge1").text(response.Message.PatientAge);
                  $("#PatientGender1").text(response.Message.PatientGender);
                  $("#MobileNo1").text(response.Message.PatientMobileNo);
                  $("#Instructions1").text(response.Message.Instructions)
                  $("#address1").text(address);

                  const tbody = $('#tbody1')
                  response.Message.doctor_orders.map(Order => {
                      tbody.append('<tr></tr>').append(`<td>${Order.MedicineName}</td>
                      
                      <td>${Order.Quantity} </td>
                      <td>${Order.Dose}</td>
                      <td>${Order.DoseInterval}</td>
                      <td>${Order.DoseDuration}</td>
                      
                      
                      `)
                  })

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
 
  const printButton = document.getElementById("printbutton1");

  printButton.addEventListener("click", () => {
    window.print();
  });

  


});