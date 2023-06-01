$(document).ready(function() {
    $("#approveiquipmentbottun").on("click", function (e) {
      
        e.preventDefault();
    
        // Create form data
        let formData = new FormData();
        
        // Read user inputs
        formData.append("OrderId", $("#OrderId").val());
        
    
        $.ajax({
          method: "POST",
          url: "/inventory/manage-order-equipment/approveEquipment",
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
                  $("#approveform")[0].reset();
                  // window.location.reload();
                  window.location.replace("/inventory/equipment-order");
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
   
    $("#MedicineOrder tbody").on("click", "#orderview", function(e) {
        e.preventDefault();
        const ID = $(this).attr("rowid");
        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("OrderId", ID);

        $.ajax({
            method: "POST",
            url: "/inventory/manage-order-equipment/get_approveEquipment",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {

                    // insertType = "Update";
                    $("#staticBackdrop").modal("show");
                    

                    
                    $("#OrderId").val(response.Message.id);

                    if(response.Message.Status=='Approved'){
                      var button = document.getElementById("approveiquipmentbottun");
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
    
});
