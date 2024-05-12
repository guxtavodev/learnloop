
Swal.fire({
  title: 'Conheça o Sessão de Estudos',
  text: "Preparado para elevar sua organização e produtividade nos estudos? Aqui, você tem controle total sobre o que estuda. Inicie o cronômetro, faça anotações e, se necessário, clique em 'Aprimorar anotação com IA' para uma versão mais estruturada. Salve suas sessões de estudo, revise suas anotações e compartilhe seu progresso. Aproveite ao máximo!",
  icon: 'icon'
})





document.addEventListener('DOMContentLoaded', function() {
  let tempoEstudado = '00:00:00'; // Tempo estudado inicial
  let cronometroInterval; // Variável para armazenar o intervalo do cronômetro
  let cronometroRodando = false; // Indicador se o cronômetro está rodando

  // Função para formatar o tempo estudado
  function formatarTempo(segundos) {
    const horas = Math.floor(segundos / 3600);
    const minutos = Math.floor((segundos % 3600) / 60);
    const seg = segundos % 60;
    return `${horas.toString().padStart(2, '0')}:${minutos.toString().padStart(2, '0')}:${seg.toString().padStart(2, '0')}`;
  }

  // Função para iniciar o cronômetro
  function iniciarCronometro() {
    cronometroInterval = setInterval(function() {
      const tempoArray = tempoEstudado.split(':');
      const horas = parseInt(tempoArray[0]);
      const minutos = parseInt(tempoArray[1]);
      const seg = parseInt(tempoArray[2]);

      // Incrementar o tempo estudado
      tempoEstudado = formatarTempo(seg + 1);

      // Atualizar o texto do tempo estudado
      document.getElementById('tempo-estudado').innerText =  tempoEstudado;
    }, 1000);
    cronometroRodando = true;
  }

  // Função para pausar o cronômetro
  function pausarCronometro() {
    clearInterval(cronometroInterval);
    cronometroRodando = false;
  }

  // Função para parar o cronômetro
  function pararCronometro() {
    clearInterval(cronometroInterval);
    tempoEstudado = '00:00:00';
    document.getElementById('tempo-estudado').innerText = tempoEstudado;
    cronometroRodando = false;
  }

  // Botão para iniciar, pausar e parar o cronômetro
  const iniciarBtn = document.querySelector('button#iniciar');
  iniciarBtn.addEventListener('click', function() {
    if (!cronometroRodando) {
      iniciarCronometro();
      iniciarBtn.textContent = 'Pausar';
    } else {
      pausarCronometro();
      iniciarBtn.textContent = 'Continuar';
    }
  });

  // Botão para parar o cronômetro
  const pararBtn = document.querySelector('button#parar');
  pararBtn.addEventListener('click', function() {
    pararCronometro();
    iniciarBtn.textContent = 'Iniciar';
  });

  // Botão para aprimorar anotações com IA
  const aprimorarBtn = document.querySelector('button#aprimorar');
  aprimorarBtn.addEventListener('click', function() {
    const resumo = document.querySelector('textarea#resumo').value;
    document.querySelector("#resumo").value = "Aguarda um pouquinho!"


    
//￼￼￼￼￼￼  Enviar as anotações para o backend
    axios.post('/api/get-resumo-ia', { notes: resumo })
      .then(function(response) {
        const novoResumo = response.data.msg;
        // Atualizar a área de texto com o resumo aprimorado
        document.querySelector('textarea#resumo').value = novoResumo;
      })
      .catch(function(error) {
        console.error('Erro ao aprimorar as anotações:', error);
      });
  });

  // Botão para salvar a sessão de estudos
  const salvarBtn = document.querySelector('button#salvar');
  salvarBtn.addEventListener('click', function() {
    const assunto = document.querySelector('#assunto').value;

    // Enviar os dados da sessão para o backend
    axios.post('/save-session', { assunto: assunto, tempo: tempoEstudado, resumo: document.querySelector("#resumo").value })
      .then(function(response) {
        // Exibir uma mensagem de sucesso ao usuário
        Swal.fire({
          icon: 'success',
          title: 'Sessão de estudos salva!',
          text: `${response.data.msg}`,
          showConfirmButton: false,
          timer: 1500
        });
      })
      .catch(function(error) {
        console.error('Erro ao salvar a sessão de estudos:', error);
      });
  });

  const sessoes = document.querySelectorAll('.sessao-estudos');
  sessoes.forEach(function(sessao) {
    sessao.addEventListener('click', function() {
      const resumo = sessao.getAttribute('data-resumo');
      const assunto = sessao.getAttribute('data-assunto');
      const dia = sessao.getAttribute('data-dia');
      const tempo = sessao.getAttribute('data-tempo');

      // Exibir os dados da sessão em um SweetAlert
      Swal.fire({
        title: 'Detalhes da Sessão de Estudos',
        html: `
          <p><strong>Assunto:</strong> ${assunto}</p>
          <p><strong>Dia:</strong> ${dia}</p>
          <p><strong>Tempo Estudado:</strong> ${tempo}</p>
          <p><strong>Anotação:</strong> ${resumo}</p>
        `,
        icon: 'info',
        confirmButtonText: 'Fechar'
      });
    });
  });
});
