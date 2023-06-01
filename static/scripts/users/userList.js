$(document).ready(function () {


                                         

    $('#userList_table').on("click", "#Activation_btn", function (e) {
        let ID  =  $(this).attr("userIDs");
        let type = "";
        if ($(this).prop("checked")) {
          type = "activate";
          handleEmployeeApprovel(type, ID)
        } else {
          type = "deactive";
          handleEmployeeApprovel(type, ID)
        }
    
        
        // let formData = new FormData();
        // formData.append("type", type);
        // formData.append("userIDs", $(this).attr("userIDs"));
        // formData.append("status", type);
        // formData.append("employee_id", employee);
        // Swal.fire({
        //   title: "Are you sure",
        //   text: "Are you sure to " + type + " ?",
        //   icon: "warning",
        //   showCancelButton: !0,
        //   confirmButtonColor: "#2ab57d",
        //   cancelButtonColor: "#fd625e",
        //   confirmButtonText: "Yes, " + status + " it",
        // })
        // $.ajax({
        //   method: "POST",
        //   url: "/users/users-management/activate_user",
        //   headers: { "X-CSRFToken": csrftoken },
        //   processData: false,
        //   contentType: false,
        //   data: formData,
        //   async: false,
        //   success: function (response) {
        //     if (!response.isError) {
              
        //          Swal.fire({
        //                 title: response.title,
        //                 text: response.Message,
        //                 icon: response.type,
        //                 confirmButtonClass: "btn btn-primary w-xs mt-2",
        //                 buttonsStyling: !1,
        //                 showCloseButton: !0,
        //             }).then((e) => {
        //               if (e.value) {
        //                   window.location.reload()
        //               }
        //           });
        //     }
        //   },
        // })
      });

  // Finction to handle job approval
  function handleEmployeeApprovel(status,id) {
    // Prepare the form data
    let formData = new FormData();
    // Append data to form data

    formData.append("type", status);
    formData.append("userIDs", id);
    Swal.fire({
      title: "Are you sure",
      text: "to " + status + " this user ?",
      icon: "warning",
      showCancelButton: !0,
      confirmButtonColor: "#2ab57d",
      cancelButtonColor: "#fd625e",
      confirmButtonText: "Yes, " + status + " it",
    }).then(function (e) {
      if(e.isDismissed == true && e.isConfirmed == false && e.isDenied == false){
        $('#userList_table input').each(function(index, item){
          $(item).prop('checked', false)
        })
      }
      else{
        $.ajax({
          method: "POST",
          url: "/users/users-management/activate_user",
          headers: { "X-CSRFToken": csrftoken },
          processData: false,
          contentType: false,
          data: formData,
          async: false,
          success: function (data) {
            if (!data.isError) {               
              Swal.fire({
                title: data.title,
                text: data.Message,
                icon: data.type,
                confirmButtonColor: "#2ab57d",
                cancelButtonColor: "#fd625e",
                confirmButtonText: "Ok it!",
              }).then((e) => {
                if (e.value) {
                  // hide the modal and resret the form
                  window.location.reload()
      
                }
              });
    
            }
    
          
          },
          error: function (error) {
            (error);
          },
        
        });
      }
    
    }
    

   
    
    )

  }


})

