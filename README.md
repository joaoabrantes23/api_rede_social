<h1 align="center">API Rede Social</h1>

<p align="center">Esta é uma API de rede social simples desenvolvida com Flask e SQLAlchemy, permitindo o gerenciamento de usuários e posts. Ela oferece funcionalidades para criação de conta, login de usuários, e a capacidade de criar, editar, listar e deletar posts.</p>

#### Tecnologias Usadas
<ul>
  <li><strong>Flask</strong> - Framework web para Python.</li>
  <li><strong>SQLAlchemy</strong> - ORM para interação com o banco de dados.</li>
  <li><strong>Postgres</strong> - Usado para armazenar dados de usuários e posts.</li>
  <li><strong>Docker</strong> - Para containerização da aplicação.</li>
  <li><strong>Swagger</strong> - Para documentação automática da API.</li>
</ul>

#### Autenticação
<ul>
  <li><strong>Login:</strong> Permite que usuários logados acessem a aplicação com seus credenciais.</li>
</ul>

#### Usuário
<ul>
  <li><strong>Criação de usuário:</strong> Usuários podem criar uma conta.</li>
  <li><strong>Edição de usuário:</strong> Usuários podem editar suas próprias informações.</li>
  <li><strong>Buscar usuário por ID:</strong> Busca as informações de um usuário específico.</li>
  <li><strong>Listar usuários:</strong> Lista todos os usuários cadastrados.</li>
  <li><strong>Deletar usuário:</strong> Usuários podem deletar suas próprias contas.</li>
</ul>

#### Posts
<ul>
  <li><strong>Criação de post:</strong> Usuários logados podem criar posts de texto.</li>
  <li><strong>Edição de post:</strong> Usuários podem editar seus próprios posts.</li>
  <li><strong>Buscar post por ID:</strong> Permite a busca de um post específico.</li>
  <li><strong>Listar todos os posts:</strong> Exibe todos os posts com o autor (ID e nome).</li>
  <li><strong>Listar posts por ID de usuário:</strong> Exibe posts de um usuário específico.</li>
  <li><strong>Deletar post:</strong> Usuários podem deletar seus próprios posts.</li>
</ul>

### Regras de Admin
<ul>
  <li><strong>Somente usuários administradores podem:</strong></li>
  <ul>
    <li>Editar ou deletar usuários que não são os seus próprios.</li>
    <li>Editar ou deletar posts que não são os seus próprios.</li>
  </ul>
</ul>


## Instalação

Com a aplicação dockerizada, não é necessário instalar as dependências diretamente no seu computador. Você pode rodar a aplicação facilmente utilizando Docker.

### Requisitos
- **Docker**: Para rodar a aplicação e o banco de dados em containers.

### Passo a Passo

1. Clone o repositório:
   ```bash
   git clone https://github.com/joaoabrantes23/api_rede_social.git

2. Navegue até a pasta do projeto:
   ```bash
   cd api_rede_social

3. Para rodar a aplicação com Docker e subir o banco de dados, execute:
   ```bash
   docker-compose up --build

4. Caso não precise recompilar as imagens, execute o comando sem o --build:
   ```bash
   docker-compose up

5. Após isso a API estará acessível.

5. Para acessar a API, utilize uma ferramenta como **Postman** ou **Insomnia** para enviar requisições HTTP.  

   - Você pode verificar se a API está rodando corretamente acessando a documentação no navegador:  
     ```bash
     http://localhost:5000/swagger-ui
     ```
