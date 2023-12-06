function validaEntrada() {
  let curYear =  new Date().getFullYear();
  // Pegar valor inserido no campo 'Ano'
  let ano = document.getElementById("inputAno").value;
  let mes = document.getElementById("inputMes").value;
  // If x is Not a Number or less than one or greater than 10
  if (ano === '' || ano < 2000 || ano > curYear) {
    alert("Ano inválido");
  } else if (mes === '' || mes < 1 || mes > 12) {
    alert("Mês inválido");
  } else{
    lista = getList(ano, mes)
  }
console.log(lista)

}

/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/

const getList = async (inputAno, inputMes) => {
  const formData = new FormData();
  formData.append('ano', inputAno);
  formData.append('mes', inputMes);
  
  fetch(`http://127.0.0.1:5000/lista_itens?ano=${inputAno}&mes=${inputMes}`, {method:'get'})
  .then((response) => response.json())
  .then((response) => {
    if(response.length>0){
      let i = 0;
      while (i<response.length){
        insertList(response[i].referencia, (response[i].nome).toUpperCase(), response[i].valor, response[i].data);
        i++;
      }
    }else{
      alert("Não há registros para o período selecionado")
    }
  })
  .catch((error) => {
    console.error('Error:', error);
  });
  resetarList()
  removeElement()
  
}

/*
  --------------------------------------------------------------------------------------
  Função para colocar um item na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/
const postItem = async (inputReferencia, inputNome, inputValor, inputData) => {
  const formData = new FormData();
  formData.append('referencia', inputReferencia);
  formData.append('nome', inputNome);
  formData.append('data_pgto', inputData);
  formData.append('valor', inputValor);

  let url = 'http://127.0.0.1:5000/add_item';
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada item da lista
  --------------------------------------------------------------------------------------
*/
const insertButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
}

const insertEditButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u270E");
  span.className = "edit";
  span.appendChild(txt);
  parent.appendChild(span);
}

/*
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
function removeElement() {
  let close = document.getElementsByClassName("close");
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      var nomeItem = div.getElementsByTagName('td')[1].innerHTML;
      var valorItem = div.getElementsByTagName('td')[2].innerHTML;
      var dataItem = div.getElementsByTagName('td')[3].innerHTML;

      fetch('http://127.0.0.1:5000/lista_tudo', {method:'get'})
      .then((response) => response.json())
      .then((response) => {
        if(response.length>0){
          let i = 0;
          while (i<response.length){
            if((response[i].nome).toUpperCase() == nomeItem && response[i].valor == valorItem && response[i].data == dataItem){
              if (confirm("Você tem certeza?")) {
                div.remove();
                deleteItem(response[i].id);
                alert("Removido!");
              }
            }
            i++;
          }
        }else{
          alert("Não há registros para o período selecionado");
          
        }
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    }
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para deletar um item da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deleteItem = (id) => {
  console.log(id)
  let url = `http://127.0.0.1:5000/del_item?id=${id}`;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo item com nome, quantidade e valor 
  --------------------------------------------------------------------------------------
*/
const newItem = () => {
  let inputReferencia = document.getElementById("inputReferencia").value;
  let inputNome = (document.getElementById("inputNome").value).toUpperCase();
  let inputValor = document.getElementById("inputValor").value;
  let inputData = document.getElementById("inputData").value;

  if (inputNome === '') {
    alert("Escreva o nome de um item!");
  } else if (inputValor === '' || inputData === '') {
    alert("Valor e/ou data precisam ser preenchidos!");
  } else if (inputReferencia === '') {
    alert("Selecione uma referência");
  } else {
    insertList(inputReferencia, inputNome, inputValor, inputData)
    postItem(inputReferencia, inputNome, inputValor, inputData)
    alert("Item adicionado!")
  }
  removeElement()
}

/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertList = (inputReferencia, inputNome, inputValor, inputData) => {
  var item = [inputReferencia, inputNome, inputValor, inputData]
  var table = document.getElementById('myTable');
  var row = table.insertRow();

  for (var i = 0; i < item.length; i++) {
    var cel = row.insertCell(i);
    cel.textContent = item[i];
  }
  insertButton(row.insertCell(-1))
  insertEditButton(row.insertCell(-1))
  document.getElementById("inputReferencia").value = "";
  document.getElementById("inputNome").value = "".toUpperCase();
  document.getElementById("inputValor").value = "";
  document.getElementById("inputData").value = "";

  removeElement()
}

const resetarList = () => {
  let tabela = document.getElementById('myTable')
  let linhas = tabela.childNodes[1]
  let linhas_children = linhas.children

  let i = 0;
  for (i = 0; i < linhas_children.length; i++) {
    if (linhas_children.length>1){
      linhas_children.item(1).remove()
    }
  }
  resetarList();
}