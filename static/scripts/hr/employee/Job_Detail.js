$(document).ready(function () {
   
    let insertType = "Insert";

    $('#newJobDetail').on('click', function () {
        $(".AddJobDetail").modal("show");

        $("#job_type").val('');
        $("#empl_type").val('');
        $("#depart_id").val('');
        $("#section_id").val('');
        $("#salary").val('');

        $("#section_id").val('');
        $("#depart_id").val('');
        $("#fix_alowence").val('');

        $("#directorate_id").val('');
        $("#netpay").val('');
        $("#Jobtype_Salary").val('');

        netpay
        netpay
        Jobtype_Salary

        insertType = "Insert";

    });


    $("#empl_type").on("change", function () {
        if ($("#empl_type").val() != "") {
            $(".Classify-exit").addClass("d-none");
            if ($("option:selected", "#empl_type").text() == "Department Head") {
                $(".directorClass").removeClass("col-lg-12");
                $(".directorClass").addClass("col-lg-6");
                $(".departmentClass").addClass("col-lg-6");
                $(".departmentClass").removeClass("col-lg-12");
                $(".secretoryClass").addClass("d-none");
                $(".departmentClass").removeClass("d-none");
                $(".sections").addClass("d-none");
                $(".netpayClass").removeClass("col-lg-12");
                $(".netpayClass").addClass("col-lg-6");


            }
            else if ($("option:selected", "#empl_type").text() == "Hospital Director") {

                $(".directorClass").removeClass("col-lg-6");
                $(".directorClass").addClass("col-lg-12");
                $(".secretoryClass").addClass("d-none");
                $(".departmentClass").addClass("d-none");
                $(".sections").addClass("d-none");
                $(".netpayClass").removeClass("col-lg-12");
                $(".netpayClass").addClass("col-lg-6");



            }
            else if ($("option:selected", "#empl_type").text() == "Director Secretory") {
                $(".directorClass").removeClass("col-lg-12");

                $(".directorClass").addClass("col-lg-6");
                $(".secretoryClass").removeClass("d-none");
                $(".departmentClass").addClass("d-none");

                $(".sections").addClass("d-none");
                $(".netpayClass").removeClass("col-lg-12");
                $(".netpayClass").addClass("col-lg-6");

            }
            else if ($("option:selected", "#empl_type").text() == "Section Head") {
                $(".directorClass").removeClass("col-lg-12");
                $(".directorClass").addClass("col-lg-6");
                $(".directorClass").removeClass("d-none");

                $(".secretoryClass").addClass("d-none");
                $(".departmentClass").removeClass("d-none");
                $(".departmentClass").removeClass("col-lg-12");

                $(".departmentClass").addClass("col-lg-6");
                $(".sections").removeClass("d-none");
                $(".netpayClass").addClass("col-lg-12");

            }
            else {

                $(".directorClass").removeClass("col-lg-12");
                $(".directorClass").addClass("col-lg-6");

                $(".departmentClass").removeClass("col-lg-12");
                $(".departmentClass").addClass("col-lg-6");

                $(".secretoryClass").addClass("d-none");
                $(".departmentClass").removeClass("d-none");

                $(".sections").removeClass("d-none");
                $(".netpayClass").removeClass("col-lg-6");
                $(".netpayClass").addClass("col-lg-12");



            }
        } else {

            $(".directorClass").removeClass("col-lg-12");
            $(".directorClass").addClass("col-lg-6");
            $(".departmentClass").removeClass("col-lg-12");
            $(".departmentClass").addClass("col-lg-6");
            $(".secretoryClass").addClass("d-none");
            $(".departmentClass").removeClass("d-none");
            $(".sections").removeClass("d-none");
            $(".sections").removeClass("col-lg-12");
            $(".sections").addClass("col-lg-6");
            $(".netpayClass").removeClass("col-lg-6");
            $(".netpayClass").addClass("col-lg-12");

        }
    });

    // saving and updating
    $("#job_detail_save").on("click", function (e) {
        // Prevent the page from loading or refreshing
        e.preventDefault();

        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("employee_id", employee_id);
        formData.append("job_type", $("#job_type").val());
        formData.append("empl_type", $("#empl_type").val());
        formData.append("depart_id", $("#depart_id").val());
        formData.append("section_id", $("#section_id").val());
        formData.append("directorate_id", $("#directorate_id").val());
        formData.append("secretory_id", $("#secretory_id").val());
        formData.append("Jobtype_Salary", $("#Jobtype_Salary").val());
        formData.append("salary", $("#salary_id").val());
        formData.append("fix_alowence", $("#fix_alowence").val());
        let urls = ""

        if (insertType == "Insert") {
            urls = "/hrm/manage_Job_Detail/new_JobDetail";
        } else {
            urls = "/hrm/manage_Job_Detail/update_JobDetail";            
            formData.append("id", $("#job_detail_id").val());
            formData.append("salary_id", $("#salary_id").val());

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
                    $(".AddJobDetail").modal("hide");
                  
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



    //Retrieving single data and display modal
    $("#job_detail_table").on("click", ".editJobdetail", function (e) {
        e.preventDefault();
        const ID = $(this).attr("jofDe_id");
      

        // Create form data
        let formData = new FormData();
        // Read user inputs
        formData.append("id", ID);


        $.ajax({
            method: "POST",
            url: "/hrm/manage_Job_Detail/getData",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function (response) {
                if (!response.isError) {

                    insertType = "Update";
                    $(".AddJobDetail").modal("show");
                    $("#modaltitle").text("Update Job Detail");

                    $("#job_type").val(response.Message.job_type);
                    $("#empl_type").val(response.Message.employee_type);
                    $("#depart_id").val(response.Message.department);



                    $("#is_active").val(response.Message.is_active);
                    $("#salary").val(response.Message.salary);
                    $("#salary_id").val(response.Message.salary_id);
                    $("#fix_alowence").val(response.Message.fix_allow);


                    // Fill sections first
                    get_department_section($("#depart_id").val());
                    $("#section_id").val(response.Message.department_section)


                    let x = response.Message.id;

                    $("#job_detail_id").val(x);

                    ("#section_id").val(response.Message.department_section)

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



    $('#CurrentJobEdit').on('click', function(e){
        let ID = $(this).attr('currentID')
        $(".AddJobDetail").modal("show"); 
        let formData = new FormData();
        formData.append("id", ID);
    
        $.ajax({
            method: "POST",
            url: "/hrm/manage_Job_Detail/getData",
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            async: false,
            success: function (response) {
                if (!response.isError) {
    
                    insertType = "Update";
                    $(".AddJobDetail").modal("show");
                    $("#modaltitle").text("Update Job Detail");
    
                    $("#job_detail_id").val(response.Message.id);
                    $("#job_type").val(response.Message.job_type);
                    $("#empl_type").val(response.Message.employee_type);
                    $("#directorate_id").val(response.Message.director);

                    if(response.Message.employee_type == 'General-Director'){                       
                        $(".directorClass").removeClass("col-lg-6");
                        $(".directorClass").addClass("col-lg-12");
                        $(".secretoryClass").addClass("d-none");
                        $(".departmentClass").addClass("d-none");
                        $(".sections").addClass("d-none");
                        $(".netpayClass").removeClass("col-lg-12");
                        $(".netpayClass").addClass("col-lg-6");            
                    } 
                    else if(response.Message.employee_type == 'Director-Secretory'){
                        $(".directorClass").removeClass("col-lg-12");
                        $(".directorClass").addClass("col-lg-6");
                        $(".secretoryClass").removeClass("d-none");
                        $(".departmentClass").addClass("d-none");
                        $(".sections").addClass("d-none");
                        $(".netpayClass").removeClass("col-lg-12");
                        $(".netpayClass").addClass("col-lg-6");
               
                    }            
                    else if(response.Message.employee_type == 'Department-Head'){
                        $(".directorClass").removeClass("col-lg-12");
                        $(".directorClass").addClass("col-lg-6");
                        $(".departmentClass").addClass("col-lg-6");
                        $(".departmentClass").removeClass("col-lg-12");
                        $(".secretoryClass").addClass("d-none");
                        $(".departmentClass").removeClass("d-none");
                        $(".sections").addClass("d-none");
                        $(".netpayClass").removeClass("col-lg-12");
                        $(".netpayClass").addClass("col-lg-6");                 
                    }            
                    else if(response.Message.employee_type == 'Section-Head'){

                        $(".directorClass").removeClass("col-lg-12");
                        $(".directorClass").addClass("col-lg-6");
                        $(".directorClass").removeClass("d-none");
                        
                        $(".secretoryClass").addClass("d-none");
                        $(".departmentClass").removeClass("d-none");
                        $(".departmentClass").removeClass("col-lg-12");

                        $(".departmentClass").addClass("col-lg-6");
                        $(".sections").removeClass("d-none");
                        $(".netpayClass").addClass("col-lg-12");         
                    }     
                    else{
                        $(".directorClass").removeClass("col-lg-12");
                        $(".directorClass").addClass("col-lg-6");
                        $(".directorClass").removeClass("d-none");

                        $(".secretoryClass").addClass("d-none");
                        $(".departmentClass").removeClass("d-none");
                        $(".departmentClass").removeClass("col-lg-12");

                        $(".departmentClass").addClass("col-lg-6");
                        $(".sections").removeClass("d-none");
                        $(".netpayClass").addClass("col-lg-12");                     
                    }            
                  
                    netpay
                    netpay
                    Jobtype_Salary

                    get_secretory_name(response.Message.director); 
                    $("#secretory_id").val(response.Message.secretary);                    

                    get_department_name(response.Message.director);
                    $("#depart_id").val(response.Message.department);

                    get_department_section($("#depart_id").val());
                    $("#section_id").val(response.Message.department_section); 

                    get_salary($("#job_type").val());
                    $("#Jobtype_Salary").val(response.Message.Jobtype_Salary); 
    
                    $("#salary").val(response.Message.salary);
                    $("#netpay").val(response.Message.basebay);
                    $("#fix_alowence").val(response.Message.fix_allow);
              
    
    
                    // Fill sections first
                    // get_department_section(("#directorate_id").val());
                    // $("#section_id").val(response.Message.department_section)
    
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
    $("#directorate_id").on("change", function () {

        // Clear all other fields
        $("#secretory_id").html('');
        $("#section_id").html("");
        


        // if the data selected is not empty
        if ($(this).val() != "") {

            get_secretory_name($("#directorate_id").val()); 
            get_department_name($("#directorate_id").val());

        }
    });

    $("#depart_id").on("change", function () {

        // Clear all other fields
        $("#section_id").html("");
        


        // if the data selected is not empty
        if ($(this).val() != "") {
            get_department_section($("#depart_id").val());

        }
    });

    $("#job_type").on("change", function () {

        // Clear all other fields
        $("#salary ").val("");
        $("#fix_alowence").val("");


        // if the data selected is not empty
        if ($(this).val() != "") {
            get_salary($("#job_type").val());
        }
    });

    $("#Jobtype_Salary").on("change", function () {

        // Clear all other fields
        $("#salary ").val(""); 
        $("#netpay ").val("");


        // if the data selected is not empty
        if ($(this).val() != "") {
            get_subcategory_salary($("#Jobtype_Salary").val());
        }
    });






    function get_secretory_name(secretary) {
        let formData = new FormData();
       
        formData.append("secretary", secretary);
        $.ajax({
            method: "POST",
            url: "/hrm/manage_Job_Detail/get_director_assistance_func",
            async: false,
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            success: function (response) {
                if (!response.isError) {

                    $("#secretory_id").html("");

                    // if the data length is 0
                    if (response.Message.length == 0) {
                        // Add disabled attribute from directorate
                        // $("#job_directorate").attr("disabled", true);
                        $("#secretory_id").append(
                            `<option value="Not available">Not available</option>`
                        );
                        // $("#job_department").append(
                        //   `<option value="Not available">Not available</option>`
                        // );
                        // $("#job_section").append(
                        //   `<option value="Not available">Not available</option>`
                        // );
                        // $("#job_branch").append(
                        //   `<option value="Not available">Not available</option>`
                        // );
                        // $("#job_sub_branch").append(
                        //   `<option value="Not available">Not available</option>`
                        // );
                    } else {
                        // Remove disabled attribute from directorate
                        // $("#job_directorate").attr("disabled", false);
                    }

                    response.Message.forEach((item, index) => {
                        index == 0 &&
                            $("#secretory_id").append(
                                `<option value="">Select Section</option>`
                            );
                        $("#secretory_id").append(
                            `<option value="${item.id}">${item.name}</option>`
                        );
                    });
                } else {
                    Swal.fire("Something Wrong!!", data.Message, "error");
                }
            },
            error: function (error) { },
        });
    }

    function get_department_section(section) {
        let formData = new FormData();
        
        formData.append("department", section);
        $.ajax({
            method: "POST",
            url: "/hrm/manage_Job_Detail/get_deb_section_func",
            async: false,
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            success: function (response) {
                if (!response.isError) {

                    $("#section_id").html("");

                    // if the data length is 0
                    if (response.Message.length == 0) {
                        // Add disabled attribute from directorate
                        // $("#job_directorate").attr("disabled", true);
                        $("#section_id").append(
                            `<option value="Not available">Not available</option>`
                        );
                        // $("#job_department").append(
                        //   `<option value="Not available">Not available</option>`
                        // );
                        // $("#job_section").append(
                        //   `<option value="Not available">Not available</option>`
                        // );
                        // $("#job_branch").append(
                        //   `<option value="Not available">Not available</option>`
                        // );
                        // $("#job_sub_branch").append(
                        //   `<option value="Not available">Not available</option>`
                        // );
                    } else {
                        // Remove disabled attribute from directorate
                        // $("#job_directorate").attr("disabled", false);
                    }

                    response.Message.forEach((item, index) => {
                        index == 0 &&
                            $("#section_id").append(
                                `<option value="">Select Section</option>`
                            );
                        $("#section_id").append(
                            `<option value="${item.id}">${item.name}</option>`
                        );
                    });
                } else {
                    Swal.fire("Something Wrong!!", data.Message, "error");
                }
            },
            error: function (error) { },
        });
    }

    function get_salary(salary) {
        let formData = new FormData();
      
        formData.append("department", salary);
        $.ajax({
            method: "POST",
            url: "/hrm/manage_Job_Detail/get_salary_func",
            async: false,
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            success: function (response) {
                if (!response.isError) {



                    $("#Jobtype_Salary").html("");
                    if (response.Message.length == 0) {
                        $("#Jobtype_Salary").append(
                            `<option value="Not available">Not available</option>`
                        );

                    } else {
                        // Remove disabled attribute from directorate
                        // $("#job_directorate").attr("disabled", false);
                    }


                    response.Message.forEach((item, index) => {
                        index == 0 &&
                            $("#Jobtype_Salary").append(
                                `<option value="">Select Salary Type</option>`
                            );
                        $("#Jobtype_Salary").append(
                            `<option value="${item.id}">${item.name}</option>`
                        );
                    });



                } else {
                    Swal.fire("Something Wrong!!", data.Message, "error");
                }
            },
            error: function (error) { },
        });
    }

    $("#fix_alowence").on("input", function () {
        if ($(this).val() < 0) {          
            $(this).val(0);
        }
        let salary = $("#salary").val();
        let fix_alowence = $("#fix_alowence").val();
        salary = salary == "" ? 0 : salary;
        fix_alowence = fix_alowence == "" ? 0 : fix_alowence;
        let total_amount = parseFloat(salary) + parseFloat(fix_alowence);
        $("#netpay").val(total_amount);


    });



    function get_subcategory_salary(subsalary) {
        let formData = new FormData();
       
        formData.append("subsalary", subsalary);
        $.ajax({
            method: "POST",
            url: "/hrm/manage_Job_Detail/get_sub_category_salary_func",
            async: false,
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            success: function (response) {
                if (!response.isError) {

                    $("#salary").val(response.Message[0].base_salary);
                    $("#salary_id").val(response.Message[0].id);

                    let salary = $("#salary").val();
                    let fix_alowence = $("#fix_alowence").val();
                    salary = salary == "" ? 0 : salary;
                    fix_alowence = fix_alowence == "" ? 0 : fix_alowence;
                    let total_amount = parseFloat(salary) + parseFloat(fix_alowence);
                    $("#netpay").val(total_amount);


                } else {
                    Swal.fire("Something Wrong!!", response.Message, "error");
                }
            },
            error: function (error) { },
        });
    }

    function get_department_name(department_id) {
        let formData = new FormData();
       
        formData.append("department_id", department_id);
        $.ajax({
            method: "POST",
            url: "/hrm/manage_Job_Detail/get_departments_func",
            async: false,
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            data: formData,
            success: function (response) {
                if (!response.isError) {
    
                    $("#depart_id").html("");
    
                    if (response.Message.length == 0) {
    
                        $("#depart_id").append(
                            `<option value="Not available">No Departments</option>`
                        );
                      
                    } else {
                       
                    }
    
                    response.Message.forEach((item, index) => {
                        index == 0 &&
                            $("#depart_id").append(
                                `<option value="">Select Section</option>`
                            );
                        $("#depart_id").append(
                            `<option value="${item.id}">${item.name}</option>`
                        );
                    });
                } else {
                    Swal.fire("Something Wrong!!", data.Message, "error");
                }
            },
            error: function (error) { },
        });
    }
    
});






// const netPays = Number((response.Message[0].base_salary))  +  Number($("#fix_alowence").val() )

