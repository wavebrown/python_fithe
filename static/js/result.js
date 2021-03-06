const hero = document.querySelector('.hero');
const text = hero.querySelector('h1');
const walk = 100;

const shadow = e => {
    const {
        offsetWidth: width,
        offsetHeight: height
    } = hero;
    let {
        offsetX: x,
        offsetY: y
    } = e;
    if (hero !== e.target) {
        x = x + e.target.offsetLeft;
        y = y + e.target.offsetTop;
    }

    const xWalk = Math.round((x / width * walk) - (walk / 2));
    const yWalk = Math.round((y / height * walk) - (walk / 2));

    document.documentElement.style.setProperty(`--x`, `${xWalk}px`);
    document.documentElement.style.setProperty(`--y`, `${yWalk}px`);

    // Transform shadows without CSS animation ( but without CSS vars );
    // text.style.textShadow =`
    //   ${xWalk * -1}px ${yWalk * -1}px 0 rgba(255,0,255,.7),
    //   ${xWalk * -1}px ${yWalk}px 0 rgba(255,255,0,.7),
    //   ${yWalk * -1}px ${xWalk * -1}px 0 rgba(0,255,255,.7),
    //   ${yWalk}px ${xWalk}px 0 rgba(0,0,0,.7)
    // `;
}

hero.addEventListener('mousemove', shadow);