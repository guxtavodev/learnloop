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
  text: "E aí, bro, aqui é onde tu manda ver no que aprendeu. Digita os rolês que tu quer treinar, aí vai pipocar umas perguntas quando tu clicar em 'criar quiz com Learn.Ai'. Depois, responde tudo e manda bala clicando em 'enviar respostas' pra ver se tá certinho",
  icon: 'icon'
})