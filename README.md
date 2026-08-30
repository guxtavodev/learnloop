# 🎓 Estudaê

> **Tecnologia para transformar a forma de estudar.**

O **Estudaê** é uma plataforma educacional criada para ampliar o acesso a ferramentas de preparação para o **ENEM**, especialmente entre estudantes da rede pública.

A plataforma reúne recursos de estudo, escrita e revisão em um único ambiente, utilizando tecnologia e Inteligência Artificial para oferecer uma experiência de aprendizagem mais acessível, prática e personalizada.

---

## 🚀 Sobre o projeto

O Estudaê nasceu a partir da percepção de que muitos estudantes possuem acesso limitado a ferramentas de preparação de qualidade para o ENEM.

A proposta é utilizar tecnologia para diminuir essa barreira, oferecendo recursos que auxiliem o estudante durante sua preparação — desde a produção de uma redação até a organização dos estudos.

### 🎯 Objetivo

Democratizar o acesso à tecnologia educacional e ajudar estudantes a desenvolverem autonomia durante sua preparação para o ENEM.

---

## ✨ Funcionalidades

### ✍️ Corretor de Redações

Ferramenta de correção de redações baseada nas competências avaliadas pelo ENEM.

O sistema busca fornecer uma avaliação detalhada e orientações para que o estudante compreenda seus erros e possa melhorar sua escrita.

### 📝 Redação Guiada

Recurso desenvolvido para auxiliar o estudante na construção de uma redação passo a passo.

Em vez de simplesmente entregar uma nota, a proposta é ajudar o estudante a **entender como construir um bom texto**.

### 📚 Caderno Digital

Espaço para organização dos estudos, permitindo reunir conteúdos e anotações em um único ambiente.

### 🧠 Revisões Inteligentes

Sistema pensado para auxiliar o estudante na revisão dos conteúdos estudados, utilizando tecnologia para tornar o processo mais personalizado.

---

## 🤖 Inteligência Artificial

A Inteligência Artificial é utilizada como uma ferramenta de apoio à aprendizagem.

No Estudaê, a IA pode atuar na análise de redações, geração de feedbacks e outras funcionalidades educacionais.

O objetivo não é substituir professores ou o processo de aprendizagem, mas **utilizar a tecnologia como uma ferramenta complementar**.

---

## 🛠️ Tecnologias

O projeto utiliza tecnologias modernas para desenvolvimento web e processamento de dados.

| Tecnologia      | Utilização                               |
| --------------- | ---------------------------------------- |
| 🐍 Python       | Backend e lógica da aplicação            |
| 🌐 Flask        | Framework web                            |
| 🗄️ Supabase    | Banco de dados e serviços backend        |
| 🤖 Azure OpenAI | Recursos de Inteligência Artificial      |
| 🧠 JavaScript   | Interações e funcionalidades do frontend |
| 🎨 HTML/CSS     | Interface da plataforma                  |

> A arquitetura e as tecnologias utilizadas podem mudar conforme a evolução do projeto.

---

## 🏗️ Estrutura do projeto

Uma estrutura simplificada pode ser organizada da seguinte forma:

```text
estudae/
├── app/
│   ├── routes/
│   ├── templates/
│   └── static/
│
├── requirements.txt
├── main.py
└── README.md
```

A estrutura pode variar de acordo com a versão atual do projeto.

---

## 💻 Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/ogustavodeveloper/learnloop.git
cd learnloop
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
```

No Windows:

```bash
venv\Scripts\activate
```

No Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` 

Exemplo:

```env
SECRET_KEY=sua_chave_secreta

SUPABASE_URL=sua_url
SUPABASE_KEY=sua_chave

AZURE_OPENAI_ENDPOINT=seu_endpoint
AZURE_OPENAI_API_KEY=sua_chave
AZURE_OPENAI_DEPLOYMENT=seu_deployment
```

> **Nunca coloque chaves de API ou credenciais diretamente no código ou no repositório.**

### 5. Execute a aplicação

```bash
python run.py
```

Depois, acesse:

```text
http://localhost:5000
```

---

## 🌱 Contribuindo

Contribuições são bem-vindas!

Se você encontrou um problema, possui uma sugestão ou deseja contribuir com o desenvolvimento:

1. Faça um **fork** do projeto;
2. Crie uma branch para sua alteração;
3. Faça suas modificações;
4. Realize um commit;
5. Abra um **Pull Request**.

Exemplo:

```bash
git checkout -b minha-feature
git commit -m "feat: adiciona nova funcionalidade"
git push origin minha-feature
```

---

## 🔐 Segurança

O Estudaê trabalha com informações de usuários e integrações com serviços externos.

Por isso:

* Não publique chaves de API;
* Não versione arquivos `.env`;
* Não compartilhe credenciais;
* Reporte vulnerabilidades de segurança de forma responsável.

---

## 📌 Status

🚧 **Em desenvolvimento**

O Estudaê está em constante evolução, com novas funcionalidades e melhorias sendo desenvolvidas.

---

## 🎓 Projeto educacional

O Estudaê é um projeto de tecnologia educacional desenvolvido com o propósito de utilizar **inovação e Inteligência Artificial para ampliar o acesso à educação**.

A plataforma busca aproximar estudantes da rede pública de ferramentas tecnológicas que possam contribuir para sua preparação acadêmica e para o ENEM.

---

## 👨‍💻 Desenvolvedor

**Gustavo**

Estudante de **Bacharelado Interdisciplinar em Ciência, Tecnologia e Inovação — UFBA**.

---

<p align="center">
  Feito com tecnologia, educação e propósito. 💙
</p>
