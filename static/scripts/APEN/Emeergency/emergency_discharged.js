$(document).ready(function () {

    // Update The Entries Selection
    $("#DataNumber").val($("#DataNumber").attr("DataNumber"));

    $("#discharge_status").val($("#discharge_status").attr("discharge_status"));


    $("#discharge_status").change(function () {
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
        let discharge_status = $("#discharge_status").val();

        let url = `/patient/dishcarged-patients-list?DataNumber=${entries}&discharge_status=${discharge_status}&page=${page}`;

        if (search != "") {
            url += `&SearchQuery=${search}`;
        }


        window.location.replace(url);

    }



});