$(document).ready(function () {

  // Update The Entries Selection
  $("#DataNumber").val($("#DataNumber").attr("DataNumber"));

  const id =  $("#departid").attr("departid");
  const shids =  $("#filterShift").attr("filterShift");

  $("#depName").val($("#depName").attr("depName"));datechoose
  $("#attendings").val($("#attendings").attr("attendings"));
  $("#datechoose").val($("#datechoose").attr("datechoose"));


  $("#datechoose").change(function () {
       RefreshPage();
});

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
      let attendingss = $("#attendings").val();
      let datechooses = $("#datechoose").val();


      let url = `/hrm/attendancelist/?DataNumber=${entries}&depName=${depNames}&attendings=${attendingss}&page=${page}&datechoose=${datechooses}`;

      if (search != "") {
          url += `&SearchQuery=${search}`;
      }



      window.location.replace(url);
    }
   // attending employee days present
    
  

  
    //Retrieving single data and display modal
    $("#manage_shift_table tbody").on("click", "#viewmngeshift", function (e) {
      e.preventDefault();
      const ID = $(this).attr("mngeshiftID");
      $(".EditDays_modal").modal("show");
      let formData = new FormData();
      formData.append("id", ID);
      $.ajax({
        method: "POST",
        url: "/hrm/manageshiftlist/get_attending_days" ,
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
  
   
  });
  