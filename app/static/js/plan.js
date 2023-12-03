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

Swal.fire({
  title: 'Conheça o LearnPlan',
  text: "Brother, saca só esse lugar maneiro onde tu manda ver no teu plano de estudos! Dá pra montar na mão mesmo, só digitando o que tu acha que precisa pra estudar um tópico específico. Ou, se quiser moleza, pede pro Learn.Ai criar o plano pra tu, só manda bem na hora de digitar teu objetivo com o plano de estudos. Facinho, né? Vai fundo! 🚀",
  icon: 'icon'
})