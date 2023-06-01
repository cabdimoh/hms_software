$(document).ready(function () {


    $("#btn_save").on("click", function (e) {
        // Prevent the page from loading or refreshing
        e.preventDefault();

        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("employee_id", $('#empdisID').val());
        formData.append("email", $('#d_email').val());

        $.ajax({
            method: "POST",
            url: "/users/users-management/NewUser",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function (response) {
                if (!response.isError) {
                    $(".emailconfirm_modal").modal("hide");
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

    $('#employee_table').on('click', '#Add_user_btn', function () {
        const ID = $(this).attr('employeIDS');  
        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("id", ID);


        $.ajax({
            method: "POST",
            url: "/users/users-management/get_employee_data",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function (response) {
                if (!response.isError) {

                    insertType = "Update";
                    $(".emailconfirm_modal").modal("show");
                    $("#modaltitle").text("This email will be user Email");

                    $("#empdisID").val(response.Message.id);
                    $("#d_email").val(response.Message.email);
          



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









  // Finction to handle job approval
//   function handleEmployeeApprovel(ID, email) {
//     // Prepare the form data
//     let formData = new FormData();
//     // Append data to form data

//     formData.append("email", status);
//     formData.append("employee_id", employee);
//     Swal.fire({
//       title: "Are you sure",
//       text: "Are you sure to " + status + " ?",
//       icon: "warning",
//       showCancelButton: !0,
//       confirmButtonColor: "#2ab57d",
//       cancelButtonColor: "#fd625e",
//       confirmButtonText: "Yes, " + status + " it",
//     }).then(function (e) {
//       if (e.value) {
//         $.ajax({
//           method: "POST",
//           url: "/hrm/manage_employees/approve_reject_employee",
//           headers: { "X-CSRFToken": csrftoken },
//           processData: false,
//           contentType: false,
//           data: formData,
//           async: false,
//           success: function (data) {
//             if (!data.isError) {
//               getAllEmployeDatas()
//               Swal.fire({
//                 title: data.title,
//                 text: data.Message,
//                 icon: data.type,
//                 confirmButtonColor: "#2ab57d",
//                 cancelButtonColor: "#fd625e",
//                 confirmButtonText: "Ok it!",
//               }).then((e) => {
//                 if (e.value) {
//                   // hide the modal and resret the form
//                   window.location.reload()
      
//                 }
//               });

//               // Display all budgeting  by filtering year and month
//               // if ($("#SelectYear").val() != "" && $("#SelectMonth").val()) {
//               //   GetAllBudget($("#SelectYear").val(), $("#SelectMonth").val());
//               // }
//             }

//             //  else {
//             //   Swal.fire(data.title, data.Message, data.type);
//             // }
          
//           },
//           error: function (error) {
//             //(error);
//           },
        
//         });
     
//       }
    
//     }   
//     )
//   }


})

