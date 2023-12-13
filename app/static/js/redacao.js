function redacao() {
  var title = document.getElementById("titulo")
  var conteudo = document.getElementById("conteudo")

  
  
  document.getElementById("resposta").innerHTML = "<p>Esperando resposta...</p>"
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

Swal.fire({
  title: "Conheça o Treino de Redação",
  text: "Mano, aqui é o local pra você mandar a sua redação e receber umas dicas maneiras do Learn.Ai, a inteligência artificial do LearnLoop! Isso é tipo o esquema perfeito pra estudar, né não? E relaxa, a sua redação não fica salva na nossa base de dados, tudo suave! Tamo junto na missão de melhorar esse textão pro ENEM, bora nessa? ✍️💡",
  icon: 'info'
})