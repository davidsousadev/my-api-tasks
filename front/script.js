const apiUrl = "https://my-api-tasks-1.onrender.com"; // Certifique-se de que esse URL é o da sua API

// Função para mostrar o loader
function showLoader() {
    document.getElementById("loader").style.display = "block";
}

// Função para ocultar o loader
function hideLoader() {
    document.getElementById("loader").style.display = "none";
}

// Função para abrir o modal
function abrirModal(tipo) {
    const modal = document.getElementById("modal");
    const formAtividade = document.getElementById("formAtividade");
    const formRegistro = document.getElementById("formRegistro");

    // Esconde ambos os formulários inicialmente
    formAtividade.style.display = "none";
    formRegistro.style.display = "none";

    // Exibe o formulário correspondente
    if (tipo === "atividade") {
        formAtividade.style.display = "block";
    } else if (tipo === "registro") {
        carregarAtividades(); // Carregar atividades para o registro
        formRegistro.style.display = "block";
    }

    modal.style.display = "block";
}

// Função para fechar o modal
function fecharModal() {
    document.getElementById("modal").style.display = "none";
}

// Função para listar atividades e preencher o select
function carregarAtividades() {
    showLoader();
    fetch(`${apiUrl}/atividades`)
        .then(response => response.json())
        .then(data => {
            const atividadeSelect = document.getElementById("atividadeSelect");
            atividadeSelect.innerHTML = '<option value="">Selecione uma Atividade</option>'; // Limpa as opções

            if (!Array.isArray(data) || data.length === 0) {
                atividadeSelect.innerHTML += '<option value="">Nenhuma atividade encontrada</option>';
                hideLoader();
                return;
            }

            data.forEach(atividade => {
                const option = document.createElement("option");
                option.value = atividade.id;
                option.innerHTML = `${atividade.titulo} - ${atividade.descricao}`;
                atividadeSelect.appendChild(option);
            });
            hideLoader();
        })
        .catch(error => {
            console.error('Erro ao carregar atividades:', error);
            alert(`Erro ao carregar atividades: ${error.message || error}`);
            hideLoader();
        });
}

// Chama a função para carregar as atividades quando a página carregar
window.onload = carregarAtividades;

// Função para listar atividades
function listarAtividades() {
    showLoader();
    fetch(`${apiUrl}/atividades`)
        .then(response => response.json())
        .then(data => {
            const atividadeList = document.getElementById("atividadeList");
            atividadeList.innerHTML = ''; // Limpa a lista de atividades

            if (!Array.isArray(data) || data.length === 0) {
                atividadeList.innerHTML = '<li>Nenhuma atividade encontrada.</li>';
                hideLoader();
                return;
            }

            data.forEach(atividade => {
                const li = document.createElement("li");
                li.innerHTML = `
                <p><strong>ID:</strong> ${atividade.id}</p>
                <p><strong>Titulo:</strong> ${atividade.titulo}</p>
                <p><strong>Descrição:</strong> ${atividade.descricao}</p>
                <p><strong>Tempo:</strong> ${atividade.tempo_acumulado} min</p>
                <p><strong>Nota:</strong> ${atividade.media_classificacao} / 5</p>
                    <button onclick="editarAtividade(${atividade.id})">Editar</button>
                    <button onclick="deletarAtividade(${atividade.id})">Excluir</button>
                    <button onclick="listarRegistros(${atividade.id})">Ver Registros</button>`; // Botão para ver registros
                atividadeList.appendChild(li);
            });
            hideLoader();
        })
        .catch(error => {
            console.error('Erro ao listar atividades:', error);
            hideLoader();
        });
}

// Função para listar registros de uma atividade
function listarRegistros(id_atividade) {
    showLoader();
    fetch(`${apiUrl}/registros/${id_atividade}`)
        .then(response => response.json())
        .then(data => {
            const registroList = document.getElementById("registroList");
            registroList.innerHTML = ''; // Limpa a lista de registros

            if (!Array.isArray(data) || data.length === 0) {
                registroList.innerHTML = '<li>Nenhum registro encontrado para esta atividade.</li>';
                hideLoader();
                return;
            }

            data.forEach(registro => {
                const li = document.createElement("li");
                li.innerHTML = `
                <p><strong>ID:</strong> ${registro.id}</p>
                <p><strong>Tempo:</strong> ${registro.tempo} min</p>
                <p><strong>Classificação:</strong> ${registro.classificacao}</p>
                <p><strong>Descrição:</strong> ${registro.descricao}</p>
                    <button onclick="editarRegistro(${registro.id})">Editar</button>
                    <button onclick="deletarRegistro(${registro.id})">Excluir</button>`;
                registroList.appendChild(li);
            });
            hideLoader();
        })
        .catch(error => {
            console.error('Erro ao listar registros:', error);
            alert(`Erro ao listar registros: ${error.message || error}`);
            hideLoader();
        });
}

// Função para editar uma atividade
function editarAtividade(id_atividade) {
    const novoTitulo = prompt("Novo título da atividade:");
    const novaDescricao = prompt("Nova descrição da atividade:");

    if (novoTitulo && novaDescricao) {
        showLoader();
        fetch(`${apiUrl}/atividades/${id_atividade}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ titulo: novoTitulo, descricao: novaDescricao })
        })
            .then(response => response.json())
            .then(data => {
                alert("Atividade atualizada com sucesso!");
                listarAtividades(); // Atualiza a lista de atividades
            })
            .catch(error => {
                console.error('Erro ao editar atividade:', error);
                alert(`Erro ao editar atividade: ${error.message || error}`);
            })
            .finally(() => hideLoader());
    }
}

// Função para excluir uma atividade
function deletarAtividade(id_atividade) {
    if (confirm("Tem certeza que deseja excluir esta atividade?")) {
        showLoader();
        fetch(`${apiUrl}/atividades/${id_atividade}`, {
            method: "DELETE",
        })
            .then(() => {
                alert("Atividade excluída com sucesso!");
                listarAtividades(); // Atualiza a lista de atividades
            })
            .catch(error => {
                console.error('Erro ao excluir atividade:', error);
                alert(`Erro ao excluir atividade: ${error.message || error}`);
            })
            .finally(() => hideLoader());
    }
}

// Função para editar um registro
function editarRegistro(id_registro) {
    const novoTempo = prompt("Novo tempo do registro:");
    const novaClassificacao = prompt("Nova classificação do registro:");
    const novaDescricao = prompt("Nova descrição do registro:");

    if (novoTempo && novaClassificacao && novaDescricao) {
        showLoader();
        fetch(`${apiUrl}/registros/${id_registro}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ tempo: novoTempo, classificacao: novaClassificacao, descricao: novaDescricao })
        })
            .then(response => response.json())
            .then(data => {
                alert("Registro atualizado com sucesso!");
                listarRegistros(data.id_atividade); // Atualiza a lista de registros para a atividade
            })
            .catch(error => {
                console.error('Erro ao editar registro:', error);
                alert(`Erro ao editar registro: ${error.message || error}`);
            })
            .finally(() => hideLoader());
    }
}

// Função para excluir um registro
function deletarRegistro(id_registro) {
    if (confirm("Tem certeza que deseja excluir este registro?")) {
        showLoader();
        fetch(`${apiUrl}/registros/${id_registro}`, {
            method: "DELETE",
        })
            .then(() => {
                alert("Registro excluído com sucesso!");
                listarRegistros(); // Atualiza a lista de registros
            })
            .catch(error => {
                console.error('Erro ao excluir registro:', error);
                alert(`Erro ao excluir registro: ${error.message || error}`);
            })
            .finally(() => hideLoader());
    }
}

// Função para criar uma nova atividade
document.getElementById("atividadeForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const titulo = document.getElementById("titulo").value;
    const descricao = document.getElementById("descricao").value;

    showLoader();
    fetch(`${apiUrl}/atividades`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ titulo, descricao })
    })
        .then(response => response.json())
        .then(data => {
            alert("Atividade criada com sucesso!");
            listarAtividades(); // Atualiza a lista de atividades
        })
        .catch(error => {
            console.error('Erro ao criar atividade:', error);
            alert(`Erro ao criar atividade: ${error.message || error}`);
        })
        .finally(() => hideLoader());
});

// Função para criar um novo registro
document.getElementById("registroForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const id_atividade = document.getElementById("atividadeSelect").value; // Atualizei para pegar o valor correto
    const tempo = document.getElementById("tempo").value;
    const classificacao = document.getElementById("classificacao").value;
    const descricao_registro = document.getElementById("descricao_registro").value;

    showLoader();
    fetch(`${apiUrl}/registros`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ id_atividade, tempo, classificacao, descricao: descricao_registro })
    })
        .then(response => response.json())
        .then(data => {
            alert("Registro criado com sucesso!");
            listarRegistros(id_atividade); // Atualiza a lista de registros para a atividade
        })
        .catch(error => {
            console.error('Erro ao criar registro:', error);
            alert(`Erro ao criar registro: ${error.message || error}`);
        })
        .finally(() => hideLoader());
});

// Inicialização
listarAtividades(); // Carrega as atividades ao carregar a página
