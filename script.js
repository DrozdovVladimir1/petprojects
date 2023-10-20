const queue =[]
document.addEventListener('click', function(e) {
    if ((e.target.classList.contains('quadrat'))||(e.target.classList.contains('Taken'))) {
        myFunction(e.target.id);
    }
});
var arr = new Array(16);
for (var i = 0; i < 16; i++) {
  arr[i] = new Array(16);
}
for (var i = 0; i < 16; i++) {
    for (var j = 0; j < 16; j++) {
      arr[i][j] =0;
    }
  }
var tmp = new Array(16);
    for (var i = 0; i < 16; i++) {
      tmp[i] = new Array(16);
    }   
function myFunction(id) {
    console.log(id)
    let x = id.split('-')
    let i = parseInt(x[0])
    let j = parseInt(x[1])
    if (arr[i][j] == 0) {
            arr[i][j] = 1
            document.getElementById(`${i}-${j}`).className = 'Taken'
        }
    else {
            arr[i][j] = 0
            document.getElementById(`${i}-${j}`).className = 'quadrat'
        }    
}
function tick() {
    Cycle();
    RenderTheBoard();
}
function Cycle(){ console.log('Cycle')
for (var i = 0; i < 16; i++) {
    for (var j = 0; j < 16; j++) {
      tmp[i][j] =0;
    }
  }
    for (var i = 0; i < 16; i++) {
        for (var j = 0; j < 16; j++) {
            if (checkNeighbours(i, j)) {
                tmp[i][j] = 1
            }
            else {
                tmp[i][j] = 0
            }
        }
    }
    return -1
}
function checkNeighbours(i, j) {
    let x = 0
    let state = 0
    if (document.getElementById(`${i}-${j}`).classList.contains('Taken')) {
        state = 1
    }
    else {
        state = 0
    }
    if (i+1 <=15) {
        if (arr[i+1][j] == 1){
            x++
        }
    }
    if (i-1 >=0) {
        if (arr[i-1][j] == 1){
            x++
        } 
    }
    if (j+1 <=15) {
        if (arr[i][j+1] == 1){
            x++
        }
    }
    if (j-1 >=0) {
        if (arr[i][j-1] == 1){
            x++
        } 
    }
    if (j-1 >=0 && i+1 <=15) {
        if (arr[i+1][j-1] == 1){
            x++
        } 
    }
    if (j-1 >=0 && i-1 >=0) {
        if (arr[i-1][j-1] == 1){
            x++
        } 
    }
    if (j+1 <=15 && i+1 <=15) {
        if (arr[i+1][j+1] == 1){
            x++
        } 
    }
    if (j+1 <=15 && i-1 >=0) {
        if (arr[i-1][j+1] == 1){
            x++
        } 
    }
    if (state == 1) {
        if ((x <2)||(x>3)) {
            return false
        }
        return true 
    }
    if (state == 0) {
        if (x==3) {
            return true
        }
        return false
    }
}
function RenderTheBoard() {
    for (var i = 0; i < 16; i++) {
        for (var j = 0; j < 16; j++) {
            arr[i][j] = tmp[i][j]
            if (arr[i][j] == 1) {document.getElementById(`${i}-${j}`).className = 'Taken'}
            else {document.getElementById(`${i}-${j}`).className = 'quadrat'}
        }
    }

}
function startGame() {
    
    var game =0
    if (!queue.length) {game = setInterval(tick, 250);
        queue.push(game)
        document.getElementById('btn1').className = 'ingame'
        document.getElementById('btn1').textContent = 'Pause'
    }
    else {
        clearInterval(queue.pop())
        document.getElementById('btn1').className = 'start'
        document.getElementById('btn1').textContent = 'Start'
    }
}
function cleanBoard() {
    for (var i = 0; i < 16; i++) {
        for (var j = 0; j < 16; j++) {
            arr[i][j] = 0
            if (arr[i][j] == 1) {document.getElementById(`${i}-${j}`).className = 'Taken'}
            else {document.getElementById(`${i}-${j}`).className = 'quadrat'}
        }
    }
}
