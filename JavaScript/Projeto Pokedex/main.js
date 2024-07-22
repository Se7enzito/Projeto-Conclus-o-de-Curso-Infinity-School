const containerPokemons = document.querySelector(".pokemons")
const BASE_API = "https://pokeapi.co/api/v2"

function captarPokemons() {
    fetch(`${BASE_API}/pokemon`)
       .then(response => response.json())
       .then(data => {
            console.log(data.results)
            data.results.forEach(pokemon => {
                fetch(pokemon.url)
                   .then(response => response.json())
                   .then(data => {
                        containerPokemons.innerHTML += `
                            <div class="pokemon">
                                <img src="${data.sprites.versions["generation-v"]["black-white"].animated.front_default}" alt="${data.name}">
                                <h2>${data.name}</h2>
                                <div class="types">
                                ${data.types.map(item => `<span class="type">${item.type.name}</span>`).join('/')}
                                </div>
                            </div>
                        `
                    })
            })
        })
}

captarPokemons()