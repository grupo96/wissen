# wissen

### Estrutura de Diretórios e Funcionamento

1. **Frontend (React)**:

   - Diretório: `/frontend`
   - **Descrição**: Armazena o código do React e a estrutura da interface do usuário.
   - **Importante**: Divida componentes em subpastas organizadas (`/components`, `/pages`, `/assets` para imagens ou estilos).
   - **Exemplo de estrutura**:
     ```
     /frontend
     ├── public/
     ├── src/
     │   ├── components/
     │   ├── pages/
     │   ├── assets/
     │   └── index.js
     └── package.json
     ```
2. **Backend (Django)**:

   - Diretório: `/backend`
   - **Descrição**: Contém o código principal do Django (APIs, autenticação, e lógica de negócios).
   - **Importante**: Organize os apps específicos dentro do Django em `/apps`, mantendo arquivos de configuração e gerenciadores de rotas separados.
   - **Exemplo de estrutura**:
     ```
     /backend
     ├── apps/
     │   ├── core/           # App principal
     │   ├── users/          # Gestão de usuários e autenticação
     ├── settings/           # Configurações do Django
     └── manage.py
     ```
3. **Machine Learning (ML)**:

   - Diretório: `/machine_learning`
   - **Descrição**: Contém os scripts, notebooks e modelos para aprendizado de máquina, com subdiretórios para organização dos dados e modelos.
   - **Importante**: Separe datasets, scripts de pré-processamento, e notebooks de análise para facilitar manutenção e atualizações.
   - **Exemplo de estrutura**:
     ```
     /machine_learning
     ├── models/
     ├── notebooks/
     └── preprocessing/
     ```

### Fluxo de Commits e Importância de Commits Estruturados

1. **Não Commitar Diretamente na `main`**:

   - **Motivo**: A `main` deve sempre conter o código mais estável e pronto para deploy. Commits diretos podem introduzir bugs.
   - **Como Proceder**:
     - Crie branches para cada nova feature, correção ou atualização (`feature/nome-da-feature`, `fix/descricao-do-bug`).
     - Realize testes antes de pedir uma revisão e aprovação para merge na `main`.
2. **Instruções de Commit**:

   - **Mensagens de Commit**: Use mensagens descritivas e objetivas (`"Adiciona página de login"`, `"Corrige erro de autenticação"`).
   - **Push e Pull Requests**:
     - Faça `push` para a branch que criou e sempre abra uma Pull Request (PR) para que o código seja revisado antes do merge.
     - Atribua revisores na PR e documente o que foi feito para facilitar a avaliação.
