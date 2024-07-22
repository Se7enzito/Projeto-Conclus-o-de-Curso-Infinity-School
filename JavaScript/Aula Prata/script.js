const urlAPI = 'https://667f39f4f2cb59c38dc8613f.mockapi.io/api/historia/historias'

async function carregarHistorias() {
    const resposta = await fetch(urlAPI)
    const historias = await resposta.json()

    renderizarHistorias(historias)
}

async function criarHistorias() {
    const inputDesc = document.getElementById('descricao')
    let descricao = inputDesc.value

    const historiaInformada = {
        "descricao": descricao,
        "likes": 0
    }

    const detalhesReqHTPP = {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(historiaInformada)
    }

    const resposta = await fetch(urlAPI, detalhesReqHTPP)
}

function renderizarHistorias(historiasCarregas) {
    const listaHistorias = document.querySelector('#lista-historias')

    historiasCarregas.forEach(historia => {
        let trHistoria = document.createElement('tr')

        trHistoria.innerHTML = `
        <td>${historia.id}</td>
        <td>${historia.descricao}</td>
        <td>${historia.likes}</td>
        <td></td>`

        listaHistorias.appendChild(trHistoria)
    });
}

const formularioEnviaar = document.querySelector('#form-adicionar')
formularioEnviaar.addEventListener('submit', (event) => {
    event.preventDefault()
    criarHistorias()
    document.getElementById('descricao').value = ''
})

carregarHistorias()