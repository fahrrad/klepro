var marge = 0.0

function toFixed(value, precision) {
    var precision = precision || 0,
    neg = value < 0,
    power = Math.pow(10, precision),
    value = Math.round(value * power),
    integral = String((neg ? Math.ceil : Math.floor)(value / power)),
    fraction = String((neg ? -value : value) % power),
    padding = new Array(Math.max(precision - fraction.length, 0) + 1).join('0');

    return precision ? integral + '.' +  padding + fraction : integral;
}


function copyToClipboard(text) {
  window.prompt("Copy to clipboard: Ctrl+C, Enter", text);
}

function checkSubmit(e)
{
   if(e && e.keyCode == 13)
   {
      document.forms[0].submit();
   }
}

$(document).ready(function(){
  $(".klembord_button").click(function(){
      var product_lijn = $(this).parentsUntil('table').filter('tr').find('.hidden').text()
      var parts = product_lijn.split('\t')
      parts[1] = toFixed(parts[1] * marge, 2)
      product_lijn = parts.join('\t')
      copyToClipboard(product_lijn)
  })

  $(".percent_input").change(function(){
      marge = 1 + ( $(".percent_input").val() / 100)
  })

  // initial change om de waarde te zetten die uit de template komt
  $(".percent_input").change()

    $(".prijs_class_normaal").addClass("btn-default")
    $(".prijs_class_waarschuwing").addClass("btn-warning")
    $(".prijs_class_fout").addClass("btn-danger")
})