const containerPokemons = document.querySelector(".pokemons")
const carregarMais = document.querySelector(".carregar-mais")
const BASE_API = "https://pokeapi.co/api/v2"

let offset = 0;

function carregarPokemons() {
    offset += 20;
    captarPokemons()
}

function voltarMenu() {
    offset = 0;

    captarPokemons(true)
}

function captarPokemons(limparTela = false) {
    fetch(`${BASE_API}/pokemon?offset=${offset}`)
        .then(resposta => resposta.json())
        .then(dado => {
            if (limparTela) {
                containerPokemons.innerHTML = ""
            }

            carregarMais.style.display = "block"
            captarPokemon(dado.results)
        })
}


function captarPokemon(arrayPokemons) {
    for (let item of arrayPokemons) {
        fetch(item.url)
            .then(res => res.json())
            .then(pokemon => {
                const linkImg = pokemon.sprites.versions["generation-v"]["black-white"].animated.front_default ?
                    pokemon.sprites.versions["generation-v"]["black-white"].animated.front_default
                    : pokemon.sprites.front_default
                containerPokemons.innerHTML += `
                <div class="pokemon">
                    <img src="${linkImg}" />
                    <h4>${pokemon.name}</h4>
                    <div class="types">
                        ${pokemon.types.map(item => `<span class="type ${item.type.name}">${item.type.name}</span>`).join(" ")}
                    </div>
                </div>
            `

            })
    }
}

function filtrarPorTipo(tipo) {
    fetch(`${BASE_API}/type/${tipo}`)
        .then(res => res.json())
        .then(dados => {
            const pokemons = dados.pokemon.map(item => item.pokemon)

            carregarMais.style.display = 'none'
            containerPokemons.innerHTML = ""

            captarPokemon(pokemons)
        })
}

captarPokemons()