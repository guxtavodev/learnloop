

function gerarQuiz() {
  var resposta = document.querySelector("#info-topic").value
  
  if(resposta === "" || resposta === " ") {
    return document.querySelector("#info-topic").value = "Digite algo válido"
  }
  document.querySelector("#question").innerHTML = "Espera rapidinho..."
  axios.post("/gerar/quiz", {
    "dificuldades": resposta
  }).then((r) => {
    if(r.data.msg === "success") {
      document.querySelector("#question").innerHTML = r.data.response

      
    }
  })
}

function corrigirQuiz() {
var resposta = document.querySelector("#answer").value
  if(resposta === "" || resposta === " ") {
    return document.querySelector("#answer").value = "Digite algo válido"
  }
document.querySelector("#answer").value = "Calma aí..."
  
  axios.post("/corrigir/quiz", {
    "pergunta": document.querySelector("#question").innerText,
    "resposta": resposta
  }).then((r) => {
    if(r.data.msg === "success") {
      
        
      document.querySelector("#answer").value = r.data.response

      Swal.fire("Correção", r.data.response, "success")
      
    }
  })
}

Swal.fire({
  title: 'Conheça o LearnQuiz',
  text: "Olá! Seja bem vindo(a) ao LearnQuiz! O recurso inédito do LearnLoop! Aqui você digita a anotação/resumo de um assunto que você quer treinar no campo de texto abaixo dos botões, clicar em 'criar pergunta com Learn.Ai', ele vai gerar perguntas básicas para você treinar, após você responder as perguntas, clica em 'Envia Resposta', para ele corrigir automaticamente as questões, e com dicas de como não errar novamente na hora da prova/simulado etc. Bem legal, né? Se tiver dúvidas, pode ir no Direct no Instagram @learnloop.of",
  icon: 'icon'
})