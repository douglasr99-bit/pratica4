// app.js — Gerenciamento de tarefas (To-Do) com persistência em localStorage

// ==================== INICIALIZAÇÃO DO BANCO DE DADOS LOCAL ====================
// Inicializa o localStorage simulando uma estrutura db.json caso não exista
if (!localStorage.getItem('users')) {
  localStorage.setItem('users', JSON.stringify([]));
}
if (!localStorage.getItem('todos')) {
  localStorage.setItem('todos', JSON.stringify([]));
}

// Helper para obter dados do localStorage de forma segura
const getStorageData = (key) => JSON.parse(localStorage.getItem(key)) || [];
const setStorageData = (key, data) => localStorage.setItem(key, JSON.stringify(data));

// ==================== CONTROLE DE NAVEGAÇÃO DE TELAS ====================
const screens = {
  login: document.getElementById('screen-login'),
  register: document.getElementById('screen-register'),
  dashboard: document.getElementById('screen-dashboard')
};

function navigateTo(screenName) {
  Object.keys(screens).forEach(key => {
    if (key === screenName) {
      screens[key].classList.add('active');
    } else {
      screens[key].classList.remove('active');
    }
  });
  
  // Limpa mensagens de erro ao navegar
  clearAllErrors();
}

function clearAllErrors() {
  const errBoxes = ['login-error', 'register-error', 'register-success', 'todo-title-err'];
  errBoxes.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.classList.add('hidden');
  });

  const inlineErrors = ['login-email-err', 'login-password-err', 'register-name-err', 'register-email-err', 'register-password-err', 'todo-title-err'];
  inlineErrors.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.classList.add('hidden');
  });
}

// ==================== SISTEMA DE AUTENTICAÇÃO (LOGIN & CADASTRO) ====================

// Ir para tela de Cadastro
document.getElementById('goto-register').addEventListener('click', () => {
  navigateTo('register');
});

// Ir para tela de Login
document.getElementById('goto-login').addEventListener('click', () => {
  navigateTo('login');
});

// Ação de Cadastrar
document.getElementById('btn-register').addEventListener('click', () => {
  clearAllErrors();
  
  const nameInput = document.getElementById('register-name');
  const emailInput = document.getElementById('register-email');
  const passwordInput = document.getElementById('register-password');

  const name = nameInput.value.trim();
  const email = emailInput.value.trim().toLowerCase();
  const password = passwordInput.value;

  let hasError = false;

  if (!name) {
    document.getElementById('register-name-err').classList.remove('hidden');
    hasError = true;
  }
  if (!email || !validateEmail(email)) {
    document.getElementById('register-email-err').classList.remove('hidden');
    hasError = true;
  }
  if (!password || password.length < 6) {
    document.getElementById('register-password-err').classList.remove('hidden');
    hasError = true;
  }

  if (hasError) return;

  const users = getStorageData('users');
  
  // Verifica se o usuário já existe
  if (users.some(u => u.email === email)) {
    const errBox = document.getElementById('register-error');
    errBox.textContent = 'Este e-mail já está cadastrado!';
    errBox.classList.remove('hidden');
    return;
  }

  // Adiciona novo usuário
  users.push({ name, email, password });
  setStorageData('users', users);

  const successBox = document.getElementById('register-success');
  successBox.textContent = 'Conta criada com sucesso! Redirecionando para login...';
  successBox.classList.remove('hidden');

  // Limpa campos
  nameInput.value = '';
  emailInput.value = '';
  passwordInput.value = '';

  setTimeout(() => {
    navigateTo('login');
  }, 2000);
});

// Ação de Fazer Login
document.getElementById('btn-login').addEventListener('click', () => {
  clearAllErrors();

  const emailInput = document.getElementById('login-email');
  const passwordInput = document.getElementById('login-password');

  const email = emailInput.value.trim().toLowerCase();
  const password = passwordInput.value;

  let hasError = false;

  if (!email) {
    document.getElementById('login-email-err').classList.remove('hidden');
    hasError = true;
  }
  if (!password) {
    document.getElementById('login-password-err').classList.remove('hidden');
    hasError = true;
  }

  if (hasError) return;

  const users = getStorageData('users');
  const user = users.find(u => u.email === email);

  if (!user || user.password !== password) {
    const errBox = document.getElementById('login-error');
    errBox.textContent = 'E-mail não cadastrado ou senha incorreta!';
    errBox.classList.remove('hidden');
    return;
  }

  // Login com sucesso
  localStorage.setItem('currentUser', JSON.stringify({ name: user.name, email: user.email }));
  
  emailInput.value = '';
  passwordInput.value = '';

  initDashboard();
});

// Ação de Logout
document.getElementById('btn-logout').addEventListener('click', () => {
  localStorage.removeItem('currentUser');
  navigateTo('login');
});

// Função simples para validar e-mail
function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// ==================== DASHBOARD & GERENCIAMENTO DE TAREFAS ====================

function initDashboard() {
  const currentUser = JSON.parse(localStorage.getItem('currentUser'));
  if (!currentUser) {
    navigateTo('login');
    return;
  }

  // Exibe nome do usuário logado
  document.getElementById('user-name').textContent = currentUser.name;
  
  navigateTo('dashboard');
  renderTodos();
}

// Renderiza a lista de tarefas do usuário logado
function renderTodos() {
  const currentUser = JSON.parse(localStorage.getItem('currentUser'));
  if (!currentUser) return;

  const todos = getStorageData('todos');
  
  // Filtra apenas as tarefas criadas por este usuário
  const userTodos = todos.filter(t => t.userId === currentUser.email);

  // Ordena tarefas: Pendentes primeiro, Concluídas por último
  userTodos.sort((a, b) => a.done - b.done || b.id - a.id);

  const listContainer = document.getElementById('todo-list');
  const emptyState = document.getElementById('empty-state');

  listContainer.innerHTML = '';

  if (userTodos.length === 0) {
    emptyState.classList.remove('hidden');
    return;
  }

  emptyState.classList.add('hidden');

  userTodos.forEach(todo => {
    const card = document.createElement('div');
    card.className = `todo-item glass rounded-xl p-5 shadow-md flex flex-col md:flex-row md:items-center justify-between gap-4 transition-all duration-300 ${
      todo.done ? 'opacity-50 line-through border-gray-800' : 'hover:border-accent-500/40'
    }`;

    // Badge styling baseado no tipo
    let badgeClass = '';
    switch (todo.type) {
      case 'Trabalho':
        badgeClass = 'bg-blue-500/20 text-blue-300 border border-blue-500/30';
        break;
      case 'Pessoal':
        badgeClass = 'bg-purple-500/20 text-purple-300 border border-purple-500/30';
        break;
      case 'Estudos':
        badgeClass = 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30';
        break;
      default:
        badgeClass = 'bg-gray-500/20 text-gray-300 border border-gray-500/30';
    }

    card.innerHTML = `
      <div class="flex-1 space-y-2">
        <div class="flex items-center gap-3 flex-wrap">
          <h4 class="text-lg font-semibold text-white tracking-wide">${escapeHTML(todo.title)}</h4>
          <span class="text-xs px-2.5 py-1 rounded-full font-medium ${badgeClass}">${todo.type}</span>
        </div>
        ${todo.description ? `<p class="text-sm text-gray-400 break-words font-light leading-relaxed">${escapeHTML(todo.description)}</p>` : ''}
      </div>
      <div class="flex items-center gap-2 self-end md:self-center">
        ${!todo.done ? `
          <button onclick="concludeTodo(${todo.id})" class="px-4 py-2 bg-success-500/20 hover:bg-success-500 text-success-400 hover:text-white rounded-xl border border-success-500/30 hover:border-transparent text-sm font-semibold transition-all duration-200 cursor-pointer">
            Concluir
          </button>
        ` : `
          <span class="text-success-400 text-sm font-medium flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-success-500/10">
            ✓ Concluída
          </span>
        `}
      </div>
    `;

    listContainer.appendChild(card);
  });
}

// Ação de Concluir Tarefa
window.concludeTodo = function(todoId) {
  const todos = getStorageData('todos');
  const todoIndex = todos.findIndex(t => t.id === todoId);
  
  if (todoIndex !== -1) {
    todos[todoIndex].done = true;
    setStorageData('todos', todos);
    renderTodos();
  }
};

// Formulário de Adicionar Tarefa
document.getElementById('todo-form').addEventListener('submit', (e) => {
  e.preventDefault();
  clearAllErrors();

  const titleInput = document.getElementById('todo-title');
  const typeInput = document.getElementById('todo-type');
  const descInput = document.getElementById('todo-description');

  const title = titleInput.value.trim();
  const type = typeInput.value;
  const description = descInput.value.trim();

  if (!title) {
    document.getElementById('todo-title-err').classList.remove('hidden');
    return;
  }

  const currentUser = JSON.parse(localStorage.getItem('currentUser'));
  if (!currentUser) return;

  const todos = getStorageData('todos');
  
  // Cria novo objeto de tarefa
  const newTodo = {
    id: Date.now(),
    userId: currentUser.email,
    title,
    type,
    description,
    done: false
  };

  todos.push(newTodo);
  setStorageData('todos', todos);

  // Limpa campos
  titleInput.value = '';
  descInput.value = '';
  
  renderTodos();
});

// Helper simples para evitar injeção de HTML
function escapeHTML(str) {
  return str.replace(/[&<>'"]/g, 
    tag => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      "'": '&#39;',
      '"': '&quot;'
    }[tag] || tag)
  );
}

// Check session ativo ao carregar a página
window.addEventListener('DOMContentLoaded', () => {
  const currentUser = localStorage.getItem('currentUser');
  if (currentUser) {
    initDashboard();
  } else {
    navigateTo('login');
  }
});
