function archText(element, isTop = true) {
    const text = element.textContent;
    element.innerHTML = '';
    const chars = text.split('');
    const angleStep = 8;
    const startAngle = -(chars.length - 1) * angleStep / 2;
    const radius = 130;
    
    chars.forEach((char, i) => {
        const span = document.createElement('span');
        span.textContent = char;
        const angle = startAngle + (i * angleStep);
        if (isTop) {
            span.style.transform = `rotate(${angle}deg) translateY(-${radius}px)`;
        } else {
            span.style.transform = `rotate(${-angle}deg) translateY(${radius}px)`;
        }
        element.appendChild(span);
    });
}

function initialize_bee_animation(){
    if (!window.beeState){
        window.beeState = {
            maxbees: 0,
            hive: document.getElementById('hive')
        }
    }

    if (window.beeState.hive){
        window.beeState.hive.addEventListener('click', function(){
            if (window.beeState.maxbees < 8){
                create_bee();
                window.beeState.maxbees = window.beeState.maxbees + 1;
            }
        });
    }

    const topHeading = document.querySelector('.bee-heading-top');
    const bottomHeading = document.querySelector('.bee-heading-down');
    if (topHeading) archText(topHeading, true);
    if (bottomHeading) archText(bottomHeading, false);

    // Clean up bees before an htmx request
    window.addEventListener('htmx:beforeRequest', function(){
        let bees = document.getElementsByClassName('bee');
        while (bees[0]) {
            bees[0].parentNode.removeChild(bees[0]);
        }
        window.beeState = null;
    });
}

initialize_bee_animation();

function create_bee(){
    let par = document.getElementById('main')
    let hive = document.getElementById('hive')

    let posx = (hive.offsetLeft/100)*-50 +  hive.offsetLeft + hive.offsetWidth/2;
    let posy = (hive.offsetTop/100)*-50 +  hive.offsetTop + hive.offsetHeight/2;

    const bee = document.createElement("div");

    const body = document.createElement('div');
    body.classList.add('bee_body');

    const leg1 = document.createElement('div');
    leg1.classList.add('leg', 'leg-left', 'leg-left-top');

    const leg2 = document.createElement('div');
    leg2.classList.add('leg', 'leg-right', 'leg-right-top');

    const leg3 = document.createElement('div');
    leg3.classList.add('leg', 'leg-left', 'leg-left-middle');

    const leg4 = document.createElement('div');
    leg4.classList.add('leg', 'leg-right', 'leg-right-middle');

    const leg5 = document.createElement('div');
    leg5.classList.add('leg', 'leg-left', 'leg-left-bottom');

    const leg6 = document.createElement('div');
    leg6.classList.add('leg', 'leg-right', 'leg-right-bottom');

    body.appendChild(leg1);
    body.appendChild(leg2);
    body.appendChild(leg3);
    body.appendChild(leg4);
    body.appendChild(leg5);
    body.appendChild(leg6);

    const head = document.createElement('div');
    head.classList.add('bee_head');

    const eye1 = document.createElement('div');
    eye1.classList.add('eye', 'eye-left');

    const eye2 = document.createElement('div');
    eye2.classList.add('eye', 'eye-right');

    head.appendChild(eye1);
    head.appendChild(eye2);

    const tail = document.createElement('div');  
    tail.classList.add('tail');

    const stripe1 = document.createElement('div');
    stripe1.classList.add('stripe', 'stripe-top');

    const stripe2 = document.createElement('div');
    stripe2.classList.add('stripe', 'stripe-bottom');

    tail.appendChild(stripe1);
    tail.appendChild(stripe2);

    const wing1 = document.createElement('div');
    wing1.classList.add('wing', 'wing-left');

    const wing2 = document.createElement('div');
    wing2.classList.add('wing', 'wing-right');

    bee.appendChild(body);
    bee.appendChild(head);
    bee.appendChild(tail);
    bee.appendChild(wing1);
    bee.appendChild(wing2);
    
    bee.classList.add('bee');
    par.appendChild(bee);


    bee.style.position = "absolute";
    bee.style.left = posx+'px';
    bee.style.top = posy+'px';

    let id;
    let angle = Math.random() * 2 * Math.PI;
    let speed = Math.floor(Math.random() * 2)+0.5;
    let last_posy = 0;
    let bee_angle;


    id = setInterval(frame, 3);

function frame() {
    if (posy >= par.offsetHeight || posy < -50 || posx > par.offsetWidth || posx < -50) {
        clearInterval(id);
        bee.remove()
        window.beeState.maxbees = window.beeState.maxbees - 1;

    } else {
        if (wing1.style.transform == "rotate(45deg)"){
            wing1.style.transform = "rotate(0deg)";
            wing1.style.top = "10px";
        }
        else if (wing1.style.transform == "rotate(0deg)"){
            wing1.style.transform = "rotate(-45deg)";
        }
        else{
            wing1.style.transform = "rotate(45deg)";
            wing1.style.top = "18px";
        }


        if (wing2.style.transform == "rotate(135deg)"){
            wing2.style.transform = "rotate(180deg)";
            wing2.style.top = "10px";
        }
        else if (wing2.style.transform == "rotate(180deg)"){
            wing2.style.transform = "rotate(225deg)";
        }
        else{
            wing2.style.transform = "rotate(135deg)";
            wing2.style.top = "18px";
        }

        last_posy = posy

        posx = posx + Math.cos(angle) * speed;
        posy = posy + Math.sin(angle) * speed;

        if (posy < last_posy){
            bee_angle = Math.cos(angle)
            bee_angle = bee_angle * 180 / Math.PI
        }
        else{
            bee_angle = Math.cos(angle) * -1
            bee_angle = bee_angle * 180 / Math.PI + 180
        }
        
        speed = Math.floor(Math.random() * 2)+0.5;
        
        for (let rotation = 0; rotation < bee_angle; rotation++){
            bee.style.transform = "rotate(" + rotation + "deg)";
        }
        
        bee.style.top = posy+'px';
        bee.style.left = posx+'px';


        angle += (Math.random() - 0.5) * 0.5;
        }
    }
}
