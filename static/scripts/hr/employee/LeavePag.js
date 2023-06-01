$(document).ready(function () {
  // Update The Entries Selection
  $("#DataNumber").val($("#DataNumber").attr("DataNumber"));

  $("#departmentN").val($("#departmentN").attr("departmentN"));



  

$("#departmentN").change(function () {
    RefreshPage();
    });

$("#DataNumber").change(function () {
      RefreshPage();
  });

  $("#SearchQuery").on("change", function () {
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
      let departments = $("#departmentN").val();



      let url = `/hrm/leaves_employees?DataNumber=${entries}&page=${page}&departmentN=${departments}`;

      if (search != "") {
          url += `&SearchQuery=${search}`;
      }
      

      window.location.replace(url);
     
  }

});