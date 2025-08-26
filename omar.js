<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Mini Proyecto JS: Productividad</title>
  <style>
    :root {
      --bg: #0f172a; /* slate-900 */
      --panel: #111827; /* gray-900 */
      --panel-2: #0b1022; /* darker */
      --text: #e5e7eb; /* gray-200 */
      --muted: #94a3b8; /* slate-400 */
      --brand: #22d3ee; /* cyan-400 */
      --brand-2: #06b6d4; /* cyan-500 */
      --ok: #10b981; /* emerald */
      --warn: #f59e0b; /* amber */
      --danger: #ef4444; /* red */
      --shadow: 0 10px 30px rgba(2, 8, 23, .6);
    }
    * { box-sizing: border-box; }
    html, body { height: 100%; }
    body {
      margin: 0;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, "Helvetica Neue", Arial, "Apple Color Emoji", "Segoe UI Emoji";
      background: radial-gradient(1200px 600px at 80% -10%, rgba(34,211,238,0.12), transparent 60%),
                  radial-gradient(900px 500px at -10% -10%, rgba(99,102,241,0.10), transparent 60%),
                  var(--bg);
      color: var(--text);
    }
    header {
      display: flex; align-items: center; justify-content: space-between;
      padding: 18px 22px; position: sticky; top: 0; z-index: 10;
      background: linear-gradient(180deg, rgba(17,24,39,.95), rgba(17,24,39,.75));
      backdrop-filter: blur(8px);
      border-bottom: 1px solid rgba(226,232,240,.06);
    }
    .brand { display: flex; align-items: center; gap: 12px; font-weight: 700; letter-spacing: .4px; }
    .brand svg { width: 28px; height: 28px; }
    .container { max-width: 1200px; margin: 20px auto; padding: 0 16px 60px; }
    .grid { display: grid; grid-template-columns: 1.2fr .8fr; gap: 18px; }
    @media (max-width: 980px) { .grid { grid-template-columns: 1fr; } }

    .card {
      background: linear-gradient(180deg, var(--panel), var(--panel-2));
      border: 1px solid rgba(148,163,184,.15);
      border-radius: 18px; box-shadow: var(--shadow);
      overflow: hidden; display: flex; flex-direction: column;
    }
    .card h2 { margin: 0; font-size: 1.05rem; color: #cbd5e1; letter-spacing: .2px; }
    .card header { background: transparent; position: static; border: 0; padding: 14px 16px; }
    .card .content { padding: 16px; }
    .row { display: flex; gap: 8px; flex-wrap: wrap; }
    .input, select, button, textarea {
      background: #0b1222; color: var(--text);
      border: 1px solid rgba(148,163,184,.2);
      border-radius: 12px; padding: 10px 12px; font-size: .95rem;
    }
    .input:focus, select:focus, textarea:focus { outline: 2px solid rgba(34,211,238,.25); }
    .btn { cursor: pointer; user-select: none; transition: transform .06s ease, opacity .2s ease; }
    .btn:active { transform: translateY(1px) scale(.99); }
    .btn.brand { background: linear-gradient(180deg, var(--brand), var(--brand-2)); color: #062a2e; border: 0; font-weight: 700; }
    .btn.ghost { background: transparent; border-color: rgba(148,163,184,.35); }
    .btn.warn { background: rgba(245,158,11,.15); border-color: rgba(245,158,11,.4); color: #fcd34d; }
    .btn.danger { background: rgba(239,68,68,.12); border-color: rgba(239,68,68,.45); color: #fecaca; }

    /* TODO LIST */
    .todo-list { display: grid; gap: 8px; }
    .todo-item { display: grid; grid-template-columns: 28px 1fr auto; align-items: center; gap: 10px;
      padding: 10px 12px; border-radius: 14px; border: 1px dashed rgba(148,163,184,.25);
      background: rgba(2, 6, 23, .45);
    }
    .todo-item.dragging { opacity: .55; }
    .todo-title { font-weight: 600; }
    .todo-meta { font-size: .8rem; color: var(--muted); }
    .badge { font-size: .75rem; padding: 4px 8px; border-radius: 999px; border: 1px solid rgba(148,163,184,.35); }

    /* NOTES */
    .notes { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 10px; }
    .note { border: 1px dashed rgba(148,163,184,.25); background: rgba(2,6,23,.45); padding: 10px; border-radius: 14px; display: grid; gap: 6px; }
    .note .title { font-weight: 700; }

    /* POMODORO */
    .pomodoro { text-align: center; }
    .time { font-size: 48px; letter-spacing: 2px; margin: 8px 0 16px; }

    /* TABLE */
    table { width: 100%; border-collapse: collapse; font-size: .92rem; }
    th, td { padding: 9px 10px; border-bottom: 1px dashed rgba(148,163,184,.18); }
    th { text-align: left; color: #cbd5e1; font-weight: 700; }
    tbody tr:hover { background: rgba(34,211,238,.05); }

    .toolbar { display: flex; align-items: center; gap: 8px; justify-content: space-between; margin-bottom: 10px; flex-wrap: wrap; }
    .chip { font-size: .8rem; padding: 5px 8px; border: 1px solid rgba(148,163,184,.35); border-radius: 999px; }
    .kbd { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: .75rem; padding: 2px 6px; border-radius: 6px; border: 1px solid rgba(148,163,184,.35); }
    .hint { color: var(--muted); font-size: .85rem; }
    .footer { text-align: center; color: var(--muted); padding: 24px; }
  </style>
</head>
<body>
  <header>
    <div class="brand" title="Codexus Productivity">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="3" />
        <path d="M19.4 15a8 8 0 10-2.4 2.4l3.5 3.5 1.4-1.4L19.4 15z" />
      </svg>
      <span>Mini Proyecto JS — Productividad</span>
    </div>
    <div class="row">
      <button class="btn ghost" id="btn-export" title="Exportar estado (JSON)">Exportar</button>
      <button class="btn ghost" id="btn-import" title="Importar estado (JSON)">Importar</button>
      <button class="btn danger" id="btn-reset" title="Borrar todo">Reset</button>
    </div>
  </header>

  <div class="container">
    <div class="grid">
      <!-- Columna principal -->
      <section class="card" id="todo-card">
        <header>
          <h2>🗂️ Tareas (drag & drop, filtros, localStorage)</h2>
        </header>
        <div class="content">
          <div class="toolbar">
            <div class="row" style="gap:6px;">
              <input class="input" id="todo-title" placeholder="Nueva tarea..." />
              <select id="todo-priority">
                <option value="low">Baja</option>
                <option value="medium">Media</option>
                <option value="high">Alta</option>
              </select>
              <input class="input" id="todo-deadline" type="date" />
              <button class="btn brand" id="todo-add">Agregar</button>
            </div>
            <div class="row" style="gap:6px; align-items:center;">
              <input class="input" id="todo-search" placeholder="Buscar (Ctrl+/)" />
              <select id="todo-filter">
                <option value="all">Todas</option>
                <option value="open">Abiertas</option>
                <option value="done">Completadas</option>
              </select>
              <span class="chip" id="todo-count">0 tareas</span>
            </div>
          </div>
          <div class="todo-list" id="todo-list" aria-live="polite"></div>
        </div>
      </section>

      <!-- Columna secundaria -->
      <section class="card">
        <header><h2>⏱️ Pomodoro (25/5)</h2></header>
        <div class="content pomodoro">
          <div class="time" id="clock">25:00</div>
          <div class="row" style="justify-content:center;">
            <button class="btn brand" id="pomo-start">Iniciar</button>
            <button class="btn warn" id="pomo-pause">Pausar</button>
            <button class="btn ghost" id="pomo-skip">Saltar</button>
            <button class="btn danger" id="pomo-reset">Reset</button>
          </div>
          <p class="hint">Consejo: presiona <span class="kbd">Space</span> para iniciar/pausar, <span class="kbd">N</span> para saltar.</p>
        </div>
      </section>

      <section class="card">
        <header><h2>📝 Notas rápidas</h2></header>
        <div class="content">
          <div class="row">
            <input class="input" id="note-title" placeholder="Título" />
            <input class="input" id="note-tags" placeholder="#etiquetas separadas por coma" />
            <button class="btn brand" id="note-add">Agregar Nota</button>
          </div>
          <textarea class="input" id="note-text" rows="4" placeholder="Contenido de la nota..."></textarea>
          <div class="toolbar" style="margin-top:10px;">
            <input class="input" id="note-search" placeholder="Buscar nota..." />
            <span class="chip" id="note-count">0 notas</span>
          </div>
          <div class="notes" id="notes"></div>
        </div>
      </section>

      <section class="card">
        <header><h2>🌐 Usuarios (Fetch API + paginación + cache)</h2></header>
        <div class="content">
          <div class="toolbar">
            <div class="row">
              <button class="btn brand" id="users-load">Cargar usuarios</button>
              <button class="btn ghost" id="users-clear">Limpiar</button>
            </div>
            <div class="row">
              <input class="input" id="users-search" placeholder="Filtrar por nombre/email" />
              <span class="chip" id="users-count">0</span>
            </div>
          </div>
          <div style="overflow:auto;">
            <table>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Nombre</th>
                  <th>Email</th>
                  <th>Empresa</th>
                </tr>
              </thead>
              <tbody id="users-tbody"></tbody>
            </table>
          </div>
          <div class="row" style="justify-content:space-between; margin-top:10px;">
            <div class="hint">Fuente: JSONPlaceholder</div>
            <div class="row">
              <button class="btn ghost" id="prev-page">Anterior</button>
              <span class="chip" id="page-info">0 / 0</span>
              <button class="btn ghost" id="next-page">Siguiente</button>
            </div>
          </div>
        </div>
      </section>
    </div>

    <p class="footer">Hecho con JavaScript puro. Guarda estado en LocalStorage y soporta exportar/importar JSON.</p>
  </div>

  <script>
    // Utilidades generales
    const $ = (sel, parent = document) => parent.querySelector(sel);
    const $$ = (sel, parent = document) => Array.from(parent.querySelectorAll(sel));
    const fmt = (n) => new Intl.NumberFormat('es-MX').format(n);
    const uid = () => Math.random().toString(36).slice(2, 10);

    // Debounce
    const debounce = (fn, ms = 300) => {
      let t; return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
    };

    // Modiicar el archivo 

    // Persistencia sencilla
    const storage = {
      get(key, fallback) {
        try { return JSON.parse(localStorage.getItem(key)) ?? fallback; } catch { return fallback; }
      },
      set(key, value) { localStorage.setItem(key, JSON.stringify(value)); }
    };

    // Bus de eventos minimalista
    const bus = {
      events: new Map(),
      on(evt, fn) { const list = this.events.get(evt) || []; list.push(fn); this.events.set(evt, list); },
      off(evt, fn) { const list = this.events.get(evt) || []; this.events.set(evt, list.filter(f => f!==fn)); },
      emit(evt, payload) { (this.events.get(evt) || []).forEach(fn => fn(payload)); }
    };

    // ========================
    //   MOD: TODOs
    // ========================
    const TodoStore = (() => {
      const KEY = 'mp.todos.v1';
      let todos = storage.get(KEY, []);

      const save = () => storage.set(KEY, todos);
      const list = () => [...todos];
      const add = (title, priority, deadline) => {
        const t = { id: uid(), title: title.trim(), priority, deadline: deadline||null, done: false, createdAt: Date.now(), order: todos.length };
        if (!t.title) return null;
        todos.push(t); save(); bus.emit('todos:changed'); return t; };
      const toggle = (id) => { const t = todos.find(x=>x.id===id); if (t) { t.done = !t.done; save(); bus.emit('todos:changed'); } };
      const remove = (id) => { todos = todos.filter(x=>x.id!==id); reindex(); save(); bus.emit('todos:changed'); };
      const clear = () => { todos = []; save(); bus.emit('todos:changed'); };
      const reorder = (id, newIndex) => { const idx = todos.findIndex(t=>t.id===id); if (idx<0) return; const [item] = todos.splice(idx,1); todos.splice(newIndex,0,item); reindex(); save(); bus.emit('todos:changed'); };
      const reindex = () => todos.forEach((t,i)=> t.order=i);

      const importAll = (list) => { todos = list ?? []; save(); bus.emit('todos:changed'); };

      return { list, add, toggle, remove, clear, reorder, importAll };
    })();

    const TodoUI = (() => {
      const els = {
        list: $('#todo-list'),
        title: $('#todo-title'),
        priority: $('#todo-priority'),
        deadline: $('#todo-deadline'),
        add: $('#todo-add'),
        search: $('#todo-search'),
        filter: $('#todo-filter'),
        count: $('#todo-count')
      };

      let dragId = null;
      let state = { q: '', filter: 'all' };

      function matches(t) {
        const byFilter = state.filter === 'all' ? true : state.filter === 'open' ? !t.done : t.done;
        const byQuery = !state.q || (t.title.toLowerCase().includes(state.q) || (t.priority||'').includes(state.q));
        return byFilter && byQuery;
      }

      function render() {
        const items = TodoStore.list().sort((a,b)=>a.order-b.order).filter(matches);
        els.count.textContent = `${items.length} ${items.length===1?'tarea':'tareas'}`;
        els.list.innerHTML = '';
        if (!items.length) {
          const empty = document.createElement('div');
          empty.className = 'hint';
          empty.textContent = 'Sin tareas. Agrega la primera arriba.';
          els.list.appendChild(empty); return;
        }
        for (const t of items) {
          const row = document.createElement('div');
          row.className = 'todo-item'; row.draggable = true; row.dataset.id = t.id;
          row.innerHTML = `
            <input type="checkbox" ${t.done? 'checked':''} aria-label="Marcar completada" />
            <div>
              <div class="todo-title">${escapeHtml(t.title)}</div>
              <div class="todo-meta">Prioridad: <span class="badge">${t.priority}</span>
                ${t.deadline ? ` • vence: <span class="badge">${fmtDate(t.deadline)}</span>` : ''}
                • creada: <span class="badge">${new Date(t.createdAt).toLocaleString('es-MX')}</span>
              </div>
            </div>
            <div class="row">
              <button class="btn ghost btn-edit">Editar</button>
              <button class="btn danger btn-del">Eliminar</button>
            </div>`;
          els.list.appendChild(row);
        }
      }

      // Handlers
      els.add.addEventListener('click', () => {
        const t = els.title.value, p = els.priority.value, d = els.deadline.value;
        const created = TodoStore.add(t, p, d);
        if (created) { els.title.value = ''; els.deadline.value=''; els.title.focus(); }
      });
      els.title.addEventListener('keydown', (e)=>{ if(e.key==='Enter') els.add.click(); });

      els.search.addEventListener('input', debounce((e)=>{ state.q = e.target.value.toLowerCase(); render(); }, 200));
      els.filter.addEventListener('change', (e)=>{ state.filter = e.target.value; render(); });

      els.list.addEventListener('click', (e)=>{
        const row = e.target.closest('.todo-item'); if (!row) return;
        const id = row.dataset.id;
        if (e.target.matches('input[type="checkbox"]')) return TodoStore.toggle(id);
        if (e.target.classList.contains('btn-del')) return TodoStore.remove(id);
        if (e.target.classList.contains('btn-edit')) return editRow(row, id);
      });

      function editRow(row, id) {
        const data = TodoStore.list().find(x=>x.id===id); if(!data) return;
        row.innerHTML = `
          <div></div>
          <div class="row" style="flex-wrap:nowrap; gap:6px;">
            <input class="input" value="${escapeAttr(data.title)}" id="edit-title" style="flex:1;" />
            <select id="edit-priority">
              <option ${data.priority==='low'?'selected':''} value="low">Baja</option>
              <option ${data.priority==='medium'?'selected':''} value="medium">Media</option>
              <option ${data.priority==='high'?'selected':''} value="high">Alta</option>
            </select>
            <input class="input" id="edit-deadline" type="date" value="${data.deadline||''}" />
            <button class="btn brand" id="edit-save">Guardar</button>
            <button class="btn ghost" id="edit-cancel">Cancelar</button>
          </div>
          <div></div>`;
        $('#edit-title', row).focus();

        row.addEventListener('click', (ev)=>{
          if (ev.target.id==='edit-cancel') return render();
          if (ev.target.id==='edit-save') {
            const t = $('#edit-title', row).value.trim();
            const p = $('#edit-priority', row).value;
            const d = $('#edit-deadline', row).value || null;
            const all = TodoStore.list();
            const idx = all.findIndex(x=>x.id===id);
            if (idx>-1 && t) {
              all[idx] = { ...all[idx], title: t, priority: p, deadline: d };
              // Persist (reimport to keep encapsulation)
              TodoStore.importAll(all);
            } else {
              render();
            }
          }
        }, { once: true });
      }

      // Drag & Drop para reordenar
      els.list.addEventListener('dragstart', (e)=>{
        const row = e.target.closest('.todo-item'); if (!row) return;
        dragId = row.dataset.id; row.classList.add('dragging');
      });
      els.list.addEventListener('dragend', (e)=>{
        const row = e.target.closest('.todo-item'); if (row) row.classList.remove('dragging'); dragId = null;
      });
      els.list.addEventListener('dragover', (e)=>{
        e.preventDefault();
        const rows = $$('.todo-item', els.list).filter(x=>!x.classList.contains('dragging'));
        const after = rows.find(r => e.clientY <= r.getBoundingClientRect().top + r.offsetHeight/2);
        const dragging = $('.todo-item.dragging', els.list);
        if (!dragging) return;
        if (after == null) els.list.appendChild(dragging); else els.list.insertBefore(dragging, after);
      });
      els.list.addEventListener('drop', ()=>{
        const order = $$('.todo-item', els.list).map(x=>x.dataset.id);
        order.forEach((id, i) => TodoStore.reorder(id, i));
      });

      bus.on('todos:changed', render);
      render();

      // Accesos rápidos
      document.addEventListener('keydown', (e)=>{
        if ((e.ctrlKey||e.metaKey) && e.key === '/') { e.preventDefault(); els.search.focus(); }
      });

      return { render };
    })();

    // ========================
    //   MOD: NOTAS
    // ========================
    const NoteStore = (() => {
      const KEY = 'mp.notes.v1';
      let notes = storage.get(KEY, []);
      const save = () => storage.set(KEY, notes);

      const list = () => [...notes];
      const add = (title, text, tags) => {
        const n = { id: uid(), title: title.trim()||'Sin título', text: text.trim(), tags: parseTags(tags), createdAt: Date.now() };
        notes.push(n); save(); bus.emit('notes:changed'); return n;
      };
      const remove = (id) => { notes = notes.filter(n=>n.id!==id); save(); bus.emit('notes:changed'); };
      const importAll = (data) => { notes = data ?? []; save(); bus.emit('notes:changed'); };

      return { list, add, remove, importAll };
    })();

    const NoteUI = (() => {
      const els = {
        title: $('#note-title'),
        text: $('#note-text'),
        tags: $('#note-tags'),
        add: $('#note-add'),
        list: $('#notes'),
        search: $('#note-search'),
        count: $('#note-count')
      };

      let q = '';
      function render() {
        const data = NoteStore.list().filter(n =>
          !q || n.title.toLowerCase().includes(q) || n.text.toLowerCase().includes(q) || n.tags.join(',').includes(q)
        );
        els.count.textContent = `${data.length} ${data.length===1?'nota':'notas'}`;
        els.list.innerHTML = '';
        if (!data.length) {
          const hint = document.createElement('div');
          hint.className = 'hint';
          hint.textContent = 'Sin notas todavía.';
          els.list.appendChild(hint); return;
        }
        for (const n of data) {
          const card = document.createElement('div'); card.className = 'note'; card.dataset.id = n.id;
          card.innerHTML = `
            <div class="title">${escapeHtml(n.title)}</div>
            <div class="hint">${new Date(n.createdAt).toLocaleString('es-MX')}</div>
            <div class="text">${escapeHtml(n.text)}</div>
            <div class="row">${n.tags.map(t=>`<span class="chip">#${escapeHtml(t)}</span>`).join('')}</div>
            <div class="row" style="justify-content:end;">
              <button class="btn ghost btn-copy">Copiar</button>
              <button class="btn danger btn-del">Eliminar</button>
            </div>`;
          els.list.appendChild(card);
        }
      }

      els.add.addEventListener('click', ()=>{
        const title = els.title.value, text = els.text.value, tags = els.tags.value;
        if (!text.trim()) return alert('Escribe contenido para la nota.');
        NoteStore.add(title, text, tags);
        els.title.value = ''; els.text.value = ''; els.tags.value = '';
      });

      els.list.addEventListener('click', (e)=>{
        const card = e.target.closest('.note'); if (!card) return;
        const id = card.dataset.id;
        if (e.target.classList.contains('btn-del')) NoteStore.remove(id);
        if (e.target.classList.contains('btn-copy')) {
          const text = $('.text', card).textContent;
          navigator.clipboard.writeText(text).then(()=>{
            e.target.textContent = 'Copiado!'; setTimeout(()=> e.target.textContent='Copiar', 1000);
          });
        }
      });

      els.search.addEventListener('input', debounce((e)=>{ q = e.target.value.toLowerCase(); render(); }, 150));

      bus.on('notes:changed', render);
      render();

      return { render };
    })();

    // ========================
    //   MOD: POMODORO
    // ========================
    const Pomodoro = (() => {
      const els = { clock: $('#clock'), start: $('#pomo-start'), pause: $('#pomo-pause'), skip: $('#pomo-skip'), reset: $('#pomo-reset') };
      const DURATIONS = { focus: 25*60, break: 5*60 };
      let mode = 'focus';
      let seconds = DURATIONS[mode];
      let timer = null;

      function render() {
        const m = Math.floor(seconds/60).toString().padStart(2,'0');
        const s = Math.floor(seconds%60).toString().padStart(2,'0');
        els.clock.textContent = `${m}:${s}`;
        document.title = `${m}:${s} — ${mode==='focus'?'Focus':'Break'}`;
      }

      function tick() {
        if (seconds > 0) { seconds--; render(); return; }
        // Cambio de fase
        mode = mode === 'focus' ? 'break' : 'focus';
        seconds = DURATIONS[mode];
        notify(`Tiempo de ${mode==='focus'?'concentración':'descanso'}`);
        render();
      }

      function start() { if (timer) return; timer = setInterval(tick, 1000); }
      function pause() { clearInterval(timer); timer = null; }
      function skip() { seconds = 0; tick(); }
      function reset() { pause(); mode='focus'; seconds=DURATIONS[mode]; render(); }

      els.start.addEventListener('click', start);
      els.pause.addEventListener('click', pause);
      els.skip.addEventListener('click', skip);
      els.reset.addEventListener('click', reset);

      document.addEventListener('keydown', (e)=>{
        if (e.key===' ') { e.preventDefault(); if (timer) pause(); else start(); }
        if (e.key.toLowerCase()==='n') { skip(); }
      });

      render();
      return { start, pause, skip, reset };
    })();

    // ========================
    //   MOD: USERS (Fetch + paginación)
    // ========================
    const Users = (() => {
      const els = { tbody: $('#users-tbody'), load: $('#users-load'), clear: $('#users-clear'), search: $('#users-search'), count: $('#users-count'), prev: $('#prev-page'), next: $('#next-page'), pageInfo: $('#page-info') };
      const ENDPOINT = 'https://jsonplaceholder.typicode.com/users';
      const PAGE_SIZE = 5;
      let all = [];
      let page = 1;
      let q = '';

      const cacheKey = 'mp.users.cache.v1';
      function setCache(users) { storage.set(cacheKey, { at: Date.now(), users }); }
      function getCache() { const c = storage.get(cacheKey, null); if (!c) return null; // 1 día
        if ((Date.now() - c.at) > 24*60*60*1000) return null; return c.users; }

      function filterUsers() { return all.filter(u => !q || u.name.toLowerCase().includes(q) || u.email.toLowerCase().includes(q)); }

      function render() {
        const data = filterUsers();
        const total = data.length; els.count.textContent = fmt(total);
        const pages = Math.max(1, Math.ceil(total / PAGE_SIZE));
        if (page > pages) page = pages;
        const start = (page-1)*PAGE_SIZE; const slice = data.slice(start, start+PAGE_SIZE);
        els.pageInfo.textContent = `${page} / ${pages}`;
        els.tbody.innerHTML = slice.map((u,i)=>`<tr><td>${start+i+1}</td><td>${escapeHtml(u.name)}</td><td>${escapeHtml(u.email)}</td><td>${escapeHtml(u.company?.name||'-')}</td></tr>`).join('');
      }

      async function load() {
        try {
          els.tbody.innerHTML = `<tr><td colspan="4" class="hint">Cargando...</td></tr>`;
          const cache = getCache();
          if (cache) { all = cache; render(); return; }
          const res = await fetch(ENDPOINT, { headers: { 'Accept': 'application/json' } });
          if (!res.ok) throw new Error('HTTP ' + res.status);
          all = await res.json();
          setCache(all); render();
        } catch (err) {
          els.tbody.innerHTML = `<tr><td colspan="4" style="color:#fecaca;">Error al cargar: ${escapeHtml(err.message)}</td></tr>`;
        }
      }

      els.load.addEventListener('click', load);
      els.clear.addEventListener('click', ()=>{ all = []; page = 1; render(); });
      els.prev.addEventListener('click', ()=>{ if (page>1) { page--; render(); } });
      els.next.addEventListener('click', ()=>{ page++; render(); });
      els.search.addEventListener('input', debounce((e)=>{ q = e.target.value.toLowerCase(); page = 1; render(); }, 150));

      render();
      return { load };
    })();

    // ========================
    //   EXPORT/IMPORT + RESET
    // ========================
    $('#btn-export').addEventListener('click', ()=>{
      const data = {
        todos: (TodoStore.list()),
        notes: (NoteStore.list()),
        usersCache: storage.get('mp.users.cache.v1', null)
      };
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = Object.assign(document.createElement('a'), { href: url, download: 'estado.json' });
      document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
    });

    $('#btn-import').addEventListener('click', ()=>{
      const inp = Object.assign(document.createElement('input'), { type: 'file', accept: 'application/json' });
      inp.onchange = () => {
        const file = inp.files?.[0]; if (!file) return;
        const reader = new FileReader(); reader.onload = () => {
          try {
            const data = JSON.parse(reader.result);
            if (data.todos) TodoStore.importAll(data.todos);
            if (data.notes) NoteStore.importAll(data.notes);
            if (data.usersCache) storage.set('mp.users.cache.v1', data.usersCache);
            notify('Datos importados con éxito');
          } catch (e) { alert('Archivo inválido'); }
        }; reader.readAsText(file);
      };
      inp.click();
    });

    $('#btn-reset').addEventListener('click', ()=>{
      if (!confirm('Esto borrará TODO el estado local. ¿Continuar?')) return;
      localStorage.clear(); location.reload();
    });

    // ========================
    //   Helpers misceláneos
    // ========================
    function parseTags(s) { return (s||'').split(',').map(t=>t.trim()).filter(Boolean).map(t=>t.replace(/^#/, '')); }
    function fmtDate(d) { try { return new Date(d).toLocaleDateString('es-MX', { day:'2-digit', month:'short', year: 'numeric' }); } catch { return d; } }
    function escapeHtml(s) { return (s??'').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }
    function escapeAttr(s) { return (s??'').replace(/["\n]/g, c => ({'"':'&quot;','\n':' '}[c])); }
    function notify(msg) {
      if ("Notification" in window) {
        if (Notification.permission === 'granted') new Notification(msg);
        else if (Notification.permission !== 'denied') Notification.requestPermission();
      }
    }

    // Registro de Service Worker mínimo (opcional)
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register(URL.createObjectURL(new Blob([
          `self.addEventListener('install', e=>self.skipWaiting());`+
          `self.addEventListener('activate', e=>self.clients.claim());`+
          `self.addEventListener('fetch', e=>{});`
        ], { type: 'text/javascript' }))).catch(()=>{});
      });
    }

    // Estado inicial de ejemplo si no hay nada guardado
    if (!storage.get('mp.seeded', false)) {
      TodoStore.importAll([
        { id: uid(), title: 'Explorar el mini proyecto', priority: 'medium', deadline: null, done: false, createdAt: Date.now()-3600_000, order: 0 },
        { id: uid(), title: 'Agregar mi primera tarea', priority: 'high', deadline: new Date().toISOString().slice(0,10), done: false, createdAt: Date.now()-1200_000, order: 1 }
      ]);
      NoteStore.importAll([
        { id: uid(), title: 'Bienvenido', text: 'Este es un bloc de notas rápido. Puedes buscar, copiar y eliminar.', tags: ['demo','notas'], createdAt: Date.now()-1800_000 }
      ]);
      storage.set('mp.seeded', true);
    }
  </script>
</body>
</html>
