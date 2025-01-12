
  function onClickedEstimateRevenue() {
    console.log("Estimate price button clicked");
    var no_of_customers = document.getElementById("uiCustomer");
    var menu_price = document.getElementById("uiMenuPrice");
    var marketing_spend = document.getElementById("uiMarketingSpend");
    var cuisine_type = document.getElementById("cuisine_type");
    var estimatedRevenue = document.getElementById("uiEstimatedRevenue");

    var url = "http://127.0.0.1:5000/predict_monthly_revenue"; 
  
    $.post(url, {
        number_of_customers: parseInt(no_of_customers.value),
        menu_price: parseFloat(menu_price.value),
        marketing_spend: parseFloat(marketing_spend.value),
        cuisine_type: cuisine_type.value
    },function(data, status) {
        console.log(data.estimated_revenue);
        estimatedRevenue.innerHTML = "<h2> Rs. " + data.estimated_revenue.toString() + " K </h2>";
        console.log(status);
    });
  }
  
  function onPageLoad() {
    console.log( "document loaded" );
    var url = "http://127.0.0.1:5000/get_cuisine_type";
    $.get(url,function(data, status) {
      console.log("got response for get_location_names request");
      if(data) {
        var cuisine_type = data.cuisine_Type;
        var uiCuisine_type = document.getElementById("cuisine_type");
        $('#cuisine_type').empty();
  
        // Add the default option
        var defaultOption = new Option("Choose a Location", "", true, true);
        $('#cuisine_type').append(defaultOption);
  
        for(var i in cuisine_type) {
          var capitalizedCuisineType = cuisine_type[i].charAt(0).toUpperCase() + cuisine_type[i].slice(1);
          var opt = new Option(capitalizedCuisineType);
          $('#cuisine_type').append(opt);
        }
      } else {
        console.error("Failed to get cuisine data");
      }
    });
  }
  
  $(document).ready(function() {
    console.log( "document loaded" );
    onPageLoad();
  });
  