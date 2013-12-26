$(document).ready(function(){
  $(".klembord_button").click(function(){
      product_lijn = $(this).parentsUntil('table').filter('tr').find('.hidden').text()
      copyToClipboard(product_lijn)
  })
})

function copyToClipboard(text) {
  window.prompt("Copy to clipboard: Ctrl+C, Enter", text);
}