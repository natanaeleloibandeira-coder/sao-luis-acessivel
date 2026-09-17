from flask import Flask, render_template_string
import json

app = Flask(__name__)

# ==========================================================
# LOCAIS
# ==========================================================

locais = [
    {
        "nome": "Shopping da Ilha",
        "categoria": "Cadeirantes",
        "bairro": "Cohama",
        "endereco": "Av. Daniel de La Touche, 987",
        "latitude": -2.534086,
        "longitude": -44.260612,
        "nota": "4.6",
        "distancia": "2,3 km",
        "imagem": "https://images.unsplash.com/photo-1555529669-e69e7aa0ba9a?auto=format&fit=crop&w=600&q=80",
        "descricao": "Shopping com estrutura de acessibilidade para pessoas com mobilidade reduzida."
    },
    {
        "nome": "Restaurante Cheiro Verde",
        "categoria": "Cadeirantes",
        "bairro": "Olho D'Água",
        "endereco": "Av. São Luís Rei de França, 131",
        "latitude": -2.528784,
        "longitude": -44.226287,
        "nota": "4.7",
        "distancia": "4,1 km",
        "imagem": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=600&q=80",
        "descricao": "Restaurante com indicação de acessibilidade para cadeirantes."
    },
    {
        "nome": "Colégio Adventista",
        "categoria": "Cadeirantes",
        "bairro": "Maranhão Novo",
        "endereco": "Av. Daniel de La Touche, 51",
        "latitude": -2.535222,
        "longitude": -44.261158,
        "nota": "4.5",
        "distancia": "3,8 km",
        "imagem": "https://images.unsplash.com/photo-1580582932707-520aed937b7b?auto=format&fit=crop&w=600&q=80",
        "descricao": "Instituição de ensino com recursos de acessibilidade."
    },
    {
        "nome": "Colégio Literato",
        "categoria": "Cadeirantes",
        "bairro": "Olho D'Água",
        "endereco": "Av. Mário Andreazza, 10",
        "latitude": -2.500643609,
        "longitude": -44.23344806,
        "nota": "4.5",
        "distancia": "5,2 km",
        "imagem": "https://images.unsplash.com/photo-1562774053-701939374585?auto=format&fit=crop&w=600&q=80",
        "descricao": "Colégio com recursos de acessibilidade e inclusão."
    },
    {
        "nome": "Rio Anil Shopping",
        "categoria": "Cadeirantes",
        "bairro": "Turu",
        "endereco": "Av. São Luís Rei de França, 8",
        "latitude": -2.533640,
        "longitude": -44.224760,
        "nota": "4.4",
        "distancia": "7,6 km",
        "imagem": "https://images.unsplash.com/photo-1519567241046-7f570eee3ce6?auto=format&fit=crop&w=600&q=80",
        "descricao": "Shopping localizado na região do Turu."
    },
    {
        "nome": "Tropical Shopping",
        "categoria": "Cadeirantes",
        "bairro": "Jardim Renascença",
        "endereco": "Av. Colares Moreira, 400",
        "latitude": -2.501900,
        "longitude": -44.295800,
        "nota": "4.3",
        "distancia": "6,9 km",
        "imagem": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=600&q=80",
        "descricao": "Centro comercial localizado no Jardim Renascença."
    }
]


# ==========================================================
# PÁGINA
# ==========================================================

html = r"""
<!DOCTYPE html>
<html lang="pt-BR">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>São Luís Acessível</title>


<!-- LEAFLET -->

<link rel="stylesheet"
      href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">

<script
src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js">
</script>


<style>

/* =========================================================
   CONFIGURAÇÕES
========================================================= */

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background: #eef6fa;
    color: #123b5d;
}

button,
input {
    font-family: inherit;
}


/* =========================================================
   CABEÇALHO
========================================================= */

header {
    height: 82px;
    background: linear-gradient(90deg, #063b66, #075a91);
    color: white;

    display: flex;
    align-items: center;

    padding: 0 38px;

    gap: 18px;
}

.logo {
    width: 58px;
    height: 58px;

    border-radius: 50%;

    background: #10a9ee;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 31px;

    box-shadow: 0 3px 10px rgba(0,0,0,.25);
}

.logo-text {
    min-width: 240px;
}

.logo-text h1 {
    margin: 0;
    font-size: 26px;
}

.logo-text p {
    margin: 3px 0 0;
    font-size: 14px;
    opacity: .85;
}


/* =========================================================
   MENU
========================================================= */

.menu {
    display: flex;
    align-items: center;
    gap: 8px;

    margin-left: 60px;
}

.menu button {
    border: 0;
    background: transparent;

    color: white;

    padding: 12px 18px;

    border-radius: 12px;

    font-size: 15px;

    cursor: pointer;
}

.menu button:hover,
.menu button.ativo {
    background: #0799e6;
}


/* =========================================================
   LOCALIZAÇÃO
========================================================= */

.localizacao {
    margin-left: auto;

    background: rgba(255,255,255,.13);

    padding: 12px 18px;

    border-radius: 12px;

    font-size: 14px;
}


/* =========================================================
   CONTEÚDO
========================================================= */

.container {
    max-width: 1600px;
    margin: auto;
}


/* =========================================================
   HERO
========================================================= */

.hero {
    margin: 20px 24px 0;

    min-height: 210px;

    border-radius: 18px;

    padding: 30px 38px;

    color: white;

    position: relative;

    overflow: hidden;

    background:
        linear-gradient(
            90deg,
            rgba(0,107,166,.96),
            rgba(0,160,210,.78)
        ),
        url("https://images.unsplash.com/photo-1580210530074-0e9c3a5c3b70?auto=format&fit=crop&w=1600&q=80");

    background-size: cover;
    background-position: center;
}

.hero h2 {
    margin: 0 0 8px;

    font-size: 32px;
}

.hero p {
    font-size: 17px;
    margin: 0 0 20px;
}


/* =========================================================
   PESQUISA
========================================================= */

.search {
    background: white;

    height: 54px;

    max-width: 850px;

    border-radius: 15px;

    display: flex;
    align-items: center;

    padding: 0 18px;

    box-shadow: 0 5px 15px rgba(0,0,0,.15);
}

.search span {
    color: #123b5d;
    font-size: 24px;
}

.search input {
    border: 0;
    outline: 0;

    flex: 1;

    font-size: 16px;

    padding-left: 12px;
}


/* =========================================================
   ÁREA PRINCIPAL
========================================================= */

.main {
    display: grid;

    grid-template-columns: 2.1fr 1fr;

    gap: 0;

    margin: 0 24px;
}


/* =========================================================
   ESQUERDA
========================================================= */

.left {
    background: #eef8fb;
}


/* =========================================================
   FILTROS
========================================================= */

.filtros {
    padding: 20px 38px;

    background: linear-gradient(
        180deg,
        #36c3d3,
        #46cad9
    );
}

.filtros h3 {
    margin: 0 0 14px;

    font-size: 18px;
}


.filtro-botoes {
    display: grid;

    grid-template-columns:
        repeat(5, 1fr);

    gap: 12px;
}


.filtro {
    height: 90px;

    border: 0;

    border-radius: 14px;

    background: #064b78;

    color: white;

    cursor: pointer;

    font-size: 14px;

    font-weight: bold;

    transition: .2s;
}

.filtro:hover {
    transform: translateY(-2px);
}

.filtro.ativo {
    background: #078ed3;

    box-shadow:
        0 0 0 3px #8eeaff,
        0 5px 12px rgba(0,0,0,.2);
}

.filtro .icone {
    display: block;

    font-size: 31px;

    margin-bottom: 5px;
}


/* =========================================================
   LUGARES
========================================================= */

.lugares {
    padding: 22px 38px;
}

.lugares h2 {
    margin: 0 0 15px;

    font-size: 21px;
}


/* =========================================================
   CARDS
========================================================= */

.cards {
    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 13px;
}


.card {
    background: white;

    border-radius: 11px;

    overflow: hidden;

    box-shadow:
        0 2px 8px rgba(0,0,0,.12);

    transition: .2s;

    cursor: pointer;
}

.card:hover {
    transform: translateY(-3px);

    box-shadow:
        0 7px 16px rgba(0,0,0,.17);
}


.card-img {
    height: 125px;

    position: relative;

    overflow: hidden;
}

.card-img img {
    width: 100%;
    height: 100%;

    object-fit: cover;
}


.numero {
    position: absolute;

    top: 7px;
    left: 7px;

    background: #064b78;

    color: white;

    width: 29px;
    height: 29px;

    border-radius: 7px;

    display: flex;
    align-items: center;
    justify-content: center;

    font-weight: bold;
}


.nota {
    position: absolute;

    top: 7px;
    right: 7px;

    background: white;

    color: #174a6e;

    padding: 5px 8px;

    border-radius: 7px;

    font-size: 12px;

    font-weight: bold;
}


.card-content {
    padding: 10px 11px 13px;
}

.card h3 {
    margin: 0 0 7px;

    font-size: 15px;

    color: #123b5d;
}

.card .linha {
    font-size: 11px;

    margin: 5px 0;

    color: #4d6677;
}

.card .acessibilidade {
    color: #006aa3;

    font-weight: bold;
}

.card .distancia {
    font-weight: bold;
}


/* =========================================================
   LATERAL
========================================================= */

.sidebar {
    background: #f5fbfd;

    padding: 25px 18px;

    border-left: 1px solid #d7e7ee;
}


.sidebar-box {
    background: white;

    border-radius: 15px;

    padding: 16px;

    margin-bottom: 18px;

    box-shadow:
        0 2px 9px rgba(0,0,0,.09);
}


.sidebar-title {
    font-size: 18px;

    font-weight: bold;

    margin-bottom: 14px;

    color: #123b5d;
}


/* =========================================================
   CARDS LATERAIS
========================================================= */

.side-cards {
    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 8px;
}


.side-card {
    overflow: hidden;

    border-radius: 8px;

    border: 1px solid #dce8ed;

    background: white;
}


.side-card img {
    width: 100%;
    height: 65px;

    object-fit: cover;
}


.side-card div {
    padding: 7px;
}

.side-card strong {
    font-size: 11px;
    display: block;
}

.side-card small {
    font-size: 9px;
    color: #687985;
}


/* =========================================================
   EVENTO
========================================================= */

.evento {
    display: flex;

    gap: 12px;

    align-items: center;

    border: 1px solid #e2ebef;

    border-radius: 10px;

    padding: 10px;
}

.evento img {
    width: 90px;
    height: 65px;

    object-fit: cover;

    border-radius: 8px;
}

.evento h4 {
    margin: 0 0 6px;
}

.evento p {
    margin: 3px 0;

    font-size: 11px;

    color: #687985;
}


/* =========================================================
   MAPA
========================================================= */

.mapa-box {
    margin: 0 38px 30px;
}

.mapa-box h2 {
    font-size: 21px;
}

#mapa {
    width: 100%;
    height: 390px;

    border-radius: 14px;

    box-shadow:
        0 2px 10px rgba(0,0,0,.15);
}


/* =========================================================
   BOTÃO ROTA
========================================================= */

.rota {
    display: inline-block;

    background: #078ed3;

    color: white;

    text-decoration: none;

    padding: 8px 12px;

    border-radius: 7px;

    font-size: 12px;

    margin-top: 5px;
}

.rota:hover {
    background: #056da4;
}


/* =========================================================
   RODAPÉ
========================================================= */

footer {
    background: #063e69;

    color: white;

    min-height: 65px;

    display: flex;

    align-items: center;

    justify-content: space-between;

    padding: 0 40px;

    font-size: 13px;
}

footer .mensagem {
    font-size: 15px;
    font-weight: bold;
}

footer .social {
    font-size: 18px;
}


/* =========================================================
   RESPONSIVO
========================================================= */

@media (max-width: 1100px) {

    .main {
        grid-template-columns: 1fr;
    }

    .sidebar {
        border-left: 0;
    }

    .menu {
        margin-left: 10px;
    }

    .cards {
        grid-template-columns:
            repeat(2, 1fr);
    }
}


@media (max-width: 750px) {

    header {
        height: auto;

        padding: 15px;

        flex-wrap: wrap;
    }

    .menu {
        order: 3;

        width: 100%;

        justify-content: center;

        margin: 0;
    }

    .localizacao {
        display: none;
    }

    .hero {
        margin: 10px;

        padding: 25px;

        min-height: 200px;
    }

    .hero h2 {
        font-size: 24px;
    }

    .main {
        margin: 0 10px;
    }

    .filtros,
    .lugares {
        padding: 18px;
    }

    .filtro-botoes {
        grid-template-columns:
            repeat(2, 1fr);
    }

    .cards {
        grid-template-columns: 1fr;
    }

    .mapa-box {
        margin: 0 18px 20px;
    }

    .side-cards {
        grid-template-columns:
            repeat(2, 1fr);
    }

    footer {
        padding: 15px;

        flex-direction: column;

        gap: 10px;
    }
}

</style>

</head>


<body>


<!-- =====================================================
     CABEÇALHO
===================================================== -->

<header>

    <div class="logo">
        ♿
    </div>

    <div class="logo-text">

        <h1>
            São Luís Acessível
        </h1>

        <p>
            Mapa de acessibilidade e inclusão
        </p>

    </div>


    <nav class="menu">

        <button class="ativo">
            🏠 Início
        </button>

        <button>
            🔎 Explorar
        </button>

        <button onclick="irMapa()">
            🗺️ Mapa
        </button>

        <button>
            ❤️ Favoritos
        </button>

        <button>
            👤 Perfil
        </button>

    </nav>


    <div class="localizacao">
        📍 São Luís, MA
    </div>

</header>



<!-- =====================================================
     HERO
===================================================== -->

<div class="container">

<section class="hero">

    <h2>
        Bem-vindo ao São Luís Acessível!
    </h2>

    <p>
        Encontre lugares acessíveis e inclusivos na cidade.
    </p>


    <div class="search">

        <span>⌕</span>

        <input
            type="text"
            id="pesquisa"
            placeholder="Buscar lugares, bairros, endereços..."
        >

        <span>
            📍
        </span>

    </div>

</section>



<!-- =====================================================
     PRINCIPAL
===================================================== -->

<div class="main">


<div class="left">


<!-- FILTROS -->

<section class="filtros">

    <h3>
        Selecione o que você busca:
    </h3>


    <div class="filtro-botoes">

        <button
            class="filtro ativo"
            onclick="filtrarCategoria('todos', this)">

            <span class="icone">
                ♿
            </span>

            Cadeirantes

        </button>


        <button
            class="filtro"
            onclick="filtrarCategoria('banheiro', this)">

            <span class="icone">
                🚻
            </span>

            Banheiro<br>
            Adaptado

        </button>


        <button
            class="filtro"
            onclick="filtrarCategoria('braille', this)">

            <span class="icone">
                ⠿
            </span>

            Braille

        </button>


        <button
            class="filtro"
            onclick="filtrarCategoria('libras', this)">

            <span class="icone">
                🤟
            </span>

            Libras

        </button>


        <button
            class="filtro"
            onclick="filtrarCategoria('estacionamento', this)">

            <span class="icone">
                🅿
            </span>

            Estacionamento

        </button>

    </div>

</section>



<!-- LUGARES -->

<section class="lugares">

    <h2>
        ♿ Lugares Populares Próximos
    </h2>


    <div
        class="cards"
        id="cards">
    </div>

</section>



<!-- MAPA -->

<section
    class="mapa-box"
    id="areaMapa">

    <h2>
        🗺️ Mapa de acessibilidade
    </h2>

    <div id="mapa"></div>

</section>


</div>



<!-- =====================================================
     SIDEBAR
===================================================== -->

<aside class="sidebar">


<div class="sidebar-box">

    <div class="sidebar-title">
        ⭐ Próximos de você
    </div>


    <div
        class="side-cards"
        id="sideCards">
    </div>

</div>



<div class="sidebar-box">

    <div class="sidebar-title">
        📅 Destaques e Eventos Acessíveis
    </div>


    <div class="evento">

        <img
        src="https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=400&q=80">


        <div>

            <h4>
                Eventos acessíveis
            </h4>

            <p>
                ♿ Espaços com acessibilidade
            </p>

            <p>
                📍 São Luís - MA
            </p>

        </div>

    </div>

</div>


</aside>


</div>

</div>



<!-- =====================================================
     RODAPÉ
===================================================== -->

<footer>

    <div class="mensagem">
        ♿ Mais inclusão, uma São Luís melhor para todos!
    </div>

    <div class="social">
        Instagram &nbsp; Facebook &nbsp; ▶️
    </div>

    <div>
        © 2026 - São Luís Acessível
    </div>

</footer>



<script>

// ========================================================
// DADOS VINDOS DO PYTHON
// ========================================================

const locais = __DADOS_LOCAIS__;


// ========================================================
// MAPA
// ========================================================

const mapa = L.map("mapa").setView(
    [-2.5300, -44.2500],
    12
);


L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        maxZoom: 19,
        attribution: "&copy; OpenStreetMap"
    }
).addTo(mapa);


// ========================================================
// MARCADORES
// ========================================================

let marcadores = [];


function criarMarcadores(lista) {

    // Remove marcadores antigos

    marcadores.forEach(function(marker) {
        mapa.removeLayer(marker);
    });

    marcadores = [];


    lista.forEach(function(local) {

        const marker = L.marker([
            local.latitude,
            local.longitude
        ]).addTo(mapa);


        const rota =
            "https://www.google.com/maps/dir/?api=1"
            + "&destination="
            + local.latitude
            + ","
            + local.longitude;


        marker.bindPopup(`

            <div style="min-width:220px">

                <h3 style="color:#075a91">
                    ♿ ${local.nome}
                </h3>

                <p>
                    <b>Categoria:</b>
                    ${local.categoria}
                </p>

                <p>
                    ${local.descricao}
                </p>

                <p>
                    📍 ${local.endereco}
                </p>

                <a
                    class="rota"
                    href="${rota}"
                    target="_blank">

                    🚗 Como chegar

                </a>

            </div>

        `);


        marcadores.push(marker);

    });

}


// ========================================================
// CARDS
// ========================================================

function mostrarCards(lista) {

    const cards =
        document.getElementById("cards");

    cards.innerHTML = "";


    lista.forEach(function(local, index) {

        const rota =
            "https://www.google.com/maps/dir/?api=1"
            + "&destination="
            + local.latitude
            + ","
            + local.longitude;


        const card =
            document.createElement("div");


        card.className = "card";


        card.onclick = function() {

            mapa.setView(
                [
                    local.latitude,
                    local.longitude
                ],
                16
            );

        };


        card.innerHTML = `

            <div class="card-img">

                <img
                    src="${local.imagem}"
                    onerror="this.style.display='none'"
                >

                <div class="numero">
                    ${index + 1}.
                </div>

                <div class="nota">
                    ${local.nota} ⭐
                </div>

            </div>


            <div class="card-content">

                <h3>
                    ${local.nome}
                </h3>


                <div class="linha acessibilidade">

                    ♿ Acessível para cadeirantes

                </div>


                <div class="linha">

                    📍 ${local.endereco}

                </div>


                <div class="linha">

                    ${local.bairro} - São Luís, MA

                </div>


                <div class="linha distancia">

                    📍 ${local.distancia}

                </div>

            </div>

        `;


        cards.appendChild(card);

    });

}


// ========================================================
// CARDS LATERAIS
// ========================================================

function mostrarLaterais(lista) {

    const container =
        document.getElementById("sideCards");

    container.innerHTML = "";


    lista.slice(0, 4).forEach(function(local, index) {

        const card =
            document.createElement("div");


        card.className = "side-card";


        card.innerHTML = `

            <img src="${local.imagem}">

            <div>

                <strong>
                    ${index + 1}. ${local.nome}
                </strong>

                <small>
                    ♿ ${local.categoria}
                </small>

                <small>
                    📍 ${local.bairro}
                </small>

            </div>

        `;


        container.appendChild(card);

    });

}


// ========================================================
// FILTRO
// ========================================================

let categoriaAtual = "todos";


function filtrarCategoria(categoria, botao) {

    categoriaAtual = categoria;


    document
        .querySelectorAll(".filtro")
        .forEach(function(b) {

            b.classList.remove("ativo");

        });


    botao.classList.add("ativo");


    atualizar();

}


// ========================================================
// ATUALIZAR
// ========================================================

function atualizar() {

    const texto =
        document
        .getElementById("pesquisa")
        .value
        .toLowerCase();


    let resultado =
        locais.filter(function(local) {

            const textoLocal =
                (
                    local.nome
                    + " "
                    + local.bairro
                    + " "
                    + local.endereco
                ).toLowerCase();


            return textoLocal.includes(texto);

        });


    criarMarcadores(resultado);

    mostrarCards(resultado);

    mostrarLaterais(resultado);

}


// ========================================================
// PESQUISA
// ========================================================

document
    .getElementById("pesquisa")
    .addEventListener(
        "input",
        atualizar
    );


// ========================================================
// IR PARA MAPA
// ========================================================

function irMapa() {

    document
        .getElementById("areaMapa")
        .scrollIntoView({
            behavior: "smooth"
        });

}


// ========================================================
// INICIAR
// ========================================================

atualizar();


setTimeout(function() {

    mapa.invalidateSize();

}, 500);

</script>


</body>
</html>
"""


# ==========================================================
# ROTA FLASK
# ==========================================================

@app.route("/")
def inicio():

    dados = json.dumps(
        locais,
        ensure_ascii=False
    )

    pagina = html.replace(
        "__DADOS_LOCAIS__",
        dados
    )

    return render_template_string(pagina)


# ==========================================================
# INICIAR
# ==========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
