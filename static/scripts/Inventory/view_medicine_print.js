$("#printbutton").on("click", function () {
    printStatement();
});
function printStatement() {
    let printarea = document.querySelector("#viewmedicine")
    let printarea2 = document.querySelector("#transactiontable")
    let printarea3 = document.querySelector("#transactiontable2")
    let printarea4 = document.querySelector("#transactiontable3")
    let newWindow = window.open("");
    newWindow.document.write(`<html><thead><title></title>`);
    newWindow.document.write(`<style media="print">
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500&display=swap');
  body {
    font-family: 'Poppins', sans-serif;

  }
  tbody {
    border-collapse: collapse;
    width: 100%;
    margin-bottom: 20px;
}

  body {
    
    background-color: grey;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 5px;
   
   
    
    
  }

  th {
    background-color: #04AA6D !important;
    color: green !important;
    border: 1px solid black;
	padding: 5px;
  }
  

  </style>`)
  
    newWindow.document.write(`</thead><body`);
    newWindow.document.write(printarea.innerHTML);
    newWindow.document.write(printarea2.innerHTML);
    newWindow.document.write(printarea3.innerHTML);
    newWindow.document.write(printarea4.innerHTML);
    newWindow.document.write(`</body></html>`);
    newWindow.print();
    newWindow.close();

}