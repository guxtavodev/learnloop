function gerarQuiz() {
  var resposta = document.querySelector("#area").value

  if(resposta === "" || resposta === " ") {
    return document.querySelector("#area").value = "Digite algo válido"
  }
  document.querySelector("#area").value = "Espera rapidinho..."
  axios.post("/gerar/quiz", {
    "dificuldades": resposta
  }).then((r) => {
    if(r.data.msg === "success") {
      document.querySelector("#area").value = r.data.response

      
    }
  })
}

function corrigirQuiz() {
var resposta = document.querySelector("#area").value
  if(resposta === "" || resposta === " ") {
    return document.querySelector("#area").value = "Digite algo válido"
  }
document.querySelector("#area").value = "Calma aí..."
  
  axios.post("/corrigir/quiz", {
    "quiz": resposta
  }).then((r) => {
    if(r.data.msg === "success") {
      
        
      document.querySelector("#area").value = r.data.response
    }
  })
}

Swal.fire({
  title: 'Conheça o LearnQuiz',
  text: "Olá! Seja bem vindo(a) ao LearnQuiz! O recurso inédito do LearnLoop! Aqui você digita a anotação/resumo de um assunto que você quer treinar, clicar em 'criar quiz com Learn.Ai', ele vai gerar 5 perguntas básicas para você treinar, após você responder todas as perguntas, clica em 'Enviar Respostas', para ele corrigir automaticamente as questões, e com dicas de como não errar novamente na hora da prova/simulado etc. Bem legal, né? Se tiver dúvidas, pode ir no Direct no Instagram @learnloop.of",
  icon: 'icon'
})