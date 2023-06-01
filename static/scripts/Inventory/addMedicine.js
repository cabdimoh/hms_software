$(document).ready(function () {
    insertType = "Insert"
    let image = "";
    $("#image").on("change", function (e) {
        image = e.target.files[0];
    });
    let Medicine_categories = "";
    $("#SelectCategory").on("change", () => {
        Medicine_categories = $("#SelectCategory option:selected").val()
    })
    $("#btn_submit").on("click", function (e) {




        // Prevent the page from loading or refreshing
        e.preventDefault();

        // Create form data
        let formData = new FormData();

        // Read user 
        formData.append("bach_no", $("#bach_no").val());
        formData.append("MedicineName", $("#MedicineName").val());
        formData.append("SelectCategory", $("#SelectCategory").val());
        formData.append("box", $("#box").val());
        formData.append("quantity", $("#quantity").val());
        formData.append("dosage", $("#dosage").val());
        formData.append("manufacturing", $("#manufacturing").val());
        formData.append("manufacturingdate", $("#manufacturingdate").val());
        formData.append("ExpireDate", $("#ExpireDate").val());
        formData.append("supplierPrice", $("#supplierPrice").val());
    
        
         




        $.ajax({
            method: "POST",
            url: "/inventory/manage-medicine/new_medicine",
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
                            $("#medicineForm")[0].reset();
                            window.location.reload();
                            
                            // window.location.replace("/inventory/medicines");
                            // $(".bank_modal").modal("hide");

                            // Read all spouses information
                            // getBanks(employeeID);
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


    $("#btn_submit_edit_medicine").on("click", function (e) {




        // Prevent the page from loading or refreshing
        e.preventDefault();

        // Create form data
        let formData = new FormData();

        // Read user 
        
        formData.append("MedicineName", $("#MedicineName1").val());
        formData.append("SelectCategory", $("#SelectCategory1").val());
        formData.append("MedicineID1", $("#MedicineID1").val());
        
    
        
         




        $.ajax({
            method: "POST",
            url: "/inventory/manage-medicine/update_medicine",
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
                            $("#medicineForm")[0].reset();
                            window.location.reload();
                            
                            // window.location.replace("/inventory/medicines");
                            // $(".bank_modal").modal("hide");

                            // Read all spouses information
                            // getBanks(employeeID);
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
});
$("#btn_submit_refill").on("click", function(e) {
    // Prevent the page from loading or refreshing
    e.preventDefault();

    // Create form data
    let formData = new FormData();

    // Read user inputs
    formData.append("MedicineName2", $("#MedicineName2").val());
    formData.append("SelectCategory2", $("#SelectCategory2").val());
    formData.append("bach_no2", $("#bach_no2").val());
    formData.append("ExpireDate2", $("#ExpireDate2").val());
    formData.append("supplierPrice2", $("#supplierPrice2").val());
    
    formData.append("box2", $("#box2").val());
    formData.append("quantity2", $("#quantity2").val());
    // formData.append("manufacturing2", $("#manufacturing2").val());
    formData.append("manufacturingdate2", $("#manufacturingdate2").val());
    formData.append("medid", $("#medid").val());
   

    

    // $("#MedicineID").val(response.Message.id);
    


    $.ajax({
        method: "POST",
        url: "/inventory/manage-medicine/new_refill",
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        async: false,
        success: function(response) {
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
                        $("#medicineForm1")[0].reset();
                        window.location.replace("/inventory/medicines");
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
        error: function(response) {},
    });


});


$("#medicineTable tbody").on("click", "#EditMedicineButton", function (e) {
    e.preventDefault();
    const ID = $(this).attr("rowid");

    let formData = new FormData();

    formData.append("Medicine_id", ID);

    $.ajax({
        method: "POST",
        url: "/inventory/manage-medicine/getMedicine",
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        async: false,
        success: function (response) {
            if (!response.isError) {

                insertType = "Update";
                $("#myModaledit").modal("show");
                $("#myModalLabel2").text("Update medicine");

                
                // $("#bach_no").val(response.Message.BatchNO);
                $("#MedicineName1").val(response.Message.MedicineName);
                $("#SelectCategory1").val(response.Message.SelectCategory);
              
                $("#MedicineID1").val(response.Message.id);
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

})
$("#medicineTable tbody").on("click", "#Refill", function(e) {
    e.preventDefault();
    const ID = $(this).attr("rowid");

    let formData = new FormData();

    formData.append("Medicine_id", ID);

    $.ajax({
        method: "POST",
        url: "/inventory/manage-medicine/refill",
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        async: false,
        success: function(response) {
            if (!response.isError) {
                // insertType = "Update";
                $("#refail").modal("show");
                $("#myModalLabel1").text("refill medicine");
                
                $("#medid").val(response.Message.id);
               
                $("#MedicineName2").val(response.Message.MedicineName1);
                $("#SelectCategory2").val(response.Message.SelectCategory1);
                
                
    
                // $("#report").attr({ target: '_blank', href: document_url });
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

})

// $("#medicineTable tbody").on("click", "#viewmedicine", function(e) {
//     e.preventDefault();
//     const ID = $(this).attr("rowid");

//     let formData = new FormData();

//     formData.append("Medicine_id", ID);

//     $.ajax({
//         method: "POST",
//         url: "/inventory/manage-medicine/viewmediicnedetails",
//         headers: { "X-CSRFToken": csrftoken },
//         processData: false,
//         contentType: false,
//         data: formData,
//         async: false,
//         success: function(response) {
//             if (!response.isError) {
//                 // insertType = "Update";
//                 $("#modalView").modal("show");
//                 $("#myLargeModalLabel").text("view medicine");
                
//                 $("#id").text(response.Message.id);
//                 // $("#bach_no1").text(response.Message.bach_no);
//                 $("#MedicineName1").text(response.Message.MedicineName);
//                 $("#SelectCategory1").text(response.Message.SelectCategory);
//                 $("#box1").text(response.Message.box);
//                 $("#quantity1").text(response.Message.quantity);
//                 $("#manufacturing1").text(response.Message.manufacturing);
//                 // $("#manufacturingdate1").text(response.Message.manufacturing_date);
//                 $("#dosage1").text(response.Message.dosage);
//                 // $("#ExpireDate1").text(response.Message.ExpireDate);
//                  $("#supplierPrice1").text(response.Message.supplierPrice);
//                 const tbody = $('#tbody')
//                     response.Message.view_medicine_list.map(view => {
                        
//                         tbody.append('<tr></tr>').append(`
                        
//                         <td>${view.id}</td>
//                         <td>${view.type}</td>
//                         <td>${view.bach_no}</td>
//                         <td>${view.box}</td>
//                         <td>${view.quantity}</td>
                       
//                         <td>${view.manufacturing_date}</td>
//                         <td>${view.ExpireDate}</td>
//                         <td>${view.supplierPrice}</td>
//                         <td>${view.date}</td>
//                         `
                        
//                         )
//                     })
                
    
//                 // $("#report").attr({ target: '_blank', href: document_url });
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

// })

$("#printbutton").on("click", function () {
    printStatement();
});

function printStatement() {
    let printarea = document.querySelector("#medicineTable")
    let printarea2 = document.querySelector("#transactiontable")
    let newWindow = window.open("");
    newWindow.document.write(`<html><thead><title></title>`);
    newWindow.document.write(`<style media="print">
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500&display=swap');
  body {
    font-family: 'Poppins', sans-serif;

  }

  body {
    
    background-color: #e4e4e4;
   
   
    
    
  }

  th {
    background-color: #04AA6D !important;
    color: green !important;
  }

  </style>`)
    newWindow.document.write(`</thead><body`);
    newWindow.document.write(printarea.innerHTML);
    newWindow.document.write(printarea2.innerHTML);
    newWindow.document.write(`</body></html>`);
    newWindow.print();
    newWindow.close();

}
