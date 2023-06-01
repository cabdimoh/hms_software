$(document).ready(function () {
   
$('#printmodalreveal').on('click', function(e){
    e.preventDefault()
   $('.printPage_modals').modal('show')
})



$(".print_checks").on("click", "input", function () {
    // Select the label
    // Extract the for attribute value
    let label = $(this).parent().find("label").attr("for");

    if ($(this).is(":checked")) {
      // if the all is checked
      // check all inputs
      if (label == "all") {
        $(".print_checks input").each(function () {
          if ($(this).parent().find("label").attr("for") != "job_history") {
            $(this).prop("checked", true);
          } else {
            $(this).prop("checked", false);
          }
        });

        // if all inputs checked then check the all input
        let is_all_checked = true;

        $(".print_checks input").each(function () {
          if (
            !$(this).is(":checked") &&
            $(this).parent().find("label").attr("for") != "all" &&
            $(this).parent().find("label").attr("for") != "job_history"
          ) {
            is_all_checked = false;
          }
        });

        if (is_all_checked) $(".print_checks #all").prop("checked", true);
      }

      if (label == "job_history") {
        $(".print_checks input:checked").each(function () {
          if ($(this).parent().find("label").attr("for") != "job_history") {
            $(this).prop("checked", false);
          }
        });
      } else {
        $(".print_checks #job_history").prop("checked", false);
      }
    } else {
      // if the all is unchecked
      // uncheck all inputs
      if (label == "all")
        $(".print_checks input").each(function () {
          $(this).prop("checked", false);
        });

      if (label != "all") $(".print_checks #all").prop("checked", false);
    }
  });

$("#process_btn").on("click", function (e) {
    e.preventDefault();

    // Get all checked inputs
    let is_checked = false;
    let names = "basicInfo";
    $(".print_checks input").each(function () {
      if (
        $(this).is(":checked") &&
        $(this).parent().find("label").attr("for") != "all"
      ) {
        is_checked = true;

        names +=
          names == ""
            ? $(this).parent().find("label").attr("for")
            : `,${$(this).parent().find("label").attr("for")}`;
      }
    });

    // if any input is checked
    if (is_checked) {
      window.location.replace(
        `/hrm/printEmployee?employee=${employee_id}&inputs=${names}`
      );
    } else {
      Swal.fire({
        title: "Unchecked",
        text: "Please select at least one field to print",
        icon: "error",
        confirmButtonClass: "btn btn-primary w-xs mt-2",
        buttonsStyling: !1,
        showCloseButton: !0,
      });
    }
  });

})