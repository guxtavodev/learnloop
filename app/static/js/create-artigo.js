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
      return axios.post('/api/gerar-artigo-ai', { resumo })
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


function gerarArtigoCaderno() {
  Swal.fire({
    title: 'Learn.Ai - Gerar Artigo a partir de Caderno',
    html: `
      <input type="file" id="foto-caderno" />
    `,
    showCancelButton: true,
    confirmButtonText: 'Gerar Artigo',
    preConfirm: () => {
      const fotoCaderno = document.getElementById('foto-caderno').files[0];
      if (!fotoCaderno) {
        Swal.showValidationMessage('Por favor, envie uma imagem.');
      }
      
      const formData = new FormData();
      formData.append('foto', fotoCaderno);

      return axios.post('/api/gerar-artigo', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => {
        const artigo = response.data.artigo;
        document.getElementById('conteudo-art').value = artigo;
        localStorage.setItem('conteudoArtigo', artigo);
      })
      .catch(error => {
        Swal.fire('Erro ao gerar artigo', error.message, 'error');
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

Swal.fire({
  title: 'Conheça o Criador de Artigo',
  text: "Olá, seja bem vindo ao criador de artigo do LearnLoop! Aqui, você cria artigos que pode servir para você mesmo, futuramente, e de bônus ainda ajuda outros estudantes, você pode ir em 'Criar com Learn.Ai', digita algum resumo ou anotação do quadro ou do caderno, e o Learn.Ai vai gerar um artigo bem descontraído, leve e compreensível, ajudando você de fato, aprender algum novo assunto.",
  icon: 'icon'
})