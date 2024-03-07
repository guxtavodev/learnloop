// Função para obter informações sobre uma dúvida

function generateRespostasHTML(respostas) {
  let html = '<ul>';
  respostas.forEach(resposta => {
    html += `<li><strong>${resposta.autor}:</strong> ${resposta.texto}</li>`; // Ajuste aqui para acessar a propriedade correta do objeto resposta
  });
  html += '</ul>';
  return html;
}

function getDuvida(duvida) {
  axios.get(`/get-duvida/${duvida}`)
    .then(response => {
      if (response.data.msg === 'success') {
        const infos = response.data.dados;
        const respostasHTML = generateRespostasHTML(response.data.respostas);

        // Exibir informações e respostas em uma janela de diálogo
        Swal.fire({
          title: infos.texto,
          text: infos.autor,
          html: respostasHTML,
          showCloseButton: true,  // Adiciona o botão de fechar
          showCancelButton: true,
          confirmButtonText: 'Deletar Dúvida',
          cancelButtonText: 'Fechar',
          showLoaderOnConfirm: true,
          preConfirm: () => {
            // Chama a função para deletar a dúvida
            return deletarDuvida(duvida);
          },
        });
      } else {
        window.location.href = '/login';
      }
    })
    .catch(error => {
      console.error('Erro ao obter dúvida:', error);
    });
}

// Função para deletar uma dúvida
function deletarDuvida(duvidaId) {
  return axios.post('/deletar-duvida', { duvidaId })
    .then(response => {
      if (response.data.msg === 'success') {
        Swal.fire({
          title: 'Dúvida deletada com sucesso!',
          icon: 'success',
        });

        // Adapte esta parte para remover a dúvida da interface
        // Exemplo: document.getElementById('duvida-container').remove();
      } else {
        Swal.fire({
          title: 'Erro ao deletar dúvida',
          text: response.data.msg,
          icon: 'error',
        });
      }
    })
    .catch(error => {
      console.error('Erro ao deletar dúvida:', error);
      Swal.fire({
        title: 'Erro ao deletar dúvida',
        text: 'Ocorreu um erro ao tentar deletar a dúvida.',
        icon: 'error',
      });
    });
}


// Função para adicionar uma nova dúvida
function addDuvida() {
  Swal.fire({
    title: 'Publicar Dúvida (sua dúvida não será deletada)',
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

            document.querySelector(".list-duvidas").innerHTML += `
              <div>
                <p onclick='getDuvida("${response.data.id}")'><strong>${result.value}</strong></p>
                <button style='margin-top: 1em;' onclick='responderDuvida("${response.data.id}")'>Responder Dúvida</button>
              </div>
            `
          } else {
            window.location.href = '/login'
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