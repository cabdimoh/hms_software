``
` javascript
$(document).ready(function () {
  // Global variables
  let track_elements = 2; // Tracks how many elements have been added to the DOM
  var available_items = get_available_items(); // Number of items to add to the DOM

  function get_available_items() {
    let list = "";
    $.ajax({
      method: "POST",
      url: "/logistics/manage_statioanry/get_available_items",
      headers: { "X-CSRFToken": csrftoken },
      async: false,
      success: function (response) {
        if (!response.isError) {
          list = response.Message;
        } else {
          Swal.fire({
            title: "Something Wrong!!",
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

    return list;
  }

  function return_option_elements() {
    let options = "";
    available_items.forEach((item, index) => {
      options += ` < option value = "${item.id}"
remaining = "${item.remaining}" > $ { item.name } < /option>`;
});

return options;
}

// Rendering new elements
$(".add_new_item").on("click", function(e) {
    e.preventDefault();

    // Create new element
    let new_item = `
    <div class="col-md-12  order_element_${track_elements}" row=${track_elements}>
        <div class="row">
          <div class="col-md-3">
              <div class="mb-3">
                  <label for="" class="form-label">Select Item</label>
                  <select name="" id="stationary_item" class="form-control stationary_item_${track_elements}" row=${track_elements}>
                      ${return_option_elements()}
                  </select>
              </div>
          </div>
          <div class="col-md-2">
              <div class="mb-3">
                  <label for="" class="form-label">Items Available</label>
                  <input type="number" class="form-control remaining_item_${track_elements}" id="remaining_item" placeholder='Number of items available' disabled>
              </div>
          </div>
          <div class="col-md-2">
              <div class="mb-3">
                  <label for="" class="form-label">Number Of Items</label>
                  <input type="number" class="form-control quantity_${track_elements}" id="quantity" row=${track_elements} placeholder='Number of items'>
              </div>
          </div>
          <div class="col-md-5">
              <div class="mb-3">
                  <label for="" class="form-label">Description ( Optional )</label>
                  <div class="input-group">
                      <input type="text" class="form-control description_${track_elements}" id="description" aria-label="Recipient's username" aria-describedby="button-addon2" placeholder='Description.....'>
                      <button class="btn btn-danger remove_item" type="button" id="button-" row=${track_elements}><i class="bx bx-trash-alt"></i></button>
                  </div>
              </div>
          </div>
        </div>
    </div>
    `;

    // Attach the new item to the list
    $(".render_items").append(new_item);

    // Add the new item to the order informatiom
    $(".order_information_summary").append(
        `
      <div class="col-md-12 order_summary_${track_elements}">
          <div class="row">
              <div class="col-md-6 text-left">
                  <p id="title">----</p>
              </div>
              <div class="col-md-6 d-flex justify-content-end align-items-center">
                  <p id="quantity_number">--</p>
              </div>
          </div>
      </div>
      `
    );

    // Increase the tracker value
    track_elements += 1;

    SummarizeOrder();
});

// Removing the item from the list
$("#render_items").on("click", ".remove_item", function() {
    let row = $(this).attr("row");
    $(".order_element_" + row).remove();
    $(".order_summary_" + row).remove();

    // Reset the tracker value to 1
    track_elements = 2;

    // Update previous elements
    $("#render_items .col-md-12").each(function(index, item) {
        // index > 0
        // means that the first col-md-12 will no be deleted
        if (index > 0) {
            // Get the row element
            row = $(this).attr("row");

            // Modify the parent element
            $(this).removeClass("order_element_" + row);
            $(this).addClass("order_element_" + track_elements);
            $(this).attr("row", track_elements);

            // Updating the order details
            let orderDetailElement = document.querySelector(
                ".order_summary_" + row
            );

            orderDetailElement.classList.remove("order_summary_" + row);
            orderDetailElement.classList.add("order_summary_" + track_elements);

            // Modify element's children
            $(this).find(".remove_item").attr("row", track_elements);
            $(this)
                .find("#stationary_item")
                .removeClass("stationary_item_" + row);
            $(this)
                .find("#remaining_item_")
                .removeClass("remaining_item_" + row);
            $(this)
                .find("#quantity")
                .removeClass("quantity_" + row);
            $(this)
                .find("#stationary_item")
                .addClass("stationary_item_" + track_elements);
            $(this)
                .find("#remaining_item_")
                .addClass("remaining_item_" + track_elements);
            $(this)
                .find("#quantity")
                .addClass("quantity_" + track_elements);

            // Increase the tracker value
            track_elements += 1;
        }
    });

    SummarizeOrder();
});

// Reset the tracker value and elements been generated
$("#reset_elements").on("click", function(e) {
    e.preventDefault();

    $(".render_items").html("");
    track_elements = 2;
});

// Gathering generated elements with their respective values
// and saving them in the database
$("#save_changes").on("click", function(e) {
    e.preventDefault();
    let formData = new FormData();

    // Get all elements generated
    let types = [];
    let remainings = [];
    let quantities = [];
    let description = [];

    // loop through tracke elements
    for (let i = 1; i < track_elements; i++) {
        types.push($(".stationary_item_" + i).val());
        remainings.push($(".remaining_item_" + i).val());
        quantities.push($(".quantity_" + i).val());
        description.push($(".description_" + i).val());
    }

    formData.append("items", types);
    formData.append("remainings", remainings);
    formData.append("quantities", quantities);
    formData.append("description", description);
    formData.append("employee", $("#search_employee").attr("userid"));

    $.ajax({
        method: "POST",
        url: "/logistics/manage_statioanry/RequestOrder",
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        async: false,
        success: function(response) {
            if (!response.isError) {
                list = response.Message;
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
});

// Performinmg the employee search
// Performing autocomplete function
$("#search_employee").on("input", function(e) {
    $("#search_employee").removeAttr("userid");
    var listUsers = [];
    if ($(this).val() != "" && $(this).val().length > 3) {
        listUsers = SearchEngine($(this).val());

        $("#search_employee").autocomplete({
            source: listUsers,
            select: function(event, ui) {
                const item = ui.item.userid;
                const value = ui.item.value;

                if (value != "") {
                    $("#search_employee").attr("userid", item);
                    $(".card_display").removeClass("d-none");
                }
            },
            response: function(event, ui) {
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
        success: function(data) {
            $(".users-body .list").html("");
            data.Message.forEach((user) => {
                list.push(user);
            });
        },
    });

    return list;
}

$("#render_items").on("change", "#stationary_item", function() {
    SummarizeOrder();

    const row = $(this).attr("row");
    $(".remaining_item_" + row).val("");

    $(".quantity_" + row).removeClass("border");
    $(".quantity_" + row).removeClass("border-danger");
    $(".quantity_" + row).removeClass("text-danger");

    if ($(this).val() != "") {
        $(".remaining_item_" + row).val(
            $("option:selected", this).attr("remaining")
        );

        const remaining = $("option:selected", this).attr("remaining");

        if (parseInt($(".quantity_" + row).val()) > parseInt(remaining)) {
            $(".quantity_" + row).addClass("border");
            $(".quantity_" + row).addClass("border-danger");
            $(".quantity_" + row).addClass("text-danger");
        }
    }
});

$("#render_items").on("input", "#quantity", function() {
    if ($(this).val() < 0) {
        $(this).val(0);
    }

    $(this).removeClass("border");
    $(this).removeClass("border-danger");
    $(this).removeClass("text-danger");

    const row = $(this).attr("row");
    const remaining = $("option:selected", ".stationary_item_" + row).attr(
        "remaining"
    );

    if (parseInt($(this).val()) > parseInt(remaining)) {
        $(this).addClass("border");
        $(this).addClass("border-danger");
        $(this).addClass("text-danger");
    }

    SummarizeOrder();
});

$("#render_items").on("input", "#description", function() {
    SummarizeOrder();
});

function SummarizeOrder() {
    let total = 0;

    for (var i = 1; i < track_elements; i++) {
        let name = $("option:selected", ".stationary_item_" + i).val();
        let quantity = $(".quantity_" + i).val();

        $(".order_summary_" + i + " #title").text("--");
        $("#total_quantity_order").text("--");

        // check if the values are none or null
        if (name != "") {
            $(".order_summary_" + i + " #title").text(
                $("option:selected", ".stationary_item_" + i).text()
            );
        }

        if (quantity != "") {
            quantity = parseInt(quantity);
            $(".order_summary_" + i + " #quantity_number").text(quantity);

            total += quantity;
        }
    }

    if (total != 0) {
        $("#total_quantity_order").text(total);
    }
}
});

``
`