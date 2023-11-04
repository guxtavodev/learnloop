function redacao() {
  var title = document.getElementById("titulo")
  var conteudo = document.getElementById("conteudo")

  axios.post("/learn-ai/redacao", {
    title: title.value,
    content: conteudo.value
}).then((r) => {
  if (r.data.msg === "success") {
    document.getElementById("resposta").innerHTML = r.data.response
  } else {
    document.getElementById("resposta").innerHTML = "Erro ao enviar redação"
  }
})
}