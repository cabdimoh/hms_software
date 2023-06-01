$(document).ready(function() {
    $("#approvebutton1").on("click", function (e) {
      
        e.preventDefault();
    
        // Create form data
        let formData = new FormData();
        
        // Read user inputs
        formData.append("OrderId", $("#OrderId").val());
        
        
    
        $.ajax({
          method: "POST",
          url: "/inventory/manage-order-medicine/get_approvers",
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
                  window.location.reload();
                  window.location.replace("/inventory/medicine-order");
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
        formData.append("order_id", ID);

        $.ajax({
            method: "POST",
            url: "/inventory/manage-order-medicine/MedicineOderView",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {

                    // insertType = "Update";
                    $("#addapprove1").modal("show"); 
                    $("#OrderId").val(response.Message.OrderId);
                 
                    const tbody = $('#tbody')
                    response.Message.medicineOrder.map(Order => {
                        tbody.append('<tr></tr>').append(`<td>${Order.MedicineName}</td>
                        
                        <td>${Order.Quantity} </td>
                        `)
                    })

                    if(response.Message.Status=='Approved'){
                      var button = document.getElementById("approvebutton1");
                      button.style.display = "none";
                      
                      
                    }
                    // const message = document.createElement("p");
                    //   message.textContent = "Your message goes here";
                    //   document.body.appendChild(message);

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
