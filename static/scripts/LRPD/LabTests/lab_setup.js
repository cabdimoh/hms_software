$(document).ready(function() {

    GetAllLabGroups();
    GetAllLabSubGroup();
    let insertType = "Insert";


    // -------------------------------lab group --------------------------------------------
    $('#add_lab_group').on('click', function() {
        $(".add_lab_group_modal").modal("show");


        $("#lab_group_name").val('');
        $("#lab_group_description").val('');
        insertType = "Insert";


    });

    // saving and updating
    $("#save_lab_group").on("click", function(e) {
        // Prevent the page from loading or refreshing
        e.preventDefault();

        // Create form data
        let formData = new FormData();
        // Read user inputs

        formData.append("lab_group_name", $("#lab_group_name").val());
        formData.append("lab_group_description", $("#lab_group_description").val());



        let urls = ""

        if (insertType == "Insert") {
            urls = "/prescription/manage-lab-setup/new_LabGroup";
        } else {
            urls = "/prescription/manage-lab-setup/edit_LabGroup";
            let x = $("#lab_group_id").val();

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
            success: function(response) {
                if (!response.isError) {
                    $(".add_lab_group_modal").modal("hide");
                    GetAllLabGroups();
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
                            $("#labGroupForm")[0].reset();
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
            error: function(response) {},
        });
    });

    //Retrieving single data and display modal
    $("#lab_group_table").on("click", ".group_btn", function(e) {
        e.preventDefault();
        const ID = $(this).attr("groupId");
        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("id", ID);



        $.ajax({
            method: "POST",
            url: "/prescription/manage-lab-setup/getSingleLabGroup",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {

                    insertType = "Update";
                    $(".add_lab_group_modal").modal("show");
                    $(".modal-title").text("Update Lab Group");
                    $("#lab_group_name").val(response.Message.name);
                    $("#lab_group_description").val(response.Message.discription);
                    $("#lab_group_id").val(response.Message.id);




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



    // Get all employee qualification data 
    function GetAllLabGroups() {
        // Create form data
        let formData = new FormData();
        // Read user inputs

        $.ajax({
            method: "POST",
            url: "/prescription/manage-lab-setup/getLabGroup",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {
                    let table = $("#lab_group_table").DataTable().clear().draw();

                    for (let index = 0; index < response.Message.length; index++) {
                        let temp = [

                            response.Message[index].id,
                            response.Message[index].sampleType,
                            response.Message[index].name,
                            response.Message[index].discription,




                            `<a href="#" class="group_btn" groupId=${response.Message[index].id}  style="color:white;" >
                    <button type="button" class="btn btn-primary rounded">
                    
                        <i class="las la-pen"></i>
                   
                    </button>
                    </a>
      
                
              `
                        ];
                        table.row.add(temp).draw();
                    }

                }
            },
            error: function(response) {},
        });
    }



    // -------------------------------lab Sub group --------------------------------------------
    $('#add_lab_subgroup').on('click', function() {
        $(".add_lab_subgroup_modal").modal("show");


        $("#lab_subgroup_name").val('');
        $("#lab_subgroup_descriptions").val('');
        $("#Choosed_Group").val('');
        insertType = "Insert";


    });

    // saving and updating
    $("#save_lab_subgroup").on("click", function(e) {
        // Prevent the page from loading or refreshing
        e.preventDefault();

        // Create form data
        let formData = new FormData();
        // Read user inputs

        formData.append("lab_subgroup_name", $("#lab_subgroup_name").val());
        formData.append("lab_subgroup_descriptions", $("#lab_subgroup_descriptions").val());
        formData.append("Choosed_Group", $("#Choosed_Group").val());



        let urls = ""

        if (insertType == "Insert") {
            urls = "/prescription/manage-lab-setup/new_LabSubGroup";
        } else {
            urls = "/prescription/manage-lab-setup/edit_LabSubGroup";
            let x = $("#lab_subgroup_id").val();

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
            success: function(response) {
                if (!response.isError) {
                    $(".add_lab_subgroup_modal").modal("hide");
                    GetAllLabSubGroup();
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
                            $("#LabSubgroupForm")[0].reset();
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
            error: function(response) {},
        });
    });

    //Retrieving single data and display modal
    $("#LabSubGroupTable").on("click", ".subgroup_btn", function(e) {
        e.preventDefault();
        const ID = $(this).attr("subgroupid");
        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("id", ID);



        $.ajax({
            method: "POST",
            url: "/prescription/manage-lab-setup/getSingleLabSubGroup",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {

                    insertType = "Update";
                    $(".add_lab_subgroup_modal").modal("show");
                    $(".modal-title").text("Update Lab Category");
                    $("#lab_subgroup_name").val(response.Message.name);
                    $("#Choosed_Group").val(response.Message.group_id);
                    $("#lab_subgroup_descriptions").val(response.Message.discription);
                    $("#lab_subgroup_id").val(response.Message.id);




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



    // Get all employee qualification data 
    function GetAllLabSubGroup() {
        // Create form data
        let formData = new FormData();
        // Read user inputs

        $.ajax({
            method: "POST",
            url: "/prescription/manage-lab-setup/getLabSubGroup",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function(response) {
                if (!response.isError) {
                    let table = $("#LabSubGroupTable").DataTable().clear().draw();

                    for (let index = 0; index < response.Message.length; index++) {
                        let temp = [

                            response.Message[index].id,
                            response.Message[index].sampleType,
                            response.Message[index].group,
                            response.Message[index].name,
                            response.Message[index].discription,




                            `<a href="#" class="subgroup_btn" subgroupid=${response.Message[index].id}  style="color:white;" >
                <button type="button" class="btn btn-sm btn-primary rounded">
                
                    <i class="las la-pen"></i>
               
                </button>
                </a>
    
            
          `
                        ];
                        table.row.add(temp).draw();
                    }

                }
            },
            error: function(response) {},
        });
    }
});