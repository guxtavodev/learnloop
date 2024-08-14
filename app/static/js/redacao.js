function redacao() {
  var title = document.getElementById("titulo");
  var conteudo = document.getElementById("conteudo");

  document.getElementById("resposta").innerHTML = "<p>Esperando resposta...</p>";
  
  axios.post("/learn-ai/redacao", {
    title: title.value,
    content: conteudo.value
  }).then((r) => {
    if (r.data.msg === "success") {
      document.getElementById("resposta").innerHTML = r.data.response;
    } else {
      document.getElementById("resposta").innerHTML = "Erro ao enviar redação";
    }
  }).catch((error) => {
    document.getElementById("resposta").innerHTML = "Erro ao enviar redação";
    console.error("Erro:", error);
  });
}

Swal.fire({
  title: "Conheça o Treino de Redação",
  text: "Mano, aqui é o local pra você mandar a sua redação e receber umas dicas maneiras do Learn.Ai, a inteligência artificial do LearnLoop! Isso é tipo o esquema perfeito pra estudar, né não? E relaxa, a sua redação não fica salva na nossa base de dados, tudo suave! Tamo junto na missão de melhorar esse textão pro ENEM, bora nessa? ✍️💡",
  icon: 'info'
});

function carregarFoto() {
  Swal.fire({
    title: "Carregar Foto",
    description: "Faça o upload da foto de seu caderno aqui",
    html: `
      <input type="file" id="foto" >
    `,
    preConfirm: () => {
      const formData = new FormData();
      var foto = document.getElementById("foto");
      formData.append("foto", foto.files[0]);

      return axios.post("/api/carregar-redacao", formData, {
        headers: {
          "Content-Type": `multipart/form-data; boundary=${formData._boundary}`
        }
      }).then((f) => {
        if (f.data.msg === "success") {
          document.getElementById("conteudo").value = f.data.redacao;
        }
      }).catch((error) => {
        console.error("Erro ao carregar a foto:", error);
      });
    }
  });
}

function salvarRedacao() {
  var titulo = document.getElementById("titulo").value;
  var texto = document.getElementById("conteudo").value;

  Swal.fire({
    title: "Salvando sua redação...",
    text: "Por favor, aguarde.",
    icon: "info",
    allowOutsideClick: false,
    showConfirmButton: false,
    didOpen: () => {
      Swal.showLoading();

      axios.post("/api/save-redacao", {
        titulo: titulo,
        texto: texto
      }).then((response) => {
        Swal.close();
        if (response.data.msg === "success") {
          Swal.fire({
            title: "Sucesso!",
            text: "Redação salva com sucesso.",
            icon: "success",
            confirmButtonText: "OK"
          });
        } else {
          Swal.fire({
            title: "Erro",
            text: "Erro ao salvar a redação.",
            icon: "error",
            confirmButtonText: "Tentar novamente"
          });
        }
      }).catch((error) => {
        Swal.close();
        Swal.fire({
          title: "Erro",
          text: "Ocorreu um erro ao tentar salvar sua redação.",
          icon: "error",
          confirmButtonText: "Tentar novamente"
        });
        console.error("Erro:", error);
      });
    }
  });
}
