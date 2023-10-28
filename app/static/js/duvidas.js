// Função para obter informações sobre uma dúvida
function getDuvida(duvida) {
  axios.get(`/get-duvida/${duvida}`)
    .then((response) => {
      if (response.data.msg === 'success') {
        var infos = response.data.dados;
        var respostasHTML = '';
        console.log(infos)
        console.log(response.data.respostas)

        // Construir o HTML das respostas
        response.data.respostas.forEach((res) => {
          respostasHTML += `
            <p><strong>${res['autor']}:</strong> ${res['texto']}</p>
          `;
        });

        // Exibir informações e respostas em uma janela de diálogo
        Swal.fire({
          title: infos['texto'],
          text: infos['autor'],
          html: respostasHTML,
        });
      }
    });
}

// Função para adicionar uma nova dúvida
function addDuvida() {
  Swal.fire({
    title: 'Publicar Dúvida',
    html: `
      <input type='text' placeholder='Digite a sua dúvida' id='duvida'>
    `,
    showCancelButton: true,
    confirmButtonText: 'Publicar',
    preConfirm: () => {
      const duvida = document.querySelector('#duvida').value;
      if (!duvida) {
        Swal.showValidationMessage('Por favor, digite a sua dúvida.');
      }
      return duvida;
    },
  }).then((result) => {
    if (result.isConfirmed) {
      axios.post('/create-duvidas', {
        texto: result.value,
        
      })
        .then((response) => {
          if (response.data.msg === 'success') {
            Swal.fire({
              title: 'Dúvida publicada com sucesso!',
              icon: 'success',
            });
          }
        });
    }
  });
}

// Função para responder a uma dúvida
function responderDuvida(duvidaId) {
  Swal.fire({
    title: 'Responder Dúvida',
    html: `
      <input type='text' placeholder='Digite a sua resposta' id='resposta-duvida'>
    `,
    showCancelButton: true,
    confirmButtonText: 'Responder',
    preConfirm: () => {
      const resposta = document.querySelector('#resposta-duvida').value;
      if (!resposta) {
        Swal.showValidationMessage('Por favor, digite a sua resposta.');
      }
      return resposta;
    },
  }).then((result) => {
    if (result.isConfirmed) {
      axios.post('/responder-duvida', {
        duvidaId: duvidaId,
        resposta: result.value,
      })
        .then((response) => {
          if (response.data.msg === 'success') {
            Swal.fire({
              title: 'Sucesso!',
              text: 'Sua resposta foi enviada com sucesso!',
              icon: 'success',
            });
          }
        });
    }
  });
}


function search() {
  var search = prompt("Digite o que você quer pesquisar:")
  if(search == false) {
    return;
  } else {
    axios.get("/search/artigos?pesquisa="+search)
  }
}

function excluirConta() {
  var senha = prompt("Digite sua senha para deletar sua conta:")
  if(senha === false) {
    return;
  } else {
    axios.post("/api/delete-user", {
      "senha": senha
    }).then((r) => {
      if(r.data.msg === "usuario deletado com sucesso") {
        window.location.href = "/login"
      } else {
        Swal.fire({
          title: 'Erro!',
          text: 'Senha incorreta!',
          icon: 'error',
        });
      }
    })
  }
}