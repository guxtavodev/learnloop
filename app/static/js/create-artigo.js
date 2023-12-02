function gerarArtigo() {
  Swal.fire({
    title: 'Learn.Ai - Gerar Artigo a partir de Resumos',
    html: `
      <textarea id="res" placeholder="Digite o resumo do que você entendeu em sala de aula"></textarea>
    `,
    showCancelButton: true,
    confirmButtonText: 'Gerar Artigo',
    preConfirm: () => {
      const resumo = document.getElementById('res').value;
      if (!resumo) {
        Swal.showValidationMessage('Por favor, insira um resumo.');
      }
      return axios.post('/gerar-artigo-ai', { resumo })
        .then(response => {
          // Aqui você pode lidar com a resposta da rota e preencher o input "texto" com a resposta.
          const respostaGPT3 = response.data.response;
          document.getElementById('conteudo-art').value = respostaGPT3;
        })
        .catch(error => {
          // Lidar com erros, exibir uma mensagem de erro, etc.
          Swal.fire('Erro ao gerar plano', error.message, 'error');
        });
    }
  });
}

function previewArtigo() {
  var artigo = document.getElementById("conteudo-art").value 
  // Crie um objeto Showdown
  var converter = new showdown.Converter();

  // Converta o Markdown para HTML
  var htmlContent = converter.makeHtml(artigo);

  Swal.fire({
    title: 'Preview do artigo',
    html: htmlContent
  })
}