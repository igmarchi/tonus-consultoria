# -*- coding: utf-8 -*-
"""
Gera o blog da Tonus Consultoria: /blog/index.html (listagem) e
/blog/<slug>.html (cada post), a partir da lista POSTS abaixo — mesmo
padrão de fonte única de verdade usado em gerar_paginas_servico.py.

Também atualiza automaticamente o bloco de URLs do blog em sitemap.xml
(entre os marcadores <!-- BLOG_URLS_START --> e <!-- BLOG_URLS_END -->).

Enquanto POSTS estiver vazio, blog/index.html é gerado com um estado
"em breve" e marcado como noindex (conteúdo fino demais pra valer a
pena indexar) — assim que o primeiro post entrar na lista, a página
de listagem passa a ser indexável automaticamente e os posts entram
no sitemap. O link "Blog" só deve ser adicionado ao menu principal do
site (NAV_LINKS em index.html e em gerar_paginas_servico.py) quando o
primeiro post for publicado — não faz sentido divulgar uma página vazia.
"""
import os, json, re, urllib.parse
from datetime import datetime

BASE_URL = "https://www.tonusconsultoria.com.br"
OUT_DIR = "/home/claude/tonus_site_fix/blog"
SITEMAP_PATH = "/home/claude/tonus_site_fix/sitemap.xml"
os.makedirs(OUT_DIR, exist_ok=True)

# Pilar -> serviço relacionado (pra link interno automático em cada post)
PILAR_SERVICO = {
    "Gestão Financeira": ("gestao-financeira", "Gestão Financeira"),
    "Diagnóstico Empresarial": ("diagnostico-empresarial", "Diagnóstico Empresarial"),
    "Planejamento Estratégico": ("planejamento-estrategico", "Planejamento Estratégico"),
    "Gestão de Equipes": ("gestao-de-equipes", "Gestão de Equipes"),
    "Reestruturação Operacional": ("reestruturacao-operacional", "Reestruturação Operacional"),
    "Educação Financeira Pessoal": ("educacao-financeira-pessoal", "Educação Financeira Pessoal"),
}

# ---------------------------------------------------------------------
# POSTS: lista vazia até os temas do "Plano de Conteúdo" serem validados
# e os artigos escritos. Formato de cada item, quando adicionado:
#
# {
#   "slug": "fluxo-de-caixa-mei-pirassununga",
#   "pilar": "Gestão Financeira",
#   "titulo": "Como fazer fluxo de caixa de MEI em Pirassununga",
#   "resumo": "Frase de 1-2 linhas usada no card da listagem e no meta description.",
#   "meta_desc": "Meta description otimizada (até ~155 caracteres).",
#   "keywords": "fluxo de caixa mei, ...",
#   "data_publicacao": "2026-09-15",   # AAAA-MM-DD
#   "tempo_leitura": "6 min",
#   "corpo_html": "<p>...</p><h2>...</h2><p>...</p>",  # HTML já pronto do artigo
# }
# ---------------------------------------------------------------------
POSTS = [
    {
        "slug": "fluxo-de-caixa-mei-pirassununga",
        "pilar": "Gestão Financeira",
        "titulo": "Como fazer fluxo de caixa de MEI: passo a passo simples",
        "resumo": "Um guia direto pra organizar as entradas e saídas do seu negócio sem depender de planilha complexa — com os números do MEI atualizados para 2026.",
        "meta_desc": "Guia prático de fluxo de caixa para MEI em Pirassununga: passo a passo simples, sem planilha complexa, com os limites e valores do MEI atualizados para 2026.",
        "keywords": "fluxo de caixa mei pirassununga, controle financeiro mei, como fazer fluxo de caixa",
        "data_publicacao": "2026-09-03",
        "tempo_leitura": "7 min",
        "corpo_html": """<p>Se você é MEI em Pirassununga ou região e nunca fez um fluxo de caixa de verdade, não está sozinho — é provavelmente a dúvida mais comum entre quem abre um MEI: "eu sei que estou vendendo, mas não sei pra onde o dinheiro vai". A boa notícia é que fluxo de caixa não é contabilidade complicada. É só um registro organizado de quanto entra e quanto sai, dia a dia, pra você nunca ser pego de surpresa.</p>

<h2>O que exatamente é fluxo de caixa (sem economês)</h2>
<p>Fluxo de caixa é simplesmente a diferença, todo mês, entre o que entrou e o que saiu do seu negócio. Parece óbvio, mas a maioria dos MEIs não separa isso: o dinheiro da venda cai na mesma conta que paga o aluguel de casa, o cartão pessoal e o boleto do fornecedor — tudo misturado. Quando chega o fim do mês, ninguém sabe dizer se sobrou ou faltou, só que "o dinheiro sumiu".</p>

<h2>Passo a passo pra montar o seu</h2>
<p>Não precisa de sistema caro nem de curso de contabilidade. Dá pra começar hoje, com uma planilha simples ou até um caderno:</p>
<ul>
<li><strong>Abra uma conta só pra empresa.</strong> Mesmo sendo MEI, ter uma conta separada (pode ser uma conta digital gratuita) é o passo que resolve boa parte da confusão — tudo que entra e sai do negócio passa só por ali.</li>
<li><strong>Anote toda entrada, todo dia.</strong> Venda à vista, no cartão, no Pix — cada uma, com data e valor.</li>
<li><strong>Anote toda saída, no mesmo lugar.</strong> Fornecedor, gasolina, embalagem, DAS-MEI, tudo — inclusive as pequenas, que são as que mais escapam.</li>
<li><strong>Separe o que é custo fixo do que é custo variável.</strong> Custo fixo é o que você paga todo mês, venda pouco ou muito (aluguel, DAS, internet). Custo variável muda com o volume de venda (embalagem, matéria-prima).</li>
<li><strong>Feche a conta toda semana, não só no fim do mês.</strong> Fechar semanalmente é o que evita a surpresa — se algo está errado, você percebe em 7 dias, não em 30.</li>
</ul>

<h2>Um detalhe que trava muito MEI da região</h2>
<p>Em 2026, o limite de faturamento anual do MEI continua em R$ 81.000 — ou seja, uma média de R$ 6.750 por mês. E o DAS-MEI (o boleto mensal obrigatório) varia entre R$ 82,05 e R$ 87,05, dependendo da atividade (comércio, serviço ou os dois). Um erro comum: esquecer de contar o DAS como custo fixo dentro do fluxo de caixa — ele sai todo mês, então precisa estar na conta desde o primeiro dia, não ser uma surpresa quando o boleto chega.</p>

<h2>Um exemplo prático</h2>
<p>Imagine uma prestadora de serviço de estética em Pirassununga que fatura R$ 4.500 num mês. Se ela não separar os custos, pode achar que sobrou tudo isso pra ela. Mas tirando produto (R$ 900), aluguel da sala (R$ 600), DAS (R$ 86) e uma parcela de equipamento (R$ 400), o que sobra de verdade é R$ 2.514 — bem diferente dos R$ 4.500 que "pareciam" ter sobrado. É exatamente esse tipo de conta que o fluxo de caixa revela, e que a intuição sozinha não pega.</p>

<h2>Quando vale sair da planilha</h2>
<p>Enquanto o volume de venda é baixo, planilha ou caderno resolvem bem. O sinal de que já é hora de organizar isso de um jeito mais estruturado é quando você começa a perder tempo demais reconciliando números, ou quando não consegue mais responder de cabeça "quanto eu realmente lucro por mês" — nesse ponto, vale ter alguém de fora olhando pros números com você.</p>""",
    },
    {
        "slug": "o-que-e-diagnostico-empresarial",
        "pilar": "Diagnóstico Empresarial",
        "titulo": "O que é um diagnóstico empresarial e por que toda pequena empresa deveria fazer um",
        "resumo": "Entenda o que esse tipo de avaliação analisa de verdade, como costuma funcionar, e por que costuma revelar problemas que o dono nem sabia que existiam.",
        "meta_desc": "O que é um diagnóstico empresarial, como funciona e por que pequenas empresas e MEIs de Pirassununga e região deveriam considerar fazer um antes de investir em crescimento.",
        "keywords": "diagnóstico empresarial, o que é diagnóstico empresarial, avaliação de negócio",
        "data_publicacao": "2026-09-03",
        "tempo_leitura": "6 min",
        "corpo_html": """<p>"Diagnóstico empresarial" soa como algo que só empresa grande faz, com consultoria cara e relatório de dezenas de páginas. Na prática, pra pequena empresa e MEI, é bem mais simples do que isso — e é justamente quem tem um negócio pequeno que mais se beneficia de fazer um, porque geralmente é quem decide tudo "no olho".</p>

<h2>O problema que o diagnóstico resolve</h2>
<p>A maioria dos donos de negócio pequeno tem uma sensação vaga de que "algo não está redondo" — vende bem mas não sobra dinheiro, trabalha demais mas não vê a empresa crescer, tem uma equipe mas sente que precisa estar em tudo. O problema é que essa sensação, sozinha, não aponta o que fazer. Sem enxergar com clareza onde exatamente o negócio está saudável e onde está sangrando, qualquer decisão de investir tempo ou dinheiro vira aposta.</p>

<h2>O que é avaliado, na prática</h2>
<p>Um diagnóstico sério não olha só pra números financeiros — ele avalia o negócio como um todo, geralmente em algumas frentes:</p>
<ul>
<li><strong>Financeiro:</strong> fluxo de caixa, precificação, margem real por produto ou serviço.</li>
<li><strong>Operacional:</strong> processos, gargalos, o que depende demais do dono.</li>
<li><strong>Comercial:</strong> de onde vêm os clientes, taxa de conversão, ticket médio.</li>
<li><strong>Pessoas:</strong> estrutura de equipe, papéis, dependência de pessoas-chave.</li>
<li><strong>Estratégia:</strong> pra onde o negócio está indo, e se existe um plano ou só reação ao dia a dia.</li>
<li><strong>Gestão:</strong> que informação o dono tem em mãos pra decidir, e com que frequência.</li>
</ul>

<h2>Como costuma funcionar</h2>
<p>Normalmente envolve uma conversa estruturada com quem toca o negócio (não é um questionário genérico de internet), análise dos números que já existem — mesmo que estejam bagunçados — e, ao final, um retrato objetivo: o que está funcionando, o que está travando, e em que ordem vale atacar cada ponto. A parte mais importante não é o relatório em si, é a priorização — porque quase todo negócio pequeno tem mais problemas do que tempo pra resolver todos ao mesmo tempo.</p>

<h2>Por que costuma revelar coisa que o dono não esperava</h2>
<p>É comum o diagnóstico apontar que o problema real não é o que o dono achava. Um exemplo típico: o empresário acha que o problema é "vender mais", mas o diagnóstico mostra que ele já vende o suficiente — o problema é que cada venda dá pouca margem, porque o preço está errado há anos. Vender mais, nesse caso, só multiplicaria o prejuízo por venda. Sem uma visão de fora, olhando os números com distância, esse tipo de coisa é difícil de enxergar sozinho — porque quem está dentro do negócio todo dia perde a referência do que é normal e do que não é.</p>

<h2>Quando faz sentido fazer um</h2>
<p>Não precisa esperar uma crise. Os melhores momentos costumam ser: antes de um investimento grande (contratar, abrir uma filial, comprar equipamento), quando a sensação de "trabalho muito e sobra pouco" persiste por mais de alguns meses, ou simplesmente quando já faz tempo que ninguém olha pro negócio de fora — só de dentro, correndo atrás do dia a dia.</p>""",
    },
    {
        "slug": "erros-fluxo-de-caixa-pequena-empresa",
        "pilar": "Gestão Financeira",
        "titulo": "5 erros de fluxo de caixa que travam pequenas empresas",
        "resumo": "Os deslizes mais comuns que fazem um negócio faturar bem e, mesmo assim, nunca sobrar dinheiro no fim do mês.",
        "meta_desc": "Os 5 erros de fluxo de caixa mais comuns em pequenas empresas de Pirassununga e região — e como corrigir cada um deles na prática.",
        "keywords": "erros fluxo de caixa pequena empresa, fluxo de caixa errado, controle financeiro pequena empresa",
        "data_publicacao": "2026-09-03",
        "tempo_leitura": "6 min",
        "corpo_html": """<p>Tem um padrão que se repete em quase toda pequena empresa que "fatura bem mas não sobra dinheiro": não é falta de venda, é erro na forma como o fluxo de caixa é (ou não é) acompanhado. Aqui vão os cinco mais comuns que a gente vê na prática, com o que fazer em cada um.</p>

<h2>1. Misturar conta pessoal com conta da empresa</h2>
<p>É o erro mais comum de todos, disparado. Quando o dinheiro da venda cai na mesma conta que paga o mercado e a mensalidade da escola do filho, fica praticamente impossível saber quanto a empresa lucra — porque "lucro" e "meu dinheiro pra viver" viram a mesma coisa na cabeça. A correção é simples de descrever (abrir uma conta separada) e difícil de manter na rotina — mas é o primeiro passo, sem exceção.</p>

<h2>2. Contar a entrada, esquecer o custo fixo escondido</h2>
<p>Muita gente registra as vendas certinho, mas esquece de contar custos que não são mensais óbvios: manutenção de equipamento uma vez por ano, taxa de cartão, imposto, uma ferramenta que renova anual. Esses custos "escondidos" divididos por 12 meses continuam sendo custo todo mês — só que ninguém provisiona pra eles, e quando chegam, parecem um imprevisto que "come" o caixa.</p>

<h2>3. Confundir faturamento com lucro</h2>
<p>Faturar R$ 10 mil não quer dizer ter R$ 10 mil de lucro — mas é assim que muita gente pensa na hora de decidir se pode fazer um investimento ou tirar um valor maior pra si. Sem separar o que é custo do que é sobra de verdade, a sensação de "está indo bem" pode estar completamente descolada da realidade do caixa.</p>

<h2>4. Não olhar pra frente, só pra trás</h2>
<p>Fluxo de caixa não serve só pra registrar o que já aconteceu — o valor real está em projetar os próximos 30, 60, 90 dias. Se você sabe que um cliente grande vai pagar em 45 dias mas o aluguel vence em 10, precisa enxergar esse buraco com antecedência, não descobrir no dia que falta dinheiro na conta.</p>

<h2>5. Deixar pra fechar as contas só no fim do mês</h2>
<p>Quando o fechamento é só mensal, qualquer erro ou esquecimento só aparece 30 dias depois — tempo suficiente pra virar um problema maior. Fechar semanalmente (mesmo que rápido, 10 minutos) é o que permite corrigir o rumo enquanto ainda dá tempo, em vez de só constatar o estrago no fim do mês.</p>

<h2>O fio comum entre os cinco</h2>
<p>Nenhum desses erros é sobre inteligência ou esforço — são sobre rotina e visibilidade. A maioria dos empresários da região que passa por isso trabalha duro e entende o próprio negócio profundamente; só falta uma estrutura simples que transforme intuição em número. E, uma vez montada essa estrutura, ela costuma se manter sozinha com pouco esforço contínuo.</p>""",
    },
    {
        "slug": "separar-financas-pessoais-empresa-mei",
        "pilar": "Educação Financeira Pessoal",
        "titulo": "Separar as contas da empresa das contas pessoais: guia para MEI e pequenos negócios",
        "resumo": "Por que essa é, de longe, a mudança mais simples com o maior impacto na saúde financeira de quem tem um negócio pequeno.",
        "meta_desc": "Como e por que separar as finanças pessoais das da empresa quando você é MEI ou dono de um pequeno negócio — guia prático e sem economês.",
        "keywords": "separar finanças pessoais empresa mei, pf pj separar contas, educação financeira empreendedor",
        "data_publicacao": "2026-09-03",
        "tempo_leitura": "6 min",
        "corpo_html": """<p>Se tivesse que escolher uma única mudança financeira com o maior impacto pra quem tem um MEI ou pequeno negócio, seria essa: separar de vez o dinheiro da empresa do dinheiro pessoal. Parece básico, mas é surpreendente quantos negócios — inclusive já estabelecidos — ainda não fizeram essa separação de verdade.</p>

<h2>Por que isso acontece tanto</h2>
<p>No começo, é natural: você abre o MEI, ainda não tem volume suficiente pra "justificar" uma conta separada, e vai usando a conta pessoal mesmo. O problema é que esse hábito raramente muda sozinho — o negócio cresce, o volume de dinheiro passando por ali aumenta, e a mistura vai junto, cada vez mais difícil de desfazer.</p>

<h2>O que a mistura esconde</h2>
<p>Quando pessoa física e pessoa jurídica dividem a mesma conta, três coisas ficam praticamente impossíveis de enxergar com clareza: quanto a empresa realmente fatura, quanto ela realmente gasta pra funcionar, e quanto sobra de lucro de verdade — sem contar o valor que você "tira" informalmente sempre que precisa. Isso também dificulta decisões importantes, como saber se dá pra contratar, investir em equipamento, ou se pode reduzir o próprio sustento num mês mais fraco.</p>

<h2>Como fazer a separação, na prática</h2>
<ul>
<li><strong>Abra uma conta PJ (ou uma conta digital gratuita em nome do CNPJ).</strong> Não precisa ser um banco tradicional — a maioria das fintechs oferece conta gratuita pra MEI.</li>
<li><strong>Defina um "pró-labore" fixo — mesmo informal.</strong> Escolha um valor mensal que a empresa "paga" pra você, como se fosse um salário. Isso obriga você a tratar o resto como dinheiro da empresa, não seu.</li>
<li><strong>Todo gasto do negócio sai da conta PJ, sem exceção.</strong> Mesmo aquele gasto pequeno "que nem vale a pena anotar" — são esses que mais se acumulam sem controle.</li>
<li><strong>Transferências entre as contas só de um jeito: PJ paga o pró-labore pra PF.</strong> Nunca o contrário, e nunca sem registrar.</li>
</ul>

<h2>O que muda quando isso está separado</h2>
<p>Além de finalmente saber quanto a empresa lucra de verdade, a separação também facilita muito na hora de declarar impostos, pedir crédito (bancos avaliam melhor um CNPJ com movimentação própria e organizada) e, se um dia você quiser vender o negócio ou trazer um sócio, ter as contas limpas facilita — e muito — esse processo.</p>

<h2>Um lembrete importante</h2>
<p>Separar as contas não resolve sozinho um problema de fluxo de caixa apertado — mas é o que torna esse problema visível o suficiente pra ser resolvido. Sem essa separação, qualquer tentativa de organizar as finanças do negócio esbarra na mesma dificuldade: não dá pra organizar o que está tudo misturado.</p>""",
    },
    {
        "slug": "planejamento-estrategico-pequena-empresa-por-onde-comecar",
        "pilar": "Planejamento Estratégico",
        "titulo": "Planejamento estratégico para pequena empresa: por onde começar sem complicar",
        "resumo": "Não precisa de um plano de 40 páginas — precisa de clareza sobre pra onde o negócio está indo e como medir se está no caminho certo.",
        "meta_desc": "Planejamento estratégico para pequena empresa: um jeito simples e prático de começar, sem depender de metodologias complicadas ou planos gigantes.",
        "keywords": "planejamento estratégico pequena empresa, como fazer planejamento estratégico, metas empresa pequena",
        "data_publicacao": "2026-09-03",
        "tempo_leitura": "6 min",
        "corpo_html": """<p>"Planejamento estratégico" é um daqueles termos que soa grande demais pra um negócio pequeno — parece coisa de multinacional, com slide de apresentação e consultoria cara. Mas na prática, pra uma pequena empresa, planejamento estratégico pode (e deve) ser simples: uma página, algumas metas claras, e uma rotina pra revisar.</p>

<h2>O problema de não ter nenhum</h2>
<p>Sem um plano, mesmo mínimo, o dia a dia acaba tomando conta de tudo — e qualquer resultado parece "bom o suficiente", porque não existe um ponto de comparação. É fácil trabalhar muito, o ano inteiro, e no fim não conseguir dizer com clareza se o negócio avançou de verdade ou só rodou no mesmo lugar.</p>

<h2>Os quatro elementos que realmente importam</h2>
<p>Não precisa de metodologia complicada. Um planejamento estratégico simples, mas eficaz, tem só quatro partes:</p>
<ul>
<li><strong>Onde você está agora.</strong> Um raio-x honesto: o que está funcionando, o que não está, e por quê.</li>
<li><strong>Onde você quer chegar.</strong> Não precisa ser um sonho gigante — pode ser algo concreto como "dobrar o número de clientes recorrentes" ou "parar de depender de um único cliente grande".</li>
<li><strong>O que separa um do outro.</strong> As duas ou três coisas que, se resolvidas, mais aproximam você do destino — não uma lista de 20 tarefas, só as que realmente movem o ponteiro.</li>
<li><strong>Como saber se está no caminho.</strong> Dois ou três números simples que você acompanha com regularidade — não precisa de painel sofisticado, uma planilha revisada mensalmente já resolve.</li>
</ul>

<h2>Um exemplo de como isso fica na prática</h2>
<p>Uma pequena oficina mecânica da região, por exemplo, pode definir: "hoje dependemos demais de indicação boca a boca, sem controle de quantos clientes voltam" (onde está); "queremos que 40% do faturamento venha de clientes recorrentes em 12 meses" (onde quer chegar); "criar um cadastro simples de clientes e um lembrete de revisão periódica" (o que separa um do outro); "acompanhar mensalmente o número de clientes cadastrados e a taxa de retorno" (como medir). Isso cabe numa folha de papel — e já é mais planejamento estratégico do que a maioria dos negócios pequenos tem.</p>

<h2>O erro mais comum: fazer o plano e nunca mais olhar</h2>
<p>De nada adianta escrever isso uma vez e guardar na gaveta. O que faz o planejamento funcionar de verdade é revisar com uma frequência definida — trimestral costuma ser um bom equilíbrio: frequente o suficiente pra corrigir o rumo cedo, espaçado o suficiente pra não virar só mais uma tarefa administrativa.</p>

<h2>Por onde começar hoje</h2>
<p>Se você nunca fez isso, não tente fazer o plano perfeito na primeira tentativa. Pegue uma folha, escreva as quatro perguntas acima, responda com o que você já sabe sobre o próprio negócio — mesmo que de forma imperfeita — e marque uma data pra revisar daqui a três meses. Esse primeiro rascunho, por mais simples que seja, já é mais direção do que a maioria dos negócios pequenos opera.</p>""",
    },
]

for p in POSTS:
    p["url"] = f"{BASE_URL}/blog/{p['slug']}.html"

BLOG_INDEX_URL = f"{BASE_URL}/blog/"

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

.blog-hero{background:var(--navy);padding:56px 24px 48px;margin-top:22px;}
.blog-hero-inner{max-width:820px;margin:0 auto;}
.eyebrow{font-size:11px;letter-spacing:2.5px;text-transform:uppercase;color:var(--gold);font-weight:600;margin-bottom:16px;display:flex;align-items:center;gap:12px;}
.eyebrow::before{content:'';width:24px;height:1px;background:var(--gold);}
.blog-hero h1{font-family:'Cormorant Garamond',serif;font-size:clamp(32px,5vw,48px);font-weight:300;color:var(--cream);line-height:1.15;margin-bottom:16px;}
.blog-subtitulo{color:rgba(247,244,239,.62);font-size:16px;line-height:1.7;max-width:64ch;}
.blog-meta{display:flex;gap:14px;align-items:center;margin-top:22px;flex-wrap:wrap;}
.blog-tag{display:inline-block;background:rgba(200,151,58,.14);color:var(--gold);font-size:11px;font-weight:700;letter-spacing:1px;padding:5px 12px;border-radius:20px;}
.blog-data{color:rgba(247,244,239,.45);font-size:12.5px;}

.blog-corpo{max-width:760px;margin:0 auto;padding:48px 24px 8px;}
.blog-corpo p{color:var(--dark);font-size:15.5px;line-height:1.85;margin-bottom:20px;max-width:70ch;}
.blog-corpo h2{font-family:'Cormorant Garamond',serif;font-size:24px;font-weight:600;color:var(--navy);margin:34px 0 14px;}
.blog-corpo ul{margin:0 0 20px 20px;}
.blog-corpo li{font-size:15px;color:var(--dark);line-height:1.8;margin-bottom:8px;}
.blog-corpo strong{color:var(--navy);}

.blog-share{max-width:760px;margin:32px auto 0;padding:0 24px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;}
.blog-share-label{font-size:11px;color:var(--muted);letter-spacing:1.5px;font-weight:700;text-transform:uppercase;}
.blog-share-btn{display:inline-flex;align-items:center;gap:7px;padding:9px 16px;border-radius:20px;font-size:12.5px;font-weight:600;letter-spacing:.2px;border:1px solid rgba(27,58,92,.15);color:var(--navy);background:#fff;transition:border-color .2s,transform .2s,background .2s;}
.blog-share-btn:hover{border-color:var(--gold);transform:translateY(-1px);}
.blog-share-btn svg{width:15px;height:15px;flex-shrink:0;}
.blog-share-btn.wa{background:#25D366;color:#fff;border-color:#25D366;}
.blog-share-btn.wa:hover{opacity:.9;}
.blog-share-btn.copy{cursor:pointer;}

.blog-cta{max-width:760px;margin:28px auto 48px;padding:26px 28px;background:rgba(200,151,58,.08);border-left:3px solid var(--gold);border-radius:0 10px 10px 0;}
.blog-cta-badge{font-size:11px;font-weight:700;letter-spacing:1.5px;color:var(--gold);text-transform:uppercase;margin-bottom:10px;}
.blog-cta p{color:var(--navy);font-size:14.5px;line-height:1.7;margin-bottom:16px;max-width:60ch;}
.blog-cta-botoes{display:flex;flex-wrap:wrap;gap:12px;align-items:center;}
.btn-cta{display:inline-block;background:var(--gold);color:var(--navy);padding:14px 30px;font-size:12px;font-weight:700;letter-spacing:2.5px;border-radius:6px;transition:opacity .2s;}
.btn-cta:hover{opacity:.88;}
.btn-cta-outline{display:inline-block;border:1px solid var(--navy);color:var(--navy);padding:12px 26px;font-size:11.5px;font-weight:600;letter-spacing:2px;border-radius:6px;}

.blog-outros{max-width:820px;margin:24px auto 0;padding:40px 24px 72px;border-top:1px solid rgba(27,58,92,.1);}
.blog-outros h2{font-family:'Cormorant Garamond',serif;font-size:26px;font-weight:400;color:var(--navy);margin-bottom:22px;}

.blog-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;max-width:820px;margin:0 auto;padding:0 24px;}
.blog-card{display:block;background:#fff;border:1px solid rgba(27,58,92,.1);border-radius:12px;padding:22px 24px;transition:border-color .2s,transform .2s;}
.blog-card:hover{border-color:var(--gold);transform:translateY(-2px);}
.blog-card .blog-tag{margin-bottom:10px;}
.blog-card h3{font-family:'Cormorant Garamond',serif;font-size:19px;font-weight:600;color:var(--navy);margin-bottom:8px;line-height:1.3;}
.blog-card p{font-size:13px;color:var(--muted);line-height:1.6;}

.blog-listagem-hero{max-width:820px;margin:0 auto;padding:56px 24px 8px;}
.blog-empty{max-width:520px;margin:32px auto 88px;text-align:center;padding:0 24px;}
.blog-empty .blog-empty-icone{font-size:34px;margin-bottom:18px;}
.blog-empty p{color:var(--muted);font-size:15px;line-height:1.75;margin-bottom:26px;}

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
  .blog-grid{grid-template-columns:1fr;}
}
@media(max-width:640px){
  .blog-hero{padding:40px 20px 36px;}
  .blog-corpo{padding:36px 20px 8px;}
  .blog-outros{padding:32px 20px 56px;}
  .breadcrumb{padding:18px 20px 0;}
  .blog-share{padding:0 20px;}
  .blog-share-label{width:100%;}
  .footer-top{grid-template-columns:1fr;gap:24px;}
  footer{padding:36px 20px 24px;}
  .wa-float{width:52px;height:52px;bottom:18px;right:18px;}
  .wa-float svg{width:26px;height:26px;}
  .wa-tooltip{display:none;}
}
"""

# NAV_LINKS igual ao do site (index.html e gerar_paginas_servico.py),
# já com o item "Blog" incluído — ativado junto com a publicação dos
# primeiros posts.
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
function copiarLinkArtigo(btn){
  var url = window.location.href;
  var label = btn.querySelector('.copy-label');
  var original = label ? label.textContent : '';
  function feedback(ok){
    if(!label) return;
    label.textContent = ok ? 'Link copiado ✓' : 'Não foi possível copiar';
    setTimeout(function(){ label.textContent = original; }, 2200);
  }
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(url).then(function(){ feedback(true); }, function(){ feedback(false); });
  } else {
    try{
      var ta = document.createElement('textarea');
      ta.value = url; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      feedback(true);
    } catch(e){ feedback(false); }
  }
}"""

WA_FLOAT_HTML = """<a class="wa-float" href="https://wa.me/5519992486831?text=Ol%C3%A1%2C%20li%20um%20artigo%20do%20blog%20e%20queria%20saber%20mais%20sobre%20a%20Tonus%20Consultoria." target="_blank" rel="noopener noreferrer" aria-label="Falar com a Tonus Consultoria no WhatsApp">
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
</script>"""

def article_schema(post):
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post["titulo"],
        "description": post["meta_desc"],
        "url": post["url"],
        "datePublished": post["data_publicacao"],
        "dateModified": post.get("data_atualizacao", post["data_publicacao"]),
        "author": {"@type": "Organization", "name": "Tonus Consultoria", "url": BASE_URL},
        "publisher": {
            "@type": "Organization", "name": "Tonus Consultoria",
            "logo": {"@type": "ImageObject", "url": f"{BASE_URL}/favicon-512.png"},
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": post["url"]},
        "inLanguage": "pt-BR",
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": BLOG_INDEX_URL},
            {"@type": "ListItem", "position": 3, "name": post["titulo"], "item": post["url"]},
        ],
    }
    return schema, breadcrumb

def outros_posts_html(slug_atual, limite=4):
    itens = []
    for post in POSTS:
        if post["slug"] == slug_atual:
            continue
        itens.append(f'''<a class="outro-item" href="/blog/{post['slug']}.html">
      <div class="oi-nome">{post['titulo']}</div>
      <div class="oi-resumo">{post['resumo']}</div>
    </a>''')
        if len(itens) >= limite:
            break
    return "\n    ".join(itens)

def share_html(post):
    texto_wa = f"{post['titulo']} — {post['url']}"
    wa_url = "https://wa.me/?text=" + urllib.parse.quote(texto_wa)
    return f"""<div class="blog-share">
  <span class="blog-share-label">Gostou? Compartilhe:</span>
  <a class="blog-share-btn wa" href="{wa_url}" target="_blank" rel="noopener noreferrer" aria-label="Compartilhar este artigo no WhatsApp">
    <svg viewBox="0 0 32 32" aria-hidden="true"><path fill="currentColor" d="M16.004 3C9.377 3 4 8.373 4 15c0 2.31.64 4.47 1.75 6.31L4 29l7.86-1.7A11.94 11.94 0 0 0 16.004 27C22.63 27 28 21.627 28 15S22.63 3 16.004 3Zm6.99 16.87c-.3.84-1.5 1.55-2.44 1.75-.65.14-1.5.25-4.36-.94-3.66-1.52-6.02-5.24-6.2-5.48-.18-.24-1.48-1.97-1.48-3.76 0-1.79.94-2.67 1.27-3.03.33-.36.72-.45.96-.45.24 0 .48 0 .69.01.22.01.52-.08.81.62.3.72 1.02 2.5 1.11 2.68.09.18.15.39.03.63-.12.24-.18.39-.36.6-.18.21-.38.47-.54.63-.18.18-.37.38-.16.74.21.36.94 1.55 2.02 2.51 1.39 1.24 2.56 1.62 2.92 1.8.36.18.57.15.78-.09.21-.24.9-1.05 1.14-1.41.24-.36.48-.3.81-.18.33.12 2.1.99 2.46 1.17.36.18.6.27.69.42.09.15.09.87-.21 1.71Z"/></svg>
    WhatsApp
  </a>
  <button class="blog-share-btn copy" type="button" onclick="copiarLinkArtigo(this)" aria-label="Copiar link deste artigo">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
    <span class="copy-label">Copiar link</span>
  </button>
</div>"""

def cta_servico_html(post):
    servico = PILAR_SERVICO.get(post["pilar"])
    servico_html = ""
    if servico:
        slug, nome = servico
        servico_html = f'<a class="btn-cta-outline" href="/servicos/{slug}.html">CONHECER {nome.upper()}</a>'
    return f"""<div class="blog-cta">
  <div class="blog-cta-badge">💡 Próximo passo</div>
  <p><strong>Reconheceu alguma dessas situações no seu negócio?</strong> O diagnóstico gratuito da Tonus leva de 8 a 12 minutos e mostra, na prática, por onde começar — sem custo e sem compromisso.</p>
  <div class="blog-cta-botoes">
    <a class="btn-cta" href="/diagnostico-cliente.html">QUERO MEU DIAGNÓSTICO GRATUITO</a>
    {servico_html}
  </div>
</div>"""

POST_TEMPLATE = """<!DOCTYPE html>
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
<meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">

<title>@@TITULO@@ — Blog Tonus Consultoria</title>
<meta name="description" content="@@META_DESC@@">
<meta name="keywords" content="@@KEYWORDS@@">
<meta name="author" content="Tonus Consultoria">
<meta name="robots" content="index, follow">
<link rel="canonical" href="@@URL@@">
<link rel="sitemap" type="application/xml" href="/sitemap.xml">

<meta property="og:type" content="article">
<meta property="og:url" content="@@URL@@">
<meta property="og:title" content="@@TITULO@@ — Tonus Consultoria">
<meta property="og:description" content="@@META_DESC@@">
<meta property="og:image" content="@@BASE_URL@@/og-image.jpg">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Tonus Consultoria">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="@@TITULO@@ — Tonus Consultoria">
<meta name="twitter:description" content="@@META_DESC@@">

<script type="application/ld+json">
@@ARTICLE_JSON@@
</script>
<script type="application/ld+json">
@@BREADCRUMB_JSON@@
</script>

<meta name="theme-color" content="#1B3A5C">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">

<style>@@CSS@@</style>
</head>
<body>

@@NAV@@

<div class="breadcrumb"><a href="/">Início</a> / <a href="/blog/">Blog</a> / <span>@@TITULO@@</span></div>

<header class="blog-hero">
  <div class="blog-hero-inner">
    <div class="eyebrow">BLOG TONUS</div>
    <h1>@@TITULO@@</h1>
    <p class="blog-subtitulo">@@RESUMO@@</p>
    <div class="blog-meta">
      <span class="blog-tag">@@PILAR@@</span>
      <span class="blog-data">@@DATA_FORMATADA@@ · @@TEMPO_LEITURA@@ de leitura</span>
    </div>
  </div>
</header>

<article class="blog-corpo">
  @@CORPO_HTML@@
</article>

@@SHARE_HTML@@

@@CTA_HTML@@

<section class="blog-outros">
  <h2>Continue lendo</h2>
  <div class="outros-grid" style="display:grid;grid-template-columns:repeat(2,1fr);gap:14px;">
    @@OUTROS@@
  </div>
</section>

@@FOOTER@@

@@WA_FLOAT@@

<script>
@@MENU_JS@@
</script>

</body>
</html>
"""

def post_card_html(post):
    return f"""<a class="blog-card" href="/blog/{post['slug']}.html">
    <span class="blog-tag">{post['pilar']}</span>
    <h3>{post['titulo']}</h3>
    <p>{post['resumo']}</p>
  </a>"""

INDEX_TEMPLATE = """<!DOCTYPE html>
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
<meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">

<title>Blog — Tonus Consultoria | Pirassununga e Região, SP</title>
<meta name="description" content="Conteúdo prático sobre gestão financeira, planejamento estratégico e gestão de equipes para MEI e PME de Pirassununga e região.">
<meta name="author" content="Tonus Consultoria">
<meta name="robots" content="@@ROBOTS@@">
<link rel="canonical" href="@@URL@@">
<link rel="sitemap" type="application/xml" href="/sitemap.xml">

<meta property="og:type" content="website">
<meta property="og:url" content="@@URL@@">
<meta property="og:title" content="Blog — Tonus Consultoria">
<meta property="og:description" content="Conteúdo prático sobre gestão financeira, planejamento estratégico e gestão de equipes para MEI e PME de Pirassununga e região.">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Tonus Consultoria">

<script type="application/ld+json">
@@BREADCRUMB_JSON@@
</script>

<meta name="theme-color" content="#1B3A5C">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">

<style>@@CSS@@</style>
</head>
<body>

@@NAV@@

<div class="breadcrumb"><a href="/">Início</a> / <span>Blog</span></div>

<div class="blog-listagem-hero">
  <div class="eyebrow">CONTEÚDO TONUS</div>
  <h1 style="font-family:'Cormorant Garamond',serif;font-size:clamp(30px,4.5vw,42px);font-weight:300;color:var(--navy);line-height:1.2;">Ideias práticas para quem toca um negócio pequeno</h1>
  <p style="color:var(--muted);font-size:15px;line-height:1.75;max-width:64ch;margin-top:14px;">Gestão financeira, planejamento e gestão de equipes explicados sem economês — pensado pra MEI e PME de Pirassununga e região.</p>
</div>

@@CONTEUDO@@

@@FOOTER@@

@@WA_FLOAT@@

<script>
@@MENU_JS@@
</script>

</body>
</html>
"""

MESES = ["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"]
def data_formatada(iso):
    d = datetime.strptime(iso, "%Y-%m-%d")
    return f"{d.day} de {MESES[d.month-1]} de {d.year}"

# ---------------------------------------------------------------------
# Geração dos posts
# ---------------------------------------------------------------------
for post in POSTS:
    article_json, breadcrumb_json = article_schema(post)
    html = POST_TEMPLATE
    replacements = {
        "@@TITULO@@": post["titulo"], "@@RESUMO@@": post["resumo"], "@@PILAR@@": post["pilar"],
        "@@DATA_FORMATADA@@": data_formatada(post["data_publicacao"]), "@@TEMPO_LEITURA@@": post["tempo_leitura"],
        "@@META_DESC@@": post["meta_desc"], "@@KEYWORDS@@": post.get("keywords", ""),
        "@@URL@@": post["url"], "@@BASE_URL@@": BASE_URL,
        "@@ARTICLE_JSON@@": json.dumps(article_json, ensure_ascii=False, indent=2),
        "@@BREADCRUMB_JSON@@": json.dumps(breadcrumb_json, ensure_ascii=False, indent=2),
        "@@CORPO_HTML@@": post["corpo_html"],
        "@@SHARE_HTML@@": share_html(post),
        "@@CTA_HTML@@": cta_servico_html(post),
        "@@OUTROS@@": outros_posts_html(post["slug"]) or '<p style="color:var(--muted);font-size:14px;">Mais artigos em breve.</p>',
        "@@CSS@@": CSS, "@@NAV@@": nav_html(), "@@FOOTER@@": footer_html(),
        "@@WA_FLOAT@@": WA_FLOAT_HTML, "@@MENU_JS@@": MENU_JS,
    }
    for token, value in replacements.items():
        html = html.replace(token, value)
    out_path = os.path.join(OUT_DIR, f"{post['slug']}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("gerado:", out_path)

# ---------------------------------------------------------------------
# Geração da listagem /blog/index.html
# ---------------------------------------------------------------------
if POSTS:
    cards = "\n  ".join(post_card_html(post) for post in sorted(POSTS, key=lambda x: x["data_publicacao"], reverse=True))
    conteudo = f'<div class="blog-grid">\n  {cards}\n  </div>'
    robots = "index, follow"
else:
    conteudo = """<div class="blog-empty">
  <div class="blog-empty-icone">✍️</div>
  <p>Os primeiros artigos estão a caminho — conteúdo prático sobre fluxo de caixa, planejamento e gestão para MEI e PME da região. Enquanto isso, conheça o diagnóstico gratuito ou fale com a gente.</p>
  <a class="btn-cta" href="/diagnostico-cliente.html">QUERO MEU DIAGNÓSTICO GRATUITO</a>
</div>"""
    robots = "noindex, follow"

breadcrumb_index = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Início", "item": f"{BASE_URL}/"},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": BLOG_INDEX_URL},
    ],
}

index_html = INDEX_TEMPLATE
index_replacements = {
    "@@URL@@": BLOG_INDEX_URL, "@@ROBOTS@@": robots,
    "@@BREADCRUMB_JSON@@": json.dumps(breadcrumb_index, ensure_ascii=False, indent=2),
    "@@CONTEUDO@@": conteudo,
    "@@CSS@@": CSS, "@@NAV@@": nav_html(), "@@FOOTER@@": footer_html(),
    "@@WA_FLOAT@@": WA_FLOAT_HTML, "@@MENU_JS@@": MENU_JS,
}
for token, value in index_replacements.items():
    index_html = index_html.replace(token, value)
with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)
print("gerado:", os.path.join(OUT_DIR, "index.html"))

# ---------------------------------------------------------------------
# Atualização do bloco de URLs do blog em sitemap.xml
# ---------------------------------------------------------------------
today = datetime.now().strftime("%Y-%m-%d")
blog_urls_xml = ""
if POSTS:
    entries = [f"""  <url>
    <loc>{BLOG_INDEX_URL}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>"""]
    for post in POSTS:
        entries.append(f"""  <url>
    <loc>{post['url']}</loc>
    <lastmod>{post.get('data_atualizacao', post['data_publicacao'])}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>""")
    blog_urls_xml = "\n" + "\n".join(entries) + "\n"

with open(SITEMAP_PATH, "r", encoding="utf-8") as f:
    sitemap = f.read()

if "<!-- BLOG_URLS_START -->" not in sitemap:
    # primeira execução: insere os marcadores logo antes de </urlset>
    sitemap = sitemap.replace(
        "</urlset>",
        f"  <!-- BLOG_URLS_START -->{blog_urls_xml}  <!-- BLOG_URLS_END -->\n</urlset>"
    )
else:
    sitemap = re.sub(
        r"<!-- BLOG_URLS_START -->.*?<!-- BLOG_URLS_END -->",
        f"<!-- BLOG_URLS_START -->{blog_urls_xml}  <!-- BLOG_URLS_END -->",
        sitemap, flags=re.DOTALL
    )

with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
    f.write(sitemap)
print("sitemap.xml atualizado:", "com" if POSTS else "sem", "posts do blog")
