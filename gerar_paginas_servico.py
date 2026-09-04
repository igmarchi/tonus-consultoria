# -*- coding: utf-8 -*-
"""
Gera as 6 páginas de serviço da Tonus Consultoria em /servicos/*.html
a partir do mesmo conteúdo que já existe nos modais do index.html
(objeto modalData). Não inventa texto novo além de meta description,
title, breadcrumb e alt-texts de SEO.
"""
import os, json, re

BASE_URL = "https://www.tonusconsultoria.com.br"
OUT_DIR = "/home/claude/tonus_site_fix/servicos"
os.makedirs(OUT_DIR, exist_ok=True)

# mesma lista de 15 cidades já usada no schema do index.html (Ajuste 1 do GBP)
AREA_SERVED = [
    "Pirassununga", "Porto Ferreira", "Descalvado", "Santa Cruz das Palmeiras",
    "São Carlos", "Rio Claro", "Araras", "Leme", "Mogi Guaçu", "Mogi Mirim",
    "Casa Branca", "Santa Rita do Passa Quatro", "Analândia", "Tambaú", "Aguaí",
]

SERVICOS = [
    {
        "slug": "diagnostico-empresarial",
        "eyebrow": "O QUE ENTREGAMOS",
        "icone": "🩺",
        "titulo": "Diagnóstico Empresarial",
        "resumo": "Avaliação completa em 6 dimensões com relatório detalhado e apresentação de resultado.",
        "problema": "A maioria dos empresários toma decisões baseadas em intuição — e não por falta de inteligência, mas por falta de informação organizada. Sem enxergar claramente onde o negócio está saudável e onde está sangrando, qualquer investimento ou mudança vira aposta. O resultado é um ciclo de esforço sem resultado proporcional.",
        "fazemos": "Realizamos uma avaliação estruturada em 6 dimensões: financeiro, operacional, comercial, pessoas, estratégia e gestão. Entrevistamos o fundador, analisamos os números disponíveis e mapeamos os pontos críticos. Ao final, entregamos um relatório objetivo com os principais achados e apresentamos as prioridades de ação em ordem de impacto.",
        "resultado": "Finalmente saber onde a energia está sendo gasta sem retorno — e onde agir primeiro para virar o jogo.",
        "meta_desc": "Diagnóstico empresarial completo em 6 dimensões (financeiro, operacional, comercial, pessoas, estratégia e gestão) para MEI e PME em Pirassununga e região. Relatório objetivo com prioridades de ação.",
        "keywords": "diagnóstico empresarial, diagnóstico de negócio, consultoria empresarial Pirassununga, avaliação de negócio MEI PME",
        "faq": [
            ("Quanto tempo leva o diagnóstico empresarial?", "O diagnóstico é feito em 6 dimensões — financeiro, operacional, comercial, pessoas, estratégia e gestão — e termina com um relatório objetivo e a apresentação das prioridades de ação. Atualmente ele está disponível gratuitamente por tempo limitado para os primeiros interessados."),
            ("O diagnóstico é pago?", "Por tempo limitado, o diagnóstico completo é oferecido gratuitamente para os primeiros interessados, sem compromisso de contratação posterior."),
        ],
    },
    {
        "slug": "gestao-financeira",
        "eyebrow": "O QUE ENTREGAMOS",
        "icone": "📊",
        "titulo": "Gestão Financeira",
        "resumo": "Fluxo de caixa, precificação, controle de custos e clareza sobre o lucro real do negócio.",
        "problema": "Faturar bem e não sobrar dinheiro é um dos problemas mais comuns — e mais frustrantes — entre MEIs e PMEs. Sem fluxo de caixa estruturado, sem saber o custo real de cada produto ou serviço e sem separar pessoa física de pessoa jurídica, o empresário trabalha muito para lucrar pouco. Muitos só descobrem o prejuízo quando a conta não fecha.",
        "fazemos": "Organizamos o fluxo de caixa, calculamos o custo real e o preço justo de cada produto ou serviço, identificamos desperdícios ocultos e criamos uma rotina financeira simples de manter. Não usamos planilhas complexas — usamos ferramentas que o empresário consegue operar sozinho depois que saímos.",
        "resultado": "Saber, pela primeira vez, quanto realmente se lucra por mês — e muitas vezes descobrir que o preço cobrado estava abaixo do que deveria.",
        "meta_desc": "Gestão financeira para MEI e PME em Pirassununga e região: fluxo de caixa, precificação e controle de custos. Descubra quanto sua empresa realmente lucra.",
        "keywords": "gestão financeira empresarial, consultoria financeira Pirassununga, fluxo de caixa MEI PME, precificação",
        "faq": [
            ("Preciso ter uma planilha financeira pronta para começar?", "Não. Organizamos o fluxo de caixa e o controle de custos do zero, com ferramentas simples que você consegue operar sozinho depois do acompanhamento — sem depender de planilhas complexas."),
            ("Serve para quem já fatura bem mas não sabe se está lucrando?", "Sim — é exatamente esse o cenário mais comum: faturar bem sem saber o custo real de cada produto ou serviço. Ajudamos a calcular o preço justo e a identificar onde o dinheiro está sendo perdido."),
        ],
    },
    {
        "slug": "reestruturacao-operacional",
        "eyebrow": "O QUE ENTREGAMOS",
        "icone": "⚙️",
        "titulo": "Reestruturação Operacional",
        "resumo": "Organização de processos, eliminação de gargalos e rotinas que funcionam sem o fundador.",
        "problema": "Quando tudo depende do dono, o negócio não escala — ele sufoca. O empresário vira o gargalo da própria empresa: está em tudo, decide tudo e, quando sai, tudo para. Processos informais, retrabalho constante e falta de padrão geram custos invisíveis e impedem o crescimento mesmo quando a demanda existe.",
        "fazemos": "Mapeamos os processos atuais, identificamos gargalos e atividades que consomem tempo sem gerar valor. Criamos rotinas, checklists e padrões operacionais que a equipe consegue seguir sem depender do fundador para cada decisão. O objetivo é liberar o dono para trabalhar no negócio, não dentro dele.",
        "resultado": "Conseguir se afastar do dia a dia — férias, uma viagem, um imprevisto — sem que o negócio pare.",
        "meta_desc": "Reestruturação operacional para MEI e PME em Pirassununga e região: mapeamento de processos, eliminação de gargalos e rotinas que não dependem do fundador.",
        "keywords": "reestruturação operacional, consultoria de processos, gargalos operacionais, consultoria Pirassununga",
        "faq": [
            ("Serve para negócios pequenos, com poucos funcionários?", "Sim. O problema de tudo depender do dono aparece mesmo em negócios pequenos ou sem funcionários — criamos rotinas e padrões que funcionam para qualquer porte, de MEI a PME."),
            ("O que muda no dia a dia depois da reestruturação?", "O objetivo é reduzir a dependência do fundador: processos, checklists e padrões que a equipe consegue seguir sozinha, liberando o dono para trabalhar no negócio, não apenas dentro dele."),
        ],
    },
    {
        "slug": "planejamento-estrategico",
        "eyebrow": "O QUE ENTREGAMOS",
        "icone": "🎯",
        "titulo": "Planejamento Estratégico",
        "resumo": "Metas, posicionamento e plano de crescimento com indicadores que mostram o caminho.",
        "problema": "Trabalhar duro sem direção clara é como remar forte num barco sem leme. Muitos empresários estão tão ocupados resolvendo o dia a dia que nunca param para definir onde querem chegar — e isso não é falta de ambição, é falta de método. Sem metas concretas e indicadores, qualquer resultado parece bom o suficiente, mas nenhum é suficientemente bom.",
        "fazemos": "Definimos juntos o posicionamento do negócio, os diferenciais reais frente à concorrência, as metas de crescimento para 12 e 36 meses e os indicadores que vão mostrar se o caminho está correto. O plano é prático, não teórico — cabe numa página e é revisado a cada trimestre.",
        "resultado": "Sair com um plano de 12 meses no papel, indicadores claros e a sensação de saber para onde o negócio está indo.",
        "meta_desc": "Planejamento estratégico empresarial para MEI e PME em Pirassununga e região: metas de 12 e 36 meses, posicionamento e indicadores de acompanhamento trimestral.",
        "keywords": "planejamento estratégico empresarial, consultoria estratégica Pirassununga, metas de crescimento MEI PME",
        "faq": [
            ("O plano estratégico é revisado com que frequência?", "O plano é revisado a cada trimestre, com metas de crescimento definidas para 12 e 36 meses e indicadores que mostram se o caminho está correto."),
            ("Preciso já ter clareza sobre onde quero chegar?", "Não. Grande parte do trabalho é justamente ajudar a definir esse destino — o posicionamento, os diferenciais reais e as metas concretas, com método, não só intuição."),
        ],
    },
    {
        "slug": "gestao-de-equipes",
        "eyebrow": "O QUE ENTREGAMOS",
        "icone": "👥",
        "titulo": "Gestão de Equipes",
        "resumo": "Estrutura de papéis, delegação, cultura organizacional e redução da dependência do líder.",
        "problema": "Uma equipe sem estrutura clara de papéis e responsabilidades gera conflito, retrabalho e desmotivação — mesmo com boas pessoas. O problema raramente é quem trabalha, mas como o trabalho está organizado. Líderes que não delegam porque “é mais rápido fazer eu mesmo” acabam sobrecarregados, e a equipe, subutilizada.",
        "fazemos": "Desenhamos o organograma funcional, definimos claramente as responsabilidades de cada função, criamos critérios de delegação e desenvolvemos com o empresário um modelo de liderança que engaja sem gerar dependência. Quando necessário, apoiamos na estruturação de processos de seleção, integração e avaliação de desempenho.",
        "resultado": "Ver a equipe resolver a maior parte dos problemas sozinha — não porque foi mandada, mas porque sabe o que fazer.",
        "meta_desc": "Consultoria em gestão de equipes para MEI e PME em Pirassununga e região: estrutura de papéis, delegação e cultura organizacional que reduz a dependência do fundador.",
        "keywords": "gestão de equipes, consultoria de liderança, delegação empresarial, consultoria Pirassununga",
        "faq": [
            ("Isso serve mesmo sem eu ter uma equipe grande?", "Sim. Trabalhamos com negócios de 1 a 50 colaboradores — o desenho de papéis e os critérios de delegação ajudam tanto quem tem uma equipe pequena quanto quem já está maior."),
            ("Vocês ajudam também na contratação da equipe?", "Quando necessário, apoiamos na estruturação de processos de seleção, integração e avaliação de desempenho — mas o foco principal é a estrutura de papéis e o modelo de liderança."),
        ],
    },
    {
        "slug": "educacao-financeira-pessoal",
        "eyebrow": "O QUE ENTREGAMOS",
        "icone": "💡",
        "titulo": "Educação Financeira Pessoal",
        "resumo": "Para profissionais que querem organizar finanças, criar reservas e planejar o futuro. Sem produto financeiro.",
        "problema": "Profissionais que ganham bem muitas vezes chegam ao fim do mês sem saber onde o dinheiro foi. Sem organização financeira pessoal, não há reserva de emergência, não há investimento, não há planejamento de aposentadoria. A sensação de “trabalhar para pagar contas” se perpetua independente do salário — porque o problema não é quanto se ganha, é como se gerencia.",
        "fazemos": "Trabalhamos o orçamento pessoal, a separação de gastos por categoria, a criação de uma reserva de emergência e os primeiros passos no mundo dos investimentos — sem indicar produto financeiro e sem conflito de interesse. O foco é consciência e método, não produto. Atendemos pessoas físicas e também sócios que querem separar definitivamente as finanças pessoais das empresariais.",
        "resultado": "Construir a primeira reserva de emergência e parar de usar o cartão de crédito como muleta em poucos meses de acompanhamento.",
        "meta_desc": "Educação financeira pessoal em Pirassununga e região: orçamento, reserva de emergência e primeiros passos em investimentos, sem indicar produto financeiro.",
        "keywords": "educação financeira pessoal, consultoria financeira pessoal, reserva de emergência, orçamento pessoal Pirassununga",
        "faq": [
            ("Vocês indicam produtos de investimento?", "Não. Trabalhamos consciência e método — orçamento, reserva de emergência e primeiros passos em investimentos — sem indicar produto financeiro e sem conflito de interesse."),
            ("Esse serviço é só para quem tem uma empresa?", "Não. Atendemos pessoas físicas e também sócios que querem separar definitivamente as finanças pessoais das empresariais."),
        ],
    },
    {
        "slug": "sistema-de-gestao-sob-medida",
        "eyebrow": "O QUE ENTREGAMOS",
        "icone": "💻",
        "icone_tabler": "ti-device-desktop-analytics",
        "titulo": "Sistema de Gestão Sob Medida",
        "resumo": "Cadastro de clientes, estoque, financeiro e produtividade em um sistema só, construído pro seu negócio.",
        "problema": "Muitos negócios pequenos ainda controlam tudo em cadernos, grupos de WhatsApp ou planilhas soltas — sem visibilidade real de quanto entra, quanto sai, o que está no estoque ou o que cada cliente já comprou. Sem esses dados organizados, toda decisão vira chute, e problemas como estoque parado ou inadimplência só aparecem tarde demais.",
        "fazemos": "Desenvolvemos um sistema de gestão sob medida para o seu negócio — não um software genérico de prateleira. Reunimos em um só lugar o que faz sentido pra sua operação: cadastro de clientes, controle de estoque, fluxo de caixa, indicadores de produtividade e histórico de atendimentos. Simples de usar no dia a dia, sem depender de planilhas paralelas. Quando o diagnóstico aponta uma fragilidade na presença digital do negócio, a mesma equipe também ajuda a estruturar ou reformular o site — dentro do plano de ação, não como um serviço à parte.",
        "resultado": "Ter, pela primeira vez, uma visão real do negócio — o que entra, o que sai, o que está faltando — tudo em um lugar só, sem depender de anotações espalhadas.",
        "meta_desc": "Sistema de gestão sob medida para MEI e PME em Pirassununga e região: cadastro de clientes, controle de estoque, fluxo de caixa e indicadores de produtividade em um só lugar.",
        "keywords": "sistema de gestão sob medida, software de gestão para pequenas empresas, sistema de controle de estoque e financeiro, consultoria Pirassununga",
        "faq": [
            ("O sistema é feito do zero ou é um software pronto?", "É construído sob medida pro seu negócio — partimos do que você realmente precisa controlar no dia a dia, em vez de adaptar sua operação a um software genérico de prateleira."),
            ("Preciso ter conhecimento técnico para usar?", "Não. O sistema é pensado pra ser operado por quem toca o negócio no dia a dia, sem treinamento técnico — cadastro, lançamentos e consultas ficam em telas simples e diretas."),
            ("Vocês também fazem o site do negócio?", "Não é um serviço padrão da Tonus, mas quando o diagnóstico aponta que a presença digital está travando o negócio, ajudamos a estruturar ou criar o site — dentro do plano de ação definido com você, com a mesma equipe que cuida do seu sistema de gestão."),
        ],
        "media_html": """<div class="servico-media">
    <img src="/clientes/no-grau-tour.gif" alt="Tour em vídeo pelo sistema de gestão desenvolvido para a No Grau Estética Automotiva: cadastro de clientes, estoque, atendimentos e financeiro" loading="lazy" width="680" height="383">
    <p class="servico-media-legenda">Prévia real do sistema desenvolvido para a <a href="/#servicos">No Grau — Estética Automotiva</a>, cliente da Tonus desde agosto de 2026.</p>
  </div>""",
    },
]

for s in SERVICOS:
    s["url"] = f"{BASE_URL}/servicos/{s['slug']}.html"

CSS = """
*{margin:0;padding:0;box-sizing:border-box;}
:root{
  --navy:#1B3A5C;--gold:#C8973A;--burg:#5C1F3A;--cream:#F7F4EF;
  --muted:#7A8090;--dark:#0D1117;
}
html{scroll-behavior:smooth;}
body{background:var(--cream);font-family:'DM Sans',sans-serif;color:var(--dark);overflow-x:hidden;}
a{text-decoration:none;color:inherit;}
button{cursor:pointer;font-family:'DM Sans',sans-serif;}

nav{background:var(--navy);padding:0 52px;display:flex;align-items:center;justify-content:space-between;height:68px;position:sticky;top:0;z-index:100;border-bottom:1px solid rgba(200,151,58,.1);}
.nav-logo{font-family:'Cormorant Garamond',serif;font-size:22px;font-weight:700;color:var(--cream);letter-spacing:4px;}
.nav-logo span{display:block;font-size:9px;font-weight:300;color:var(--gold);letter-spacing:5px;margin-top:-5px;}
.nav-links{display:flex;gap:32px;}
.nav-links a{color:rgba(247,244,239,.6);font-size:12px;letter-spacing:1.5px;transition:color .2s;}
.nav-links a:hover{color:var(--gold);}
.nav-cta{display:inline-block;background:transparent;border:1px solid var(--gold);color:var(--gold);padding:8px 22px;font-size:11px;letter-spacing:2px;transition:all .2s;}
.nav-cta:hover{background:var(--gold);color:var(--navy);}
.nav-hamburger{display:none;flex-direction:column;gap:5px;background:none;border:none;padding:6px;cursor:pointer;}
.nav-hamburger span{display:block;width:22px;height:2px;background:var(--gold);transition:all .3s;}
.nav-hamburger.open span:nth-child(1){transform:translateY(7px) rotate(45deg);}
.nav-hamburger.open span:nth-child(2){opacity:0;}
.nav-hamburger.open span:nth-child(3){transform:translateY(-7px) rotate(-45deg);}
.nav-mobile{display:none;position:fixed;top:68px;left:0;width:100%;background:var(--navy);border-top:1px solid rgba(200,151,58,.1);flex-direction:column;z-index:99;padding:24px 24px 32px;}
.nav-mobile.open{display:flex;}
.nav-mobile a{color:rgba(247,244,239,.7);font-size:14px;letter-spacing:1.5px;padding:12px 0;border-bottom:1px solid rgba(255,255,255,.05);}
.nav-mobile a:last-child{border-bottom:none;}
.nav-mobile a:hover{color:var(--gold);}
.nav-cta-mobile{display:block;margin-top:16px;background:var(--gold);color:var(--navy);border:none;padding:13px;font-size:11px;letter-spacing:2.5px;font-weight:500;width:100%;text-align:center;}

.breadcrumb{max-width:820px;margin:0 auto;padding:22px 24px 0;font-size:12px;color:var(--muted);letter-spacing:.3px;}
.breadcrumb a{color:var(--muted);}
.breadcrumb a:hover{color:var(--gold);}
.breadcrumb span{color:var(--navy);font-weight:500;}

.servico-hero{background:var(--navy);padding:56px 24px 48px;margin-top:22px;}
.servico-hero-inner{max-width:820px;margin:0 auto;}
.eyebrow{font-size:11px;letter-spacing:2.5px;text-transform:uppercase;color:var(--gold);font-weight:600;margin-bottom:16px;display:flex;align-items:center;gap:12px;}
.eyebrow::before{content:'';width:24px;height:1px;background:var(--gold);}
.servico-icone{font-size:38px;margin-bottom:14px;}
.servico-hero h1{font-family:'Cormorant Garamond',serif;font-size:clamp(32px,5vw,48px);font-weight:300;color:var(--cream);line-height:1.15;margin-bottom:16px;}
.servico-resumo{color:rgba(247,244,239,.62);font-size:16px;line-height:1.7;max-width:64ch;}

.servico-corpo{max-width:820px;margin:0 auto;padding:48px 24px 8px;}
.servico-bloco{margin-bottom:32px;}
.bloco-label{font-size:11px;letter-spacing:2px;color:var(--gold);font-weight:700;margin-bottom:10px;}
.servico-bloco p{color:var(--dark);font-size:15.5px;line-height:1.8;max-width:70ch;}
.servico-resultado{background:rgba(200,151,58,.08);border-left:3px solid var(--gold);padding:20px 24px;margin-bottom:36px;}
.servico-resultado .bloco-label{color:#7a5a19;}
.servico-resultado p{color:var(--navy);font-size:15px;line-height:1.75;font-style:italic;max-width:70ch;}
.servico-media{margin:0 0 36px;}
.servico-media img{width:100%;max-width:520px;display:block;margin:0 auto;border-radius:10px;border:1px solid rgba(27,58,92,.12);box-shadow:0 8px 28px rgba(27,58,92,.14);}
.servico-media-legenda{text-align:center;font-size:12.5px;color:var(--muted);margin-top:12px;max-width:60ch;margin-left:auto;margin-right:auto;}
.servico-media-legenda a{color:var(--gold);font-weight:600;}
.servico-media-legenda a:hover{text-decoration:underline;}
.btn-cta{display:inline-block;background:var(--gold);color:var(--navy);padding:16px 34px;font-size:12px;font-weight:700;letter-spacing:2.5px;border-radius:6px;transition:opacity .2s;}
.btn-cta:hover{opacity:.88;}

.servico-faq{max-width:820px;margin:0 auto;padding:8px 24px 44px;}
.servico-faq h2{font-family:'Cormorant Garamond',serif;font-size:26px;font-weight:400;color:var(--navy);margin-bottom:18px;}
.faq-item{border-bottom:1px solid rgba(27,58,92,.12);}
.faq-item:last-child{border-bottom:none;}
.faq-pergunta{width:100%;background:none;border:none;padding:16px 0;font-size:15px;font-weight:600;color:var(--navy);text-align:left;display:flex;justify-content:space-between;align-items:center;gap:12px;font-family:'DM Sans',sans-serif;}
.faq-seta{flex-shrink:0;color:var(--gold);font-size:18px;transition:transform .2s;}
.faq-item.ativo .faq-seta{transform:rotate(45deg);}
.faq-resposta{max-height:0;overflow:hidden;transition:max-height .25s ease;}
.faq-resposta p{padding:0 0 16px;font-size:14px;color:var(--muted);line-height:1.7;max-width:70ch;}

.servico-outros{max-width:820px;margin:24px auto 0;padding:40px 24px 72px;border-top:1px solid rgba(27,58,92,.1);}
.servico-outros h2{font-family:'Cormorant Garamond',serif;font-size:26px;font-weight:400;color:var(--navy);margin-bottom:22px;}
.outros-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;}
.outro-item{display:block;background:#fff;border:1px solid rgba(27,58,92,.1);border-radius:10px;padding:18px 20px;transition:border-color .2s,transform .2s;}
.outro-item:hover{border-color:var(--gold);transform:translateY(-2px);}
.outro-item .oi-nome{font-weight:700;font-size:14px;color:var(--navy);margin-bottom:4px;}
.outro-item .oi-resumo{font-size:12.5px;color:var(--muted);line-height:1.5;}

footer{background:var(--dark);padding:52px 52px 32px;margin-top:0;}
.footer-top{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:48px;margin-bottom:40px;}
.footer-brand{font-family:'Cormorant Garamond',serif;font-size:22px;font-weight:700;color:var(--cream);letter-spacing:4px;}
.footer-brand-sub{font-size:9px;color:var(--gold);letter-spacing:5px;margin-top:-4px;margin-bottom:16px;}
.footer-tagline{font-size:13px;color:rgba(247,244,239,.28);line-height:1.68;max-width:260px;}
.footer-col h4{font-size:9px;letter-spacing:2.5px;color:var(--gold);margin-bottom:16px;font-weight:500;}
.footer-col a{display:block;font-size:12px;color:rgba(247,244,239,.3);margin-bottom:9px;transition:color .2s;}
.footer-col a:hover{color:var(--gold);}
.footer-bottom{border-top:1px solid rgba(255,255,255,.05);padding-top:22px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;}
.footer-copy{font-size:10px;color:rgba(247,244,239,.16);letter-spacing:1px;}
.footer-legal{display:flex;gap:20px;}
.footer-legal a{font-size:10px;color:rgba(247,244,239,.16);}

.wa-float{position:fixed;bottom:24px;right:24px;width:58px;height:58px;border-radius:50%;background:#25D366;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 18px rgba(0,0,0,.28);z-index:998;transition:transform .2s;}
.wa-float:hover{transform:scale(1.07);}
.wa-tooltip{position:absolute;right:70px;top:50%;transform:translateY(-50%);background:rgba(15,37,64,.95);color:var(--cream);font-size:12px;font-weight:500;letter-spacing:.3px;padding:8px 14px;border-radius:6px;white-space:nowrap;opacity:0;pointer-events:none;transition:opacity .2s;border:1px solid rgba(200,151,58,.2);}
.wa-float:hover .wa-tooltip{opacity:1;}
@media print{.wa-float{display:none;}}

@media(max-width:900px){
  nav{padding:0 24px;}
  .nav-links,.nav-cta{display:none;}
  .nav-hamburger{display:flex;}
  footer{padding:44px 24px 28px;}
  .footer-top{grid-template-columns:1fr 1fr;gap:28px;}
}
@media(max-width:640px){
  .servico-hero{padding:40px 20px 36px;}
  .servico-corpo{padding:36px 20px 8px;}
  .servico-outros{padding:32px 20px 56px;}
  .outros-grid{grid-template-columns:1fr;}
  .breadcrumb{padding:18px 20px 0;}
  .footer-top{grid-template-columns:1fr;gap:24px;}
  footer{padding:36px 20px 24px;}
  .wa-float{width:52px;height:52px;bottom:18px;right:18px;}
  .wa-float svg{width:26px;height:26px;}
  .wa-tooltip{display:none;}
}
"""

NAV_LINKS = [
    ("/#sobre", "Sobre"), ("/#fundadores", "Quem somos"), ("/#diagnostico", "Diagnóstico"),
    ("/#servicos", "Serviços"), ("/#metodo", "Método"), ("/#blog", "Blog"), ("/#noticias", "Notícias"), ("/#contato", "Contato"),
]

def nav_html():
    links = "\n    ".join(f'<a href="{href}" role="menuitem">{label}</a>' for href, label in NAV_LINKS)
    mobile_links = "\n  ".join(f'<a href="{href}" onclick="closeMenu()">{label}</a>' for href, label in NAV_LINKS)
    return f"""<nav role="navigation" aria-label="Navegação principal">
  <a class="nav-logo" href="/" aria-label="Tonus Consultoria">TONUS<span>CONSULTORIA</span></a>
  <div class="nav-links" role="menubar">
    {links}
  </div>
  <a class="nav-cta" href="/diagnostico-cliente.html" aria-label="Começar diagnóstico">COMEÇAR DIAGNÓSTICO</a>
  <button class="nav-hamburger" id="hamburger" onclick="toggleMenu()" aria-label="Abrir menu" aria-expanded="false">
    <span></span><span></span><span></span>
  </button>
</nav>

<div class="nav-mobile" id="navMobile" role="navigation" aria-label="Menu mobile">
  {mobile_links}
  <a class="nav-cta-mobile" href="/diagnostico-cliente.html">QUERO MEU DIAGNÓSTICO</a>
</div>"""

def footer_html():
    return """<footer>
  <div class="footer-top">
    <div>
      <div class="footer-brand" aria-label="Tonus Consultoria">TONUS</div>
      <div class="footer-brand-sub">CONSULTORIA</div>
      <div class="footer-tagline">Negócios saudáveis precisam de tônus para crescer. Diagnóstico preciso. Equilíbrio que gera resultado.</div>
    </div>
    <div class="footer-col">
      <h4>EMPRESA</h4>
      <a href="/#sobre">Sobre a Tonus</a>
      <a href="/#fundadores">Quem somos</a>
      <a href="/#metodo">Nosso método</a>
      <a href="/#contato">Contato</a>
    </div>
    <div class="footer-col">
      <h4>SERVIÇOS</h4>
      <a href="/servicos/diagnostico-empresarial.html">Diagnóstico</a>
      <a href="/servicos/gestao-financeira.html">Gestão financeira</a>
      <a href="/servicos/planejamento-estrategico.html">Planejamento estratégico</a>
      <a href="/servicos/educacao-financeira-pessoal.html">Educação financeira</a>
    </div>
    <div class="footer-col">
      <h4>REDES</h4>
      <a href="https://instagram.com/tonus.consultoria" target="_blank" rel="noopener noreferrer">Instagram</a>
      <a href="https://www.linkedin.com/company/tonus-consultoria/about/" target="_blank" rel="noopener noreferrer">LinkedIn</a>
      <a href="https://wa.me/5519992486831" target="_blank" rel="noopener noreferrer">WhatsApp</a>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="footer-copy">© 2026 TONUS CONSULTORIA · PIRASSUNUNGA E REGIÃO, SP</div>
    <div class="footer-legal">
      <a href="/privacidade.html">Política de privacidade</a>
      <a href="/termos.html">Termos de uso</a>
    </div>
  </div>
</footer>"""

MENU_JS = """function toggleMenu(){
  const ham = document.getElementById('hamburger');
  const nav = document.getElementById('navMobile');
  const isOpen = nav.classList.toggle('open');
  ham.classList.toggle('open', isOpen);
  ham.setAttribute('aria-expanded', isOpen);
}
function closeMenu(){
  document.getElementById('hamburger').classList.remove('open');
  document.getElementById('navMobile').classList.remove('open');
  document.getElementById('hamburger').setAttribute('aria-expanded','false');
}
document.addEventListener('click', function(e){
  const nav = document.getElementById('navMobile');
  const ham = document.getElementById('hamburger');
  if(nav.classList.contains('open') && !nav.contains(e.target) && !ham.contains(e.target)){
    closeMenu();
  }
});
function toggleFAQ(botao){
  const item = botao.closest('.faq-item');
  const resposta = item.querySelector('.faq-resposta');
  const aberto = item.classList.contains('ativo');
  document.querySelectorAll('.faq-item').forEach(function(el){
    el.classList.remove('ativo');
    el.querySelector('.faq-resposta').style.maxHeight = null;
  });
  if(!aberto){
    item.classList.add('ativo');
    resposta.style.maxHeight = resposta.scrollHeight + 'px';
  }
}"""

def outros_servicos_html(atual_slug):
    itens = []
    for s in SERVICOS:
        if s["slug"] == atual_slug:
            continue
        itens.append(f'''<a class="outro-item" href="/servicos/{s['slug']}.html">
      <div class="oi-nome">{s['icone']} {s['titulo']}</div>
      <div class="oi-resumo">{s['resumo']}</div>
    </a>''')
    return "\n    ".join(itens)

def schema_json(s):
    service = {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": s["titulo"],
        "name": s["titulo"] + " — Tonus Consultoria",
        "description": s["meta_desc"],
        "url": s["url"],
        "provider": {
            "@type": "LocalBusiness",
            "name": "Tonus Consultoria",
            "url": BASE_URL,
            "telephone": "+5519992486831",
            "address": {"@type": "PostalAddress", "addressLocality": "Pirassununga", "addressRegion": "SP", "addressCountry": "BR"}
        },
        "areaServed": [
            {"@type": "City", "name": c, "containedInPlace": {"@type": "State", "name": "São Paulo"}}
            for c in AREA_SERVED
        ],
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Serviços", "item": f"{BASE_URL}/#servicos"},
            {"@type": "ListItem", "position": 3, "name": s["titulo"], "item": s["url"]},
        ]
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": pergunta, "acceptedAnswer": {"@type": "Answer", "text": resposta}}
            for pergunta, resposta in s["faq"]
        ]
    }
    return service, breadcrumb, faq

def faq_html(s):
    itens = []
    for pergunta, resposta in s["faq"]:
        itens.append(f'''<div class="faq-item">
      <button class="faq-pergunta" onclick="toggleFAQ(this)">{pergunta}<span class="faq-seta">+</span></button>
      <div class="faq-resposta"><p>{resposta}</p></div>
    </div>''')
    return "\n    ".join(itens)

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-QT3MYPH525"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-QT3MYPH525');
</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon-512.png" type="image/png" sizes="512x512">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="X-Frame-Options" content="DENY">
<meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">
<meta http-equiv="Permissions-Policy" content="camera=(), microphone=(), geolocation=()">

<title>@@TITULO@@ — Tonus Consultoria | Pirassununga e Região, SP</title>
<meta name="description" content="@@META_DESC@@">
<meta name="keywords" content="@@KEYWORDS@@">
<meta name="author" content="Tonus Consultoria">
<meta name="robots" content="index, follow">
<link rel="canonical" href="@@URL@@">
<link rel="sitemap" type="application/xml" href="/sitemap.xml">

<meta property="og:type" content="website">
<meta property="og:url" content="@@URL@@">
<meta property="og:title" content="@@TITULO@@ — Tonus Consultoria">
<meta property="og:description" content="@@META_DESC@@">
<meta property="og:image" content="@@BASE_URL@@/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Tonus Consultoria">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="@@TITULO@@ — Tonus Consultoria">
<meta name="twitter:description" content="@@META_DESC@@">
<meta name="twitter:image" content="@@BASE_URL@@/og-image.jpg">

<script type="application/ld+json">
@@SERVICE_JSON@@
</script>
<script type="application/ld+json">
@@BREADCRUMB_JSON@@
</script>
<script type="application/ld+json">
@@FAQ_JSON@@
</script>

<meta name="theme-color" content="#1B3A5C">
<link rel="preload" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400&family=DM+Sans:wght@300;400;500&display=swap" as="style">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">

<style>@@CSS@@</style>
</head>
<body>

@@NAV@@

<div class="breadcrumb"><a href="/">Início</a> / <a href="/#servicos">Serviços</a> / <span>@@TITULO@@</span></div>

<header class="servico-hero">
  <div class="servico-hero-inner">
    <div class="eyebrow">@@EYEBROW@@</div>
    <div class="servico-icone" aria-hidden="true">@@ICONE@@</div>
    <h1>@@TITULO@@</h1>
    <p class="servico-resumo">@@RESUMO@@</p>
  </div>
</header>

<section class="servico-corpo">
  <div class="servico-bloco">
    <div class="bloco-label">O PROBLEMA</div>
    <p>@@PROBLEMA@@</p>
  </div>
  <div class="servico-bloco">
    <div class="bloco-label">O QUE A TONUS FAZ</div>
    <p>@@FAZEMOS@@</p>
  </div>
  @@MEDIA_HTML@@
  <div class="servico-resultado">
    <div class="bloco-label">RESULTADO ESPERADO</div>
    <p>@@RESULTADO@@</p>
  </div>
  <a class="btn-cta" href="/diagnostico-cliente.html">QUERO COMEÇAR MEU DIAGNÓSTICO</a>
</section>

<section class="servico-faq">
  <h2>Dúvidas frequentes</h2>
  @@FAQ_HTML@@
</section>

<section class="servico-outros">
  <h2>Outros serviços</h2>
  <div class="outros-grid">
    @@OUTROS@@
  </div>
</section>

@@FOOTER@@

<a class="wa-float" href="https://wa.me/5519992486831?text=Ol%C3%A1%2C%20vim%20pelo%20site%20e%20queria%20saber%20mais%20sobre%20a%20Tonus%20Consultoria." target="_blank" rel="noopener noreferrer" aria-label="Falar com a Tonus Consultoria no WhatsApp">
  <svg viewBox="0 0 32 32" width="30" height="30" aria-hidden="true"><path fill="#fff" d="M16.004 3C9.377 3 4 8.373 4 15c0 2.31.64 4.47 1.75 6.31L4 29l7.86-1.7A11.94 11.94 0 0 0 16.004 27C22.63 27 28 21.627 28 15S22.63 3 16.004 3Zm6.99 16.87c-.3.84-1.5 1.55-2.44 1.75-.65.14-1.5.25-4.36-.94-3.66-1.52-6.02-5.24-6.2-5.48-.18-.24-1.48-1.97-1.48-3.76 0-1.79.94-2.67 1.27-3.03.33-.36.72-.45.96-.45.24 0 .48 0 .69.01.22.01.52-.08.81.62.3.72 1.02 2.5 1.11 2.68.09.18.15.39.03.63-.12.24-.18.39-.36.6-.18.21-.38.47-.54.63-.18.18-.37.38-.16.74.21.36.94 1.55 2.02 2.51 1.39 1.24 2.56 1.62 2.92 1.8.36.18.57.15.78-.09.21-.24.9-1.05 1.14-1.41.24-.36.48-.3.81-.18.33.12 2.1.99 2.46 1.17.36.18.6.27.69.42.09.15.09.87-.21 1.71Z"/></svg>
  <span class="wa-tooltip">Fale no WhatsApp</span>
</a>
<script>
(function(){
  var wa = document.querySelector('.wa-float');
  var bar = document.querySelector('.footer-bottom');
  if(!wa || !bar) return;
  function update(){
    var rect = bar.getBoundingClientRect();
    var vh = window.innerHeight;
    if(rect.top < vh && rect.bottom > 0){
      wa.style.transform = 'translateY(-' + (vh - rect.top + 16) + 'px)';
    } else {
      wa.style.transform = '';
    }
  }
  window.addEventListener('scroll', update, {passive:true});
  window.addEventListener('resize', update);
  update();
})();
</script>

<script>
@@MENU_JS@@
</script>

</body>
</html>
"""

for s in SERVICOS:
    service_schema, breadcrumb_schema, faq_schema = schema_json(s)
    html = PAGE_TEMPLATE
    replacements = {
        "@@TITULO@@": s["titulo"], "@@EYEBROW@@": s["eyebrow"], "@@ICONE@@": s["icone"],
        "@@RESUMO@@": s["resumo"], "@@PROBLEMA@@": s["problema"], "@@FAZEMOS@@": s["fazemos"],
        "@@RESULTADO@@": s["resultado"], "@@META_DESC@@": s["meta_desc"], "@@KEYWORDS@@": s["keywords"],
        "@@URL@@": s["url"], "@@BASE_URL@@": BASE_URL,
        "@@SERVICE_JSON@@": json.dumps(service_schema, ensure_ascii=False, indent=2),
        "@@BREADCRUMB_JSON@@": json.dumps(breadcrumb_schema, ensure_ascii=False, indent=2),
        "@@FAQ_JSON@@": json.dumps(faq_schema, ensure_ascii=False, indent=2),
        "@@FAQ_HTML@@": faq_html(s),
        "@@MEDIA_HTML@@": s.get("media_html", ""),
        "@@CSS@@": CSS, "@@NAV@@": nav_html(), "@@FOOTER@@": footer_html(), "@@MENU_JS@@": MENU_JS,
        "@@OUTROS@@": outros_servicos_html(s["slug"]),
    }
    for token, value in replacements.items():
        html = html.replace(token, value)
    out_path = os.path.join(OUT_DIR, f"{s['slug']}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("gerado:", out_path)
