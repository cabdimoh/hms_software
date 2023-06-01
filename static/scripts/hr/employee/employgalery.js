$(document).ready(function () {
    // Update The Entries Selection
    $("#DataNumber").val($("#DataNumber").attr("DataNumber"));

  $("#Jobtitle").val($("#Jobtitle").attr("Jobtitle"));


    
    $("#Jobtitle").change(function () {
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
        let Jobtitles = $("#Jobtitle").val();


        let url = `/hrm/employee_galery?DataNumber=${entries}&Jobtitle=${Jobtitles}&page=${page}`;

        if (search != "") {
            url += `&SearchQuery=${search}`;
        }
        

        window.location.replace(url);
       
    }

});