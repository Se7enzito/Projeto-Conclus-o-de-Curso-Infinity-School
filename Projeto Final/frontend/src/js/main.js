// Mostrar senha
var senha = $('#senha');
var olho = $("#olho");

olho.click(function() {
  var type = senha.attr("type") === "password" ? "text" : "password";
  senha.attr("type", type);
});
