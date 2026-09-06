import { FormEvent, useEffect, useState } from "react";
import type { ReactNode } from "react";

type Role = "cliente" | "colaborador" | "administrador";
type Session = { token: string; role: Role; displayName: string; companyIds: string[] };
type DocumentItem = { id: string; original_filename: string; status: string; file_size_bytes: number; checksum_hash: string };
type Competency = { id: string; year: number; month: number; status: string };
type Category = { id: string; code: string; name: string };
type Ticket = { id: string; subject: string; description: string; status: string; company_id: string; department_id: string | null };
type Message = { id: string; ticket_id: string; author_user_id: string; body: string };
type Notification = { id: string; title: string; body: string; event_type: string; is_read: boolean };
type Company = { id: string; legal_name: string; trade_name: string | null; tax_identifier: string; status: string };
type AdminUser = { id: string; email: string; display_name: string; status: string };
type AuditEntry = { id: string; action: string; target_type: string; outcome: string; created_at: string };

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
const navigation: Record<Role, string[]> = {
  cliente: ["Visão geral", "Documentos da contabilidade", "Enviar documentos", "Chamados", "Notificações"],
  colaborador: ["Visão geral", "Empresas", "Pendências", "Documentos recebidos", "Chamados"],
  administrador: ["Visão geral", "Empresas", "Usuários e papéis", "Departamentos", "Auditoria"],
};

async function request<T>(path: string, token: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`, { ...init, headers: { Authorization: `Bearer ${token}`, ...init.headers } });
  if (!response.ok) throw new Error(`API ${response.status}`);
  return response.status === 204 ? undefined as T : response.json() as Promise<T>;
}

function resolveRole(roles: string[]): Role {
  if (roles.includes("Administrador")) return "administrador";
  if (roles.includes("Cliente")) return "cliente";
  return "colaborador";
}

export function App() {
  const [session, setSession] = useState<Session | null>(null);
  const [selectedPage, setSelectedPage] = useState("Visão geral");
  const [loginError, setLoginError] = useState("");

  async function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setLoginError("");
    const form = new FormData(event.currentTarget);
    try {
      const login = await fetch(`${apiBaseUrl}/api/v1/auth/login`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email: form.get("email"), password: form.get("password") }) });
      if (!login.ok) throw new Error("login");
      const result = await login.json() as { access_token: string };
      const profile = await request<{ display_name: string; roles: string[]; company_ids: string[] }>("/api/v1/auth/me", result.access_token);
      setSession({ token: result.access_token, role: resolveRole(profile.roles), displayName: profile.display_name, companyIds: profile.company_ids });
      setSelectedPage("Visão geral");
    } catch { setLoginError("Não foi possível conectar ao portal. Verifique a API e tente novamente."); }
  }

  if (!session) return <LoginScreen onSubmit={handleLogin} error={loginError} />;
  if (session.role === "cliente" && selectedPage === "Visão geral") return <ClientHome session={session} onNavigate={setSelectedPage} onLogout={() => setSession(null)} />;
  return <div className="shell">
    <aside className="sidebar"><div className="brand"><span className="brand-mark">L</span><span>Labore Portal</span></div><div className="profile"><span className="avatar">{session.displayName.slice(0, 1).toUpperCase()}</span><div><strong>{session.displayName}</strong><small>{session.role}</small></div></div><nav>{navigation[session.role].map((item) => <button className={selectedPage === item ? "nav-item active" : "nav-item"} key={item} onClick={() => setSelectedPage(item)}>{item}</button>)}</nav><button className="logout" onClick={() => setSession(null)}>Sair</button></aside>
    <main className="content"><header className="topbar"><div><span className="eyebrow">Portal privado</span><h1>{selectedPage}</h1></div><span className="connection"><i /> API conectada</span></header><Workspace page={selectedPage} session={session} /></main>
  </div>;
}

function ClientHome({ session, onNavigate, onLogout }: { session: Session; onNavigate: (page: string) => void; onLogout: () => void }) {
  return <main className="client-home">
    <div className="client-home-topline">
      <button className="client-notifications" onClick={() => onNavigate("Notificações")} aria-label="Abrir notificações"><span className="bell-mark" aria-hidden="true">♧</span><span>Notificações</span></button>
      <div className="client-user"><span>{session.displayName}</span><button onClick={onLogout}>Sair</button></div>
    </div>
    <img className="client-home-logo" src="/assets/labore-logo.png" alt="Labore" />
    <div className="client-home-actions" aria-label="Atalhos principais do cliente">
      <button className="client-hotspot support" onClick={() => onNavigate("Chamados")} aria-label="Abrir suporte"><span>Suporte</span></button>
      <button className="client-hotspot accounting" onClick={() => onNavigate("Documentos da contabilidade")} aria-label="Abrir documentos da contabilidade"><span>Documentos da contabilidade</span></button>
      <button className="client-hotspot upload" onClick={() => onNavigate("Enviar documentos")} aria-label="Enviar documentos"><span>Enviar documentos</span></button>
      <button className="client-hotspot finance" onClick={() => onNavigate("Documentos da contabilidade")} aria-label="Abrir financeiro"><span>Financeiro</span></button>
    </div>
  </main>;
}

function Workspace({ page, session }: { page: string; session: Session }) {
  if (session.role === "cliente") return <ClientWorkspace page={page} session={session} />;
  if (session.role === "administrador") return <AdminWorkspace page={page} session={session} />;
  return <CollaboratorWorkspace page={page} session={session} />;
}

function ClientWorkspace({ page, session }: { page: string; session: Session }) {
  const [documents, setDocuments] = useState<DocumentItem[]>([]); const [competencies, setCompetencies] = useState<Competency[]>([]); const [categories, setCategories] = useState<Category[]>([]); const [tickets, setTickets] = useState<Ticket[]>([]); const [notifications, setNotifications] = useState<Notification[]>([]); const [message, setMessage] = useState("");
  const companyId = session.companyIds[0];
  useEffect(() => { if (!companyId) return; Promise.all([request<DocumentItem[]>(`/api/v1/documents?company_id=${companyId}`, session.token), request<Competency[]>(`/api/v1/documents/competencies?company_id=${companyId}`, session.token), request<Category[]>("/api/v1/documents/categories", session.token), request<Ticket[]>(`/api/v1/tickets/companies/${companyId}`, session.token), request<Notification[]>("/api/v1/notifications", session.token)]).then(([docs, loadedCompetencies, loadedCategories, loadedTickets, loadedNotifications]) => { setDocuments(docs); setCompetencies(loadedCompetencies); setCategories(loadedCategories); setTickets(loadedTickets); setNotifications(loadedNotifications); }).catch(() => setMessage("Não foi possível carregar os dados da empresa.")); }, [companyId, session.token]);
  if (!companyId) return <EmptyState title="Nenhuma empresa vinculada" detail="Solicite ao escritório o vínculo da sua empresa." />;
  if (page === "Documentos da contabilidade") return <Panel title="Documentos da contabilidade" detail="Arquivos liberados pelo escritório, organizados por competência."><DocumentList token={session.token} documents={documents} empty="Nenhum documento foi disponibilizado ainda." /></Panel>;
  if (page === "Enviar documentos") return <Panel title="Enviar documentos" detail="O envio passa pela API e entra em quarentena até validação."><UploadForm token={session.token} companyId={companyId} competencyId={competencies[0]?.id} categoryId={categories[0]?.id} onUploaded={() => setMessage("Documento enviado e aguardando validação.")} /><Notice message={message} /></Panel>;
  if (page === "Chamados") return <TicketPanel token={session.token} companyId={companyId} tickets={tickets} onCreated={(ticket) => setTickets([ticket, ...tickets])} />;
  if (page === "Notificações") return <NotificationPanel notifications={notifications} />;
  return <Summary title="Sua operação" cards={[[String(documents.length), "Documentos disponíveis"], [String(tickets.filter((ticket) => ticket.status !== "closed").length), "Chamados abertos"], [String(notifications.filter((notification) => !notification.is_read).length), "Notificações não lidas"]]} detail={message} />;
}

function CollaboratorWorkspace({ page, session }: { page: string; session: Session }) {
  const [companies, setCompanies] = useState<Company[]>([]); const [documents, setDocuments] = useState<DocumentItem[]>([]); const [tickets, setTickets] = useState<Ticket[]>([]); const [error, setError] = useState("");
  useEffect(() => { request<Company[]>("/api/v1/workspace/companies", session.token).then(setCompanies).catch(() => setError("Sem acesso às empresas ou nenhuma empresa cadastrada.")); request<DocumentItem[]>("/api/v1/workspace/documents", session.token).then(setDocuments).catch(() => undefined); request<Ticket[]>("/api/v1/workspace/tickets", session.token).then(setTickets).catch(() => undefined); }, [session.token]);
  if (page === "Empresas") return <Panel title="Empresas atendidas" detail="Visão operacional limitada às permissões do colaborador."><List items={companies.map((company) => `${company.legal_name} · ${company.tax_identifier}`)} empty={error || "Nenhuma empresa encontrada."} /></Panel>;
  if (page === "Documentos recebidos" || page === "Pendências") return <Panel title={page} detail="Triagem por empresa e competência."><List items={documents.map((document) => `${document.original_filename} · ${document.status}`)} empty="Nenhum documento disponível para triagem." /></Panel>;
  if (page === "Chamados") return <Panel title="Chamados do escritório" detail="Acesse os chamados das empresas vinculadas conforme seu papel."><List items={tickets.map((ticket) => `${ticket.subject} · ${ticket.status}`)} empty="Nenhum chamado pendente." /></Panel>;
  return <Summary title="Visão operacional" cards={[[String(companies.length), "Empresas acessíveis"], [String(documents.length), "Documentos para triagem"], ["RBAC", "Permissões aplicadas"]]} detail={error} />;
}

function AdminWorkspace({ page, session }: { page: string; session: Session }) {
  const [companies, setCompanies] = useState<Company[]>([]); const [roles, setRoles] = useState<string[]>([]); const [users, setUsers] = useState<AdminUser[]>([]); const [audit, setAudit] = useState<AuditEntry[]>([]); const [message, setMessage] = useState("");
  useEffect(() => { Promise.all([request<Company[]>("/api/v1/admin/companies", session.token), request<string[]>("/api/v1/admin/roles", session.token), request<AdminUser[]>("/api/v1/admin/users", session.token), request<AuditEntry[]>("/api/v1/admin/audit", session.token)]).then(([loadedCompanies, loadedRoles, loadedUsers, loadedAudit]) => { setCompanies(loadedCompanies); setRoles(loadedRoles); setUsers(loadedUsers); setAudit(loadedAudit); }).catch(() => setMessage("Não foi possível carregar os dados administrativos.")); }, [session.token]);
  if (page === "Empresas") return <Panel title="Gestão de empresas" detail="Cadastro e consulta sujeitos à auditoria."><List items={companies.map((company) => `${company.legal_name} · ${company.status}`)} empty="Nenhuma empresa cadastrada." /></Panel>;
  if (page === "Usuários e papéis") return <Panel title="Usuários e papéis" detail="Usuários e papéis carregados da API administrativa."><List items={[...roles.map((role) => `Papel · ${role}`), ...users.map((user) => `${user.display_name} · ${user.email} · ${user.status}`)]} empty="Nenhum usuário ou papel carregado." /></Panel>;
  if (page === "Departamentos") return <Panel title="Departamentos" detail="A distribuição de chamados usa departamentos do escritório."><List items={["Contábil", "Fiscal", "Departamento Pessoal", "Legalização", "Financeiro", "Outros"]} empty="Nenhum departamento." /></Panel>;
  if (page === "Auditoria") return <Panel title="Auditoria" detail="Últimos eventos registrados pela API."><List items={audit.map((entry) => `${entry.action} · ${entry.target_type} · ${entry.outcome} · ${entry.created_at}`)} empty="Nenhum evento de auditoria." /></Panel>;
  return <Summary title="Visão administrativa" cards={[[String(companies.length), "Empresas"], [String(roles.length), "Papéis RBAC"], ["API", "Autorização ativa"]]} detail={message} />;
}

function TicketPanel({ token, companyId, tickets, onCreated }: { token: string; companyId: string; tickets: Ticket[]; onCreated: (ticket: Ticket) => void }) { const [subject, setSubject] = useState(""); const [description, setDescription] = useState(""); const [message, setMessage] = useState(""); const [error, setError] = useState(""); const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null); const [messages, setMessages] = useState<Message[]>([]); async function submit(event: FormEvent) { event.preventDefault(); try { const ticket = await request<Ticket>("/api/v1/tickets", token, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ company_id: companyId, subject, description }) }); onCreated(ticket); setSubject(""); setDescription(""); } catch { setError("Não foi possível abrir o chamado."); } } async function selectTicket(ticket: Ticket) { setSelectedTicket(ticket); try { setMessages(await request<Message[]>(`/api/v1/tickets/${ticket.id}/messages`, token)); } catch { setError("Não foi possível carregar a conversa."); } } async function sendMessage(event: FormEvent) { event.preventDefault(); if (!selectedTicket || !message.trim()) return; try { const created = await request<Message>(`/api/v1/tickets/${selectedTicket.id}/messages`, token, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ body: message }) }); setMessages([...messages, created]); setMessage(""); } catch { setError("Não foi possível enviar a mensagem."); } } return <Panel title="Chamados e suporte" detail="Abra um chamado, acompanhe o histórico e converse pelo portal."><form className="inline-form" onSubmit={submit}><input placeholder="Assunto" value={subject} onChange={(event) => setSubject(event.target.value)} required /><textarea placeholder="Descreva sua solicitação" value={description} onChange={(event) => setDescription(event.target.value)} required /><button className="primary" type="submit">Abrir chamado</button></form><Notice message={error} /><div className="ticket-layout"><div><List items={tickets.map((ticket) => `${ticket.subject} · ${ticket.status}`)} empty="Nenhum chamado aberto." />{tickets.map((ticket) => <button className="text-button ticket-select" key={ticket.id} onClick={() => selectTicket(ticket)}>Abrir conversa: {ticket.subject}</button>)}</div>{selectedTicket && <div className="conversation"><h3>{selectedTicket.subject}</h3><List items={messages.map((item) => item.body)} empty="Nenhuma mensagem ainda." /><form className="inline-form" onSubmit={sendMessage}><textarea placeholder="Escreva uma resposta" value={message} onChange={(event) => setMessage(event.target.value)} required /><button className="primary" type="submit">Enviar mensagem</button></form></div>}</div></Panel>; }
function UploadForm({ token, companyId, competencyId, categoryId, onUploaded }: { token: string; companyId: string; competencyId?: string; categoryId?: string; onUploaded: () => void }) { const [file, setFile] = useState<File | null>(null); const [error, setError] = useState(""); async function submit(event: FormEvent) { event.preventDefault(); if (!file || !competencyId || !categoryId) { setError("Nenhuma competência ou categoria está disponível para envio."); return; } const form = new FormData(); form.append("company_id", companyId); form.append("competency_id", competencyId); form.append("category_id", categoryId); form.append("file", file); try { const response = await fetch(`${apiBaseUrl}/api/v1/documents`, { method: "POST", headers: { Authorization: `Bearer ${token}` }, body: form }); if (!response.ok) throw new Error(); onUploaded(); setFile(null); } catch { setError("Não foi possível enviar o documento."); } } return <form className="upload-form" onSubmit={submit}><input type="file" onChange={(event) => setFile(event.target.files?.[0] ?? null)} required /><button className="primary" type="submit">Enviar para validação</button><Notice message={error} /></form>; }

function DocumentList({ token, documents, empty }: { token: string; documents: DocumentItem[]; empty: string }) { const [error, setError] = useState(""); async function download(item: DocumentItem) { try { const response = await fetch(`${apiBaseUrl}/api/v1/documents/${item.id}/download`, { headers: { Authorization: `Bearer ${token}` } }); if (!response.ok) throw new Error(); const blob = await response.blob(); const url = URL.createObjectURL(blob); const link = globalThis.document.createElement("a"); link.href = url; link.download = item.original_filename; link.click(); URL.revokeObjectURL(url); } catch { setError("Não foi possível baixar este documento."); } } return documents.length ? <><ul className="data-list">{documents.map((item) => <li className="data-list-row" key={item.id}><span>{item.original_filename} · {Math.ceil(item.file_size_bytes / 1024)} KB</span><button className="text-button" onClick={() => download(item)}>Baixar</button></li>)}</ul><Notice message={error} /></> : <div className="empty-state">{empty}</div>; }
function NotificationPanel({ notifications }: { notifications: Notification[] }) { return <Panel title="Notificações" detail="Avisos de documentos, chamados e pendências da sua empresa."><List items={notifications.map((notification) => `${notification.title} · ${notification.is_read ? "lida" : "não lida"}`)} empty="Nenhuma notificação recebida." /></Panel>; }
function Summary({ title, cards, detail }: { title: string; cards: string[][]; detail: string }) { return <section className="workspace"><div className="welcome"><div><span className="eyebrow">Área de trabalho</span><h2>{title}</h2></div></div><div className="metrics">{cards.map(([value, label]) => <article className="metric" key={label}><strong>{value}</strong><span>{label}</span></article>)}</div><Notice message={detail || "Os dados desta área são carregados pela API conforme suas permissões."} /></section>; }
function Panel({ title, detail, children }: { title: string; detail: string; children: ReactNode }) { return <section className="workspace"><div className="welcome"><div><span className="eyebrow">Área de trabalho</span><h2>{title}</h2><p className="panel-detail">{detail}</p></div></div><div className="panel">{children}</div></section>; }
function List({ items, empty }: { items: string[]; empty: string }) { return items.length ? <ul className="data-list">{items.map((item) => <li key={item}>{item}</li>)}</ul> : <div className="empty-state">{empty}</div>; }
function Notice({ message }: { message: string }) { return message ? <div className="notice">{message}</div> : null; }
function EmptyState({ title, detail }: { title: string; detail: string }) { return <section className="workspace"><div className="empty-state"><h2>{title}</h2><p>{detail}</p></div></section>; }
function LoginScreen({ onSubmit, error }: { onSubmit: (event: FormEvent<HTMLFormElement>) => void; error: string }) { return <main className="login-page"><section className="login-intro"><div className="brand"><span className="brand-mark">L</span><span>Labore Portal</span></div><div><span className="eyebrow">Gestão contábil, com clareza</span><h1>O trabalho importante, em um só lugar.</h1><p>Documentos, pendências e atendimento organizados por empresa e competência.</p></div></section><form className="login-card" onSubmit={onSubmit}><span className="eyebrow">Acesso seguro</span><h2>Entrar no portal</h2><label>E-mail<input name="email" type="email" autoComplete="username" required /></label><label>Senha<input name="password" type="password" autoComplete="current-password" required /></label>{error && <div className="error">{error}</div>}<button className="primary" type="submit">Entrar</button><small>Ambiente: desenvolvimento</small></form></main>; }
