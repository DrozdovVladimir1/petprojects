// var snakeHead = {
//     x: 0,
//     y: 0,
//     Dir: 'ArrowLeft',
// }
const snakeBody = {
    x: 0,
    y: 0,
    
    Dir: 'ArrowRight',
}
var fruit = {
    x: 0,
    y: 0,
    ammount: 1,
}
let snake = [{
  x: 0,
  y: 0,
  
  Dir: 'ArrowRight',
},
{
  x: 0,
  y: 0,
  
  Dir: 'ArrowRight',
},
{
  x: 0,
  y: 0,
  
  Dir: 'ArrowRight',
},
{
  x: 0,
  y: 0,
  
  Dir: 'ArrowRight',
}
];
let score = 0;

(function() { //default settings for the snake
let a = 6;
for (let i=0; i<snake.length; i++) {
 snake[i].x = a;
 snake[i].y = 8;
 a--;
// console.log(`----- ${snake[0].x} ${snake[1].x} ${snake[2].x} ${snake[3].x} -----`)
}
//console.log(`DEFAULT SETTINGS FOR SNAKE ${(snake[0].x)}`);
fruit.x = 1;
fruit.y = 1;
})();
let currentDir = 'ArrowRight';
document.addEventListener('keydown', (event) => {
    var name = event.key;
    var code = event.code;
    //document.getElementById('text').textContent = code;
    if ((code == 'ArrowUp')&&(snake[0].Dir != 'ArrowDown')) {currentDir = code}
    if ((code == 'ArrowDown')&&(snake[0].Dir != 'ArrowUp')) {currentDir = code}
    if ((code == 'ArrowLeft')&&(snake[0].Dir != 'ArrowRight')) {currentDir = code}
    if ((code == 'ArrowRight')&&(snake[0].Dir != 'ArrowLeft')) {currentDir = code}

  }, false);


  let game = setInterval(tick, 500);
  
  function tick() {
    Move();
    score+=20;
    RenderTheBoard();
  }
  let hasEatenFruit = false;
  function  Move() {
    if (!hasEatenFruit) {
    snake.pop();}
    snake.unshift({
      x: 0,
      y: 0,
      
      Dir: 'ArrowRight',
    }
    );
    if (snake.length === 100) {winOutcome()}
    snake[0].Dir = currentDir;
    snake[0].x = snake[1].x;
    snake[0].y = snake[1].y;
    switch(currentDir) {
      case 'ArrowUp': 
        snake[0].y-=1;
        if(snake[0].y<0) {loseOutcome()}
        break;
      case 'ArrowDown':
        snake[0].y+=1;
        if(snake[0].y > 9) {loseOutcome()}
        break;
      case 'ArrowLeft':
        snake[0].x-=1;
        if(snake[0].x < 0) {loseOutcome()}
        break;
      case 'ArrowRight':
        snake[0].x+=1;
        if(snake[0].x > 9) {loseOutcome()}
        break;
    }
    if (document.getElementById(`${snake[0].y}-${snake[0].x}`).classList.contains('zmeika')) {loseOutcome()}
    hasEatenFruit= ((snake[0].x === fruit.x)&&(snake[0].y === fruit.y));
    if (hasEatenFruit) {score +=2000; GenerateFruit()}
  }
  function GenerateFruit() {
    fruit.x = Math.floor((Math.random()*9));
    fruit.y = Math.floor((Math.random()*9));
    if (document.getElementById(`${fruit.y}-${fruit.x}`).classList.contains(`zmeika`)) {GenerateFruit()}
  }
  function loseOutcome() {
    clearInterval(game);
    alert('you lose');
  }
  function winOutcome() {
    clearInterval(game);
    alert(`You won! Congratulations! Your final score is ${score}`);
  }
  function RenderTheBoard() { /*element.classList.add("my-class");
                                element.classList.remove("my-class");*/
    for (let i=0; i<=9; i++) {
      for (let j=0; j<=9; j++) {
        document.getElementById(`${i}-${j}`).classList.remove('zmeika');
        document.getElementById(`${i}-${j}`).classList.remove('fruit');
      }
    }
    for (let i=0; i<snake.length; i++) {
      // console.log(`render => snake[${i}].x = ${snake[i].x}; snake[${i}].y = ${snake[i].y}`)
      document.getElementById(`${snake[i].y}-${snake[i].x}`).classList.add('zmeika');
    }
    document.getElementById(`${fruit.y}-${fruit.x}`).classList.add('fruit');
    document.getElementById('score').textContent = `Score: ${score}`;
  }
