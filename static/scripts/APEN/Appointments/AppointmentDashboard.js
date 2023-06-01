$.ajax({
    method: "POST",
    url: "/patient/manage-appointment/getChartData",
    headers: { "X-CSRFToken": csrftoken },
    processData: false,
    contentType: false,
    async: false,
    success: function(response) {
        if (!response.isError) {

            var columnColors = getChartColorsArray("#column_chart"),
                options = {
                    chart: { height: 350, type: "bar", toolbar: { show: !1 } },
                    plotOptions: { bar: { horizontal: !1, columnWidth: "45%" } },
                    dataLabels: { enabled: !1 },
                    stroke: { show: !0, width: 2, colors: ["transparent"] },
                    series: [{ name: "Completed Appointments", data: [response.Message.completed_jan, response.Message.completed_feb, response.Message.completed_mar, response.Message.completed_april, response.Message.completed_may, response.Message.completed_jun, response.Message.completed_july, response.Message.completed_aug, response.Message.completed_sep, response.Message.completed_oct, response.Message.completed_nov, response.Message.completed_dec] },
                        { name: "Appointments", data: [response.Message.all_jan, response.Message.all_feb, response.Message.all_mar, response.Message.all_april, response.Message.all_may, response.Message.all_jun, response.Message.all_july, response.Message.all_aug, response.Message.all_sep, response.Message.all_oct, response.Message.all_nov, response.Message.all_dec] },
                        { name: "Cancelled Appointments", data: [response.Message.cancelled_jan, response.Message.cancelled_feb, response.Message.cancelled_mar, response.Message.cancelled_april, response.Message.cancelled_may, response.Message.cancelled_jun, response.Message.cancelled_july, response.Message.cancelled_aug, response.Message.cancelled_sep, response.Message.cancelled_oct, response.Message.cancelled_nov, response.Message.cancelled_dec] }
                    ],
                    colors: columnColors,
                    xaxis: { categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] },
                    yaxis: { title: { text: "(Patients)", style: { fontWeight: "500" } } },
                    grid: { borderColor: "#f1f1f1" },
                    fill: { opacity: 1 },
                    tooltip: { y: { formatter: function(e) { return e + " Patients" } } }
                };
            (chart = new ApexCharts(document.querySelector("#column_chart"), options)).render();


            console.log(response.Message.jan_data);

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