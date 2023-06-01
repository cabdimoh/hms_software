$(document).ready(function () {
  let insertType="Insert";
  // Update The Entries Selection
  $("#DataNumber").val($("#DataNumber").attr("DataNumber"));

  const id =  $("#departid").attr("departid");
  const shids =  $("#filterShift").attr("filterShift");

  $("#depName").val($("#depName").attr("depName"));



  $("#depName").change(function () {
    RefreshPage();
});
  $("#attendings").change(function () {
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



      let url = `/hrm/attendance/?DataNumber=${entries}&depName=${depNames}&page=${page}`;

      if (search != "") {
          url += `&SearchQuery=${search}`;
      }



      window.location.replace(url);
    }
   // attending employee days present
   $("#manage_shift_table tbody").on("click", ".attendClass", function () {
    if ($(this).prop("checked")) {
      $(this).attr("data", 1);
    } else {
      $(this).attr("data", 0);
    }

    $("#CheckAll").prop("checked", false);
  });

  $("#CheckAll").on("click", function () {
    if ($(this).prop("checked")) {
      $("#manage_shift_table tbody .attendClass").each(function () {
        $(this).prop("checked", true);
        $(this).attr("data", 1);
      });
    } else {
      $("#manage_shift_table tbody .attendClass").each(function () {
        $(this).prop("checked", false);
        $(this).attr("data", 0);
      });
    }
  });
  

    $("#manage_shift_table tbody").on("click", ".attendClass", function () {
      if ($(this).prop("checked")) {
        $(this).attr("data", 1);
      } else {
        $(this).attr("data", 0);
      }
  
      $("#CheckAll").prop("checked", false);
    });
  
    $("#CheckAll").on("click", function () {
      if ($(this).prop("checked")) {
        $("#manage_shift_table tbody .attendClass").each(function () {
          $(this).prop("checked", true);
          $(this).attr("data", 1);
        });
      } else {
        $("#manage_shift_table tbody .attendClass").each(function () {
          $(this).prop("checked", false);
          $(this).attr("data", 0);
        });
      }
    });
    
    // Approval Actions
    $("#presentday").on("click", function (e) {
      Swal.fire({
        text: "Are you sure?",
        title: "Do you want to add employee present list",
        icon: "warning",
        showCancelButton: !0,
        confirmButtonColor: "#2ab57d",
        cancelButtonColor: "#fd625e",
        confirmButtonText: "Yes,add it",
      }).then(function (e) {
        if (e.value) {
          SendAction("Present");
        }
      });
    });

    // Reject Actions
    $("#btn_save_attend").on("click", function (e) {
      insertType="Insert";
      let attendSwitches = document.querySelectorAll(".attendClass");
      let employees = [];
      let Status = [];
      let attendID = [];
      let shiftID=[]
      attendSwitches.forEach((input) => {
        employees.push($(input).attr("employeeID"));
        Status.push($(input).attr("data"));
        shiftID.push($(input).attr("shiftID"));
       
        // insertType != "Insert" && attendID.push($(input).attr("AttendID"));
      });
      Swal.fire({
        text: "Are you sure?",
        title: "That selected employe are Attended",
        icon: "warning",
        showCancelButton: !0,
        confirmButtonColor: "#2ab57d",
        cancelButtonColor: "#fd625e",
        confirmButtonText: "Yes, attend it",
      }).then(function (e) {
        if (e.value) {
       
        SendAction(employees,Status,shiftID,'','take_attendance')
   
        }
      });
    });
    $("#btn_update_attend").on("click", function (e) {
      insertType="Update"
      let attendSwitches = document.querySelectorAll(".attendClass");
      let employees = [];
      let Status = [];
      let attendID = [];
      let shiftID=[]
      attendSwitches.forEach((input) => {
        employees.push($(input).attr("employeeID"));
        Status.push($(input).attr("data"));
        shiftID.push($(input).attr("shiftID"));
        attendID.push($(input).attr("attendedID"));
        // insertType != "Insert" && attendID.push($(input).attr("AttendID"));
      });
      Swal.fire({
        text: "Are you sure?",
        title: "That selected employe will be updated",
        icon: "warning",
        showCancelButton: !0,
        confirmButtonColor: "#2ab57d",
        cancelButtonColor: "#fd625e",
        confirmButtonText: "Yes, updated it",
      }).then(function (e) {
        if (e.value) {
        console.log("Employees",employees)
        console.log("Status",Status);
        console.log("shift",shiftID)
        console.log("attendID",attendID)        
        SendAction(employees,Status,shiftID,attendID,"update_attendance")
          
        }
      });
    });
    function SendAction(employees,status,shiftlist,attendID,action) {
     

      let formData = new FormData();
      formData.append("employees", employees);     
      formData.append("status", status);    
      formData.append("shift", shiftlist);  
      formData.append("department", $("#depName").val());  
      
      if (insertType!="Insert"){
        formData.append("attendID", attendID);
      } 
      
      $.ajax({
        method: "POST",
        url: "/hrm/manageshiftlist/"+action ,
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
  

  
    //Retrieving single data and display modal
    $("#manage_shift_table tbody").on("click", "#viewmngeshift", function (e) {
      e.preventDefault();
      const ID = $(this).attr("mngeshiftID");
      $(".EditDays_modal").modal("show");
      let formData = new FormData();
      formData.append("id", ID);
      $.ajax({
        method: "POST",
        url: "/hrm/manageshiftlist/get_single_shiftmanagement" ,
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        async: false,
        success: function (data) {
          if (!data.isError) {
            $('.days').val(data.Message[0].days)
            
            let days = $(".days").val()
            days = days.split(',')
            $('.days .col-4 .form-check input').each(function (index, item) {
  
              if (days.includes($(item).attr('id'))) {
                $(item).prop('checked', true)
              }
              else {
                
                $(item).prop('checked', false)
  
              }
  
            });
  
         
          } else {
            Swal.fire(data.title, data.Message, data.type);
          }
        },
        error: function (error) {
          error;
        },
      });
      
    });
  
    $('#attendanceDetail').on('click', function(){
      $('.ShowDetailAtten_modla').modal('show')
      
    })

  });
  