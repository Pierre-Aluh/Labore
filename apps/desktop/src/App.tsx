import { FormEvent, useState } from "react";

type Role = "cliente" | "escritorio" | "administrador";
type Session = { token: string; role: Role; displayName: string };
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
const navigation: Record<Role, string[]> = {
  cliente: ["Visão geral", "Documentos da contabilidade", "Enviar documentos", "Chamados", "Notificações"],
  escritorio: ["Visão geral", "Empresas", "Pendências", "Documentos recebidos", "Chamados"],
  administrador: ["Visão geral", "Empresas", "Usuários e papéis", "Departamentos", "Auditoria"],
};

export function App() {
  const [session, setSession] = useState<Session | null>(null);
  const [selectedPage, setSelectedPage] = useState("Visão geral");
  const [loginError, setLoginError] = useState("");

  async function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setLoginError("");
    const form = new FormData(event.currentTarget);
    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/auth/login`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email: form.get("email"), password: form.get("password") }) });
      if (!response.ok) throw new Error("login");
      const result = await response.json() as { access_token: string };
      const email = String(form.get("email"));
      setSession({ token: result.access_token, role: "cliente", displayName: email.split("@")[0] });
    } catch { setLoginError("Não foi possível conectar ao portal. Verifique a API e tente novamente."); }
  }

  if (!session) return <LoginScreen onSubmit={handleLogin} error={loginError} />;
  return <div className="shell">
    <aside className="sidebar">
      <div className="brand"><span className="brand-mark">L</span><span>Labore Portal</span></div>
      <div className="profile"><span className="avatar">{session.displayName.slice(0, 1).toUpperCase()}</span><div><strong>{session.displayName}</strong><small>{session.role}</small></div></div>
      <nav>{navigation[session.role].map((item) => <button className={selectedPage === item ? "nav-item active" : "nav-item"} key={item} onClick={() => setSelectedPage(item)}>{item}</button>)}</nav>
      <button className="logout" onClick={() => setSession(null)}>Sair</button>
    </aside>
    <main className="content"><header className="topbar"><div><span className="eyebrow">Portal privado</span><h1>{selectedPage}</h1></div><span className="connection"><i /> API configurada</span></header><Dashboard page={selectedPage} role={session.role} /></main>
  </div>;
}

function LoginScreen({ onSubmit, error }: { onSubmit: (event: FormEvent<HTMLFormElement>) => void; error: string }) {
  return <main className="login-page"><section className="login-intro"><div className="brand"><span className="brand-mark">L</span><span>Labore Portal</span></div><div><span className="eyebrow">Gestão contábil, com clareza</span><h1>O trabalho importante, em um só lugar.</h1><p>Documentos, pendências e atendimento organizados por empresa e competência.</p></div></section><form className="login-card" onSubmit={onSubmit}><span className="eyebrow">Acesso seguro</span><h2>Entrar no portal</h2><label>E-mail<input name="email" type="email" autoComplete="username" required /></label><label>Senha<input name="password" type="password" autoComplete="current-password" required /></label>{error && <div className="error">{error}</div>}<button className="primary" type="submit">Entrar</button><small>Ambiente: desenvolvimento</small></form></main>;
}

function Dashboard({ page, role }: { page: string; role: Role }) {
  const cards = role === "cliente" ? [["03", "Pendências abertas"], ["08", "Documentos disponíveis"], ["01", "Chamado aguardando resposta"]] : [["24", "Empresas acompanhadas"], ["17", "Pendências para triagem"], ["06", "Chamados abertos"]];
  return <section className="workspace"><div className="welcome"><div><span className="eyebrow">{role === "cliente" ? "Sua operação" : "Visão operacional"}</span><h2>{page === "Visão geral" ? "Bom dia. Aqui está o que pede atenção." : page}</h2></div><button className="secondary">Atualizar</button></div><div className="metrics">{cards.map(([value, label]) => <article className="metric" key={label}><strong>{value}</strong><span>{label}</span></article>)}</div><div className="activity"><div className="section-heading"><h3>Atividade recente</h3><button className="text-button">Ver histórico</button></div><div className="activity-row"><span className="activity-icon blue">D</span><div><strong>Área pronta para uso</strong><span>Os dados aparecerão aqui conforme a API receber movimentações.</span></div><time>Agora</time></div><div className="activity-row"><span className="activity-icon green">✓</span><div><strong>Ambiente separado</strong><span>Você está trabalhando em um ambiente de desenvolvimento.</span></div><time>Hoje</time></div></div></section>;
}
