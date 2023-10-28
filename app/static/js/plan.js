function gerarPlano() {
  Swal.fire({
    title: 'Learn.Ai - Gerar Plano de Estudos',
    html: `
      <textarea id="res" placeholder="Digite o seu próposito com o plano de estudos"></textarea>
    `,
    showCancelButton: true,
    confirmButtonText: 'Gerar Plano',
    preConfirm: () => {
      const resumo = document.getElementById('res').value;
      if (!resumo) {
        Swal.showValidationMessage('Por favor, insira um resumo.');
      }
      return axios.post('/gerar-plano-ai', { resumo })
        .then(response => {
          // Aqui você pode lidar com a resposta da rota e preencher o input "texto" com a resposta.
          const respostaGPT3 = response.data.response;
          document.getElementById('texto-plan').innerHTML = respostaGPT3;
        })
        .catch(error => {
          // Lidar com erros, exibir uma mensagem de erro, etc.
          Swal.fire('Erro ao gerar plano', error.message, 'error');
        });
    }
  });
}
