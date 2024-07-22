let tarefas = []
const formulario = document.querySelector("form")
const containerDasTarefas = document.querySelector("#tarefas")

formulario.addEventListener("submit", adicionarTarefa)

function adicionarTarefa(evento) {
    evento.preventDefault()

    const nomeTarefa = formulario.nome_tarefa.value

    if (nomeTarefa === "" /* !nomeTarefa */) {
        alert("Preencha os dados")
        return
    }

    if (tarefas.includes(nomeTarefa)) {
        alert("Tarefa já existe")
        return
    }

    tarefas.push(nomeTarefa)

    mostrarNaTela()
}

function mostrarNaTela() {
    containerDasTarefas.innerHTML = ""

    for (let tarefa of tarefas) {
        let input = document.createElement("input")
        input.type = "checkbox"
        
        let p = document.createElement("p")
        p.innerText = tarefa
        
        let botaoEditar = document.createElement("button")
        botaoEditar.innerText = "Editar"

        let botaoApagar = document.createElement("button")
        botaoApagar.innerText = "Apagar"
        
        let containerBotoes = document.createElement("div")

        containerBotoes.append(botaoEditar, botaoApagar)

        let containerTarefa = document.createElement("div")

        containerTarefa.append(input, p, containerBotoes)
        containerTarefa.classList.add("tarefa")

        containerDasTarefas.append(containerTarefa)
    }
}