console.log("this is working");

let list_photos_link = [
    '/static/pic 1.png',
    '/static/pic 2.png',
    '/static/pic 3.png',
    '/static/pic 4.png'
];

function photos_changes() {
    let num = Math.floor(Math.random() * list_photos_link.length);
    document.getElementById("image").src = list_photos_link[num];
}

photos_changes();

setInterval(photos_changes, 2000);
