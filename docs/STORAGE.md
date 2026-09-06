# STORAGE

## 1. Objetivo
Definir regras para armazenamento físico de documentos no servidor.

## 2. Premissas
- Arquivos salvos no disco local do servidor.
- PostgreSQL armazena somente metadados.
- Estrutura física recuperável sem software proprietário.

## 3. Estrutura Conceitual
Raiz sugerida:
- storage/clientes/{company_id}/{ano}/{competency_id}/{categoria}/{entity_id}

Os identificadores físicos devem ser estáveis e controlados pelo sistema. Nome fantasia ou razão social pode aparecer apenas como informação auxiliar, nunca como única referência do caminho.

Exemplo de categorias:
- MOVIMENTACAO_CONTABIL
- EXTRATOS
- INVESTIMENTOS
- DOCUMENTOS_CONTABILIDADE

## 4. Convenções de Nomes
- Normalização de nomes (sem caracteres perigosos).
- Preservação de nome original em metadado.
- Identificador interno para evitar colisões.

## 5. Pipeline de Upload
1. Autenticar usuário.
2. Autorizar ação por RBAC e empresa.
3. Validar tipo, tamanho e extensão.
4. Sanitizar nome.
5. Persistir arquivo em diretório controlado.
6. Gerar hash.
7. Registrar metadado no banco.
8. Registrar auditoria.

## 6. Pipeline de Download
1. Autenticar usuário.
2. Autorizar acesso ao arquivo pela empresa e permissão.
3. Resolver caminho físico com base no metadado.
4. Entregar stream ao cliente.
5. Registrar auditoria.

## 7. Lixeira e Retenção
- Exclusão lógica inicial (soft delete).
- Janela de retenção antes de purge definitivo.
- Restauração autorizada dentro da janela.

## 8. Integridade
- Hash de conteúdo no upload.
- Verificações periódicas opcionais por amostragem.
- Tratamento de inconsistência entre metadado e arquivo por reconciliação operacional auditada.
- Escrita deve usar arquivo temporário e publicação atômica quando suportado pelo filesystem.

## 9. Decisões Pendentes
- Tempo oficial de retenção da lixeira.
- Processo exato de purge definitivo.
- Política de antivírus e quarentena.
- Política de restauração quando o banco e o arquivo divergirem.

## 10. Implementação da Fase 05

- Caminho físico usa UUIDs de empresa, competência e documento.
- Extensões permitidas seguem a lista inicial da especificação.
- Upload grava em arquivo temporário e publica por `os.replace`.
- Hash SHA-256 e metadados são registrados pela API.
- Estado inicial é `quarantined`; somente documento aprovado fica disponível para download.
- O limite padrão é configurável por `LABORE_MAX_UPLOAD_SIZE_BYTES` e começa em 50 MiB.
