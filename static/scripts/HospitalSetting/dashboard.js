$(document).ready(function() {
// Generate the year buttons dynamically
var yearDropdown = document.querySelector(".year_list");
var currentYear = new Date().getFullYear();
for (var year = currentYear; year >= currentYear - 3; year--) {
    var button = document.createElement("a");
    button.classList.add("dropdown-item", "btn");
    button.dataset.year = year;
    button.textContent = year.toString();
    if (year === currentYear) {
        button.classList.add("active");
        document.querySelector("#selected_year").textContent = currentYear;
    }
    yearDropdown.appendChild(button);
}

// Set the initial selected year to the current year
var selectedYear = currentYear;

// Update the chart or table based on the current year
updateChart(selectedYear);

// Add a click event listener to the year dropdown
yearDropdown.addEventListener("click", function(event) {
    var button = event.target.closest(".dropdown-item");
    if (button) {
        var year = parseInt(button.dataset.year);
        if (year !== selectedYear) {
            selectedYear = year;
            document.querySelector("#selected_year").textContent = selectedYear;
            updateChart(selectedYear);
        }
        yearDropdown.classList.remove("show");
    }
});
 
function updateChart(year) {
    // Prepare the form data
    let formData = new FormData();
    // Append data to form data
    formData.append("yearr", year);

    console.log(year);

    $.ajax({
        method: "POST",
        url: "/patient/manage-appointment/getChartData",
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        async: true,
        data: formData,
        success: function(response) {
            if (!response.isError) {
                console.log(response.Message.completed_may);
                function getChartColorsArray(t){if(null!==document.getElementById(t)){t=document.getElementById(t).getAttribute("data-colors");
                if(t)return(t=JSON.parse(t)).map(function(t){var e=t.replace(" ","");
                return-1===e.indexOf(",")?getComputedStyle(document.documentElement).getPropertyValue(e)||e:2==(t=t.split(",")).length?"rgba("+getComputedStyle(document.documentElement).getPropertyValue(t[0])+","+t[1]+")":e})}}
               
                
                var chartColumnColors=getChartColorsArray("column_chart1"),
                chartColumnDatatalabelColors=(
                    chartColumnColors&&(
                        options={
                            chart:{height:350,type:"bar",toolbar:{show:!1}},
                            plotOptions:{bar:{horizontal:!1,columnWidth:"45%",endingShape:"rounded"}},
                            dataLabels:{enabled:!1},stroke:{show:!0,width:2,colors:["transparent"]},
                            series: [{ name: "Completed Appointments", data: [response.Message.completed_jan, response.Message.completed_feb, response.Message.completed_mar, response.Message.completed_april, response.Message.completed_may, response.Message.completed_jun, response.Message.completed_july, response.Message.completed_aug, response.Message.completed_sep, response.Message.completed_oct, response.Message.completed_nov, response.Message.completed_dec] },
                                    { name: "Appointments", data: [response.Message.all_jan, response.Message.all_feb, response.Message.all_mar, response.Message.all_april, response.Message.all_may, response.Message.all_jun, response.Message.all_july, response.Message.all_aug, response.Message.all_sep, response.Message.all_oct, response.Message.all_nov, response.Message.all_dec] },
                                    { name: "Cancelled Appointments", data: [response.Message.cancelled_jan, response.Message.cancelled_feb, response.Message.cancelled_mar, response.Message.cancelled_april, response.Message.cancelled_may, response.Message.cancelled_jun, response.Message.cancelled_july, response.Message.cancelled_aug, response.Message.cancelled_sep, response.Message.cancelled_oct, response.Message.cancelled_nov, response.Message.cancelled_dec] }
                                ],
                                colors:chartColumnColors,xaxis:{categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] },
                                yaxis:{title:{text:" (Appointments)"}},
                                grid:{borderColor:"#f1f1f1"},
                                fill:{opacity:1},
                                tooltip:{y:{formatter:function(t){return" "+t+" Patients"}}}},
                    (chart=new ApexCharts(document.querySelector("#column_chart1"),options)).render()
                    ));
            }
        },
        error: function(xhr, status, error) {
            console.log("Error fetching chart data:", error);
        }
    });
}
       
})

    
    $(".year_list").on("click", "#2022", function () {

        appointmentchart(
        "2022",
        );
    });

    $(".year_list").on("click", "#2021", function () {

        appointmentchart(
        "2021",
        );
    });
    
    $(".year_list").on("click", "#2020", function () {

        appointmentchart(
        "2020",
        );
    });

    // Finction to handle job approval
    function appointmentchart(year) {
        // Prepare the form data
        let formData = new FormData();
        // Append data to form data
        formData.append("yearr", year);
        var cacheBuster = new Date().getTime(); // Get current timestamp

        console.log(year);

        $.ajax({
            method: "POST",
            url: "/patient/manage-appointment/getChartData?cache=" + cacheBuster, 
            headers: { "X-CSRFToken": csrftoken },
            processData: false,
            contentType: false,
            async: false,
            data: formData,
            success: function(response) {
                if (!response.isError) {
                    var chartColumnColors=getChartColorsArray("column_chart"),
                    chartColumnDatatalabelColors=(
                        chartColumnColors&&(
                            options={
                                chart:{height:350,type:"bar",toolbar:{show:!1}},
                                plotOptions:{bar:{horizontal:!1,columnWidth:"45%",endingShape:"rounded"}},
                                dataLabels:{enabled:!1},stroke:{show:!0,width:2,colors:["transparent"]},
                                series: [{ name: "Completed Appointments", data: [response.Message.completed_jan, response.Message.completed_feb, response.Message.completed_mar, response.Message.completed_april, response.Message.completed_may, response.Message.completed_jun, response.Message.completed_july, response.Message.completed_aug, response.Message.completed_sep, response.Message.completed_oct, response.Message.completed_nov, response.Message.completed_dec] },
                                        { name: "Appointments", data: [response.Message.all_jan, response.Message.all_feb, response.Message.all_mar, response.Message.all_april, response.Message.all_may, response.Message.all_jun, response.Message.all_july, response.Message.all_aug, response.Message.all_sep, response.Message.all_oct, response.Message.all_nov, response.Message.all_dec] },
                                        { name: "Cancelled Appointments", data: [response.Message.cancelled_jan, response.Message.cancelled_feb, response.Message.cancelled_mar, response.Message.cancelled_april, response.Message.cancelled_may, response.Message.cancelled_jun, response.Message.cancelled_july, response.Message.cancelled_aug, response.Message.cancelled_sep, response.Message.cancelled_oct, response.Message.cancelled_nov, response.Message.cancelled_dec] }
                                    ],
                                    colors:chartColumnColors,xaxis:{categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] },
                                    yaxis:{title:{text:" (Appointments)"}},
                                    grid:{borderColor:"#f1f1f1"},
                                    fill:{opacity:1},
                                    tooltip:{y:{formatter:function(t){return" "+t+" Patients"}}}},
                        (chart=new ApexCharts(document.querySelector("#column_chart"),options)).render()
                        ));

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
        
        }   




//      -------------------------------------------inventory type  ----------------------------------------------------------------------


        $(".medicinechart_year_list").on("click", "#2023", function () {

            inventorychart(
            "2023",
            );
        });
        
        $(".medicinechart_year_list").on("click", "#2022", function () {
    
            inventorychart(
            "2022",
            );
        });
    
        $(".medicinechart_year_list").on("click", "#2021", function () {
    
            inventorychart(
            "2021",
            );
        });
        
        $(".medicinechart_year_list").on("click", "#2020", function () {
    
            inventorychart(
            "2020",
            );
        });
    
        // Finction to handle job approval
        function inventorychart(year) {
            // Prepare the form data
            let formData = new FormData();
            // Append data to form data
            formData.append("yearr", year);
            
    
            console.log(year);
    
            $.ajax({
                method: "POST",
                url: "/inventory/manage-medicine/i_inventory", 
                headers: { "X-CSRFToken": csrftoken },
                processData: false,
                contentType: false,
                async: false,
                data: formData,
                success: function(response) {
                    if (!response.isError) {
                        var upadatedonutchart,chartPieBasicColors=getChartColorsArray("medicinechart"),
                        chartDonutBasicColors=(chartPieBasicColors&&(options={series:[response.Message.mediicne_list,response.Message.MedicineListpaid,response.Message.ExpireMedicine],
                        chart:{height:320,type:"pie"},labels:["Purchase Medicne","Dispensed Medicine","Expired Medicine"],legend:{position:"bottom"},
                        dataLabels:{dropShadow:{enabled:!1}},colors:chartPieBasicColors},
                        (chart=new ApexCharts(document.querySelector("#medicinechart"),options)).render()));
                        


                        // var upadatedonutchart,chartPieBasicColors=getChartColorsArray("equipmentchart"),
                        // chartDonutBasicColors=(chartPieBasicColors&&(options={series:[response.Message.parchase_equipment,response.Message.paid_equipment,response.Message.lost_and_damaged_equipment],
                        // chart:{height:320,type:"pie"},labels:["Purchase Equipment","Paid Equipment","Lost And Dameged Equipment"],legend:{position:"bottom"},
                        // dataLabels:{dropShadow:{enabled:!1}},colors:chartPieBasicColors},
                        // (chart=new ApexCharts(document.querySelector("#equipmentchart"),options)).render()));
                        
                        
                   


                
    
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


        
            
            }   

        

        
        
            $(".equipment_year_list").on("click", "#2023", function () {

                equipmentchart(
                "2023",
                );
            });
            
            $(".equipment_year_list").on("click", "#2022", function () {
        
                equipmentchart(
                "2022",
                );
            });
        
            $(".equipment_year_list").on("click", "#2021", function () {
        
                equipmentchart(
                "2021",
                );
            });
            
            $(".equipment_year_list").on("click", "#2020", function () {
        
                equipmentchart(
                "2020",
                );
            });
        
            // Finction to handle job approval
            function equipmentchart(year) {
                // Prepare the form data
                let formData = new FormData();
                // Append data to form data
                formData.append("yearr", year);
                
        
                console.log(year);
        
                $.ajax({
                    method: "POST",
                    url: "/inventory/manage-equipment/dashequipment", 
                    headers: { "X-CSRFToken": csrftoken },
                    processData: false,
                    contentType: false,
                    async: false,
                    data: formData,
                    success: function(response) {
                        if (!response.isError) {
                           
                            
    
    
                            var upadatedonutchart,chartPieBasicColors=getChartColorsArray("equipmentchart"),
                            chartDonutBasicColors=(chartPieBasicColors&&(options={series:[response.Message.parchase_equipment,response.Message.paid_equipment,response.Message.lost_and_damaged_equipment],
                            chart:{height:320,type:"pie"},labels:["Purchase Equipment","Paid Equipment","Lost And Dameged Equipment"],legend:{position:"bottom"},
                            dataLabels:{dropShadow:{enabled:!1}},colors:chartPieBasicColors},
                            (chart=new ApexCharts(document.querySelector("#equipmentchart"),options)).render()));
                            
                            
                       
    
    
                    
        
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
    
    
            
                
                }
            

            

           

            

