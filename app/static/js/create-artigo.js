// Adiciona um ouvinte de evento para salvar o conteúdo antes de sair da página
document.addEventListener('beforeunload', function() {
  const resumo = document.getElementById('conteudo-art').value;
  localStorage.setItem('conteudoArtigo', resumo);
});

function gerarArtigo() {
  // Recuperar o conteúdo salvo (se existir)
  const conteudoSalvo = localStorage.getItem('conteudoArtigo') || '';

  Swal.fire({
    title: 'Learn.Ai - Gerar Artigo a partir de Resumos',
    html: `
      <textarea id="res" placeholder="Digite o resumo do que você entendeu em sala de aula">${conteudoSalvo}</textarea>
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
          const respostaGPT3 = response.data.response;
          document.getElementById('conteudo-art').value = respostaGPT3;
          localStorage.setItem('conteudoArtigo', resumo);
        })
        .catch(error => {
          Swal.fire('Erro ao gerar plano', error.message, 'error');
        });
    }
  });
}

function previewArtigo() {
  var artigo = document.getElementById("conteudo-art").value 
  var converter = new showdown.Converter();
  var htmlContent = converter.makeHtml(artigo);

  Swal.fire({
    title: 'Preview do artigo',
    html: htmlContent
  });
}
