<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script>
// ugly Jinja hacked in variables.
var TAX = {{ county.tax }};
var GOLD_CHANGE = {{ county.get_gold_change() }};
var HAPPINESS_CHANGE = {{ county.get_happiness_change() }};
var GRAIN_STORAGE_CHANGE = {{ county.grain_storage_change() }};
var RATIONS = {{ county.rations }};
var FOOD_EATEN = {{ county.get_food_to_be_eaten() }};
var NOURISHMENT_CHANGE = {{ county.get_nourishment_change() }};
// end of Jinja code. Please keep it inside here.

function sendForm (form, callback) {
    $.ajax({
        url: form.attr("action"),
        method: "POST",
        // need to verify csrf id, I might be wrong.
        headers: {"X-CSRF-TOKEN": $("#csrf_token").val()},
        data: form.serialize(),
        dataType: "json",  // type of data returned, not type sent.
    })
    .always(function (data, status) {
            if (status === "success") {
                console.log()
                callback(data);
            } else {
                console.log(data);
            }
    });
}

// The constants are defined at the beginning and use evil Jinja in JS.
var app = new Vue({
  el: '#economy-form',
  data: {
    goldChange: GOLD_CHANGE,
    selectedTaxRate: TAX,
    happinessChange: HAPPINESS_CHANGE,
    grainStorageChange: GRAIN_STORAGE_CHANGE,
    selectedRations: RATIONS,
    foodEaten: FOOD_EATEN,
    nourishmentChange: NOURISHMENT_CHANGE
  },
  methods: {
    updatePage: function (data) {
      this.goldChange = data.goldChange;
      this.happinessChange = data.happinessChange;
      this.grainStorageChange = data.grainStorageChange;
      this.foodEaten = data.foodEaten;
      this.nourishmentChange = data.nourishmentChange;
    }
  },
  watch: {
    selectedTaxRate: function () {
      sendForm($("#economy-form"), this.updatePage);
    },
    selectedRations: function () {
      sendForm($("#economy-form"), this.updatePage);
    }
  }
});
</script>