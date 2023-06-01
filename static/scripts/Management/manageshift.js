$(document).ready(function () {
   
  // Update The Entries Selection
  $("#DataNumber").val($("#DataNumber").attr("DataNumber"));

  const id =  $("#departid").attr("departid");
  const shids =  $("#filterShift").attr("filterShift");

  $("#depName").val($("#depName").attr("depName"));
  //   $("#sectiondep").val($("#sectiondep").attr("sectiondep"));

  $("#depName").change(function () {
      RefreshPage();
  });

  $("#DataNumber").change(function () {
      RefreshPage();
  });

  $("#SearchQuery").on("change", function () {
      RefreshPage();
  });

  $("#SearchQueryBTN").on("click", function () {
      RefreshPage();
  });

  $(".pagination .page-item").on("click", function () {
      const pageNumber = $(this).attr("page");
      $(".activePage").attr("activePage", pageNumber);
      RefreshPage();
  });


  function RefreshPage() {
      let page = $(".activePage").attr("activePage");
      let search = $("#SearchQuery").val();
      let entries = $("#DataNumber").val();
      let depNames = $("#depName").val();
      let departmentid = id;
      let shid = shids

      let url = `/hrm/view_shift/${shift}?DataNumber=${entries}&depName=${depNames}&page=${page}`;

      if (search != "") {
          url += `&SearchQuery=${search}`;
      }



      window.location.replace(url);
    }
  
    // Performing autocomplete function
    $("#search").on("input", function (e) {
      $("#title").val("");
      $("#search").removeAttr("userid");
      var listUsers = [];
      if ($(this).val() != "" && $(this).val().length > 3) {
        listUsers = SearchEngine($(this).val());
  
        $("#search").autocomplete({
          source: listUsers,
          select: function (event, ui) {
            const item = ui.item.userid;
            const value = ui.item.value;
  
            if (value != "") {
              $("#search").attr("userid", item);
            }
          },
          response: function (event, ui) {
            if (!ui.content.length) {
              var noResult = { value: "", label: "No result found" };
              ui.content.push(noResult);
            }
          },
          minLength: 4,
        });
      }
    });
  
    function SearchEngine(letter) {
      var list = [];
      $.ajax({
        method: "GET",
        url: "/users/search_engine/" + letter + "/" + "EM,FromEmployee",
        async: false,
        headers: { "X-CSRFToken": csrftoken },
        success: function (data) {
          $(".users-body .list").html("");
          data.Message.forEach((user) => {
            list.push(user);
          });
        },
      });
  
      return list;
    }
  
    // Directorate Actions for approving and Rejecting
    $("#check_all").on("click", function (e) {
      $("#dept_approval_table tbody #check_once").prop("checked", $(this).prop("checked")
      );
     
      if ($(this).prop("checked")) {
        $(".Approved").removeClass("d-none");
      } else {
        $(".Approved").addClass("d-none");
      }
    });
  
    $("#dept_approval_table tbody").on("click", "#check_once", function (e) {
      // Check if all checked
      $("#check_all").prop("checked", false);
      let is_all_checked = [true, false];
     
    
  
      $("#dept_approval_table tbody #check_once").each(function () {
        if (!$(this).prop("checked")) {
            is_all_checked[0] = false;
            console.log('unchecked'); 
            $(".Approved").addClass("d-none");
        } else {
          is_all_checked[1] = true;        
          console.log('checked'); 
        
        }
      });
  
      if (is_all_checked[0]) {
        $("#check_all").prop("checked", true);        
        console.log('unchecked');
      }
  
      if (is_all_checked[1]) {     
        $(".Approved").removeClass("d-none");
        console.log('checked'); 
       
        
      }
    });


    
    // Approval Actions
    $(".Approved").on("click", function (e) {
      Swal.fire({
        text: "Are you sure?",
        title: "Do you want to add shift",
        icon: "warning",
        showCancelButton: !0,
        confirmButtonColor: "#2ab57d",
        cancelButtonColor: "#fd625e",
        confirmButtonText: "Yes,add it",
      }).then(function (e) {
        if (e.value) {
          SendAction("Approved");
        }
      });
    });

    // Reject Actions
    $("#removeShift").on("click", function (e) {
      Swal.fire({
        text: "Are you sure?",
        title: "Do you want to remove shifts",
        icon: "warning",
        showCancelButton: !0,
        confirmButtonColor: "#2ab57d",
        cancelButtonColor: "#fd625e",
        confirmButtonText: "Yes,remove it",
      }).then(function (e) {
        if (e.value) {
          SendAction("Remove");
        }
      });
    });
  
    function SendAction(status) {
      let employees = []; 
        $("#dept_approval_table tbody #check_once:checked").each(function () {
          employees.push($(this).attr("employeeIDs"));       
      });

      console.log(employees);
      let formData = new FormData();
      formData.append("employees", employees);      
      formData.append("shift", shift);  
      console.log(shift, 'ayan wada');    
      formData.append("status", status);    
      $.ajax({
        method: "POST",
        url: "/hrm/manages_shifts/new_assigning_shift",
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        async: false,
        success: function (response) {
          if (!response.isError) {
            Swal.fire({
              title: response.title,
              text: response.Message,
              icon: response.type,
              confirmButtonClass: "btn btn-primary w-xs mt-2",
              buttonsStyling: !1,
            }).then((e) => {
            
              window.location.reload();
              console.log('saving is done');
            });
          } else {
            Swal.fire({
              title: response.title,
              text: response.Message,
              icon: response.type,
              confirmButtonClass: "btn btn-primary w-xs mt-2",
              buttonsStyling: !1,
            });
          }
        },
        error: function (response) {},
      });

    }
  
    // Saving and Update Function
    $("#submit").on("click", function (e) {
      e.preventDefault();
      let employee_id = $("#search").attr("userid");
      let userval = $("#search").val();
      let vehicle_id = $("#vehicle_id").val();
      let chassis_number = $("#chassis_number").val();
      let vehicle_model = $("#vehicle_model").val();
      let vehicles = $("#vehicles").val();
      let fuel_per_km = $("#fuel_per_km").val();
      let total_liter = $("#total_liter").val();
      let description = $("#description").val();
      let fuel_type = $("#fuel_type").val();
      let formData = new FormData();
      let method, link;
  
      method = "POST";
      link = "/logistics/manage_vehicles/" + vehicle_id;
      // Validations
      if (employee_id == undefined || userval == "") {
        Swal.fire("Warning!!", "Fadlan soo geli shaqaalaha", "warning");
      } else if (vehicles == undefined || vehicles == "") {
        Swal.fire("Warning!!", "Fadlan dooro gawaarida", "warning");
      } else if (chassis_number == "") {
        Swal.fire(
          "Warning!!",
          "Fadlan soo geli Lambarka Aqoonsiga Baabuurka ama Nambarka Chassis-ka",
          "warning"
        );
      } else if (
        vehicle_model == "" ||
        vehicle_model == undefined ||
        vehicle_model == null
      ) {
        Swal.fire("Warning!!", "Fadlan dooro nuuca gaariga", "warning");
      } else if (fuel_type == "" || fuel_type == undefined || fuel_type == null) {
        Swal.fire("Warning!!", "Fadlan dooro nuuca shidalka", "warning");
      } else if (fuel_per_km == "") {
        Swal.fire(
          "Warning!!",
          "Fadlan soo geli inta shidaal/basiin oo halkii KM cuni karo",
          "warning"
        );
      } else if (total_liter == "") {
        Swal.fire(
          "Warning!!",
          "Fadlan soo geli inta liitar oo shidaal/basiin uu qaado karo",
          "warning"
        );
      } else if (description == "") {
        Swal.fire("Warning!!", "Fadlan soo geli faahfaahin", "warning");
      } else {
        formData.append("employee_id", employee_id);
        formData.append("vehicles", vehicles);
        formData.append("chassis_number", chassis_number);
        formData.append("model", vehicle_model);
        formData.append("description", description);
        formData.append("fuel_type", fuel_type);
        formData.append("fuel_per_km", fuel_per_km);
        formData.append("total_liter", total_liter);
        formData.append("Type", "Changevehicle");
  
        $.ajax({
          method: method,
          url: link,
          headers: { "X-CSRFToken": csrftoken },
          processData: false,
          contentType: false,
          data: formData,
          async: true,
          success: function (response) {
            if (!response.isError) {
              insertType = "Insert";
  
              setTimeout(function () {
                window.location.reload();
              }, 2000);
              Swal.fire({
                title: response.title,
                text: response.Message,
                icon: response.type,
                confirmButtonClass: "btn btn-primary w-xs mt-2",
                buttonsStyling: !1,
                showCloseButton: !0,
              });
            } else {
              Swal.fire({
                title: response.title,
                text: response.Message,
                icon: "error",
                confirmButtonClass: "btn btn-primary w-xs mt-2",
                buttonsStyling: !1,
                showCloseButton: !0,
              });
            }
          },
          error: function (response) {},
        });
      }
    });
  
    //Retrieving single data and display modal
    $("#dept_approval_table  tbody").on("click", "#Edit", function (e) {
      e.preventDefault();
      const ID = $(this).attr("rowid");
      Swal.fire({
        title: "Do you wants to update",
        text: "to sure to update ?",
        icon: "warning",
        showCancelButton: !0,
        confirmButtonColor: "#2ab57d",
        cancelButtonColor: "#fd625e",
        confirmButtonText: "Yes, update it",
      }).then(function (e) {
        if (e.value) {
          if (ID != "" && ID != undefined) {
            $.ajax({
              method: "GET",
              url: "/logistics/manage_vehicles/" + ID,
              headers: { "X-CSRFToken": csrftoken },
              async: false,
              success: function (data) {
                if (!data.isError) {
                  vehicle_model();
                  Fuel_Type();
                  $("#VehicleModal").modal("show");
                  $("#search").val(data.Message.employee.name);
                  $("#search").attr("userid", data.Message.employee.id);
                  $("#vehicle_id").val(data.Message.id);
                  $("#chassis_number").val(data.Message.chassis_number);
                  $("#vehicle_model").val(data.Message.vehicle_model);
                  $("#fuel_type").val(data.Message.fuel_type);
                  $("#fuel_per_km").val(data.Message.fuel_per_km);
                  $("#total_liter").val(data.Message.total_liter);
  
                  $("#vehicles").val(data.Message.vehicle_store);
                  $("#description").val(data.Message.description);
                } else {
                  Swal.fire(data.title, data.Message, data.type);
                }
              },
              error: function (error) {
                error;
              },
            });
          }
        }
      });
    });
  
    // get weapon model

  });
  